from __future__ import annotations
from datetime import date, datetime
import time

import model
from loaders.loader_base import LoaderBase
from model.jobs import Provider, JobType
from model.symbols import Symbol
from model.symbols_norgate import SymbolNorgate
from sqlalchemy import func, not_
from providers.ibkr import IbkrCommon, IbkrMarketDataSnapshot
from model.market_daily import MarketDaily
import logging


class LoadSnapshotsFromIbkr(LoaderBase):

    @staticmethod
    def load(commit: bool, update: bool, market_day: date):
        # first time empty response
        IbkrMarketDataSnapshot.get_market_snapshot('416888') # RUT

        all_us_contracts = IbkrCommon.load_contracts('AMEX')
        # all_ca_contracts = IbkrCommon.load_contracts('TSE')
        unmatched_count = 0
        unreturned_count = 0

        # Norgate symbol convention: TICKER-YYYYMM, where YYYYMM is the year and month of the delisting
        with model.Session() as session:
            logging.getLogger('sqlalchemy.engine').setLevel(logging.WARNING)
            norgate_symbols: list[SymbolNorgate] = session.query(SymbolNorgate)\
                .filter(not_(SymbolNorgate.symbol.like('%-%')))\
                .order_by(SymbolNorgate.symbol).all()
                # .filter(SymbolNorgate.symbol.like('MTLS%')) \


                # .order_by(func.random()).all()
            print(f"*** {len(norgate_symbols)} Norgatesymbols")


            batch_size = 50
            for i in range(0, len(norgate_symbols), batch_size):
                batch = norgate_symbols[i:i+batch_size]
                conids = []
                for symbol in batch: 
                    conid = all_us_contracts.get(symbol.symbol)
                    if conid:
                        conids.append(str(conid))
                    else:
                        unmatched_count += 1
                        print(f"*** {symbol.symbol} not matched to IBKR conid")
                print(f"batch {(i / batch_size)}, {len(conids)} conids")

                time.sleep(1)
                market_data_snapshots: dict[str, IbkrMarketDataSnapshot] = IbkrMarketDataSnapshot.get_market_snapshot(','.join(conids))           
                for snapshot in market_data_snapshots.values():
                    if snapshot.symbol:
                        symbol = Symbol.get_unique_by_ticker_and_country(session, snapshot.symbol, 'US')
                        if not symbol:
                            unreturned_count += 1
                            print(f"*** {snapshot.symbol} not returned from IBKR")
                        else:
                            print(f"*** {symbol.symbol} returned from IBKR")
                            market_daily = MarketDaily.get_unique(session, symbol, market_day, Provider.IBKR.name)
                            if not market_daily:
                                market_daily = MarketDaily(symbol=symbol, market_day=market_day, creator=Provider.IBKR.name)
                                session.add(market_daily)
                                loader.records_added += 1
                                LoadSnapshotsFromIbkr.update_fields(market_daily, snapshot)

                            else:
                                if update:
                                    loader.records_updated += 1
                                    LoadSnapshotsFromIbkr.update_fields(market_daily, snapshot)
                    else:
                        unreturned_count += 1
                        print(f"*** {symbol.symbol} not returned from IBKR")

                if commit: # commit after each batch
                    session.commit()

        print(f"*** {len(norgate_symbols)} Norgate symbols, {unmatched_count} unmatched, {unreturned_count} unreturned, {loader.records_added} added, {loader.records_updated} updated")
    
    def update_fields(market_daily, snapshot):     
        market_daily.iv = snapshot.iv.replace('%', '').replace(',', '') if snapshot.iv and snapshot.iv != 'N/A' else None
        market_daily.pc_ratio = snapshot.p2c.replace('%', '').replace(',', '') if snapshot.p2c and snapshot.p2c != 'N/A' else None
        market_daily.next_earnings = snapshot.earn
        market_daily.market_cap = snapshot.cap
        market_daily.eps = snapshot.eps
        market_daily.shortable = snapshot.shortable
        market_daily.fee_rate = snapshot.fee.replace('%', '').replace(',', '') if snapshot.fee and snapshot.fee != 'N/A' else None
        market_daily.updated = datetime.now() 


if __name__ == '__main__':
    commit = True
    update = True
    market_day = datetime.strftime(datetime.now(), '%Y-%m-%d') # '2024-10-22' # 
    loader = LoadSnapshotsFromIbkr()
    loader.job_id = LoaderBase.start_job(provider=Provider.IBKR, job_type=JobType.IbkrSnapshots, params=f"commit:{str(commit)} update:{str(update)} market_day:{market_day}")
    loader.load(commit, update, market_day) 
    LoaderBase.finish_job(loader)
