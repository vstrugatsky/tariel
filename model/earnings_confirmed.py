from __future__ import annotations
from typing import Optional
from datetime import datetime, date

from sqlalchemy.orm import relationship
from sqlalchemy import Column, String, Date, DateTime, Text, PrimaryKeyConstraint

import model
from model.symbols_norgate import SymbolNorgate

class EarningsConfirmed(model.Base):
    __tablename__ = 'earnings_confirmed'

    symbol_norgate = Column(String(20), nullable=False)
    report_date = Column(Date, nullable=False)
    creator = Column(String(20), nullable=False)
    PrimaryKeyConstraint(symbol_norgate, report_date, creator)

    report_time = Column(String(20), nullable=True)
    report_when = Column(String(20), nullable=True)
    publication_date = Column(Date, nullable=True)
    publication_title = Column(Text, nullable=True)
    publication_url = Column(Text, nullable=True)

    created = Column(DateTime(timezone=True), default=datetime.now())
    updated = Column(DateTime(timezone=True), default=datetime.now())


    @staticmethod
    def get_unique(session: model.Session, symbol_norgate: SymbolNorgate, report_date: date, creator: str) -> Optional[EarningsConfirmed]:
        return session.query(EarningsConfirmed). \
            filter(EarningsConfirmed.symbol_norgate == symbol_norgate,
                   EarningsConfirmed.report_date == report_date,
                   EarningsConfirmed.creator == creator). \
            scalar()
