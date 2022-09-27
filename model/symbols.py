import model as model
from sqlalchemy import Column, String, TIMESTAMP, Boolean
import requests
from datetime import datetime
from providers.polygon_io import PolygonIo


class Symbol(model.Base):
    __tablename__ = 'symbols'
    symbol = Column(String(10), primary_key=True)
    currency = Column(String(10), nullable=False)

    eod_exchange_code = Column(String(6), nullable=True)
    eod_exchange = Column(String(10), nullable=True)
    eod_name = Column(String(200), nullable=True)
    eod_country = Column(String(3), nullable=True)
    eod_type = Column(String(20), nullable=True)
    eod_isin = Column(String(12), nullable=True)

    polygon_exchange = Column(String(10), nullable=True)
    polygon_name = Column(String(200), nullable=True)
    polygon_market = Column(String(10), nullable=True)
    polygon_locale = Column(String(2), nullable=True)
    polygon_active = Column(Boolean)
    polygon_type = Column(String(10), nullable=True)

    polygon_cik = Column(String(20), nullable=True)
    polygon_composite_figi = Column(String(20), nullable=True)
    polygon_share_class_figi = Column(String(20), nullable=True)
    polygon_last_updated_utc = Column(TIMESTAMP, nullable=True)

    @classmethod
    def from_polygon(cls, i):
        return cls(symbol=i.get('ticker'),
                   currency=i.get('currency_name').upper(),
                   polygon_locale=i.get('locale'),
                   polygon_market=i.get('market'),
                   polygon_name=i.get('name'),
                   polygon_exchange=i.get('primary_exchange', None),
                   polygon_type=i.get('type'),
                   polygon_active=i.get('active'),
                   polygon_cik=i.get('cik', None),
                   polygon_composite_figi=i.get('composite_figi', None),
                   polygon_share_class_figi=i.get('share_class_figi', None),
                   polygon_last_updated_utc=i.get('last_updated_utc'))

    @classmethod
    def from_eod(cls, i):
        return cls(symbol=i.get('Code'),
                   currency=i.get('Currency').upper(),
                   eod_name=i.get('Name'),
                   eod_exchange=i.get('Exchange', None),
                   eod_type=i.get('Type'),
                   eod_isin=i.get('Isin'))

    @staticmethod
    def lookup_symbol(symbol):
        session = model.Session()
        return session.query(Symbol.symbol).filter(Symbol.symbol == symbol).scalar()


def eod_update_symbols(exchange_code: str):
    payload = {'fmt': 'json', 'api_token': model.eodApiKey}
    r = requests.get(model.eodPrefix + 'exchange-symbol-list/' + exchange_code, params=payload)
    print(f'{datetime.utcnow()} URL = {r.url}; Status = {r.status_code}; JSON = {r.json()}')
    session = model.Session()
    for i in r.json():
        symbol = Symbol.from_eod(i)
        symbol.eod_exchange_code = exchange_code
        session.merge(symbol)
    session.commit()
    session.close()


if __name__ == '__main__':
    eod_update_symbols('TO')  # loaded US, V, TO
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
