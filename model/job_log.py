from __future__ import annotations
import enum

from sqlalchemy.orm import relationship
from sqlalchemy import Column, Enum, Text, Integer, DateTime, Identity, ForeignKey, FetchedValue

import model


class MsgSeverity(enum.Enum):
    FATAL = 1
    ERROR = 2
    WARN = 3
    INFO = 4
    DEBUG = 5
    TRACE = 6


class JobLog(model.Base):
    __tablename__ = 'job_log'
    id = Column('id', Integer, Identity(always=True), primary_key=True)
    id_job = Column(Integer, ForeignKey("jobs.id"))
    job = relationship("Job")
    severity = Column(Enum(MsgSeverity))
    msg = Column(Text, nullable=False)
    created = Column(DateTime(timezone=True), FetchedValue())
