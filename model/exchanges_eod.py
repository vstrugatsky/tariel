import model as model
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship
import requests
from model.countries import Country


class ExchangeEod(model.Base):
    __tablename__ = 'exchanges_eod'
    eod_exchange_code = Column(String(10), primary_key=True)
    operating_mic = Column(String(20))
    name = Column(String(100))
    currency = Column(String(10))
    country_iso2 = Column(String(2), ForeignKey("countries.iso_code_2"))
    country = relationship("Country")


def eod_update_exchanges():  # poor data as Exchanges can be comma-separated and no acronyms
    payload = {'fmt': 'json', 'api_token': model.eodApiKey}
    r = requests.get(model.eodPrefix + 'exchanges-list', params=payload)
    print(r.url)
    print(r.json())
    print(r.status_code)
    session = model.Session()
    for i in r.json():
        exchange = ExchangeEod(
            eod_exchange_code=i['Code'],
            operating_mic=i['OperatingMIC'] if i['OperatingMIC'] != "" else None,
            name=i['Name'],
            country_iso2=i['CountryISO2'] if i['CountryISO2'] != "" else None,
            currency=i['Currency'] if i['Currency'] != "" else None
        )
        session.merge(exchange)
    session.commit()
