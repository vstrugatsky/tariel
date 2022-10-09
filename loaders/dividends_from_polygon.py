from __future__ import annotations
from model.jobs import Provider, Job, JobType
from model.symbols import Symbol
from model.dividends import Dividend
from providers.polygon import Polygon
import model as model
from datetime import date, datetime, timedelta


class LoadDividendsFromPolygon:
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
    # tested by dividends_from_polygon_test.py
    def find_candidate_symbol(symbols: [Symbol], ex_dividend_date: date) -> Symbol | None:
        # active sorts false first, delisted - older date first
        symbols.sort(key=lambda x: (x.active, x.delisted))
        for symbol in symbols:
            if symbol.active or (not symbol.active and symbol.delisted.date() > ex_dividend_date):
                return symbol
        return None

    @staticmethod
    def load(i: dict, session: model.Session, method_params: dict):
        ticker: str = i.get('ticker')
        ex_dividend_date: date = datetime.strptime(i.get('ex_dividend_date'), "%Y-%m-%d").date()
        country_code: str = method_params.get("country_code")
        exchange: str = Symbol.find_exchange_by_symbol_and_country(ticker, country_code, session)
        if exchange is None:
            print(f'WARN {datetime.utcnow()} {i.get("ticker")} not found in Symbols for country={country_code}')
            return

        symbols = Symbol.get_symbols_by_symbol_and_exchange(session, ticker, exchange)
        candidate_symbol: Symbol = LoadDividendsFromPolygon.find_candidate_symbol(symbols, ex_dividend_date)

        if candidate_symbol:
            dividend: Dividend = Dividend.get_unique(session, candidate_symbol, ex_dividend_date)
            if dividend:
                dividend.updated = datetime.now()
                dividend.updater = Provider.Polygon
            else:
                dividend = Dividend(symbol=candidate_symbol,
                                    ex_dividend_date=i.get('ex_dividend_date'),
                                    creator=Provider.Polygon)
                session.add(dividend)

            LoadDividendsFromPolygon.update_dividend_from_polygon(dividend, i)
        else:
            print(f'WARN {datetime.utcnow()} .\
            could not find matching Symbol for {i.get("ticker")} and ex_dividend_date={ex_dividend_date}')


if __name__ == '__main__':
    job: Job
    params = {'limit': 1000  # ,'declaration_date.gte': datetime.utcnow() - timedelta(50),
              }
    commit = True
    paginate = True

    if commit:
        with model.Session() as session:
            job = Job(provider=Provider.Polygon,
                      job_type=JobType.Dividends,
                      parameters=str(params) + ' paginate: ' + str(paginate),
                      started=datetime.now())
            session.add(job)
            session.commit()

    Polygon.call_paginated_api(
        Polygon.polygonPrefix + 'v3/reference/dividends',
        payload=params | {'order': 'asc', 'sort': 'ticker'},
        method=LoadDividendsFromPolygon.load,
        method_params={'country_code': 'US'},
        commit=commit, paginate=paginate, cursor=None)

    if commit:
        with model.Session() as session:
            job.completed = datetime.now()
            session.merge(job)
            session.commit()
