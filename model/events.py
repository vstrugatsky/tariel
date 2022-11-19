from __future__ import annotations

from typing import Optional
from datetime import date
import enum

from sqlalchemy.ext.mutable import MutableList
from sqlalchemy.orm import relationship
from sqlalchemy import func, Enum, Column, String, Numeric, DateTime, Date, Integer, Identity, FetchedValue, Text, \
    BigInteger
from sqlalchemy.dialects.postgresql import JSONB, ARRAY

import model
import model.symbols as s  # can't import Symbol directly due to circular import error
from model.jobs import Provider
from model.event_symbols import event_symbol_association


class EventType(enum.Enum):
    Earnings_Report = 1
    Guidance = 2
    Dividend = 3
    Split = 4


class Event(model.Base):

    __tablename__ = 'events'
    id = Column('id', Integer, Identity(always=True), primary_key=True)
    symbols = relationship("Symbol",
                           secondary=event_symbol_association,
                           back_populates='events')

    event_type = Column(Enum(EventType))
    __mapper_args__ = {"polymorphic_on": event_type}

    event_date = Column(Date, nullable=False)
    sentiment = Column(Numeric)
    parsed_positive = Column(MutableList.as_mutable(ARRAY(Text)))
    parsed_negative = Column(MutableList.as_mutable(ARRAY(Text)))
    currency = Column(String(3))

    provider_info = Column(MutableList.as_mutable(JSONB))
    data_quality_note = Column(Text)

    created = Column(DateTime(timezone=True), FetchedValue())
    creator = Column(Enum(Provider))
    updated = Column(DateTime(timezone=True))
    updater = Column(Enum(Provider))

    @staticmethod
    def get_unique(session: model.Session, symbol: s.Symbol, event_type: EventType, event_date: date) -> Optional[Event]:
        return session.query(Event).join(Event.symbols). \
            filter(s.Symbol.id == symbol.id,
                   Event.event_type == event_type,
                   Event.event_date == event_date).scalar()

    @staticmethod
    def get_unique_by_symbol_and_date_range(session: model.Session, symbol: s.Symbol, event_type: EventType,
                                            start_date: date, end_date: date) -> Optional[Event]:
        return session.query(Event).join(Event.symbols). \
            filter(s.Symbol.id == symbol.id,
                   Event.event_type == event_type,
                   Event.event_date >= start_date,
                   Event.event_date <= end_date).scalar()

    @staticmethod
    def get_max_date(provider: str) -> Optional[DateTime]:
        session = model.Session()
        return session.query(func.max(Event.created)). \
            filter(Event.creator == provider). \
            scalar()

    @staticmethod
    def get_unique_by_symbols_and_date(session: model.Session, symbols: dict, event_type: EventType, report_date: date) \
            -> Optional[Event]:
        er: Optional[Event] = None
        for key in symbols:
            er = Event.get_unique(session, symbol=symbols[key], event_type=event_type, event_date=report_date)
            if er:
                break
        return er

    @staticmethod
    def get_unique_by_symbols_and_date_range(session: model.Session, symbols: dict, event_type: EventType,
                                             start_date: date, end_date: date) -> Optional[Event]:
        er: Optional[Event] = None
        for key in symbols:
            er = Event.get_unique_by_symbol_and_date_range(session, symbol=symbols[key], event_type=event_type,
                                                           start_date=start_date, end_date=end_date)
            if er:
                break
        return er


class ER(Event):
    max_earnings_sentiment = 2
    __mapper_args__ = {"polymorphic_identity": EventType.Earnings_Report}
    eps = Column('er_eps', Numeric)
    eps_surprise = Column('er_eps_surprise', Numeric)
    revenue = Column('er_revenue', BigInteger)
    revenue_surprise = Column('er_revenue_surprise', BigInteger)


class Guidance(Event):
    max_guidance_sentiment = 2
    __mapper_args__ = {"polymorphic_identity": EventType.Guidance}
