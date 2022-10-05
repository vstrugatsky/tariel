from model.jobs import Provider, Job, JobType
from model.symbols import Symbol
from model.market_identifiers import MarketIdentifier
from providers.polygon import Polygon
import model as model
from datetime import datetime


class LoadSymbolsFromPolygon:
    @staticmethod
    def load(i: dict, session: model.Session, method_params: dict) -> Symbol:
        if i.get('market') == 'otc':
            exchange = 'OTCM'
        else:
            exchange = MarketIdentifier.lookup_operating_mic_by_mic(i.get('primary_exchange'), session)
        if exchange:
            return Symbol(symbol=i.get('ticker'),
                          exchange=exchange,
                          active=i.get('active'),
                          name=i.get('name'),
                          currency=i.get('currency_name'),
                          type=i.get('type'),
                          cik=i.get('cik'),
                          composite_figi=i.get('composite_figi'),
                          share_class_figi=i.get('share_class_figi'),
                          provider_last_updated=i.get('last_updated_utc'),
                          delisted=i.get('delisted_utc'),
                          creator=Provider.Polygon)
        else:
            print(f'WARN {datetime.utcnow()} exchange {i.get("primary_exchange")} \
            not found for ticker {i.get("ticker")}')


if __name__ == '__main__':
    job: Job
    params: [dict] = [  # {'market': 'stocks', 'active': True},
                      {'market': 'stocks', 'active': False},
                      #  {'market': 'otc', 'active': True},
                      {'market': 'otc', 'active': False}]
    for param in params:
        with model.Session() as session:
            job = Job(provider=Provider.Polygon,
                      job_type=JobType.Symbols,
                      parameters=str(param),
                      started=datetime.now())
            session.merge(job)
            session.commit()

        Polygon.call_paginated_api(Polygon.polygonPrefix + 'v3/reference/tickers',
                                   param | {'limit': 1000, 'order': 'asc', 'sort': 'ticker'},
                                   method=LoadSymbolsFromPolygon.load, method_params={},
                                   commit=True, paginate=True, cursor=None)

        with model.Session() as session:
            job.completed = datetime.now()
            session.merge(job)
            session.commit()
