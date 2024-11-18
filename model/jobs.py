import enum

from sqlalchemy import Column, DateTime, Enum, Text, Identity, UniqueConstraint, BigInteger
from sqlalchemy.dialects.postgresql import JSONB

import model

class Provider(enum.Enum):
    EOD = 1
    Polygon = 2
    Twitter_Livesquawk = 10         # lower-priority
    Twitter_Marketcurrents = 11      # higher-priority
    Norgate = 12
    AlphaVantage = 13
    Tariel = 14
    FMP = 15
    Edgar = 16
    IBKR = 17


class JobType(enum.Enum):
    Symbols = 1
    Dividends = 2
    Splits = 3
    EarningsReports = 4
    MarketDaily = 5
    Events = 6
    RealTestEventList = 7
    EarningsCalendar = 8
    EarningsConfirmed = 9
    IbkrSnapshots = 10
    

class Job(model.Base):
    __tablename__ = 'jobs'
    id = Column('id', BigInteger, Identity(always=True), primary_key=True)
    provider = Column(Enum(Provider))
    job_type = Column(Enum(JobType))
    parameters = Column(Text)
    job_info = Column(JSONB)
    started = Column(DateTime(timezone=True), nullable=False)
    completed = Column(DateTime(timezone=True))
    UniqueConstraint(provider, job_type, started)
