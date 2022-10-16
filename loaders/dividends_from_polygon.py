from __future__ import annotations
from loaders.loader_base import LoaderBase
from model.job_log import MsgSeverity
from model.jobs import Provider, JobType
from model.symbols import Symbol
from model.dividends import Dividend
from providers.polygon import Polygon
import model as model
from datetime import date, datetime, timedelta


class LoadDividendsFromPolygon(LoaderBase):
    @staticmethod
    def update_dividend_from_polygon(dividend: Dividend, i: dict):
        dividend.dividend_type = i.get('dividend_type'),
        dividend.cash_amount = i.get('cash_amount'),
        dividend.currency = i.get('currency', 'USD').upper(),
        dividend.declaration_date = i.get('declaration_date'),
        dividend.pay_date = i.get('pay_date'),
        dividend.record_date = i.get('record_date'),
        dividend.frequency = i.get('frequency')

    @staticmethod
    def load(i: dict, session: model.Session, method_params: dict):
        loader: LoadDividendsFromPolygon = method_params.get('loader')
        ticker: str = i.get('ticker')
        ex_dividend_date: date = datetime.strptime(i.get('ex_dividend_date'), "%Y-%m-%d").date()
        country_code: str = method_params.get("country_code")

        exchange: str = Symbol.find_exchange_by_ticker_and_country(session, ticker, country_code)
        if exchange is None:
            msg = ticker + ' not found in Symbols for country=' + country_code
            LoaderBase.write_job_log(session, loader.job_id, MsgSeverity.WARN, msg)
            loader.warnings += 1
            return

        symbols = Symbol.get_symbols_by_ticker_and_exchange(session, ticker, exchange)
        candidate_symbol: Symbol = LoaderBase.find_candidate_symbol(symbols, ex_dividend_date)

        if candidate_symbol:
            dividend: Dividend = Dividend.get_unique(session, candidate_symbol, ex_dividend_date)
            if dividend:
                dividend.updated = datetime.now()
                dividend.updater = Provider.Polygon
                loader.records_updated += 1
            else:
                dividend = Dividend(symbol=candidate_symbol,
                                    ex_dividend_date=ex_dividend_date, creator=Provider.Polygon)
                session.add(dividend)
                loader.records_added += 1

            LoadDividendsFromPolygon.update_dividend_from_polygon(dividend, i)
        else:
            msg = 'could not find matching Symbol for ' + ticker + ' and ex_dividend_date=' + str(ex_dividend_date)
            LoaderBase.write_job_log(session, loader.job_id, MsgSeverity.WARN, msg)
            loader.warnings += 1


if __name__ == '__main__':
    loader = LoadDividendsFromPolygon()
    days_to_go_back = 5
    commit = True
    paginate = True
    params = {'limit': 1000,
              'declaration_date.gte': datetime.utcnow().date() - timedelta(days_to_go_back)}

    loader.job_id = LoaderBase.start_job(provider=Provider.Polygon, job_type=JobType.Dividends,
                                  params=str(params) + ' paginate: ' + str(paginate))

    Polygon.call_paginated_api(url=Polygon.url_prefix + 'v3/reference/dividends',
                               payload=params | {'order': 'asc', 'sort': 'ticker'},
                               method=LoadDividendsFromPolygon.load,
                               method_params={'country_code': 'US', 'loader': loader},
                               commit=commit, paginate=paginate, cursor=None)

    LoaderBase.finish_job(loader)
