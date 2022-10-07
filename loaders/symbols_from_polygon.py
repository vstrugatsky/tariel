from model.jobs import Provider, Job, JobType
from model.symbols import Symbol
from model.market_identifiers import MarketIdentifier
from providers.polygon import Polygon
import model as model
from datetime import datetime
import time


class LoadSymbolsFromPolygon:
    @staticmethod
    def update_symbol_from_polygon(symbol: Symbol, i: dict):
        symbol.name = i.get('name')
        symbol.type = i.get('type')
        symbol.currency = i.get('currency_name')
        symbol.cik = i.get('cik')
        symbol.composite_figi = i.get('composite_figi')
        symbol.share_class_figi = i.get('share_class_figi')
        symbol.provider_last_updated = i.get('last_updated_utc')

    @staticmethod
    def load(i: dict, session: model.Session, method_params: dict):
        if i.get('market') == 'otc':
            exchange = 'OTCM'
        else:
            exchange = MarketIdentifier.lookup_operating_mic_by_mic(i.get('primary_exchange'), session)
        if exchange:
            symbol = Symbol.get_unique(session, i.get('ticker'), exchange, i.get('active'), i.get('delisted_utc'))
            if symbol:
                symbol.updated = datetime.now()
                symbol.updater = Provider.Polygon
                LoadSymbolsFromPolygon.update_symbol_from_polygon(symbol, i)
            else:
                symbol = Symbol(symbol=i.get('ticker'),
                                exchange=exchange,
                                active=i.get('active'),
                                delisted=i.get('delisted_utc'),
                                creator=Provider.Polygon)
                LoadSymbolsFromPolygon.update_symbol_from_polygon(symbol, i)
                session.add(symbol)
        else:
            print(f'WARN {datetime.utcnow()} exchange {i.get("primary_exchange")} \
            not found for ticker {i.get("ticker")}')


if __name__ == '__main__':
    job: Job
    params: [dict] = [{'market': 'stocks', 'active': True},
                      {'market': 'stocks', 'active': False},
                      {'market': 'otc', 'active': True},
                      {'market': 'otc', 'active': False}]
    for param in params:
        with model.Session() as session:
            job = Job(provider=Provider.Polygon,
                      job_type=JobType.Symbols,
                      parameters=str(param),
                      started=datetime.now())
            session.add(job)
            session.commit()
        time.sleep(5)
        Polygon.call_paginated_api(Polygon.polygonPrefix + 'v3/reference/tickers',
                                   param | {'limit': 1000, 'order': 'asc', 'sort': 'ticker'},
                                   method=LoadSymbolsFromPolygon.load, method_params={},
                                   commit=True, paginate=True, cursor=None)

        with model.Session() as session:
            job.completed = datetime.now()
            session.merge(job)
            session.commit()
