from __future__ import annotations
from loaders.loader_base import LoaderBase
from model.job_log import MsgSeverity
from model.jobs import Provider, Job, JobType
from model.symbols import Symbol
from model.market_identifiers import MarketIdentifier
from providers.polygon import Polygon
import model as model
from datetime import datetime
import time


class LoadSymbolsFromPolygon(LoaderBase):
    @staticmethod
    def manual_data_cleanup(ticker: str) -> str | None:
        if ticker == 'CASY':
            return 'XNAS'
        else:
            return None

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
        loader: LoadSymbolsFromPolygon = method_params.get('loader')
        if i.get('market') == 'otc':
            exchange = 'OTCM'
        else:
            exchange = MarketIdentifier.lookup_operating_mic_by_mic(i.get('primary_exchange'), session)

        if not exchange:
            exchange = LoadSymbolsFromPolygon.manual_data_cleanup(i.get('ticker'))

        if exchange:
            symbol = Symbol.get_unique(session, i.get('ticker'), exchange, i.get('active'), i.get('delisted_utc'))
            if symbol:
                if symbol.updated is None or symbol.updated < symbol.provider_last_updated:
                    symbol.updated = datetime.now()
                    symbol.updater = Provider.Polygon
                    LoadSymbolsFromPolygon.update_symbol_from_polygon(symbol, i)
                    loader.records_updated += 1
            else:
                symbol = Symbol(symbol=i.get('ticker'),
                                exchange=exchange,
                                active=i.get('active'),
                                delisted=i.get('delisted_utc'),
                                creator=Provider.Polygon)
                LoadSymbolsFromPolygon.update_symbol_from_polygon(symbol, i)
                session.add(symbol)
                loader.records_added += 1
        else:
            if i.get('active'):
                msg = 'exchange ' + i.get("primary_exchange", 'None') + ' not found for active ticker ' + i.get("ticker")
                LoaderBase.write_job_log(session, loader.job_id, MsgSeverity.ERROR, msg)
                loader.errors += 1


if __name__ == '__main__':
    commit = True
    paginate = True
    params: [dict] = [{'market': 'stocks', 'active': True},
                      {'market': 'stocks', 'active': False},
                      {'market': 'otc', 'active': True},
                      {'market': 'otc', 'active': False}
                      ]
    for param in params:
        loader = LoadSymbolsFromPolygon()
        loader.job_id = LoaderBase.start_job(provider=Provider.Polygon, job_type=JobType.Symbols,
                                      params=str(param) + ' commit: ' + str(commit) + ' paginate: ' + str(paginate))
        time.sleep(5)
        Polygon.call_paginated_api(Polygon.url_prefix + 'v3/reference/tickers',
                                   param | {'limit': 1000, 'order': 'asc', 'sort': 'ticker'},
                                   method=LoadSymbolsFromPolygon.load, method_params={'loader': loader},
                                   commit=commit, paginate=paginate, cursor=None)

        LoaderBase.finish_job(loader)
