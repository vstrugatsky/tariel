from __future__ import annotations
from datetime import date, datetime
from typing import Optional

from sqlalchemy import Column, Integer, Date, DateTime, Numeric, String, Identity, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
import model
from model.symbols import Symbol


class MarketDaily(model.Base):
    __tablename__ = 'market_daily'
    id = Column('id', Integer, Identity(always=True), primary_key=True)
    id_symbol = Column(Integer, ForeignKey("symbols.id"))
    symbol = relationship("Symbol")
    market_day = Column(Date, nullable=False)
    creator = Column(String(20), nullable=False)
    UniqueConstraint(id_symbol, market_day, creator)

    price_close = Column(Numeric, nullable=False)
    price_high = Column(Numeric)
    price_low = Column(Numeric)
    price_open = Column(Numeric)
    num_transactions = Column(Numeric)
    volume = Column(Numeric)
    price_volume_weighted = Column(Numeric)
    iv = Column(Numeric, nullable=True)
    pc_ratio = Column(Numeric, nullable=True)
    next_earnings = Column(String(20), nullable=True)
    market_cap = Column(String(20), nullable=True)
    eps = Column(Numeric, nullable=True)
    shortable = Column(String(20), nullable=True)
    fee_rate = Column(Numeric, nullable=True)

    created = Column(DateTime(timezone=True), default=datetime.now())
    updated = Column(DateTime(timezone=True), default=datetime.now())

    @staticmethod
    def get_unique(session: model.Session, symbol: Symbol, market_day: date, creator: str) -> Optional[MarketDaily]:
        return session.query(MarketDaily). \
            filter(MarketDaily.id_symbol == symbol.id,
                   MarketDaily.market_day == market_day,
                   MarketDaily.creator == creator). \
            scalar()
