from __future__ import annotations
from typing import Optional
import model as model
from model.jobs import Provider
from model.symbols import Symbol
from sqlalchemy.orm import relationship
from sqlalchemy import func, Enum, Column, String, Numeric, BigInteger, DateTime, Text, Date, ForeignKey, Integer, \
    Identity, UniqueConstraint, FetchedValue
from sqlalchemy.dialects.postgresql import JSONB
from datetime import date


class EarningsReport(model.Base):
    __tablename__ = 'earnings_reports'
    id = Column('id', Integer, Identity(always=True), primary_key=True)
    id_symbol = Column(Integer, ForeignKey("symbols.id"))
    symbol = relationship("Symbol")
    report_date = Column(Date, nullable=False)

    currency = Column(String(3))
    eps = Column(Numeric)
    eps_surprise = Column(Numeric)
    revenue = Column(BigInteger)
    revenue_surprise = Column(BigInteger)
    guidance_direction = Column(String(20))
    provider_info = Column(JSONB)

    created = Column(DateTime(timezone=True), FetchedValue())
    creator = Column(Enum(Provider))
    updated = Column(DateTime(timezone=True))
    updater = Column(Enum(Provider))

    UniqueConstraint(id_symbol, report_date)

    @staticmethod
    def get_unique(session: model.Session, symbol: Symbol, report_date: date) -> Optional[EarningsReport]:
        return session.query(EarningsReport). \
            filter(EarningsReport.id_symbol == symbol.id,
                   EarningsReport.report_date == report_date). \
            scalar()

    @staticmethod
    def get_max_date():
        session = model.Session()
        return session.query(func.max(EarningsReport.created)).scalar()

