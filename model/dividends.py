from __future__ import annotations
from typing import Optional
from sqlalchemy.orm import relationship
from sqlalchemy import Column, String, Numeric, Date, Integer, DateTime, Enum, \
    Identity, ForeignKey, UniqueConstraint, FetchedValue
from datetime import date
import model as model
from model.jobs import Provider
from model.symbols import Symbol


class Dividend(model.Base):
    __tablename__ = 'dividends'
    id = Column('id', Integer, Identity(always=True), primary_key=True)
    id_symbol = Column(Integer, ForeignKey("symbols.id"))
    symbol = relationship("Symbol")
    ex_dividend_date = Column(Date, nullable=False)

    dividend_type = Column(String(2), nullable=False)
    cash_amount = Column(Numeric, nullable=False)
    currency = Column(String(3), nullable=False)
    declaration_date = Column(Date)
    record_date = Column(Date)
    pay_date = Column(Date)
    frequency = Column(Numeric, nullable=False)
    UniqueConstraint(id_symbol, ex_dividend_date)

    created = Column(DateTime(timezone=True), FetchedValue())
    creator = Column(Enum(Provider))

    updated = Column(DateTime(timezone=True))
    updater = Column(Enum(Provider))

    @staticmethod
    def get_unique(session: model.Session, symbol: Symbol, ex_dividend_date: date) -> Optional[Dividend]:
        return session.query(Dividend). \
            filter(Dividend.id_symbol == symbol.id,
                   Dividend.ex_dividend_date == ex_dividend_date). \
            scalar()
