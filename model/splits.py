from __future__ import annotations
from sqlalchemy.orm import relationship
import model as model
from model.symbols import Symbol
from model.jobs import Provider
from sqlalchemy import Column, BigInteger, Date, DateTime, Enum, Integer, Identity, ForeignKey, UniqueConstraint, FetchedValue
from datetime import date
from typing import Optional


class Split(model.Base):
    __tablename__ = 'splits'
    id = Column('id', Integer, Identity(always=True), primary_key=True)
    id_symbol = Column(Integer, ForeignKey("symbols.id"))
    symbol = relationship("Symbol")
    execution_date = Column(Date, nullable=False)
    split_from = Column(BigInteger, nullable=False)
    split_to = Column(BigInteger, nullable=False)
    UniqueConstraint(id_symbol, execution_date)

    created = Column(DateTime(timezone=True), FetchedValue())
    creator = Column(Enum(Provider))
    updated = Column(DateTime(timezone=True))
    updater = Column(Enum(Provider))

    @staticmethod
    def get_unique(session: model.Session, symbol: Symbol, execution_date: date) -> Optional[Split]:
        return session.query(Split). \
            filter(Split.id_symbol == symbol.id,
                   Split.execution_date == execution_date). \
            scalar()
