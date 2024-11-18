from __future__ import annotations
from typing import Optional
from datetime import datetime, date

from sqlalchemy import Column, String, Date, DateTime, Identity, ForeignKey, PrimaryKeyConstraint

import model
from model.symbols_norgate import SymbolNorgate

class EarningsReport(model.Base):
    __tablename__ = 'earnings_reports'

    symbol_norgate = Column(String(20), nullable=False)
    # id_symbol = Column(Integer, ForeignKey("symbols.id"))
    # symbol = relationship("Symbol")
    fiscal_date_ending = Column(Date, nullable=False)
    creator = Column(String(20), nullable=False)
    PrimaryKeyConstraint(symbol_norgate, fiscal_date_ending, creator)
    reported_date = Column(Date, nullable=False)
    report_time = Column(String(20), nullable=True)

    created = Column(DateTime(timezone=True), default=datetime.now())
    updated = Column(DateTime(timezone=True), default=datetime.now())
    provider_updated = Column(Date, nullable=True)

    @staticmethod
    def get_unique(session: model.Session, symbol_norgate: SymbolNorgate, fiscal_date_ending: date, creator: str) -> Optional[EarningsReport]:
        return session.query(EarningsReport). \
            filter(EarningsReport.symbol_norgate == symbol_norgate,
                   EarningsReport.fiscal_date_ending == fiscal_date_ending,
                   EarningsReport.creator == creator). \
            scalar()
    
    @staticmethod
    def get_latest(session: model.Session, symbol_norgate: SymbolNorgate, creator: str) -> Optional[EarningsReport]:
        return session.query(EarningsReport). \
            filter(EarningsReport.symbol_norgate == symbol_norgate,
                   EarningsReport.creator == creator). \
            order_by(EarningsReport.fiscal_date_ending.desc()). \
            limit(1). \
            scalar()
