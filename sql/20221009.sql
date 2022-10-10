alter table jobs drop constraint jobs_pkey;
alter table jobs add column id bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY;
alter table jobs add unique(provider, job_type, started);

create table if not exists job_log (
    id bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    id_job bigint not null,
    severity varchar(5) not null,
    msg text not null,
    created timestamptz NOT NULL DEFAULT now(),
    constraint job_log_fk foreign key (id_job) references jobs(id)
);

alter table splits rename to splits_polygon;
create table if not exists splits (
  id bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  id_symbol bigint not null,
  split_from bigint not null,
  split_to bigint not null,
  execution_date date not null,
  created timestamptz NOT NULL DEFAULT now(),
  creator varchar(20) not null,
  updated timestamptz,
  updater varchar(20),
  constraint split_symbol foreign key (id_symbol) references symbols(id),
  unique (id_symbol, execution_date)
);

drop table api_requests;
