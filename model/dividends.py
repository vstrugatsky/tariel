import model as model
from model.symbols import Symbol
from sqlalchemy.orm import relationship
from sqlalchemy import Column, String, Numeric, Date, ForeignKey, PrimaryKeyConstraint
from datetime import datetime, timedelta
from providers.polygon_io import PolygonIo


class Dividend(model.Base):
    __tablename__ = 'dividends'
    symbol = Column(String(10), ForeignKey("symbols.symbol"))
    symbol_object = relationship("Symbol")

    dividend_type = Column(String(2), nullable=False)
    cash_amount = Column(Numeric, nullable=False)
    currency = Column(String(3), nullable=False)
    declaration_date = Column(Date, nullable=False)
    ex_dividend_date = Column(Date, nullable=False)
    record_date = Column(Date, nullable=False)
    pay_date = Column(Date, nullable=False)
    frequency = Column(Numeric, nullable=False)
    PrimaryKeyConstraint(symbol, ex_dividend_date)

    @classmethod
    def from_polygon(cls, i):
        return cls(symbol=i.get('ticker'),
                   dividend_type=i.get('dividend_type'),
                   cash_amount=i.get('cash_amount'),
                   currency=i.get('currency', 'USD').upper(),
                   declaration_date=i.get('declaration_date'),
                   ex_dividend_date=i.get('ex_dividend_date'),
                   pay_date=i.get('pay_date'),
                   record_date=i.get('record_date'),
                   frequency=i.get('frequency'))

    @staticmethod
    def load_from_polygon(i):
        if model.Session().query(Symbol).filter(Symbol.symbol == i.get('ticker')).count() == 1:
            dividend = Dividend.from_polygon(i)
            return dividend
        else:
            print(f'WARN {datetime.utcnow()} {i.get("ticker")} not found in Symbols')
            return None


if __name__ == '__main__':
    PolygonIo.call_paginated_api(
                PolygonIo.polygonPrefix + 'v3/reference/dividends',
                {'limit': 1000,
                 'declaration_date.gte': datetime.utcnow() - timedelta(10),
                 'order': 'asc',
                 'sort': 'ticker'},
                method=Dividend.load_from_polygon, paginate=True, cursor=None)
