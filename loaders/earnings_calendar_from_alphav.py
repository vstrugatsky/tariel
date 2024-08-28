from __future__ import annotations
import csv
from datetime import date, datetime
from time import sleep

import model
from loaders.loader_base import LoaderBase
from model.jobs import Provider, JobType
from model.earnings_calendar import EarningsCalendar
from model.symbols_norgate import SymbolNorgate
from config import config
import requests

class LoadEarningsCalendarFromAlphaV(LoaderBase):

    @staticmethod
    def load(commit: bool):
        alphav_prefix = 'https://www.alphavantage.co/query?function=EARNINGS_CALENDAR'
        url = alphav_prefix + '&horizon=3month' + '&apikey=' + config.alphavantage['premium_api_key']
        with requests.Session() as s:
            download = s.get(url)
            decoded_content = download.content.decode('utf-8')
            reader = csv.reader(decoded_content.splitlines(), delimiter=',')
            next(reader) # skip header row
            for row in reader:
                alphav_symbol = row[0]
                # row[1] unused
                report_date: date = datetime.strptime(row[2], '%Y-%m-%d').date()
                fiscal_date_ending: date = datetime.strptime(row[3], '%Y-%m-%d').date()
                estimate = row[4]
                currency = row[5]
                with model.Session() as session:
                    symbol_norgate: SymbolNorgate = session.get(SymbolNorgate, alphav_symbol)
                    if symbol_norgate:
                        earnings_calendar = EarningsCalendar.get_unique(session, symbol_norgate.symbol, fiscal_date_ending, Provider.AlphaVantage.name)
                        if not earnings_calendar:
                            earnings_calendar = EarningsCalendar()
                        earnings_calendar.symbol_norgate = symbol_norgate.symbol
                        earnings_calendar.fiscal_date_ending = fiscal_date_ending
                        earnings_calendar.report_date = report_date
                        earnings_calendar.estimate = estimate
                        earnings_calendar.currency = currency
                        earnings_calendar.creator = Provider.AlphaVantage
                        earnings_calendar.updater = Provider.AlphaVantage
                        session.merge(earnings_calendar)
                        if commit:
                            session.commit()
                    else:
                        print(f'SymbolNorgate not found for : {alphav_symbol}')

        # last step - delete dates in the past
        with model.Session() as session:
            session.query(EarningsCalendar).\
                filter(EarningsCalendar.report_date < date.today()).\
                delete(synchronize_session=False)
            session.commit()


if __name__ == '__main__':
    commit = True
    loader = LoadEarningsCalendarFromAlphaV()
    loader.job_id = LoaderBase.start_job(provider=Provider.AlphaVantage, job_type=JobType.EarningsCalendar, params='')
    loader.load(commit) 
    LoaderBase.finish_job(loader)