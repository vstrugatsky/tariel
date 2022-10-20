from __future__ import annotations
from typing import Optional
from datetime import date
import model as model
from model.jobs import Provider
from model.symbols import Symbol
from sqlalchemy.orm import relationship
from sqlalchemy import func, Enum, Column, String, Numeric, BigInteger, DateTime, Date, Integer, \
    Identity, UniqueConstraint, FetchedValue
from sqlalchemy.dialects.postgresql import JSONB
from model.earnings_report_symbol import earnings_report_symbol_association


class EarningsReport(model.Base):
    __tablename__ = 'earnings_reports'
    id = Column('id', Integer, Identity(always=True), primary_key=True)
    symbols = relationship("Symbol", secondary=earnings_report_symbol_association, back_populates='earnings_reports')

    report_date = Column(Date, nullable=False)
    currency = Column(String(3))
    eps = Column(Numeric)
    eps_surprise = Column(Numeric)
    revenue = Column(BigInteger)
    revenue_surprise = Column(BigInteger)
    guidance_direction = Column(String(20))
    provider_info = Column(JSONB)
    provider_unique_id = Column(String(200), nullable=False)

    created = Column(DateTime(timezone=True), FetchedValue())
    creator = Column(Enum(Provider))
    updated = Column(DateTime(timezone=True))
    updater = Column(Enum(Provider))

    UniqueConstraint(provider_unique_id)

    @staticmethod
    def get_unique(session: model.Session, symbol: Symbol, report_date: date) -> Optional[EarningsReport]:
        return session.query(EarningsReport).join(EarningsReport.symbols). \
            filter(Symbol.id == symbol.id,
                   EarningsReport.report_date == report_date).scalar()

    @staticmethod
    def get_max_date(provider: str) -> Optional[DateTime]:
        session = model.Session()
        return session.query(func.max(EarningsReport.created)). \
            filter(EarningsReport.creator == provider). \
            scalar()
