from __future__ import annotations

import sys
from typing import Optional, Type
import model
from datetime import datetime, timedelta, date
from loaders.loader_base import LoaderBase
from loaders.twitter_account import TwitterAccount
from loaders.twitter_livesquawk import Livesquawk
from loaders.twitter_marketcurrents import Marketcurrents
from model.job_log import MsgSeverity
from model.jobs import Provider, JobType
from model.symbols import Symbol
from model.currency import Currency
from model.earnings_reports import EarningsReport
from utils.utils import Utils
import re
from providers.twitter import Twitter


class LoadEarningsReportsFromTwitter(LoaderBase):
    def __init__(self, account):
        self.account: TwitterAccount = account
        super(LoadEarningsReportsFromTwitter, self).__init__()

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

        er.guidance_direction = match_dict.get('guidance_1')

    @staticmethod
    def update_twitter_fields(er: EarningsReport, i: dict, account: TwitterAccount):
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
    def associate_tweet_with_symbol(session: model.Session, cashtags: [dict], tweet_text: str) -> Optional[Symbol]:
        symbol: Optional[Symbol] = None
        if not cashtags:
            return None
        for d in cashtags:
            cashtag: str = d.get('tag')
            if cashtag and (cashtag + ' ') in tweet_text:
                # A hack to account for Canadian symbols in cashtags - they would appear as symbol:CA in text - ignore them
                candidate_symbol: Symbol = Symbol.get_unique_by_ticker_and_country(session, cashtag, 'US')
                if candidate_symbol and symbol is None:
                    symbol = candidate_symbol
                if candidate_symbol and symbol is not None and symbol.id != candidate_symbol.id:
                    return None  # two valid and different symbols -> can't associate
        return symbol

    @staticmethod
    def load(i: dict, session: model.Session, method_params: dict):
        loader: LoadEarningsReportsFromTwitter = method_params.get('loader')
        account: TwitterAccount = method_params.get("account")
        entities = i.get('entities', None)
        cashtags = entities.get('cashtags', None) if entities else None
        print(f'TWEET {i["created_at"]} {i["text"]} {str(cashtags)}')
        if not cashtags:
            return

        match: re.Match = loader.account.parse_tweet(i['text'])
        if not match:
            print(f'INFO cannot parse earnings from {i["text"]}')
            return

        symbol = LoadEarningsReportsFromTwitter.associate_tweet_with_symbol(session, cashtags, i['text'])
        if not symbol:
            msg = 'Parsed an earnings tweet, but cannot associate symbol with cashtags ' + str(cashtags)
            LoaderBase.write_job_log(session, loader.job_id, MsgSeverity.WARN, msg)
            loader.warnings += 1
            return

        print(f'INFO associated {Symbol.symbol} and matched {match.groupdict()}')
        report_date: date = datetime.strptime(i['created_at'], '%Y-%m-%dT%H:%M:%S.%fZ').date()
        er = EarningsReport.get_unique(session, symbol, report_date)
        if not er:
            er = EarningsReport(symbol=symbol, report_date=report_date, creator=Provider.Twitter)
            session.add(er)
            loader.records_added += 1
        else:
            er.updated = datetime.now()
            er.updater = Provider.Twitter
            loader.records_updated += 1
        LoadEarningsReportsFromTwitter.update_earnings_fields(er, match.groupdict(), loader.account)
        LoadEarningsReportsFromTwitter.update_twitter_fields(er, i, loader.account)


if __name__ == '__main__':
    # loader = LoadEarningsReportsFromTwitter(Marketcurrents(Marketcurrents.account_name))
    account = sys.argv[1] if len(sys.argv) > 1 else 'Livesquawk'
    account_class: Type[TwitterAccount] = getattr(sys.modules['loaders.twitter_' + account.lower()], account)
    print(account, account_class)
    loader = LoadEarningsReportsFromTwitter(account_class(account))
    backfill = False
    commit = True
    paginate = True
    max_results = 100
    if backfill:
        max_date = datetime.utcnow() - timedelta(days=6, hours=23)  # to not hit the 7 days issue
    else:
        max_date = EarningsReport.get_max_date() or datetime.utcnow() - timedelta(days=6, hours=23)

    payload = {'query': 'from:' + loader.account.account_name,  # + ' earnings',
               'start_time': max_date.strftime("%Y-%m-%dT%H:%M:%SZ")}

    loader.job_id = LoaderBase.start_job(
        provider=Provider.Twitter, job_type=JobType.EarningsReports,
        params=str(payload) + ' paginate: ' + str(paginate))

    Twitter.call_paginated_api(
        url=Twitter.url_prefix + '/tweets/search/recent',
        payload=payload | {'tweet.fields': 'created_at,author_id,entities', 'max_results': max_results},
        method=LoadEarningsReportsFromTwitter.load,
        method_params={'loader': loader},
        paginate=paginate, commit=commit, next_token=None)

    LoaderBase.finish_job(loader)
