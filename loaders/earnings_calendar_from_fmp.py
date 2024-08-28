from __future__ import annotations
from datetime import date, datetime, timedelta

import model
from loaders.loader_base import LoaderBase
from model.jobs import Provider, JobType
from model.earnings_calendar import EarningsCalendar, ReportTime
from model.symbols_norgate import SymbolNorgate
from config import config
import requests

class LoadEarningsCalendarFromFMP(LoaderBase):

    @staticmethod
    def load(commit: bool):
        fmp_prefix = 'https://financialmodelingprep.com/api/v3/earning_calendar?'
        from_date = datetime.now().strftime('%Y-%m-%d')
        to_date = (datetime.now() + timedelta(days=7)).strftime('%Y-%m-%d')
        url = fmp_prefix + 'from=' + from_date + '&to=' + to_date + '&apikey=' + config.fmp['api_key']
        print(url)
        try:
            r = requests.get(url)
            for i in r.json():
                with model.Session() as session:
                    symbol_norgate: SymbolNorgate = session.get(SymbolNorgate, i['symbol'])
                    fiscal_date_ending: date = datetime.strptime(i['fiscalDateEnding'], '%Y-%m-%d').date()
                    if symbol_norgate:
                        earnings_calendar = EarningsCalendar.get_unique(session, symbol_norgate.symbol, fiscal_date_ending, Provider.FMP.name)
                        if not earnings_calendar:
                            earnings_calendar = EarningsCalendar()
                        earnings_calendar.symbol_norgate = symbol_norgate.symbol
                        earnings_calendar.fiscal_date_ending = fiscal_date_ending
                        earnings_calendar.report_date = datetime.strptime(i['date'], '%Y-%m-%d').date()
                        earnings_calendar.creator = Provider.FMP.name
                        earnings_calendar.provider_updated = datetime.strptime(i['updatedFromDate'], '%Y-%m-%d').date()
                        report_time = i['time']
                        if report_time == "bmo":
                            earnings_calendar.report_time = ReportTime.BEFORE_OPEN
                        elif report_time == "amc":
                            earnings_calendar.report_time = ReportTime.AFTER_CLOSE
                        elif report_time == "--":
                            earnings_calendar.report_time = None
                        else:
                            print(f"Unknown report time: {report_time}")
                        session.merge(earnings_calendar)
                        if commit:
                            session.commit()
                    else:
                        print(f"SymbolNorgate not found for : {i['symbol']}")
        except Exception as e:
            print(f"API error calling {url} e: {str(e)}")

        # last step - delete dates in the past
        with model.Session() as session:
            session.query(EarningsCalendar).\
                filter(EarningsCalendar.report_date < date.today()).\
                delete(synchronize_session=False)
            if commit:
                session.commit()


if __name__ == '__main__':
    commit = True
    loader = LoadEarningsCalendarFromFMP()
    loader.job_id = LoaderBase.start_job(provider=Provider.FMP, job_type=JobType.EarningsCalendar, params='')
    loader.load(commit) 
    LoaderBase.finish_job(loader)