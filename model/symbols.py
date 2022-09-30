import unittest
from typing import Optional, Any

from sqlalchemy.orm import relationship
import model as model
from sqlalchemy import Column, String, Boolean, PrimaryKeyConstraint, ForeignKey, DateTime
import requests
from datetime import datetime
from model.exchanges import Exchange


class Symbol(model.Base):
    __tablename__ = 'symbols'
    symbol = Column(String(10), nullable=False)
    exchange = Column(String(4), ForeignKey("exchanges.operating_mic"), nullable=False)
    active = Column(Boolean, default=True)
    name = Column(String(200), nullable=True)
    type = Column(String(20), nullable=True)
    currency = Column(String(10), nullable=False)
    isin = Column(String(12), nullable=True)
    created = Column(DateTime(timezone=True))
    PrimaryKeyConstraint(symbol, exchange, active)
    exchange_object = relationship("Exchange")

    @staticmethod
    def lookup_symbol(symbol: str, session: model.Session) -> Optional[Any]:
        returned_symbol = session.query(Symbol.symbol).\
            filter(Symbol.symbol == symbol).\
            order_by(Symbol.created.desc()).\
            first()
        if returned_symbol:
            return returned_symbol[0]
        else:
            return Symbol.convert_polygon_symbol_to_eod(symbol)

    @staticmethod
    def find_exchange_by_symbol_and_country(symbol: str, iso_code_2: str, session: model.Session) -> Optional[Any]:
        exchange = session.query(Symbol.exchange).join(Symbol.exchange_object).\
            filter(Symbol.symbol == symbol, Exchange.iso_country_code == iso_code_2, Symbol.active). \
            order_by(Symbol.created.desc()). \
            first()
        if exchange:
            return exchange[0]
        else:
            return None

    @staticmethod
    def convert_polygon_symbol_to_eod(symbol: str) -> Optional[Any]:
        # Polygon format for preferred stock:
        # replace lowercase p e.g. AAICpB -> AAIC-PB
        # replace dot e.g. AKO.A -> AKO-A
        index: int = symbol.find('p')
        if index > 0:
            return symbol[:index] + '-P' + symbol[index+1:]
        else:
            index = symbol.find('.')
            if index > 0:
                return symbol[:index] + '-' + symbol[index+1:]
            else:
                return None


def eod_update_symbols(exchange_code: str):
    payload = {'fmt': 'json', 'api_token': model.eodApiKey}
    r = requests.get(model.eodPrefix + 'exchange-symbol-list/' + exchange_code, params=payload)
    print(f'{datetime.utcnow()} URL = {r.url}; Status = {r.status_code}; JSON = {r.json()}')
    with model.Session() as session:
        for i in r.json():
            print(i)
            exchange = Exchange.lookup_by_acronym(i.get("Exchange"), session)
            if exchange is None:
                exchange = Exchange.lookup_by_code(i.get("Exchange"), session)
            if exchange:
                symbol = Symbol(symbol=i.get("Code"),
                                exchange=exchange,
                                active=True,
                                name=i.get('Name'),
                                currency=i.get("Currency"),
                                type=i.get('Type'),
                                isin=i.get('Isin'))
                session.merge(symbol)
        session.commit()


if __name__ == '__main__':
    eod_update_symbols('LSE')  # loaded US, V, TO
    # PolygonIo.call_paginated_api(model.polygonPrefix + 'v3/reference/tickers',
    #             {'market': 'stocks', 'active': True, 'limit': 1000, 'order': 'asc', 'sort': 'ticker'},
    #             method=Symbol.from_polygon, paginate=True, cursor=None)
    # PolygonIo.call_paginated_api(model.polygonPrefix + 'v3/reference/tickers',
    #             {'market': 'stocks', 'active': False, 'limit': 1000, 'order': 'asc', 'sort': 'ticker'},
    #             method=Symbol.from_polygon, paginate=True, cursor=None)
    # PolygonIo.call_paginated_api(model.polygonPrefix + 'v3/reference/tickers',
    #             {'market': 'otc', 'active': True, 'limit': 1000, 'order': 'asc', 'sort': 'ticker'},
    #             method=Symbol.from_polygon, paginate=True, cursor=None)
    # PolygonIo.call_paginated_api(model.polygonPrefix + 'v3/reference/tickers',
    #             {'market': 'otc', 'active': False, 'limit': 1000, 'order': 'asc', 'sort': 'ticker'},
    #             method=Symbol.from_polygon, paginate=True, cursor=None)


class TestFindExchangeBySymbolAndCountry(unittest.TestCase):
    @staticmethod
    def runTest():
        with model.Session() as session:
            assert(Symbol.find_exchange_by_symbol_and_country('AAPL', 'US', session) == 'XNAS')
            assert(Symbol.find_exchange_by_symbol_and_country('AAPL', 'CA', session) is None)
            assert(Symbol.find_exchange_by_symbol_and_country('A', 'US', session) == 'XNYS')
            assert(Symbol.find_exchange_by_symbol_and_country('A', 'CA', session) == 'XTSX')


class TestLookupSymbol(unittest.TestCase):
    @staticmethod
    def runTest():
        with model.Session() as session:
            assert(Symbol.lookup_symbol('AAICpB', session) == 'AAIC-PB')
            assert(Symbol.lookup_symbol('A', session) == 'A')
            assert(Symbol.lookup_symbol('AAPL', session) == 'AAPL')
            assert(Symbol.lookup_symbol('ZYZYZY', session) is None)


class TestConvertPolygonSymbolToEod(unittest.TestCase):
    @staticmethod
    def runTest():
        assert(Symbol.convert_polygon_symbol_to_eod('AAICpB') == 'AAIC-PB')
        assert(Symbol.convert_polygon_symbol_to_eod('AAICP') is None)
        assert(Symbol.convert_polygon_symbol_to_eod('ACRpC') == 'ACR-PC')
        assert(Symbol.convert_polygon_symbol_to_eod('AAIC') is None)
        assert(Symbol.convert_polygon_symbol_to_eod('AKO.A') == 'AKO-A')
