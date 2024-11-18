from __future__ import annotations
from datetime import date, datetime, time
from time import sleep

import model
from loaders.loader_base import LoaderBase
from model.jobs import Provider, JobType
from model.earnings_reports import EarningsReport
from model.symbols_norgate import SymbolNorgate
from config import config
import requests
import json

class LoadEarningsReportsFromAlphaV(LoaderBase):

    @staticmethod
    def load(commit: bool):
        # Norgate symbol convention: TICKER-YYYYMM, where YYYYMM is the year and month of the delisting
 
        with model.Session() as session:
            norgate_symbols: list[SymbolNorgate] = session.query(SymbolNorgate)\
                .order_by(SymbolNorgate.symbol).all()
                # .filter(SymbolNorgate.symbol.like('KEYS%')) \

               
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
                        report.creator = Provider.AlphaVantage.name
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
    
def get_earnings_dates(ticker: str, start_date: date, end_date: date):
    headers = {
        "User-Agent": "Tariel Algo vl.strugatsky@gmail.com"
    }
    base_url = "https://data.sec.gov/submissions/CIK{}.json"
    
    # Get the CIK number for the company
    # url = "https://www.sec.gov/include/ticker.txt"
    url = 'https://www.sec.gov/files/company_tickers.json'
    response = requests.get(url, headers=headers)
    print(response)
    data = response.json()
    # print(data)
    ticker_to_cik = {}

    for _, company_info in data.items():
        cik = str(company_info['cik_str']).zfill(10)  # Pad CIK with leading zeros
        ticker_to_cik[company_info['ticker']] = cik

    cik = ticker_to_cik.get(ticker)
    print(f"cik: {cik} ticker: {ticker}")
    
    # Fetch filing data
    response = requests.get(base_url.format(cik), headers=headers)
    print(response)
    data = json.loads(response.text)
    recent_filings: dict = data['filings']['recent']
    recent_forms: list = recent_filings['form']
    recent_filing_dates: list = recent_filings['filingDate']
    earnings_dates = []
    for index, form in enumerate(recent_forms):
        if form in ['8-K']: # ['10-Q', '10-K']:
            # file_date = datetime.strptime(recent_filing_dates[index], '%Y-%m-%d')
            file_date = datetime.strptime(recent_filings['acceptanceDateTime'][index], '%Y-%m-%dT%H:%M:%S.%fZ').date()
            report_date = datetime.strptime(recent_filings['reportDate'][index], '%Y-%m-%d')
            report_time = datetime.strptime(recent_filings['acceptanceDateTime'][index], '%Y-%m-%dT%H:%M:%S.%fZ').time()
            print(f"{form} filing_date: {recent_filings['filingDate'][index]} \
                  acceptance: {recent_filings['acceptanceDateTime'][index]} \
                  report_date: {recent_filings['reportDate'][index]} \
                  primary_document: {recent_filings['primaryDocument'][index]} \
                  primaryDocumentDescription: {recent_filings['primaryDocDescription'][index]} \
                  isXBRL: {recent_filings['isXBRL'][index]}  ")
            if start_date <= file_date <= end_date:
                # report = EarningsReport()
                # report.symbol_norgate = ticker
                # report.fiscal_date_ending = report_date
                # report.reported_date = file_date
                # if report_time < time(9, 30, 0):
                #     report.report_time = 'pre-market'
                # else:
                #     report.report_time = 'post-market'
                # report.creator = Provider.Edgar.name
                # with model.Session() as session:
                #     session.merge(report)
                #     if commit:
                #         session.commit()
                earnings_dates.append((form, file_date))
    
    return earnings_dates


if __name__ == '__main__':
    commit = True
    # loader = LoadEarningsReportsFromAlphaV()
    # loader.job_id = LoaderBase.start_job(provider=Provider.Edgar, job_type=JobType.EarningsReports, params='commit: ' + str(commit))
    # loader.load(commit) 
    # LoaderBase.finish_job(loader)
    ticker = "UPST"
    start_date = date(2024, 2, 1)
    end_date = date(2024, 2, 16)

    dates = get_earnings_dates(ticker, start_date, end_date)
    for form, date in dates:
        print(f"{form}: {date}")