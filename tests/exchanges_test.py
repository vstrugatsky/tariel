from model.exchanges import Exchange
import model


def test_lookup_exchange_by_acronym_or_code():
    with model.Session() as session:
        assert(Exchange.lookup_by_acronym_or_code('V', session) == 'XTSX')
        assert(Exchange.lookup_by_acronym_or_code('XTSX', session) == 'XTSX')