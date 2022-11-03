from __future__ import annotations

from typing import Optional
from datetime import date

from sqlalchemy.ext.mutable import MutableList
from sqlalchemy.orm import relationship
from sqlalchemy import func, Enum, Column, String, Numeric, BigInteger, DateTime, Date, Integer, \
    Identity, FetchedValue, Text
from sqlalchemy.dialects.postgresql import JSONB, ARRAY

import model
import model.symbols as s  # can't import Symbol directly due to circular import error
from model.jobs import Provider
from model.earnings_report_symbol import earnings_report_symbol_association


class EarningsReport(model.Base):
    max_earnings_sentiment = 2
    max_guidance_sentiment = 1

    __tablename__ = 'earnings_reports'
    id = Column('id', Integer, Identity(always=True), primary_key=True)
    symbols = relationship("Symbol",
                           secondary=earnings_report_symbol_association,
                           back_populates='earnings_reports')

    report_date = Column(Date, nullable=False)
    currency = Column(String(3))
    eps = Column(Numeric)
    eps_surprise = Column(Numeric)
    revenue = Column(BigInteger)
    revenue_surprise = Column(BigInteger)
    positive_earnings = Column(MutableList.as_mutable(ARRAY(Text)))
    negative_earnings = Column(MutableList.as_mutable(ARRAY(Text)))
    positive_guidance = Column(MutableList.as_mutable(ARRAY(Text)))
    negative_guidance = Column(MutableList.as_mutable(ARRAY(Text)))
    earnings_sentiment = Column(Numeric)
    guidance_sentiment = Column(Numeric)
    provider_info = Column(MutableList.as_mutable(JSONB))
    data_quality_note = Column(Text)

    created = Column(DateTime(timezone=True), FetchedValue())
    creator = Column(Enum(Provider))
    updated = Column(DateTime(timezone=True))
    updater = Column(Enum(Provider))

    @staticmethod
    def get_unique(session: model.Session, symbol: s.Symbol, report_date: date) -> Optional[EarningsReport]:
        return session.query(EarningsReport).join(EarningsReport.symbols). \
            filter(s.Symbol.id == symbol.id,
                   EarningsReport.report_date == report_date).scalar()

    @staticmethod
    def get_unique_by_symbol_and_date_range(session: model.Session, symbol: s.Symbol, start_date: date, end_date: date) \
            -> Optional[EarningsReport]:
        return session.query(EarningsReport).join(EarningsReport.symbols). \
            filter(s.Symbol.id == symbol.id,
                   EarningsReport.report_date >= start_date,
                   EarningsReport.report_date <= end_date).scalar()

    @staticmethod
    def get_max_date(provider: str) -> Optional[DateTime]:
        session = model.Session()
        return session.query(func.max(EarningsReport.created)). \
            filter(EarningsReport.creator == provider). \
            scalar()

    @staticmethod
    def get_unique_by_symbols_and_date(session: model.Session, symbols: dict, report_date: date) \
            -> Optional[EarningsReport]:
        er: Optional[EarningsReport] = None
        for key in symbols:
            er = EarningsReport.get_unique(session, symbol=symbols[key], report_date=report_date)
            if er:
                break
        return er

    @staticmethod
    def get_unique_by_symbols_and_date_range(session: model.Session, symbols: dict, start_date: date, end_date: date) \
            -> Optional[EarningsReport]:
        er: Optional[EarningsReport] = None
        for key in symbols:
            er = EarningsReport.get_unique_by_symbol_and_date_range(session, symbol=symbols[key],
                                                                    start_date=start_date, end_date=end_date)
            if er:
                break
        return er
