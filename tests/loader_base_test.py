from datetime import date, datetime
from loaders.loader_base import LoaderBase
from model.symbols import Symbol


def test_find_candidate_symbol():
    ex_dividend_date: date = datetime(2021, 11, 1).date()
    symbol_1 = Symbol(active=True, delisted=None)
    symbols = [symbol_1]
    assert (LoaderBase.find_candidate_symbol(symbols, ex_dividend_date) == symbol_1)

    ex_dividend_date: date = datetime(2021, 11, 1).date()
    symbol_1 = Symbol(active=False, delisted=datetime(2016, 10, 7))
    symbols = [symbol_1]
    assert (LoaderBase.find_candidate_symbol(symbols, ex_dividend_date) is None)

    ex_dividend_date: date = datetime(2021, 11, 1).date()
    symbol_1 = Symbol(active=False, delisted=datetime(2022, 10, 7))
    symbols = [symbol_1]
    assert (LoaderBase.find_candidate_symbol(symbols, ex_dividend_date) == symbol_1)

    ex_dividend_date: date = datetime(2021, 11, 1).date()
    symbol_1 = Symbol(active=False, delisted=datetime(2022, 10, 7))
    symbol_2 = Symbol(active=False, delisted=datetime(2021, 10, 7))
    symbols = [symbol_1, symbol_2]
    assert (LoaderBase.find_candidate_symbol(symbols, ex_dividend_date) == symbol_1)

    ex_dividend_date: date = datetime(2021, 11, 1).date()
    symbol_1 = Symbol(active=False, delisted=datetime(2020, 10, 7))
    symbol_2 = Symbol(active=False, delisted=datetime(2021, 10, 7))
    symbols = [symbol_1, symbol_2]
    assert (LoaderBase.find_candidate_symbol(symbols, ex_dividend_date) is None)

    ex_dividend_date: date = datetime(2021, 11, 1).date()
    symbol_1 = Symbol(active=True, delisted=None)
    symbol_2 = Symbol(active=False, delisted=datetime(2022, 10, 7))
    symbols = [symbol_1, symbol_2]
    assert (LoaderBase.find_candidate_symbol(symbols, ex_dividend_date) == symbol_2)

    ex_dividend_date: date = datetime(2021, 11, 1).date()
    symbol_1 = Symbol(active=True, delisted=None)
    symbol_2 = Symbol(active=False, delisted=datetime(2020, 10, 7))
    symbols = [symbol_1, symbol_2]
    assert (LoaderBase.find_candidate_symbol(symbols, ex_dividend_date) == symbol_1)