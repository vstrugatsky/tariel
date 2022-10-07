from model.jobs import Provider, Job, JobType
from model.symbols import Symbol
from model.dividends import Dividend
from providers.polygon import Polygon
import model as model
from datetime import datetime, timedelta


class LoadDividendsFromPolygon:
    @staticmethod
    def load(i: dict, session: model.Session, method_params: dict) -> Dividend:

        symbol = i.get('ticker')
        country_code = method_params.get("country_code")
        exchange = Symbol.find_exchange_by_symbol_and_country(symbol, country_code, session)
        if exchange is None:
            print(f'WARN {datetime.utcnow()} {i.get("ticker")} not found in Symbols for country={country_code}')
            return None

        symbols = Symbol.get_symbols_by_symbol_and_exchange(session, symbol, exchange)

        for j in symbols:
            print(j)
            return None

        if exchange:
            return Dividend(symbol=i.get('ticker'),
                            exchange=exchange,
                            active=True,
                            dividend_type=i.get('dividend_type'),
                            cash_amount=i.get('cash_amount'),
                            currency=i.get('currency', 'USD').upper(),
                            declaration_date=i.get('declaration_date'),
                            ex_dividend_date=i.get('ex_dividend_date'),
                            pay_date=i.get('pay_date'),
                            record_date=i.get('record_date'),
                            frequency=i.get('frequency'))


if __name__ == '__main__':
    job: Job
    with model.Session() as session:
        job = Job(provider=Provider.Polygon,
                  job_type=JobType.Dividends,
                  parameters='timedelta(50)',
                  started=datetime.now())
        session.add(job)
        session.commit()

    Polygon.call_paginated_api(
        Polygon.polygonPrefix + 'v3/reference/dividends',
        payload={'limit': 10,
                 # 'declaration_date.gte': datetime.utcnow() - timedelta(50),
                 'order': 'asc',
                 'sort': 'ticker'},
        method=LoadDividendsFromPolygon.load,
        method_params={'country_code': 'US'},
        commit=False, paginate=False, cursor=None)

    with model.Session() as session:
        job.completed = datetime.now()
        session.merge(job)
        session.commit()
