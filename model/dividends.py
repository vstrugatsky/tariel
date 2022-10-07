from sqlalchemy.orm import relationship
import model as model
from model.symbols import Symbol
from sqlalchemy import Column, String, Numeric, Date, Boolean, Integer, \
    Identity, ForeignKey, UniqueConstraint
from datetime import datetime, timedelta
from providers.polygon import Polygon


class Dividend(model.Base):
    __tablename__ = 'dividends'
    id = Column('id', Integer, Identity(always=True), primary_key=True)
    symbol_id = Column(Integer, ForeignKey("symbols.id"))
    symbol = relationship("Symbol")
    dividend_type = Column(String(2), nullable=False)
    cash_amount = Column(Numeric, nullable=False)
    currency = Column(String(3), nullable=False)
    declaration_date = Column(Date, nullable=False)
    ex_dividend_date = Column(Date, nullable=False)
    record_date = Column(Date, nullable=False)
    pay_date = Column(Date, nullable=False)
    frequency = Column(Numeric, nullable=False)
    UniqueConstraint(symbol_id, ex_dividend_date)

    @staticmethod
    def load_from_polygon(i: dict, session: model.Session, method_params: dict) -> object:
        symbol = Symbol.lookup_symbol(i.get('ticker'), session)
        if symbol is None:
            print(f'WARN {datetime.utcnow()} {i.get("ticker")} not found in Symbols')
            return None

        country_code = method_params.get("country_code")
        exchange = Symbol.find_exchange_by_symbol_and_country(symbol, country_code, session)
        if exchange is None:
            print(f'WARN {datetime.utcnow()} {i.get("ticker")} not found in Symbols for country={country_code}')
            return None

        if exchange:
            return Dividend(symbol=symbol,
                            exchange=exchange,
                            active=True,
                            dividend_type=i.get('dividend_type'),
                            cash_amount=i.get('cash_amount'),
                            currency=i.get('currency', 'USD').upper(),
                            declaration_date=i.get('declaration_date'),
                            ex_dividend_date=i.get('ex_dividend_date'),
                            pay_date=i.get('pay_date'),
                            record_date=i.get('record_date'),
                            frequency=i.get('frequency'))


if __name__ == '__main__':
    Polygon.call_paginated_api(
        Polygon.polygonPrefix + 'v3/reference/dividends',
        payload={'limit': 1000,
                 'declaration_date.gte': datetime.utcnow() - timedelta(50),
                 'order': 'asc',
                 'sort': 'ticker'},
        method=Dividend.load_from_polygon,
        method_params={'country_code': 'US'},
        commit=True, paginate=True, cursor=None)
