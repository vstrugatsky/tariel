import model as model
from sqlalchemy import Column, String, Boolean, PrimaryKeyConstraint, ForeignKey
import requests
from datetime import datetime
from model.exchanges import Exchange


class Symbol(model.Base):
    __tablename__ = 'symbols'
    symbol = Column(String(10), nullable=False)
    exchange = Column(String(4), ForeignKey("exchanges.operating_mic"), nullable=False)
    active = Column(Boolean, default=True)
    name = Column(String(200), nullable=True)
    type = Column(String(20), nullable=True)
    currency = Column(String(10), nullable=False)
    isin = Column(String(12), nullable=True)
    PrimaryKeyConstraint(symbol, exchange, active)

    @staticmethod
    def lookup_symbol(symbol: str, session: model.Session):
        return session.query(Symbol.symbol).filter(Symbol.symbol == symbol).scalar()


def eod_update_symbols(exchange_code: str):
    payload = {'fmt': 'json', 'api_token': model.eodApiKey}
    r = requests.get(model.eodPrefix + 'exchange-symbol-list/' + exchange_code, params=payload)
    print(f'{datetime.utcnow()} URL = {r.url}; Status = {r.status_code}; JSON = {r.json()}')
    with model.Session() as session:
        for i in r.json():
            print(i)
            exchange = Exchange.lookup_by_acronym(i.get("Exchange"), session)
            if exchange is None:
                exchange = Exchange.lookup_by_code(i.get("Exchange"), session)
            if exchange:
                symbol = Symbol(symbol=i.get("Code"),
                                exchange=exchange,
                                active=True,
                                name=i.get('Name'),
                                currency=i.get("Currency"),
                                type=i.get('Type'),
                                isin=i.get('Isin'))
                session.merge(symbol)
        session.commit()


if __name__ == '__main__':
    eod_update_symbols('LSE')  # loaded US, V, TO
    # PolygonIo.call_paginated_api(model.polygonPrefix + 'v3/reference/tickers',
    #             {'market': 'stocks', 'active': True, 'limit': 1000, 'order': 'asc', 'sort': 'ticker'},
    #             method=Symbol.from_polygon, paginate=True, cursor=None)
    # PolygonIo.call_paginated_api(model.polygonPrefix + 'v3/reference/tickers',
    #             {'market': 'stocks', 'active': False, 'limit': 1000, 'order': 'asc', 'sort': 'ticker'},
    #             method=Symbol.from_polygon, paginate=True, cursor=None)
    # PolygonIo.call_paginated_api(model.polygonPrefix + 'v3/reference/tickers',
    #             {'market': 'otc', 'active': True, 'limit': 1000, 'order': 'asc', 'sort': 'ticker'},
    #             method=Symbol.from_polygon, paginate=True, cursor=None)
    # PolygonIo.call_paginated_api(model.polygonPrefix + 'v3/reference/tickers',
    #             {'market': 'otc', 'active': False, 'limit': 1000, 'order': 'asc', 'sort': 'ticker'},
    #             method=Symbol.from_polygon, paginate=True, cursor=None)
