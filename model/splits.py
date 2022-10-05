import model as model
from model.symbols import Symbol
from sqlalchemy import Column, String, Boolean, BigInteger, Date, PrimaryKeyConstraint, ForeignKeyConstraint
from datetime import datetime, timedelta
from providers.polygon import Polygon


class Split(model.Base):
    __tablename__ = 'splits'
    symbol = Column(String(10), nullable=False)
    exchange = Column(String(4), nullable=False)
    active = Column(Boolean, default=True)
    execution_date = Column(Date, nullable=False)
    split_from = Column(BigInteger, nullable=False)
    split_to = Column(BigInteger, nullable=False)
    PrimaryKeyConstraint(symbol, exchange, active, execution_date)
    ForeignKeyConstraint([symbol, exchange, active], ['symbols.symbol', 'symbols.exchange', 'symbols.active'])

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

        split = Split(symbol=symbol,
                      exchange=exchange,
                      active=True,
                      split_from=i.get('split_from'),
                      split_to=i.get('split_to'),
                      execution_date=i.get('execution_date'))
        return split


if __name__ == '__main__':
    Polygon.call_paginated_api(
        Polygon.polygonPrefix + 'v3/reference/splits',
        payload={'limit': 1000,
                 'execution_date.gt': datetime.utcnow() - timedelta(5),
                 'order': 'asc',
                 'sort': 'ticker'},
        method=Split.load_from_polygon,
        method_params={'country_code': 'US'},
        commit=True, paginate=True, cursor=None)
