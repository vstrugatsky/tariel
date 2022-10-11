import model as model
from model.jobs import Provider
from sqlalchemy.orm import relationship
from sqlalchemy import func, Enum, Column, String, Numeric, BigInteger, DateTime, Text, Date, ForeignKey, Integer, \
    Identity, UniqueConstraint, FetchedValue
from sqlalchemy.dialects.postgresql import JSONB
from datetime import datetime, timedelta


class EarningsReport(model.Base):
    __tablename__ = 'earnings_reports'
    id = Column('id', Integer, Identity(always=True), primary_key=True)
    id_symbol = Column(Integer, ForeignKey("symbols.id"))
    symbol = relationship("Symbol")
    report_date = Column(Date, nullable=False)

    currency = Column(String(3))
    eps = Column(Numeric)
    eps_surprise = Column(Numeric)
    revenue = Column(BigInteger)
    revenue_surprise = Column(BigInteger)
    guidance_direction = Column(String(20))
    provider_info = Column(JSONB)

    created = Column(DateTime(timezone=True), FetchedValue())
    creator = Column(Enum(Provider))
    updated = Column(DateTime(timezone=True))
    updater = Column(Enum(Provider))

    UniqueConstraint(id_symbol, report_date)

    tweet_id = Column(BigInteger, primary_key=True)
    tweet_date = Column(DateTime(timezone=True), nullable=False)
    twitter_account = Column(String(15), nullable=False)
    tweet_text = Column(Text, nullable=False)
    tweet_short_url = Column(String(23))
    tweet_expanded_url = Column(Text)
    tweet_url_status = Column(Numeric)
    tweet_url_title = Column(Text)
    tweet_url_description = Column(Text)

    @staticmethod
    def get_max_date():
        session = model.Session()
        return session.query(func.max(EarningsReport.tweet_date)).scalar()

