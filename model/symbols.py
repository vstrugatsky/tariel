from __future__ import annotations
import unittest
from typing import Optional, Any, Set
from sqlalchemy.orm import relationship, validates
import model as model
from sqlalchemy import Column, String, Boolean, Enum, ForeignKey, DateTime, FetchedValue, \
    Identity, Integer, UniqueConstraint
import requests
from datetime import datetime
from model.exchanges import Exchange
from model.jobs import Job, Provider, JobType


class Symbol(model.Base):
    __tablename__ = 'symbols'
    id = Column('id', Integer, Identity(always=True), primary_key=True)
    symbol = Column(String(10), nullable=False)
    exchange = Column(String(4), ForeignKey("exchanges.operating_mic"), nullable=False)
    active = Column(Boolean, default=True)
    delisted = Column(DateTime(timezone=True), nullable=True)
    name = Column(String(200), nullable=True)
    type = Column(String(20), nullable=True)
    currency = Column(String(10), nullable=False)
    isin = Column(String(12), nullable=True)
    cik = Column(String(10), nullable=True)
    composite_figi = Column(String(12), nullable=True)
    share_class_figi = Column(String(12), nullable=True)
    provider_last_updated = Column(DateTime(timezone=True))

    created = Column(DateTime(timezone=True), FetchedValue())
    creator = Column(Enum(Provider))

    updated = Column(DateTime(timezone=True))
    updater = Column(Enum(Provider))

    UniqueConstraint(symbol, exchange, active, delisted)
    exchange_object = relationship("Exchange")

    @validates('currency')
    def convert_upper(self, key, value):
        return value.upper()

    @staticmethod
    def get_unique(session: model.Session, symbol: str, exchange: str, active: bool, delisted: datetime) \
            -> Optional[Symbol]:
        return session.query(Symbol). \
            filter(Symbol.symbol == symbol,
                   Symbol.exchange == exchange,
                   Symbol.active == active,
                   Symbol.delisted == delisted). \
            scalar()

    @staticmethod
    def get_symbols_by_symbol_and_exchange(session: model.Session, symbol: str, exchange: str) -> [Symbol]:
        return session.query(Symbol). \
            filter(Symbol.symbol == symbol,
                   Symbol.exchange == exchange). \
            order_by(Symbol.active.asc(), Symbol.delisted.asc()). \
            all()

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
    def find_exchange_by_symbol_and_country(symbol: str, iso_code_2: str, session: model.Session) -> Optional[str]:
        return session.query(Symbol.exchange).join(Symbol.exchange_object).\
            filter(Symbol.symbol == symbol, Exchange.iso_country_code == iso_code_2, Symbol.active). \
            order_by(Symbol.created.desc()). \
            scalar()


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


def eod_update_symbols(exchange_code: str) -> Set:
    cached_exchanges = set()
    payload = {'fmt': 'json', 'api_token': model.eodApiKey}
    r = requests.get(model.eodPrefix + 'exchange-symbol-list/' + exchange_code, params=payload, timeout=10)
    print(f'{datetime.utcnow()} URL = {r.url}; Status = {r.status_code}')
    if r.status_code != 200:
        print(f'ERROR status={r.status_code}')
        exit(1)
    with model.Session() as session:
        for i in r.json():
            print(i)
            exchange = Exchange.lookup_by_acronym_or_code(i.get("Exchange"), session)
            if exchange:
                cached_exchanges.add(exchange)
                symbol = Symbol(symbol=i.get("Code"),
                                exchange=exchange,
                                active=True,
                                name=i.get('Name'),
                                currency=i.get("Currency"),
                                type=i.get('Type'),
                                isin=i.get('Isin'),
                                updated=datetime.now())  # no need for utcnow() - the column is set to timestamptz
                session.merge(symbol)
        session.commit()
        return cached_exchanges


if __name__ == '__main__':
    exchanges_to_load = [
      'NEO', 'V', 'TO',   # Canada
        # 'LSE'  # London Stock Exchange
    # 'US'   # All US Exchanges
    ]

    job: Job
    cached_exchanges = set()

    with model.Session() as session:
        job = Job(provider=Provider.EOD,
                  job_type=JobType.Symbols,
                  parameters='exchanges_to_load: ' + ",".join(exchanges_to_load),
                  started=datetime.now())
        session.merge(job)
        session.commit()

    for e in exchanges_to_load:
        cached_exchanges.update(eod_update_symbols(e))
        print(cached_exchanges)

    with model.Session() as session:
        job.completed = datetime.now()
        session.merge(job)
        session.query(Symbol). \
            filter(Symbol.active is True,
                   Symbol.updated < job.started,
                   Symbol.exchange.in_(cached_exchanges)).\
            update({'active': False}, synchronize_session=False)
        session.commit()


class TestFindExchangeBySymbolAndCountry(unittest.TestCase):
    @staticmethod
    def runTest():
        with model.Session() as session:
            (exchange, active) = Symbol.find_exchange_by_symbol_and_country('AAPL', 'US', session)
            print(exchange, active)
            assert(Symbol.find_exchange_by_symbol_and_country('AAPL', 'US', session) == ('XNAS', True))
            assert(Symbol.find_exchange_by_symbol_and_country('AAPL', 'CA', session) == (None, False))
            assert(Symbol.find_exchange_by_symbol_and_country('A', 'US', session) == ('XNYS', True))


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


class TestGetSymbolsBySymbolAndExchange(unittest.TestCase):
    @staticmethod
    def runTest():
        with model.Session() as session:
            assert(len(Symbol.get_symbols_by_symbol_and_exchange(session, 'AAPL', 'XNAS')) == 1)
            assert(len(Symbol.get_symbols_by_symbol_and_exchange(session, 'AAPL', 'XNYS')) == 0)
            assert(len(Symbol.get_symbols_by_symbol_and_exchange(session, 'AA', 'XNYS')) == 3)

