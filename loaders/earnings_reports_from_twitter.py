from __future__ import annotations
import sys
from typing import Optional, Type
from datetime import datetime, timedelta

from sqlalchemy.orm.attributes import flag_modified

import model
from loaders.loader_base import LoaderBase
from loaders.twitter_account import TwitterAccount
from loaders.twitter_livesquawk import Livesquawk  # noqa
from loaders.twitter_marketcurrents import Marketcurrents  # noqa
from model.job_log import MsgSeverity
from model.jobs import Provider, JobType
from model.symbols import Symbol
from model.currency import Currency
from model.earnings_reports import EarningsReport
from utils.utils import Utils
from providers.twitter import Twitter


class LoadEarningsReportsFromTwitter(LoaderBase):
    def __init__(self, account):
        self.account: TwitterAccount = account
        super(LoadEarningsReportsFromTwitter, self).__init__()

    @staticmethod
    def parse_earnings_numbers(account: TwitterAccount, tweet_text: str) -> dict:
        parsed_earnings = {}

        eps_match = account.parse_eps(tweet_text)
        if eps_match:
            parsed_earnings |= eps_match.groupdict()

        revenue_match = account.parse_revenue(tweet_text)
        if revenue_match:
            parsed_earnings |= revenue_match.groupdict()

        if parsed_earnings:  # Do not parse guidance if earning numbers have not been parsed
            positive_guidance = account.parse_positive_guidance(tweet_text)
            if positive_guidance:
                parsed_earnings |= {'positive_guidance': positive_guidance}

            negative_guidance = account.parse_negative_guidance(tweet_text)
            if negative_guidance:
                parsed_earnings |= {'negative_guidance': negative_guidance}

        return parsed_earnings

    @staticmethod
    def parse_earnings_sentiments(account: TwitterAccount, tweet_text: str) -> dict:
        parsed_sentiments = {}

        positive_earnings = account.parse_positive_earnings(tweet_text)
        if positive_earnings:
            parsed_sentiments |= {'positive_earnings': positive_earnings}

        negative_earnings = account.parse_negative_earnings(tweet_text)
        if negative_earnings:
            parsed_sentiments |= {'negative_earnings': negative_earnings}

        positive_guidance = account.parse_positive_guidance(tweet_text)
        if positive_guidance:
            parsed_sentiments |= {'positive_guidance': positive_guidance}

        negative_guidance = account.parse_negative_guidance(tweet_text)
        if negative_guidance:
            parsed_sentiments |= {'negative_guidance': negative_guidance}

        print(parsed_sentiments)
        return parsed_sentiments

    @staticmethod
    def determine_currency(eps_currency, revenue_currency) -> str | None:
        currency = eps_currency if eps_currency else revenue_currency
        return Currency.currencies.get(currency, None)

    @staticmethod
    def determine_eps(eps_sign: str | None, eps: str | None) -> float | None:
        if eps_sign == '-':
            return 0.0 - float(eps)
        else:
            return float(eps) if eps else None

    @staticmethod
    def evaluate_data_quality(er: EarningsReport) -> Optional[str]:
        if er.revenue_surprise and er.revenue and (abs(er.revenue_surprise) / er.revenue) >= 0.75:
            return 'Revenue surprise ' + str(er.revenue_surprise) + ' too large for revenue=' + str(er.revenue)
        else:
            return None

    @staticmethod
    def update_er(er: EarningsReport, tweet_response: dict, match_dict: dict, account: TwitterAccount):
        LoadEarningsReportsFromTwitter.update_earnings_fields(er, match_dict, account)
        LoadEarningsReportsFromTwitter.update_sentiment_fields(er)
        LoadEarningsReportsFromTwitter.update_reference_fields(er, tweet_response, match_dict, account)
        er.data_quality_note = LoadEarningsReportsFromTwitter.evaluate_data_quality(er)

    @staticmethod
    def update_earnings_fields(er: EarningsReport, match_dict: dict, account: TwitterAccount):
        er.currency = LoadEarningsReportsFromTwitter.determine_currency\
            (match_dict.get('eps_currency'), match_dict.get('revenue_currency'))

        er.eps = LoadEarningsReportsFromTwitter.determine_eps(match_dict.get('eps_sign'), match_dict.get('eps'))
        er.revenue = account.determine_revenue(match_dict)

        er.eps_surprise = account.determine_surprise(match_dict, 'eps')
        er.revenue_surprise = account.determine_surprise(match_dict, 'revenue')

        er.positive_earnings = match_dict.get('positive_earnings')
        er.negative_earnings = match_dict.get('negative_earnings')
        er.positive_guidance = match_dict.get('positive_guidance')
        er.negative_guidance = match_dict.get('negative_guidance')

    @staticmethod
    def update_sentiment_fields(er: EarningsReport):
        er.earnings_sentiment = 0  # Complete recalc
        er.guidance_sentiment = 0
        er.earnings_sentiment = LoadEarningsReportsFromTwitter.update_earnings_sentiment\
            (er.eps_surprise, er.earnings_sentiment)

        er.earnings_sentiment = LoadEarningsReportsFromTwitter.update_earnings_sentiment\
            (er.revenue_surprise, er.earnings_sentiment)

        if er.positive_earnings:
            er.earnings_sentiment = LoadEarningsReportsFromTwitter.update_positive_sentiment\
                (er.earnings_sentiment, len(er.positive_earnings), EarningsReport.max_earnings_sentiment)

        if er.negative_earnings:
            er.earnings_sentiment = LoadEarningsReportsFromTwitter.update_negative_sentiment\
                (er.earnings_sentiment, len(er.negative_earnings), EarningsReport.max_earnings_sentiment)

        if er.positive_guidance:
            er.guidance_sentiment = LoadEarningsReportsFromTwitter.update_positive_sentiment\
                (er.guidance_sentiment, len(er.positive_guidance), EarningsReport.max_guidance_sentiment)

        if er.negative_guidance:
            er.guidance_sentiment = LoadEarningsReportsFromTwitter.update_negative_sentiment\
                (er.guidance_sentiment, len(er.negative_guidance), EarningsReport.max_guidance_sentiment)

    @staticmethod
    def update_earnings_sentiment(surprise_amount: float | None, current_sentiment: int) -> int | None:
        if surprise_amount:
            if surprise_amount > 0:
                return LoadEarningsReportsFromTwitter.update_positive_sentiment\
                    (current_sentiment, 1, EarningsReport.max_earnings_sentiment)
            elif surprise_amount < 0:
                return LoadEarningsReportsFromTwitter.update_negative_sentiment\
                    (current_sentiment, 1, EarningsReport.max_earnings_sentiment)
        else:
            return current_sentiment

    @staticmethod
    def update_positive_sentiment(current_sentiment: [int | None], update: int, max_sentiment: int):
        return min((current_sentiment or 0) + update, max_sentiment)

    @staticmethod
    def update_negative_sentiment(current_sentiment: [int | None], update: int, max_sentiment: int):
        return max((current_sentiment or 0) - update, 0 - max_sentiment)

    @staticmethod
    def update_reference_fields(er: EarningsReport, tweet_response: dict, match_dict: dict, account: TwitterAccount):
        tweet_info = {
            'tweet_id': tweet_response['id'],
            'tweet_date': tweet_response['created_at'],
            'tweet_text': tweet_response['text'],
            'twitter_account': account.account_name + '(' + tweet_response['author_id'] + ')',
            'tweet_short_url': Utils.find_first_match("entities.urls[0].url", tweet_response),
            'tweet_expanded_url': Utils.find_first_match("entities.urls[0].expanded_url", tweet_response),
            'tweet_url_status': Utils.find_first_match("entities.urls[0].status", tweet_response),
            'tweet_url_title': Utils.find_first_match("entities.urls[0].title", tweet_response),
            'tweet_url_description': Utils.find_first_match("entities.urls[0].description", tweet_response),
        }
        if 'positive_earnings' in match_dict:
            tweet_info['positive_earnings'] = match_dict['positive_earnings']
        if 'negative_earnings' in match_dict:
            tweet_info['negative_earnings'] = match_dict['negative_earnings']
        if 'positive_guidance' in match_dict:
            tweet_info['positive_guidance'] = match_dict['positive_guidance']
        if 'negative_guidance' in match_dict:
            tweet_info['negative_guidance'] = match_dict['negative_guidance']

        if er.provider_info:
            index = next((j for j, item in enumerate(er.provider_info) if item["tweet_id"] == tweet_response['id']), None)
            if index is None:
                er.provider_info.append(tweet_info)
            else:
                er.provider_info[index] = tweet_info
            print('er.provider_info=' + str(er.provider_info))
            flag_modified(er, "provider_info")
        else:
            er.provider_info = [tweet_info]

    @staticmethod
    def associate_tweet_with_symbols(session: model.Session, cashtags: [dict], tweet_text: str = 'test') -> dict:
        symbols: dict = {}
        if not cashtags:
            return symbols
        for d in cashtags:
            tag = d.get('tag')
            if tag and ('$' + tag + ' ' in tweet_text or '$' + tag + ':CA' not in tweet_text):  # exclude Canadian tickers
                candidate_symbol: Symbol = Symbol.get_unique_by_ticker_and_country(session, tag, 'US')
                if candidate_symbol:
                    symbols[candidate_symbol.symbol] = candidate_symbol
        return symbols

    @staticmethod
    def warn_if_needed(tweet_text: str, loader: LoadEarningsReportsFromTwitter, session: model.Session):
        if loader.account.should_raise_parse_warning(tweet_text):
            msg = 'Failed to parse likely earnings numbers or sentiments from ' + tweet_text
            LoaderBase.write_log(session, loader, MsgSeverity.WARN, msg)

    @staticmethod
    def load(tweet_response: dict, session: model.Session, method_params: dict):
        loader: LoadEarningsReportsFromTwitter = method_params.get('loader')
        account: TwitterAccount = loader.account
        provider = 'Twitter_' + loader.account.account_name
        tweet_text: str = tweet_response["text"]
        cashtags = Twitter.get_cashtags(tweet_response)
        print(f'TWEET {tweet_response["created_at"]} {tweet_text} {str(cashtags)}')
        if not cashtags:
            return

        if account.parse_earnings_false_positive(tweet_text):
            print(f'INFO false positive detected')
            return
        parsed_earnings = LoadEarningsReportsFromTwitter.parse_earnings_numbers(account, tweet_text)
        if not parsed_earnings:
            earnings_indicator = account.parse_earnings_indicator(tweet_text)
            if not earnings_indicator:
                print(f'INFO cannot parse earnings numbers or indicator from {tweet_text}')
                return
            else:
                parsed_earnings = LoadEarningsReportsFromTwitter.parse_earnings_sentiments(account, tweet_text)
                if not parsed_earnings:
                    indicator_text = earnings_indicator.groupdict()['earnings_indicator'].strip()
                    print(f'INFO cannot parse earnings sentiments from {tweet_text} despite indicator {indicator_text}')
                    LoadEarningsReportsFromTwitter.warn_if_needed(tweet_text, loader, session)
                    return

        symbols: dict = LoadEarningsReportsFromTwitter.associate_tweet_with_symbols(session, cashtags, tweet_text)
        if not symbols:
            msg = 'Parsed an earnings tweet, but cannot associate symbol with cashtags ' + str(cashtags)
            LoaderBase.write_log(session, loader, MsgSeverity.WARN, msg)
            return
        print(f'INFO associated {symbols.keys()} and matched {parsed_earnings}')

        report_date = datetime.strptime(tweet_response['created_at'], '%Y-%m-%dT%H:%M:%S.%fZ').date()
        er = EarningsReport.get_unique_by_symbols_and_date_range\
            (session, symbols, report_date - timedelta(days=5), report_date + timedelta(days=5))
        if not er:
            er = EarningsReport(creator=Provider[provider], report_date=report_date)
            session.add(er)
            for key in symbols:
                er.symbols.append(symbols[key])

            LoadEarningsReportsFromTwitter.update_er(er, tweet_response, parsed_earnings, loader.account)
            loader.records_added += 1
        else:
            if LoadEarningsReportsFromTwitter.should_update(er, provider):
                er.updated = datetime.now()
                er.updater = Provider[provider]
                LoadEarningsReportsFromTwitter.update_er(er, tweet_response, parsed_earnings, loader.account)
                loader.records_updated += 1

    @staticmethod
    def should_update(er: EarningsReport, provider: str) -> bool:
        # Allow update if updater is the same as creator or if updater's priority is higher than creator's
        new_updater = Provider[provider]
        new_updater_priority = new_updater.value
        creator_priority = er.creator.value
        if new_updater_priority < creator_priority:
            return False
        if er.updater:
            updater_priority = er.updater.value
            if new_updater_priority < updater_priority:
                return False
        return True


