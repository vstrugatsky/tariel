import model as model
from model.symbols import Symbol
from sqlalchemy import Column, String, Boolean, BigInteger, Date, PrimaryKeyConstraint, ForeignKeyConstraint
from datetime import datetime, timedelta
from providers.polygon_io import PolygonIo


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
    def load_from_polygon(i: dict, country_code: str, session: model.Session) -> object:
        exchange = Symbol.find_exchange_by_symbol_and_country(i.get('ticker'), country_code, session)
        if exchange:
            split = Split(symbol=i.get('ticker'),
                          exchange=exchange,
                          active=True,
                          split_from=i.get('split_from'),
                          split_to=i.get('split_to'),
                          execution_date=i.get('execution_date'))
            return split
        else:
            print(f'WARN {datetime.utcnow()} {i.get("ticker")} not found in Symbols for country={country_code}')
            return None


if __name__ == '__main__':
    PolygonIo.call_paginated_api(
        PolygonIo.polygonPrefix + 'v3/reference/splits',
        {'limit': 1000,
         'execution_date.gt': datetime.utcnow() - timedelta(50),
         'order': 'asc',
         'sort': 'ticker'},
        country_code='US',
        method=Split.load_from_polygon,
        commit=True, paginate=True, cursor=None)
