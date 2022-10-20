from __future__ import annotations
import sys
from typing import Optional, Type
import model
from datetime import datetime, timedelta
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
    def parse_tweet(account: TwitterAccount, tweet_text: str) -> Optional[dict]:
        return_dict = {}
        eps_match = account.parse_eps(tweet_text)
        if eps_match:
            return_dict |= eps_match.groupdict()

        revenue_match = account.parse_revenue(tweet_text)
        if revenue_match:
            return_dict |= revenue_match.groupdict()

        if not return_dict == {}:  # only parse guidance if we have either revenue or EPS
            guidance_match = account.parse_guidance(tweet_text)
            if guidance_match:
                return_dict |= guidance_match.groupdict()

        return None if return_dict == {} else return_dict

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
    def update_earnings_fields(er: EarningsReport, match_dict: dict, account: TwitterAccount):
        er.currency = LoadEarningsReportsFromTwitter.determine_currency(
            match_dict.get('eps_currency'), match_dict.get('revenue_currency'))

        er.eps = LoadEarningsReportsFromTwitter.determine_eps(match_dict.get('eps_sign'), match_dict.get('eps'))
        er.revenue = account.determine_revenue(match_dict)

        er.eps_surprise = account.determine_surprise(match_dict, 'eps')
        er.revenue_surprise = account.determine_surprise(match_dict, 'revenue')

        er.guidance_direction = match_dict.get('guidance_1').lower() if match_dict.get('guidance_1') else None

    @staticmethod
    def update_twitter_fields(er: EarningsReport, i: dict, account: TwitterAccount):
        er.provider_unique_id = i['id']
        er.provider_info = {
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

    @staticmethod
    def associate_tweet_with_symbols(session: model.Session, cashtags: [dict]) -> dict:
        symbols: dict = {}
        if not cashtags:
            return symbols
        for d in cashtags:
            if d.get('tag'):
                candidate_symbol: Symbol = Symbol.get_unique_by_ticker_and_country(session, d.get('tag'), 'US')
                if candidate_symbol:
                    symbols[candidate_symbol.symbol] = candidate_symbol
        return symbols

    @staticmethod
    def load(i: dict, session: model.Session, method_params: dict):
        loader: LoadEarningsReportsFromTwitter = method_params.get('loader')
        account: TwitterAccount = loader.account
        provider = 'Twitter_' + account.account_name
        entities = i.get('entities', None)
        cashtags = entities.get('cashtags', None) if entities else None
        print(f'TWEET {i["created_at"]} {i["text"]} {str(cashtags)}')
        if not cashtags:
            return

        match_dict = LoadEarningsReportsFromTwitter.parse_tweet(account, i['text'])
        if not match_dict:
            print(f'INFO cannot parse earnings from {i["text"]}')
            if account.should_raise_parse_warning(i['text']):
                msg = 'Failed to parse likely earnings from ' + i['text']
                LoaderBase.write_log(session, loader, MsgSeverity.WARN, msg)
            return

        symbols: dict = LoadEarningsReportsFromTwitter.associate_tweet_with_symbols(session, cashtags)
        if not symbols:
            msg = 'Parsed an earnings tweet, but cannot associate symbol with cashtags ' + str(cashtags)
            LoaderBase.write_log(session, loader, MsgSeverity.WARN, msg)
            return

        print(f'INFO associated {symbols.keys()} and matched {match_dict}')
        report_date = datetime.strptime(i['created_at'], '%Y-%m-%dT%H:%M:%S.%fZ').date()
        er = EarningsReport.get_unique(session, symbol=symbols[list(symbols)[0]], report_date=report_date)
        if not er:
            er = EarningsReport(creator=Provider[provider], report_date=report_date)
            for key in symbols:
                er.symbols.append(symbols[key])
                session.add(er)

            LoadEarningsReportsFromTwitter.update_earnings_fields(er, match_dict, loader.account)
            LoadEarningsReportsFromTwitter.update_twitter_fields(er, i, loader.account)
            loader.records_added += 1
        else:
            if LoadEarningsReportsFromTwitter.should_update(er, provider):
                er.updated = datetime.now()
                er.updater = Provider[provider]
                LoadEarningsReportsFromTwitter.update_earnings_fields(er, match_dict, loader.account)
                LoadEarningsReportsFromTwitter.update_twitter_fields(er, i, loader.account)
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
