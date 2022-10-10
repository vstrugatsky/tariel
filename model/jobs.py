import enum
from sqlalchemy import Column, DateTime, Enum, Text, Integer, Identity, UniqueConstraint, BigInteger
from model import Base


class Provider(enum.Enum):
    EOD = 1
    Polygon = 2
    Twitter = 3


class JobType(enum.Enum):
    Symbols = 1
    Dividends = 2
    Splits = 3


class Job(Base):
    __tablename__ = 'jobs'
    id = Column('id', BigInteger, Identity(always=True), primary_key=True)
    provider = Column(Enum(Provider))
    job_type = Column(Enum(JobType))
    parameters = Column(Text)
    started = Column(DateTime(timezone=True), nullable=False)
    completed = Column(DateTime(timezone=True))
    UniqueConstraint(provider, job_type, started)
