from __future__ import annotations
from typing import Optional, Any, Set
from sqlalchemy.orm import relationship, validates
import model as model
from sqlalchemy import Column, String, Boolean, Enum, ForeignKey, DateTime, FetchedValue, \
    Identity, Integer, UniqueConstraint
from datetime import datetime
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
    def find_exchange_by_symbol_and_country(symbol: str, iso_code_2: str, session: model.Session) -> Optional[str]:
        exchange = session.query(Symbol.exchange).join(Symbol.exchange_object).\
            filter(Symbol.symbol == symbol, Exchange.iso_country_code == iso_code_2). \
            order_by(Symbol.active.desc(), Symbol.created.desc()). \
            first()
        if exchange:
            return exchange[0]
        else:
            return None
