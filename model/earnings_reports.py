import model as model
from model.symbols import Symbol
from sqlalchemy.orm import relationship
from sqlalchemy import func, Column, String, Numeric, BigInteger, DateTime, Text, TIMESTAMP, ForeignKey
from datetime import datetime, timedelta


class EarningsReport(model.Base):
    __tablename__ = 'twitter_earnings_reports'

    tweet_id = Column(BigInteger, primary_key=True)
    tweet_date = Column(DateTime(timezone=True), nullable=False)
    twitter_account = Column(String(15), nullable=False)
    tweet_text = Column(Text, nullable=False)
    tweet_short_url = Column(String(23))
    tweet_expanded_url = Column(Text)
    tweet_url_status = Column(Numeric)
    tweet_url_title = Column(Text)
    tweet_url_description = Column(Text)

    parsed_symbol = Column(String(10), ForeignKey("symbols.symbol"), nullable=True)
    symbol_object = relationship("Symbol")
    currency = Column(String(3))
    eps = Column(Numeric)
    eps_surprise = Column(Numeric)
    revenue = Column(BigInteger)
    revenue_surprise = Column(BigInteger)
    guidance_direction = Column(String(20))

    @staticmethod
    def get_max_id():
        session = model.Session()
        return session.query(func.max(EarningsReport.tweet_id)).scalar()

    @staticmethod
    def get_max_date():
        session = model.Session()
        return session.query(func.max(EarningsReport.tweet_date)).scalar()

    # def from_twitter_marketcurrents(cls, i):
    #     return cls(symbol=i.get('ticker'),
    #                dividend_type=i.get('dividend_type'),
    #                cash_amount=i.get('cash_amount'),
    #                currency=i.get('currency', 'USD').upper(),
    #                declaration_date=i.get('declaration_date'),
    #                ex_dividend_date=i.get('ex_dividend_date'),
    #                pay_date=i.get('pay_date'),
    #                record_date=i.get('record_date'),
    #                frequency=i.get('frequency'))

    # @staticmethod
    # def load_from_polygon(i):
    #     if model.Session().query(Symbol).filter(Symbol.symbol == i.get('ticker')).count() == 1:
    #         dividend = EarningsReport.from_polygon(i)
    #         return dividend
    #     else:
    #         print(f'WARN {datetime.utcnow()} {i.get("ticker")} not found in Symbols')
    #         return None
#
#
# if __name__ == '__main__':
#     PolygonIo.call_paginated_api(
#                 PolygonIo.polygonPrefix + 'v3/reference/dividends',
#                 {'limit': 1000,
#                  'declaration_date.gte': datetime.utcnow() - timedelta(10),
#                  'order': 'asc',
#                  'sort': 'ticker'},
#                 method=Dividend.load_from_polygon, paginate=True, cursor=None)
