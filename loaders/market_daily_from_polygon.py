from __future__ import annotations
import sys
from datetime import date, datetime, timezone, timedelta

import model
from loaders.loader_base import LoaderBase
from model.job_log import MsgSeverity
from model.jobs import Provider, JobType
from model.symbols import Symbol
from model.market_daily import MarketDaily
from providers.polygon import Polygon


class LoadMarketDailyFromPolygon(LoaderBase):
    tickers_to_ignore = ['NTEST', 'NTEST.I', 'NTEST.H', 'PTEST',
                         'ZBZX', 'ZEXIT', 'ZIEXT', 'ZJZZT', 'ZTEST', 'ZTST', 'ZVZZT', 'ZWZZT', 'ZXIET', 'ZXZZT']

    @staticmethod
    def update_market_daily_from_polygon(market_daily: MarketDaily, i: dict):
        market_daily.price_close = i.get('c')
        market_daily.price_high = i.get('h')
        market_daily.price_low = i.get('l')
        market_daily.price_open = i.get('o')
        market_daily.num_transactions = i.get('n')
        market_daily.volume = i.get('v')
        market_daily.price_volume_weighted = i.get('vw')

    @staticmethod
    def load(i: dict, session: model.Session, method_params: dict):
        loader: LoadMarketDailyFromPolygon = method_params.get('loader')
        ticker: str = i.get('T')
        if ticker in LoadMarketDailyFromPolygon.tickers_to_ignore:
            return
        market_day: date = datetime.strptime(method_params.get("market_day"),'%Y-%m-%d').date()
        country_code: str = method_params.get("country_code")

        exchange: str = Symbol.find_exchange_by_ticker_and_country(session, ticker, country_code)
        if exchange is None:
            msg = ticker + ' not found in Symbols for country=' + country_code
            LoaderBase.write_log(session, loader, MsgSeverity.WARN, msg)
            return

        if datetime.fromtimestamp(float(i.get('t')) / 1000, timezone.utc).date() != market_day:
            msg = 'timestamp ' + i.get('t') + ' does not match input market_day ' + market_day
            LoaderBase.write_log(session, loader, MsgSeverity.ERROR, msg)
            return

        symbols = Symbol.get_symbols_by_ticker_and_exchange(session, ticker, exchange)
        candidate_symbol: Symbol = Symbol.find_candidate_symbol(symbols, market_day)

        if candidate_symbol:
            market_daily: MarketDaily = MarketDaily.get_unique(session, candidate_symbol, market_day)
            if market_daily:
                market_daily.updated = datetime.now()
                market_daily.updater = Provider.Polygon
                loader.records_updated += 1
            else:
                market_daily = MarketDaily(symbol=candidate_symbol,
                                           market_day=market_day, creator=Provider.Polygon)
                session.add(market_daily)
                loader.records_added += 1

            LoadMarketDailyFromPolygon.update_market_daily_from_polygon(market_daily, i)
        else:
            msg = 'could not find matching Symbol for ' + ticker + ' and market_day=' + str(market_day)
            LoaderBase.write_log(session, loader, MsgSeverity.WARN, msg)


if __name__ == '__main__':
    date_format = '%Y-%m-%d'
    start_str: str = sys.argv[1] if len(sys.argv) > 1 else datetime.strftime(datetime.now(), date_format)
    end_str: str = sys.argv[1] if len(sys.argv) > 1 else datetime.strftime(datetime.now(), date_format)
    # start_str = '2023-01-05'
    # end_str = '2023-01-07'

    start_date: date = datetime.strptime(start_str, date_format).date()
    end_date: date = datetime.strptime(end_str, date_format).date()
    current_date: date = end_date
    while current_date >= start_date:
        market_day = datetime.strftime(current_date, date_format)
        current_date -= timedelta(days=1)
        loader = LoadMarketDailyFromPolygon()
        commit = True

        loader.job_id = LoaderBase.start_job(provider=Provider.Polygon,
                             job_type=JobType.MarketDaily,
                             params=str({'market_day': market_day}))

        Polygon.call_api(url=Polygon.url_prefix + 'v2/aggs/grouped/locale/us/market/stocks/' + market_day,
                         payload={'adjusted': 'true', 'include_otc': 'true'},
                         method=LoadMarketDailyFromPolygon.load,
                         method_params={'country_code': 'US', 'market_day': market_day, 'loader': loader},
                         commit=commit,
                         paginate=False, cursor=None)  # this API is not paginated

        LoaderBase.finish_job(loader)
