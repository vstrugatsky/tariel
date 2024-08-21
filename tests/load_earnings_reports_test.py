from datetime import date
from loaders.earnings_reports_from_alphav import LoadEarningsReportsFromAlphaVantage

def test_match_eoq_date_to_norgate_symbol():

    symbols = {'TEST': None, 'TEST-202012': date(2020, 1, 1), 'TEST-202211': date(2022, 11, 1)}

    eoq_date = date(2019, 9, 30)
    assert(LoadEarningsReportsFromAlphaVantage.match_eoq_date_to_norgate_symbol(eoq_date, symbols) == 'TEST-202012')

    eoq_date = date(2021, 9, 30)
    assert(LoadEarningsReportsFromAlphaVantage.match_eoq_date_to_norgate_symbol(eoq_date, symbols) == 'TEST-202211')

    eoq_date = date(2023, 9, 30)
    assert(LoadEarningsReportsFromAlphaVantage.match_eoq_date_to_norgate_symbol(eoq_date, symbols) == 'TEST')

    symbols = {'TEST': None}
    eoq_date = date(2023, 9, 30)
    assert(LoadEarningsReportsFromAlphaVantage.match_eoq_date_to_norgate_symbol(eoq_date, symbols) == 'TEST')
