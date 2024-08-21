from __future__ import annotations
from datetime import date, datetime
from time import sleep

import model
from loaders.loader_base import LoaderBase
from model.jobs import Provider, JobType
from model.earnings_reports import EarningsReport
from model.symbols_norgate import SymbolNorgate
from config import config
import requests

class LoadEarningsReportsFromAlphaV(LoaderBase):

    @staticmethod
    def load(commit: bool):
        # Norgate symbol convention: TICKER-YYYYMM, where YYYYMM is the year and month of the delisting
 
        with model.Session() as session:
            norgate_symbols: list[SymbolNorgate] = session.query(SymbolNorgate).order_by(SymbolNorgate.symbol).all()
        # .filter(SymbolNorgate.symbol.like('TBIO%')) \
               
        previous_ticker = None
        current_ticker = None
        symbols_for_ticker: dict = {}

        for symbol in norgate_symbols:  # sorted by symbol and thus by ticker
            current_ticker = SymbolNorgate.get_ticker_for_symbol(symbol.symbol)
            if current_ticker != previous_ticker and previous_ticker is not None:
                LoadEarningsReportsFromAlphaV.load_earnings_for_ticker(previous_ticker, symbols_for_ticker, commit)
                print('previous_ticker: ' + previous_ticker, 'current_ticker: ' + current_ticker)
                symbols_for_ticker = {}

            previous_ticker = current_ticker            
            symbols_for_ticker[symbol.symbol] = symbol.delisted

        # load earnings for the last ticker
        LoadEarningsReportsFromAlphaV.load_earnings_for_ticker(current_ticker, symbols_for_ticker, commit)


    @staticmethod
    def load_earnings_for_ticker(ticker: str, symbols_for_ticker: dict, commit: bool):
        alphavantage_prefix = 'https://www.alphavantage.co/query?function=EARNINGS'
        url = alphavantage_prefix + '&symbol=' + ticker + '&apikey=' + config.alphavantage['premium_api_key']
        sleep(0.5) # 75 calls per minute
        try:
            r = requests.get(url)
            # print(r.json())
            if r.json() and r.json()['symbol'] == ticker:
                for i in r.json()['quarterlyEarnings']:
                    qtr_end: date = datetime.strptime(i['fiscalDateEnding'], '%Y-%m-%d').date()
                    symbol: str = LoadEarningsReportsFromAlphaV.match_eoq_date_to_norgate_symbol(qtr_end, symbols_for_ticker)
                    if symbol:
                        report = EarningsReport()
                        report.symbol_norgate = symbol
                        report.fiscal_date_ending = qtr_end
                        report.reported_date = i['reportedDate']
                        report.report_time = i['reportTime']
                        with model.Session() as session:
                            session.merge(report)
                            if commit:
                                session.commit()
        except Exception as e:
            print('API error calling ' + url + ' e: ' + str(e))


    @staticmethod
    def match_eoq_date_to_norgate_symbol(qtr_end: date, symbols: dict) -> str or None:
        closest_key = None
        delta_days = None
        for key in symbols:
            delisted_date = symbols[key]
            if delisted_date is None:
                if closest_key is None:
                    delta_days = 365 * 100
                    closest_key = key
            else:
                if qtr_end > delisted_date: # Quarter end after delisting
                    continue
                else:
                    if delta_days is None or delta_days > (delisted_date - qtr_end).days:
                        delta_days = (delisted_date - qtr_end).days
                        closest_key = key      
        return closest_key


if __name__ == '__main__':
    commit = True
    loader = LoadEarningsReportsFromAlphaV()
    loader.job_id = LoaderBase.start_job(provider=Provider.AlphaVantage, job_type=JobType.EarningsReports, params='commit: ' + str(commit))
    loader.load(commit) 
    LoaderBase.finish_job(loader)