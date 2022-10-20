from __future__ import annotations
from datetime import date, datetime, timedelta

from loaders.loader_base import LoaderBase
from model.job_log import MsgSeverity
from model.jobs import Provider, JobType
from model.symbols import Symbol
from model.splits import Split
from providers.polygon import Polygon
import model


class LoadSplitsFromPolygon(LoaderBase):
    @staticmethod
    def update_split_from_polygon(split: Split, i: dict):
        split.split_from = i.get('split_from'),
        split.split_to = i.get('split_to'),

    @staticmethod
    def load(i: dict, session: model.Session, method_params: dict):
        loader: LoadSplitsFromPolygon = method_params.get('loader')
        ticker: str = i.get('ticker')
        execution_date: date = datetime.strptime(i.get('execution_date'), "%Y-%m-%d").date()
        country_code: str = method_params.get("country_code")

        exchange: str = Symbol.find_exchange_by_ticker_and_country(session, ticker, country_code)
        if exchange is None:
            msg = ticker + ' not found in Symbols for country=' + country_code
            LoaderBase.write_log(session, loader, MsgSeverity.WARN, msg)
            return

        symbols = Symbol.get_symbols_by_ticker_and_exchange(session, ticker, exchange)
        candidate_symbol: Symbol = Symbol.find_candidate_symbol(symbols, execution_date)

        if candidate_symbol:
            split: Split = Split.get_unique(session, candidate_symbol, execution_date)
            if split:
                split.updated = datetime.now()
                split.updater = Provider.Polygon
                loader.records_updated += 1
            else:
                split = Split(symbol=candidate_symbol,
                              execution_date=execution_date, creator=Provider.Polygon)
                session.add(split)
                loader.records_added += 1

            LoadSplitsFromPolygon.update_split_from_polygon(split, i)
        else:
            msg = 'could not find matching Symbol for ' + ticker + ' and execution_date=' + str(execution_date)
            LoaderBase.write_log(session, loader, MsgSeverity.ERROR, msg)


if __name__ == '__main__':
    loader = LoadSplitsFromPolygon()
    days_to_go_back = 5
    commit = True
    paginate = True
    params = {'limit': 1000,
              'execution_date.gte': datetime.utcnow().date() - timedelta(days_to_go_back)}

    loader.job_id = LoaderBase.start_job(
        provider=Provider.Polygon, job_type=JobType.Splits,
        params=str(params) + ' commit: ' + str(commit) + ' paginate: ' + str(paginate))

    Polygon.call_paginated_api(
        url=Polygon.url_prefix + 'v3/reference/splits',
        payload=params | {'order': 'asc', 'sort': 'ticker'},
        method=LoadSplitsFromPolygon.load,
        method_params={'country_code': 'US', 'loader': loader},
        commit=commit, paginate=paginate, cursor=None)

    LoaderBase.finish_job(loader)
