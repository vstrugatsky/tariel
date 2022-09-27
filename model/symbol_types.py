import model as model
from sqlalchemy import Column, String
import requests
from datetime import datetime
from deprecated import deprecated


@deprecated(reason='Initially derived from Polygon but questionable data quality')
class SymbolType(model.Base):
    __tablename__ = 'symbol_types'
    code = Column(String(10), primary_key=True)
    asset_class = Column(String(10), nullable=False)
    locale = Column(String(10), nullable=False)
    description = Column(String, nullable=False)


def polygon_update_symbol_types():
    payload = {'apiKey': model.polygonApiKey, 'asset_class': 'stocks'}

    r = requests.get(model.polygonPrefix + 'v3/reference/tickers/types', params=payload)
    print(f'{datetime.utcnow()} URL={r.url} \n Status={r.status_code} Count={r.json().get("count")}')

    session = model.Session()
    for i in r.json()['results']:
        print(i)
        symbol_type = SymbolType(code=i.get('code'),
                                 asset_class=i.get('asset_class'),
                                 locale=i.get('locale'),
                                 description=i.get('description'))
        session.merge(symbol_type)
    session.commit()
    session.close()


if __name__ == '__main__':
    polygon_update_symbol_types()
