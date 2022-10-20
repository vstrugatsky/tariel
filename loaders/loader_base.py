from __future__ import annotations
from abc import ABC
from sqlalchemy import BigInteger
import model
from model.job_log import MsgSeverity, JobLog
from model.jobs import Provider, JobType, Job
from datetime import datetime


class LoaderBase(ABC):
    def __init__(self):
        self.records_added = 0
        self.records_updated = 0
        self.errors = 0
        self.warnings = 0
        self.job_id = 0

    @staticmethod
    def start_job(provider: Provider, job_type: JobType, params: str) -> BigInteger:
        started = datetime.now()
        with model.Session() as session:
            job = Job(provider=provider, job_type=job_type, parameters=params, started=started)
            session.add(job)
            session.commit()
            return session.query(Job.id). \
                filter(Job.provider == provider, Job.job_type == job_type, Job.started == started). \
                scalar()

    @staticmethod
    def finish_job(loader: LoaderBase):
        with model.Session() as session:
            job: Job = session.query(Job).filter(Job.id == loader.job_id).scalar()
            job.completed = datetime.now()
            job.job_info = {'added': loader.records_added,
                            'updated': loader.records_updated,
                            'errors': loader.errors,
                            'warnings': loader.warnings}
            session.commit()

    @staticmethod
    def write_log(session: model.Session, loader: LoaderBase, severity: MsgSeverity, msg: str):
        print(f'{severity.name} {msg}')
        if severity == MsgSeverity.WARN:
            loader.warnings += 1
        elif severity == MsgSeverity.ERROR:
            loader.errors += 1
        with session:
            job_log: JobLog = JobLog(id_job=loader.job_id, severity=severity, msg=msg)
            session.add(job_log)
            session.commit()

    @staticmethod
    def get_jobs_since(since: datetime, until: datetime = datetime.utcnow()) -> [Job]:
        with model.Session() as session:
            return session.query(Job). \
                filter(Job.started >= since, Job.started <= until). \
                order_by(Job.started.asc()). \
                all()
