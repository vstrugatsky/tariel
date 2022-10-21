import enum

from sqlalchemy import Column, DateTime, Enum, Text, Identity, UniqueConstraint, BigInteger
from sqlalchemy.dialects.postgresql import JSONB

import model


class Provider(enum.Enum):
    EOD = 1
    Polygon = 2
    Twitter_Marketcurrents = 10  # lower-priority
    Twitter_Livesquawk = 11      # higher-priority


class JobType(enum.Enum):
    Symbols = 1
    Dividends = 2
    Splits = 3
    EarningsReports = 4
    MarketDaily = 5


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
