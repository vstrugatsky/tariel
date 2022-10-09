from model.symbols import Symbol
import model


def test_get_symbols_by_symbol_and_exchange():
    with model.Session() as session:
        assert(len(Symbol.get_symbols_by_symbol_and_exchange(session, 'AAPL', 'XNAS')) == 1)
        assert(len(Symbol.get_symbols_by_symbol_and_exchange(session, 'AAPL', 'XNYS')) == 0)
        assert(len(Symbol.get_symbols_by_symbol_and_exchange(session, 'AA', 'XNYS')) == 3)


def test_find_exchange_by_symbol_and_country():
    with model.Session() as session:
        assert(Symbol.find_exchange_by_symbol_and_country('AAPL', 'US', session) == 'XNAS')
        assert(Symbol.find_exchange_by_symbol_and_country('AAPL', 'CA', session) is None)
        assert(Symbol.find_exchange_by_symbol_and_country('A', 'US', session) == 'XNYS')