from providers.polygon import Polygon


def test_convert_polygon_symbol_to_eod():
    assert(Polygon.convert_polygon_symbol_to_eod('AAICpB') == 'AAIC-PB')
    assert(Polygon.convert_polygon_symbol_to_eod('AAICP') is None)
    assert(Polygon.convert_polygon_symbol_to_eod('ACRpC') == 'ACR-PC')
    assert(Polygon.convert_polygon_symbol_to_eod('AAIC') is None)
    assert(Polygon.convert_polygon_symbol_to_eod('AKO.A') == 'AKO-A')
