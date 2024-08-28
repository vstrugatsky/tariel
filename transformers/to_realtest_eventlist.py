from __future__ import annotations
from datetime import datetime, date, timedelta
import pandas_market_calendars as mcal
import csv

import model
from loaders.loader_base import LoaderBase
from model.jobs import Provider, JobType
from model.earnings_reports import EarningsReport
from model.earnings_calendar import EarningsCalendar, ReportTime
from sqlalchemy import func

class ToRealTestEventList(LoaderBase):

    @staticmethod
    def write(csv_file_path: str):

        REALTEST_QTR_END_EVENT = '20'
        REALTEST_EARNINGS_EVENT = '21'
        REALTEST_DAYS_TO_NEXT_EARNINGS_EVENT = '22'
        TIME_POST_MARKET = '16:30:00'
        TIME_PRE_MARKET = '08:00:00'
        earnings_reports: list[EarningsReport] = []
        earnings_calendar: list[EarningsCalendar] = []
        nyse_calendar = mcal.get_calendar('NYSE')

        with model.Session() as session:
            earnings_reports = session.query(EarningsReport)\
                .filter(EarningsReport.creator == Provider.AlphaVantage.name)\
                .order_by(EarningsReport.symbol_norgate, EarningsReport.fiscal_date_ending).all()
                # .filter(EarningsReport.symbol_norgate == 'AAPL')\

            # earnings_calendar = session.query(
            #     EarningsCalendar.symbol_norgate,
            #     func.min(EarningsCalendar.report_date).label('report_date'),
            #     func.min(EarningsCalendar.fiscal_date_ending).label('fiscal_date_ending')
            #       # AlphaV may include more than one future report date for a symbol    
            # ).group_by(EarningsCalendar.symbol_norgate).all() 

            earnings_calendar = session.query(EarningsCalendar)\
                .filter(EarningsCalendar.creator == Provider.FMP.name)\
                .order_by(EarningsCalendar.symbol_norgate).all()

        with open(csv_file_path, 'w', newline='') as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow(["Symbol", "Date", "Time", "Type", "Value"])

            day_one: date = ToRealTestEventList.get_market_day_on_or_before(date.today(), nyse_calendar)
            day_two: date = ToRealTestEventList.get_market_day_on_or_after(day_one + timedelta(days=1), nyse_calendar)
            print("day_one: " + day_one.strftime('%Y-%m-%d') + " day_two: " + day_two.strftime('%Y-%m-%d'))

            for row in earnings_calendar:
                print("EC: " + row.symbol_norgate + " " + row.report_date.strftime('%Y-%m-%d'))

                # QTR End event
                fiscal_date_ending: date = ToRealTestEventList.get_market_day_on_or_before(row.fiscal_date_ending, nyse_calendar)
                writer.writerow([row.symbol_norgate, fiscal_date_ending.strftime('%Y-%m-%d'), TIME_PRE_MARKET, REALTEST_QTR_END_EVENT, '1'])

                # write a row for the closest two days to the current date to match the ending date in RT
                market_days = ToRealTestEventList.count_market_days(day_one, row.report_date, nyse_calendar)

                # latest_earnings_report = EarningsReport.get_latest(session, row.symbol_norgate)
                # if (latest_earnings_report and 
                #         (latest_earnings_report.report_time == 'pre-market' 
                #          or ToRealTestEventList.isFriday(latest_earnings_report.reported_date))):
                #     market_days = market_days - 1

                if row.report_time is None or row.report_time != ReportTime.AFTER_CLOSE:
                    market_days = market_days - 1

                writer.writerow([row.symbol_norgate, day_one.strftime('%Y-%m-%d'), TIME_PRE_MARKET, REALTEST_DAYS_TO_NEXT_EARNINGS_EVENT, market_days])
                writer.writerow([row.symbol_norgate, day_two.strftime('%Y-%m-%d'), TIME_PRE_MARKET, REALTEST_DAYS_TO_NEXT_EARNINGS_EVENT, market_days - 1])

            for row in earnings_reports:
                print("processing ER: " + row.symbol_norgate + " " + row.fiscal_date_ending.strftime('%Y-%m-%d'))

                # for each Earnings Report, write a row for the QTR end event and a row for the earnings event
                # QTR End event
                fiscal_date_ending: date = ToRealTestEventList.get_market_day_on_or_before(row.fiscal_date_ending, nyse_calendar)
                writer.writerow([row.symbol_norgate, fiscal_date_ending.strftime('%Y-%m-%d'), TIME_PRE_MARKET, REALTEST_QTR_END_EVENT, '1'])

                # Earnings Event
                reported_date: date = ToRealTestEventList.get_market_day_on_or_before(row.reported_date, nyse_calendar)
                if ToRealTestEventList.isFriday(reported_date) or row.report_time == 'pre-market': # Friday is always pre-market
                    realtest_time = TIME_PRE_MARKET 
                else:
                    realtest_time = TIME_POST_MARKET                
                writer.writerow([row.symbol_norgate, reported_date.strftime('%Y-%m-%d'), realtest_time, REALTEST_EARNINGS_EVENT, '1'])


    @staticmethod
    def isFriday(input_date: date) -> bool:
        return input_date.weekday() == 4


    @staticmethod
    def get_market_day_on_or_before(input_date: date, nyse: mcal.Calendar) -> date: 
        valid_days = nyse.valid_days(end_date=input_date, start_date=input_date - timedelta(days=10))
    
        if not valid_days.empty:
            return valid_days[-1].date()
        else:
            return input_date
        
 
    @staticmethod
    def get_market_day_on_or_after(input_date: date, nyse: mcal.Calendar) -> date: 
        valid_days = nyse.valid_days(start_date=input_date, end_date=input_date + timedelta(days=10))
        return valid_days[0].date()
        
 
    @staticmethod
    def count_market_days(start_date: date, end_date: date, nyse: mcal.Calendar) -> int:
        market_days = nyse.valid_days(start_date=start_date, end_date=end_date)
        return market_days.size
        

if __name__ == '__main__':
    transformer = ToRealTestEventList()
    transformer.job_id = LoaderBase.start_job(provider=Provider.Tariel, job_type=JobType.RealTestEventList, params='')
    transformer.write("/Volumes/[C] Windows 11/Users/vs/AlphaVantage/Earnings/" + datetime.now().strftime("%Y%m%d") + ".csv") 
    LoaderBase.finish_job(transformer)
