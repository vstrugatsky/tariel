from __future__ import annotations
from abc import ABC
from sqlalchemy import BigInteger
import model
from model.job_log import MsgSeverity, JobLog
from model.jobs import Provider, JobType, Job
from model.symbols import Symbol
from datetime import datetime, date


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
    # tested by loader_base_test.py
    def find_candidate_symbol(symbols: [Symbol], event_date: date) -> Symbol | None:
        # active sorts false first, delisted - older date first
        symbols.sort(key=lambda x: (x.active, x.delisted))
        for symbol in symbols:
            if symbol.active or (not symbol.active and symbol.delisted.date() >= event_date):
                return symbol
        return None
