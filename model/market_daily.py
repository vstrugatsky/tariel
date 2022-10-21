from __future__ import annotations
from datetime import date
from typing import Optional

from sqlalchemy import Column, Enum, Integer, Date, DateTime, Numeric, \
    UniqueConstraint, Identity, ForeignKey, FetchedValue
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import JSONB

import model
from model.jobs import Provider
from model.symbols import Symbol


class MarketDaily(model.Base):
    __tablename__ = 'market_daily'
    id = Column('id', Integer, Identity(always=True), primary_key=True)
    id_symbol = Column(Integer, ForeignKey("symbols.id"))
    symbol = relationship("Symbol")
    market_day = Column(Date, nullable=False)
    UniqueConstraint(id_symbol, market_day)

    price_close = Column(Numeric, nullable=False)
    price_high = Column(Numeric)
    price_low = Column(Numeric)
    price_open = Column(Numeric)
    num_transactions = Column(Numeric)
    volume = Column(Numeric)
    price_volume_weighted = Column(Numeric)

    created = Column(DateTime(timezone=True), FetchedValue())
    creator = Column(Enum(Provider))
    updated = Column(DateTime(timezone=True))
    updater = Column(Enum(Provider))
    provider_info = Column(JSONB)

    @staticmethod
    def get_unique(session: model.Session, symbol: Symbol, market_day: date) -> Optional[MarketDaily]:
        return session.query(MarketDaily). \
            filter(MarketDaily.id_symbol == symbol.id,
                   MarketDaily.market_day == market_day). \
            scalar()
