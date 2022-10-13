from __future__ import annotations
from typing import Optional
import model
from datetime import datetime, timedelta, date
from model.jobs import Provider
from model.symbols import Symbol
from model.earnings_reports import EarningsReport
from utils.utils import Utils
import re
from providers.twitter import Twitter


class LoadEarningsReportsFromTwitter:
    @staticmethod
    def lookup_currency(symbol: str) -> str | None:
        if symbol == '$':
            return 'USD'
        elif symbol == 'C$':
            return 'CAD'
        else:
            return None

    @staticmethod
    def determine_currency(eps_currency, revenue_currency) -> str | None:
        currency = eps_currency if eps_currency else revenue_currency
        return LoadEarningsReportsFromTwitter.lookup_currency(currency)

    @staticmethod
    def determine_eps(eps_sign: str | None, eps: str | None) -> float:
        if eps_sign == '-':
            return 0.0 - float(eps)
        else:
            return float(eps) if eps else 0

    @staticmethod
    def determine_surprise(surprise_direction: str, surprise_amount: str, surprise_uom: str | None) -> float | None:
        if not surprise_direction:
            return None
        if surprise_direction.lower() == 'misses':
            return LoadEarningsReportsFromTwitter.apply_uom(0.0 - float(surprise_amount), surprise_uom)
        elif surprise_direction.lower() == 'beats':
            return LoadEarningsReportsFromTwitter.apply_uom(float(surprise_amount), surprise_uom)
        else:
            return None

    @staticmethod
    def apply_uom(amount: float, uom: str | None) -> float:
        if not uom:
            return amount
        elif uom.upper() == 'K':
            return round(amount * 1000)
        elif uom.upper() == 'M':
            return round(amount * 1000000)
        elif uom.upper() == 'B':
            return round(amount * 1000000000)
        else:
            return amount

    @staticmethod
    def update_earnings_fields(er: EarningsReport, match_dict: dict):
        er.currency = LoadEarningsReportsFromTwitter.determine_currency(
            match_dict.get('eps_currency'), match_dict.get('revenue_currency'))

        er.eps = LoadEarningsReportsFromTwitter.determine_eps(match_dict.get('eps_sign'), match_dict.get('eps'))

        er.revenue = LoadEarningsReportsFromTwitter.apply_uom(float(match_dict.get('revenue')), match_dict.get('revenue_uom'))

        er.eps_surprise = LoadEarningsReportsFromTwitter.determine_surprise(
            match_dict.get('eps_surprise_direction'), match_dict.get('eps_surprise_amount'), surprise_uom=None)
        er.revenue_surprise = LoadEarningsReportsFromTwitter.determine_surprise(
            match_dict.get('revenue_surprise_direction'), match_dict.get('revenue_surprise_amount'), match_dict.get('revenue_surprise_uom'))

        # TODO : er.guidance_direction

    @staticmethod
    def update_twitter_fields(er: EarningsReport, i: dict):
        er.provider_info = {
            'tweet_id': i['id'],
            'tweet_date': i['created_at'],
            'twitter_account': Twitter.account + '(' + i['author_id'] + ')',
            'tweet_text': i['text'],
            'tweet_short_url': Utils.find_first_match("entities.urls[0].url", i),
            'tweet_expanded_url': Utils.find_first_match("entities.urls[0].expanded_url", i),
            'tweet_url_status': Utils.find_first_match("entities.urls[0].status", i),
            'tweet_url_title': Utils.find_first_match("entities.urls[0].title", i),
            'tweet_url_description': Utils.find_first_match("entities.urls[0].description", i),
        }

    @staticmethod
    def parse_tweet(tweet_text: str) -> re.Match:
        p = re.compile(r'''
           EPS[ ]of[ ](?P<eps_sign>[-])?(?P<eps_currency>C?[$])      
           (?P<eps>\d+\.\d+)
           [ ]?(?P<eps_surprise_direction>misses|beats)?
           ([ ]by[ ])?(?P<eps_surprise_currency>C?[$])?
           (?P<eps_surprise_amount>\d+\.\d+)?
           .+
           revenue[ ]of[ ](?P<revenue_currency>C?[$])
           (?P<revenue>\d+\.?\d*)
           (?P<revenue_uom>[MBK])
           [ ]?(?P<revenue_surprise_direction>misses|beats)?
           ([ ]by[ ])?(?P<revenue_surprise_currency>C?[$])?
           (?P<revenue_surprise_amount>\d+\.?\d*)?
           (?P<revenue_surprise_uom>[MBK])?
           ''', re.VERBOSE | re.IGNORECASE)
        return p.search(tweet_text)

    @staticmethod
    def associate_tweet_with_symbol(session: model.Session, cashtags: [dict]) -> Optional[Symbol]:
        symbol: Optional[Symbol] = None
        if not cashtags:
            return None
        for d in cashtags:
            cashtag: str = d.get('tag')
            if cashtag:
                candidate_symbol: Symbol = Symbol.get_unique_by_ticker_and_country(session, cashtag, 'US')
                if candidate_symbol and symbol is None:
                    symbol = candidate_symbol
                if candidate_symbol and symbol is not None and symbol.id != candidate_symbol.id:
                    return None  # two valid and different symbols -> can't associate
        return symbol

    @staticmethod
    def load(i: dict, session: model.Session, method_params: dict):
        cashtags = i['entities'].get('cashtags', None)
        print(f'TWEET {i["created_at"]} {i["text"]} {str(cashtags)}')
        if not cashtags:
            return
        symbol = LoadEarningsReportsFromTwitter.associate_tweet_with_symbol(session, cashtags)
        if not symbol:
            print(f'INFO cannot associate symbol with {cashtags}')
            return

        match: re.Match = LoadEarningsReportsFromTwitter.parse_tweet(i['text'])
        if not match:
            print(f'INFO cannot parse earnings from {i["text"]}')
            return

        print(f'INFO associated {Symbol.symbol} and matched {match.groupdict()}')
        report_date: date = datetime.strptime(i['created_at'], '%Y-%m-%dT%H:%M:%S.%fZ').date()
        er = EarningsReport.get_unique(session, symbol, report_date)
        if not er:
            er = EarningsReport(symbol=symbol, report_date=report_date, creator=Provider.Twitter)
            session.add(er)
        else:
            er.updated = datetime.now()
            er.updater = Provider.Twitter
        LoadEarningsReportsFromTwitter.update_earnings_fields(er, match.groupdict())
        LoadEarningsReportsFromTwitter.update_twitter_fields(er, i)


if __name__ == '__main__':
    backfill = True
    commit = True
    paginate = True
    max_results = 100
    if backfill:
        max_date = datetime.utcnow() - timedelta(days=6, hours=23)  # to not hit the 7 days issue
    else:
        max_date = EarningsReport.get_max_date() or datetime.utcnow() - timedelta(days=6, hours=23)

    payload = {'query': 'from:' + Twitter.account,  # + ' earnings',
               'max_results': max_results,
               'start_time': max_date.strftime("%Y-%m-%dT%H:%M:%SZ"),
               'tweet.fields': 'created_at,author_id,entities'}

    Twitter.call_paginated_api(
        url=Twitter.url_prefix + '/tweets/search/recent',
        payload=payload,
        method=LoadEarningsReportsFromTwitter.load, method_params={},
        paginate=paginate, commit=commit, next_token=None)
