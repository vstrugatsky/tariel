from __future__ import annotations
from typing import Optional
from datetime import datetime

from sqlalchemy.orm import validates
from sqlalchemy import Column, String, Date, DateTime, Identity, Integer

import model as model
from model.jobs import Provider

class SymbolNorgate(model.Base):
    __tablename__ = 'symbols_norgate'
    symbol = Column(String(20), primary_key=True)
    name = Column(String(300), nullable=False)
    exchange = Column(String(100), nullable=True)
    delisted = Column(Date, nullable=True)
    type = Column(String(20), nullable=True, default='Stock')
    currency = Column(String(10), nullable=False, default='USD')

    created = Column(DateTime(timezone=True), default=datetime.now())
    creator = Column(String(20), default=Provider.Norgate.name)

    updated = Column(DateTime(timezone=True), default=datetime.now())
    updater = Column(String(20), default=Provider.Norgate.name)

    @validates('currency')
    def convert_upper(self, key, value):
        return value.upper()

    @staticmethod
    def get_ticker_for_symbol(symbol: str) -> str:
        symbol_parts = symbol.split('-')
        if len(symbol_parts) == 2:  # delisted symbol in the TICKER-YYYYMM format
            return symbol_parts[0]
        else:
            return symbol