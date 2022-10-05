drop table if exists jobs;
create table if not exists jobs (
    provider varchar(20) not null,
    job_type varchar(20) not null,
    parameters text,
    started timestamptz not null,
    completed timestamptz,
    primary key (provider, job_type, started));

alter table symbols alter column type drop not null;
