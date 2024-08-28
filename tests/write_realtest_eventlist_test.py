from datetime import date
from transformers.to_realtest_eventlist import ToRealTestEventList
import pandas_market_calendars as mcal

def test_get_market_day_on_or_before():
    nyse_calendar = mcal.get_calendar('NYSE')

    input_date = date(2023, 12, 31)
    assert(ToRealTestEventList.get_market_day_on_or_before(input_date, nyse_calendar) == date(2023, 12, 29))

    input_date = date(2023, 12, 30)
    assert(ToRealTestEventList.get_market_day_on_or_before(input_date, nyse_calendar) == date(2023, 12, 29))
    
    input_date = date(2023, 12, 29)
    assert(ToRealTestEventList.get_market_day_on_or_before(input_date, nyse_calendar) == date(2023, 12, 29))

    input_date = date(2024, 1, 1)
    assert(ToRealTestEventList.get_market_day_on_or_before(input_date, nyse_calendar) == date(2023, 12, 29))

    input_date = date(2024, 1, 2)
    assert(ToRealTestEventList.get_market_day_on_or_before(input_date, nyse_calendar) == date(2024, 1, 2))
    

def test_get_market_day_on_or_after():
    nyse_calendar = mcal.get_calendar('NYSE')

    input_date = date(2023, 12, 31)
    assert(ToRealTestEventList.get_market_day_on_or_after(input_date, nyse_calendar) == date(2024, 1, 2))

    input_date = date(2023, 12, 29)
    assert(ToRealTestEventList.get_market_day_on_or_after(input_date, nyse_calendar) == date(2023, 12, 29))

    input_date = date(2024, 8, 24)
    assert(ToRealTestEventList.get_market_day_on_or_after(input_date, nyse_calendar) == date(2024, 8, 26))


def test_count_market_days():
    nyse_calendar = mcal.get_calendar('NYSE')
    assert(ToRealTestEventList.count_market_days(date(2024, 8, 22), date(2024, 8, 22), nyse_calendar) == 1)
    assert(ToRealTestEventList.count_market_days(date(2024, 8, 24), date(2024, 8, 24), nyse_calendar) == 0)
    assert(ToRealTestEventList.count_market_days(date(2024, 8, 22), date(2024, 8, 21), nyse_calendar) == 0)
    assert(ToRealTestEventList.count_market_days(date(2024, 8, 22), date(2024, 8, 23), nyse_calendar) == 2)
    assert(ToRealTestEventList.count_market_days(date(2024, 8, 22), date(2024, 8, 24), nyse_calendar) == 2)
    assert(ToRealTestEventList.count_market_days(date(2024, 8, 22), date(2024, 8, 25), nyse_calendar) == 2)
    assert(ToRealTestEventList.count_market_days(date(2024, 8, 22), date(2024, 8, 26), nyse_calendar) == 3)