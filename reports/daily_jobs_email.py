import sys
from datetime import datetime, timezone

from loaders.loader_base import LoaderBase
from model.jobs import Job
from providers.gmail import Gmail

if __name__ == '__main__':
    start_time = float(sys.argv[1])
    email_body = ''
    jobs: [Job] = LoaderBase.get_jobs_since(datetime.fromtimestamp(start_time, timezone.utc))
    for job in jobs:
        job_desc = job.started.strftime('%Y-%m-%d %H:%M:%S') + ' ' \
                   + job.completed.strftime('%Y-%m-%d %H:%M:%S') + ' ' \
                   + str(job.job_info) + ' ' \
                   + job.provider.name + ':' + job.job_type.name + '\n'
        email_body += job_desc
    Gmail.send(subject='Daily Dose of Tariel', content=email_body)

    print('email_body: ' + email_body)
