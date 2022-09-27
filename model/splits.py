import model as model
from model.symbols import Symbol
from sqlalchemy.orm import relationship
from sqlalchemy import Column, String, BigInteger, Date, ForeignKey, PrimaryKeyConstraint
from datetime import datetime, timedelta
from providers.polygon_io import PolygonIo


class Split(model.Base):
    __tablename__ = 'splits'
    symbol = Column(String(10), ForeignKey("symbols.symbol"), nullable=False)
    symbol_object = relationship("Symbol")
    split_from = Column(BigInteger, nullable=False)
    split_to = Column(BigInteger, nullable=False)
    execution_date = Column(Date, nullable=False)
    PrimaryKeyConstraint(symbol, execution_date)

    @classmethod
    def from_polygon(cls, i):
        return cls(symbol=i.get('ticker'),
                   split_from=i.get('split_from'),
                   split_to=i.get('split_to'),
                   execution_date=i.get('execution_date'))

    @staticmethod
    def load_from_polygon(i):
        if model.Session().query(Symbol).filter(Symbol.symbol == i.get('ticker')).count() == 1:
            split = Split.from_polygon(i)
            return split
        else:
            print(f'WARN {datetime.utcnow()} {i.get("ticker")} not found in Symbols')
            return None


if __name__ == '__main__':
    PolygonIo.call_paginated_api(
                PolygonIo.polygonPrefix + 'v3/reference/splits',
                {'limit': 1000,
                 'execution_date.gt': datetime.utcnow() - timedelta(30),
                 'order': 'asc',
                 'sort': 'ticker'},
                method=Split.load_from_polygon, paginate=True, cursor=None)
