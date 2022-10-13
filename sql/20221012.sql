drop table earnings_reports;
create table if not exists earnings_reports
(
    id bigint generated always as identity primary key,
    id_symbol bigint not null,
    report_date date not null,
    currency varchar(3),
    eps numeric,
    eps_surprise numeric,
    revenue numeric,
    revenue_surprise numeric,
    guidance_direction varchar(20),
    created timestamp with time zone default now() not null,
    creator varchar(20) not null,
    updated timestamptz,
    updater varchar(20),
    provider_info jsonb,
    constraint er_symbol foreign key (id_symbol) references symbols(id),
    unique (id_symbol, report_date)
);