if __name__ == '__main__':
    account_name = sys.argv[1] if len(sys.argv) > 1 else 'Livesquawk'
    account_class: Type[TwitterAccount] = getattr(sys.modules['loaders.twitter_' + account_name.lower()], account_name)
    loader = LoadEarningsReportsFromTwitter(account_class(account_name))
    provider = 'Twitter_' + account_name
    backfill = True
    commit = True
    paginate = True
    max_results = 100
    if backfill:
        max_date = datetime.utcnow() - timedelta(days=6, hours=23)  # to not hit the 7 days issue
    else:
        max_date = EarningsReport.get_max_date(provider) or datetime.utcnow() - timedelta(days=6, hours=23)

    payload = {'query': 'from:' + loader.account.account_name,  # + ' earnings',
               'start_time': max_date.strftime("%Y-%m-%dT%H:%M:%SZ")}

    loader.job_id = LoaderBase.start_job(
        provider=Provider[provider], job_type=JobType.EarningsReports,
        params=str(payload) + ' paginate: ' + str(paginate))

    Twitter.call_paginated_api(
        url=Twitter.url_prefix + '/tweets/search/recent',
        payload=payload | {'tweet.fields': 'created_at,author_id,entities', 'max_results': max_results},
        method=LoadEarningsReportsFromTwitter.load,
        method_params={'loader': loader},
        paginate=paginate, commit=commit, next_token=None)

    LoaderBase.finish_job(loader)
