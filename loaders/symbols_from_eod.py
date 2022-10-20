# NOT TESTED - DEPRECATION CANDIDATE
import requests
from datetime import datetime

import model

from model.symbols import Symbol
from model.exchanges import Exchange
from loaders.loader_base import LoaderBase
from model.jobs import Provider, JobType
from config import config


class LoadSymbolsFromEOD(LoaderBase):

    @staticmethod
    def eod_update_symbols(exchange_code: str):
        payload = {'fmt': 'json', 'api_token': config.eod['api_key']}
        r = requests.get(model.eodPrefix + 'exchange-symbol-list/' + exchange_code, params=payload, timeout=10)
        print(f'{datetime.utcnow()} URL = {r.url}; Status = {r.status_code}')
        if r.status_code != 200:
            print(f'ERROR status={r.status_code}')
            exit(1)
        with model.Session() as session:
            for i in r.json():
                print(i)
                exchange = Exchange.lookup_by_acronym_or_code(i.get("Exchange"), session)
                if exchange:
                    symbol = Symbol(symbol=i.get("Code"),
                                    exchange=exchange,
                                    active=True,
                                    name=i.get('Name'),
                                    currency=i.get("Currency"),
                                    type=i.get('Type'),
                                    isin=i.get('Isin'),
                                    updated=datetime.now())  # no need for utcnow() - the column is set to timestamptz
                    session.merge(symbol)
            session.commit()


if __name__ == '__main__':
    loader = LoadSymbolsFromEOD()
    exchanges_to_load = [
        'NEO', 'V', 'TO',   # Canada
        # 'LSE'  # London Stock Exchange
        # 'US'   # All US Exchanges
    ]

    loader.job_id = LoaderBase.start_job(provider=Provider.Polygon, job_type=JobType.Symbols,
                                  params=str(exchanges_to_load))

    for e in exchanges_to_load:
        LoadSymbolsFromEOD.eod_update_symbols(e)

    LoaderBase.finish_job(loader)
