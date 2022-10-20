from __future__ import annotations
from typing import Optional
from sqlalchemy.orm import relationship, validates
import model as model
from sqlalchemy import Column, String, Boolean, Enum, ForeignKey, DateTime, FetchedValue, \
    Identity, Integer, UniqueConstraint
from datetime import datetime
from model.earnings_report_symbol import earnings_report_symbol_association
from model.exchanges import Exchange
from model.jobs import Provider


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
    earnings_reports = relationship("EarningsReport", secondary=earnings_report_symbol_association, back_populates='symbols')

    @validates('currency')
    def convert_upper(self, key, value):
        return value.upper()

    @staticmethod
    def get_unique_by_ticker_and_country(session: model.Session, ticker: str, iso_code_2: str) -> Optional[Symbol]:
        exchange: str = Symbol.find_exchange_by_ticker_and_country(session, ticker, iso_code_2)
        if exchange:
            return Symbol.get_unique(session, ticker, exchange, active=True, delisted=None)
        else:
            return None

    @staticmethod
    def find_exchange_by_ticker_and_country(session: model.Session, ticker: str, iso_code_2: str) -> Optional[str]:
        exchange = session.query(Symbol.exchange).join(Symbol.exchange_object).\
            filter(Symbol.symbol == ticker, Exchange.iso_country_code == iso_code_2). \
            order_by(Symbol.active.desc(), Symbol.created.desc()). \
            first()
        if exchange:
            return exchange[0]
        else:
            return None

    @staticmethod
    def get_unique(session: model.Session, ticker: str, exchange: str, active: bool, delisted: datetime) \
            -> Optional[Symbol]:
        return session.query(Symbol). \
            filter(Symbol.symbol == ticker,
                   Symbol.exchange == exchange,
                   Symbol.active == active,
                   Symbol.delisted == delisted). \
            scalar()

    @staticmethod
    def get_symbols_by_ticker_and_exchange(session: model.Session, ticker: str, exchange: str) -> [Symbol]:
        return session.query(Symbol). \
            filter(Symbol.symbol == ticker,
                   Symbol.exchange == exchange). \
            order_by(Symbol.active.asc(), Symbol.delisted.asc()). \
            all()
