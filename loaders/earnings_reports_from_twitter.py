from __future__ import annotations
import sys
from typing import Optional, Type
from datetime import datetime, timedelta, date

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
        if eps_match: parsed_earnings |= eps_match.groupdict()

        revenue_match = account.parse_revenue(tweet_text)
        if revenue_match: parsed_earnings |= revenue_match.groupdict()

        positive_guidance = account.parse_positive_guidance(tweet_text)
        if positive_guidance: parsed_earnings |= {'positive_guidance': positive_guidance}

        negative_guidance = account.parse_negative_guidance(tweet_text)
        if negative_guidance: parsed_earnings |= {'negative_guidance': negative_guidance}

        return parsed_earnings

    @staticmethod
    def parse_earnings_sentiments(account: TwitterAccount, tweet_text: str) -> dict:
        parsed_sentiments = {}

        positive_earnings = account.parse_positive_earnings(tweet_text)
        if positive_earnings: parsed_sentiments |= {'positive_earnings': positive_earnings}

        negative_earnings = account.parse_negative_earnings(tweet_text)
        if negative_earnings: parsed_sentiments |= {'negative_earnings': negative_earnings}

        positive_guidance = account.parse_positive_guidance(tweet_text)
        if positive_guidance: parsed_sentiments |= {'positive_guidance': positive_guidance}

        negative_guidance = account.parse_negative_guidance(tweet_text)
        if negative_guidance: parsed_sentiments |= {'negative_guidance': negative_guidance}

        return parsed_sentiments

    @staticmethod
    def determine_currency(eps_currency, revenue_currency) -> str | None:
        currency = eps_currency if eps_currency else revenue_currency
        return Currency.currencies.get(currency, None)

    @staticmethod
    def determine_eps(eps_sign: str | None, eps: str | None) -> float:
        if eps_sign == '-':
            return 0.0 - float(eps)
        else:
            return float(eps) if eps else 0

    @staticmethod
    def evaluate_data_quality(er: EarningsReport) -> Optional[str]:
        if er.revenue_surprise and er.revenue and (abs(er.revenue_surprise) / er.revenue) >= 0.75:
            return 'Revenue surprise ' + str(er.revenue_surprise) + ' too large for revenue=' + str(er.revenue)
        else:
            return None

    @staticmethod
    def update_er(er: EarningsReport, i: dict, match_dict: dict, account: TwitterAccount):
        LoadEarningsReportsFromTwitter.update_earnings_fields(er, match_dict, account)
        LoadEarningsReportsFromTwitter.update_twitter_fields(er, i, account)
        er.data_quality_note = LoadEarningsReportsFromTwitter.evaluate_data_quality(er)

    @staticmethod
    def update_earnings_fields(er: EarningsReport, match_dict: dict, account: TwitterAccount):
        max_earnings_sentiment = 2
        max_guidance_sentiment = 1
        er.currency = LoadEarningsReportsFromTwitter.\
            determine_currency(match_dict.get('eps_currency'), match_dict.get('revenue_currency'))

        er.eps = LoadEarningsReportsFromTwitter.determine_eps(match_dict.get('eps_sign'), match_dict.get('eps'))
        er.revenue = account.determine_revenue(match_dict)

        er.eps_surprise = account.determine_surprise(match_dict, 'eps')
        er.earnings_sentiment = LoadEarningsReportsFromTwitter.\
            update_earnings_sentiment(er.eps_surprise, er.earnings_sentiment, max_earnings_sentiment)

        er.revenue_surprise = account.determine_surprise(match_dict, 'revenue')
        er.earnings_sentiment = LoadEarningsReportsFromTwitter.\
            update_earnings_sentiment(er.revenue_surprise, er.earnings_sentiment, max_earnings_sentiment)

        positive_sentiment: [] = match_dict.get('positive_sentiment')
        if positive_sentiment:
            er.earnings_sentiment = max((er.earnings_sentiment or 0) + len(positive_sentiment), max_earnings_sentiment)

        negative_sentiment: [] = match_dict.get('negative_sentiment')
        if negative_sentiment:
            er.earnings_sentiment = min((er.earnings_sentiment or 0) - len(negative_sentiment), 0 - max_earnings_sentiment)

        positive_guidance: [] = match_dict.get('positive_guidance')
        if positive_guidance:
            er.guidance_sentiment = max((er.guidance_sentiment or 0) + len(positive_guidance), max_guidance_sentiment)

        negative_guidance: [] = match_dict.get('negative_guidance')
        if negative_guidance:
            er.guidance_sentiment = max((er.guidance_sentiment or 0) - len(negative_guidance), 0 - max_guidance_sentiment)

    @staticmethod
    def update_earnings_sentiment(surprise_amount: float|None, current_sentiment: int, max_sentiment: int) -> int | None:
        if surprise_amount:
            if surprise_amount > 0:
                return max((current_sentiment or 0) + 1, max_sentiment)
            elif surprise_amount < 0:
                return min((current_sentiment or 0) - 1, 0 - max_sentiment)
        else: return None

    @staticmethod
    def update_twitter_fields(er: EarningsReport, i: dict, account: TwitterAccount):
        tweet_info = {
            'tweet_id': i['id'],
            'tweet_date': i['created_at'],
            'twitter_account': account.account_name + '(' + i['author_id'] + ')',
            'tweet_text': i['text'],
            'tweet_short_url': Utils.find_first_match("entities.urls[0].url", i),
            'tweet_expanded_url': Utils.find_first_match("entities.urls[0].expanded_url", i),
            'tweet_url_status': Utils.find_first_match("entities.urls[0].status", i),
            'tweet_url_title': Utils.find_first_match("entities.urls[0].title", i),
            'tweet_url_description': Utils.find_first_match("entities.urls[0].description", i),
        }
        if er.provider_info:
            index = next((j for j, item in enumerate(er.provider_info) if item["tweet_id"] == i['id']), None)
            if index:
                er.provider_info[index] = tweet_info
            else:
                er.provider_info.append(tweet_info)
        else:
            er.provider_info = [tweet_info]

    @staticmethod
    def associate_tweet_with_symbols(session: model.Session, cashtags: [dict], tweet_text: str = 'test') -> dict:
        symbols: dict = {}
        if not cashtags:
            return symbols
        for d in cashtags:
            tag = d.get('tag')
            if tag and (tag + ' ' in tweet_text or tag + ':CA' not in tweet_text):  # exclude Canadian tickers
                candidate_symbol: Symbol = Symbol.get_unique_by_ticker_and_country(session, tag, 'US')
                if candidate_symbol:
                    symbols[candidate_symbol.symbol] = candidate_symbol
        return symbols

    @staticmethod
    def load(i: dict, session: model.Session, method_params: dict):
        loader: LoadEarningsReportsFromTwitter = method_params.get('loader')
        provider = 'Twitter_' + loader.account.account_name
        cashtags = Twitter.get_cashtags(i)
        print(f'TWEET {i["created_at"]} {i["text"]} {str(cashtags)}')
        if not cashtags:
            return

        parsed_earnings = LoadEarningsReportsFromTwitter.parse_earnings_numbers(loader.account, i['text'])
        if not parsed_earnings:
            parsed_earnings = LoadEarningsReportsFromTwitter.parse_earnings_sentiments(loader.account, i['text'])
            if not parsed_earnings:
                print(f'INFO cannot parse earnings numbers or sentiments from {i["text"]}')
                if loader.account.should_raise_parse_warning(i['text']):
                    msg = 'Failed to parse likely earnings numbers or sentiments from ' + i['text']
                    LoaderBase.write_log(session, loader, MsgSeverity.WARN, msg)
                return

        symbols: dict = LoadEarningsReportsFromTwitter.associate_tweet_with_symbols(session, cashtags, i['text'])
        if not symbols:
            msg = 'Parsed an earnings tweet, but cannot associate symbol with cashtags ' + str(cashtags)
            LoaderBase.write_log(session, loader, MsgSeverity.WARN, msg)
            return
        print(f'INFO associated {symbols.keys()} and matched {parsed_earnings}')

        report_date = datetime.strptime(i['created_at'], '%Y-%m-%dT%H:%M:%S.%fZ').date()
        er = EarningsReport.get_unique_by_symbols_and_date_range\
            (session, symbols, report_date - timedelta(days=5), report_date + timedelta(days=5))
        if not er:
            er = EarningsReport(creator=Provider[provider], report_date=report_date)
            session.add(er)
            for key in symbols:
                er.symbols.append(symbols[key])

            LoadEarningsReportsFromTwitter.update_er(er, i, parsed_earnings, loader.account)
            loader.records_added += 1
        else:
            if LoadEarningsReportsFromTwitter.should_update(er, provider):
                er.updated = datetime.now()
                er.updater = Provider[provider]
                LoadEarningsReportsFromTwitter.update_er(er, i, parsed_earnings, loader.account)
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
    backfill = False
    commit = False
    paginate = False
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
