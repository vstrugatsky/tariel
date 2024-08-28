from __future__ import annotations
import enum
from typing import Optional
from datetime import datetime, date

from sqlalchemy.orm import relationship
from sqlalchemy import Column, String, Date, DateTime, Identity, ForeignKey, PrimaryKeyConstraint, Enum

import model
from model.symbols_norgate import SymbolNorgate

class ReportTime(enum.Enum):
    BEFORE_OPEN = "before open"
    AFTER_CLOSE = "after close"
    DURING = "during"

class EarningsCalendar(model.Base):
    __tablename__ = 'earnings_calendar'

    symbol_norgate = Column(String(20), nullable=False)
    # id_symbol = Column(Integer, ForeignKey("symbols.id"))
    # symbol = relationship("Symbol")
    fiscal_date_ending = Column(Date, nullable=False)
    report_date = Column(Date, nullable=False)
    creator = Column(String(20), nullable=False)
    PrimaryKeyConstraint(symbol_norgate, fiscal_date_ending, creator)
    estimate = Column(String(10), nullable=True)
    currency = Column(String(3), nullable=True)

    created = Column(DateTime(timezone=True), default=datetime.now())
    updated = Column(DateTime(timezone=True), default=datetime.now())
    provider_updated = Column(Date, nullable=True)
    report_time = Column(Enum(ReportTime), nullable=True)

    @staticmethod
    def get_unique(session: model.Session, symbol_norgate: SymbolNorgate, fiscal_date_ending: date, creator: str) -> Optional[EarningsCalendar]:
        return session.query(EarningsCalendar). \
            filter(EarningsCalendar.symbol_norgate == symbol_norgate,
                   EarningsCalendar.fiscal_date_ending == fiscal_date_ending,
                   EarningsCalendar.creator == creator). \
            scalar()
