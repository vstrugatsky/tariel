from __future__ import annotations
from datetime import date, datetime, timedelta

import model
from loaders.loader_base import LoaderBase
from model.earnings_confirmed import EarningsConfirmed
from model.jobs import Provider, JobType
from model.earnings_calendar import EarningsCalendar, ReportTime
from model.symbols_norgate import SymbolNorgate
from config import config
import requests

class LoadEarningsConfirmedFromFMP(LoaderBase):

    @staticmethod
    def load(commit: bool):
        fmp_prefix = 'https://financialmodelingprep.com/api/v4/earning-calendar-confirmed?'
        from_date = datetime.now().strftime('%Y-%m-%d')
        to_date = (datetime.now() + timedelta(days=7)).strftime('%Y-%m-%d')
        url = fmp_prefix + 'from=' + from_date + '&to=' + to_date + '&apikey=' + config.fmp['api_key']
        print(url)
        try:
            r = requests.get(url)
            for i in r.json():
                with model.Session() as session:
                    symbol_norgate: SymbolNorgate = session.get(SymbolNorgate, i['symbol'])
                    report_date: date = datetime.strptime(i['date'], '%Y-%m-%d').date()
                    if symbol_norgate:
                        earnings_confirmed = EarningsConfirmed.get_unique(session, symbol_norgate.symbol, report_date, Provider.FMP.name)
                        if not earnings_confirmed:
                            earnings_confirmed = EarningsConfirmed()
                        earnings_confirmed.symbol_norgate = symbol_norgate.symbol
                        earnings_confirmed.report_date = report_date
                        earnings_confirmed.creator = Provider.FMP.name
                        earnings_confirmed.report_time = i['time']
                        earnings_confirmed.report_when = i['when']
                        earnings_confirmed.publication_date = datetime.strptime(i['publicationDate'], '%Y-%m-%d').date()
                        earnings_confirmed.publication_title = i['title']
                        earnings_confirmed.publication_url = i['url']
                        session.merge(earnings_confirmed)
                        if commit:
                            session.commit()
                    else:
                        print(f"SymbolNorgate not found for : {i['symbol']}")
        except Exception as e:
            print(f"API error calling {url} e: {str(e)}")

        # last step - delete dates in the past
        with model.Session() as session:
            session.query(EarningsConfirmed).\
                filter(EarningsConfirmed.report_date < date.today()).\
                delete(synchronize_session=False)
            if commit:
                session.commit()


if __name__ == '__main__':
    commit = True
    loader = LoadEarningsConfirmedFromFMP()
    loader.job_id = LoaderBase.start_job(provider=Provider.FMP, job_type=JobType.EarningsConfirmed, params='')
    loader.load(commit) 
    LoaderBase.finish_job(loader)