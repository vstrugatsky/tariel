from model.market_identifiers import MarketIdentifier
import model


def test_lookup_operating_mic_By_mic():
    with model.Session() as session:
        assert(MarketIdentifier.lookup_operating_mic_by_mic('ARCX', session) == 'XNYS')
        assert(MarketIdentifier.lookup_operating_mic_by_mic('XNYS', session) == 'XNYS')
        assert(MarketIdentifier.lookup_operating_mic_by_mic('XXXX', session) is None)