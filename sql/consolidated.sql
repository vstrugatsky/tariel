create type iso_10383_mic_type as enum ('OPRT', 'SGMT');

create type iso_10383_status as enum ('ACTIVE', 'MODIFIED', 'DELETED');

create table if not exists countries
(
    iso_code_2          varchar(2)              not null
        primary key,
    iso_code_3          varchar(3)              not null
        unique,
    name                varchar(100)            not null,
    region              varchar(100),
    sub_region          varchar(100),
    intermediate_region varchar(100),
    created             timestamp default now() not null
);

create table if not exists market_identifier_codes_iso_10383
(
    mic                     varchar(4)                not null
        primary key,
    operating_mic           varchar(4)                not null,
    market_type             iso_10383_mic_type not null,
    name                    text                      not null,
    legal_entity_name       text,
    lei                     varchar(20),
    market_category         varchar(4),
    acronym                 varchar(30),
    iso_country_code        varchar(2)                not null
        constraint iso_10383_country
            references countries,
    city                    text                      not null,
    website                 text,
    status                  iso_10383_status   not null,
    date_created_iso_8601   varchar(8)                not null,
    date_modified_iso_8601  varchar(8)                not null,
    date_validated_iso_8601 varchar(8),
    date_expiry_iso_8601    varchar(8),
    comments                text
);

create table if not exists exchanges
(
    operating_mic    varchar(4)                             not null
        constraint exchanges_pkey1
            primary key,
    name             text                                   not null,
    acronym          varchar(30),
    iso_country_code varchar(2)                             not null
        constraint exchange_country
            references countries,
    created          timestamp with time zone default now() not null
);


create index if not exists exchange_acronym
    on exchanges (acronym);

create table if not exists exchange_acronyms
(
    operating_mic varchar(4)                             not null
        constraint acronym_operating_mic
            references exchanges,
    acronym       varchar(30)                            not null
        unique,
    created       timestamp with time zone default now() not null,
    primary key (operating_mic, acronym)
);


create table if not exists jobs
(
    provider   varchar(20)              not null,
    job_type   varchar(20)              not null,
    parameters text,
    started    timestamp with time zone not null,
    completed  timestamp with time zone,
    id         bigint generated always as identity
        primary key,
    job_info   jsonb,
    unique (provider, job_type, started)
);

create table if not exists symbols
(
    id                    bigint generated always as identity
        constraint symbols_pkey3
            primary key,
    symbol                varchar(10)                            not null,
    exchange              varchar(4)                             not null
        constraint symbol_exchange
            references exchanges,
    active                boolean                  default true,
    delisted              timestamp with time zone,
    name                  varchar(300)                           not null,
    type                  varchar(20),
    currency              varchar(10)                            not null,
    isin                  varchar(12),
    cik                   varchar(10),
    composite_figi        varchar(12),
    share_class_figi      varchar(12),
    provider_last_updated timestamp with time zone,
    created               timestamp with time zone default now() not null,
    creator               varchar(20)                            not null,
    updated               timestamp with time zone,
    updater               varchar(20),
    unique (symbol, exchange, active, delisted)
);


create table if not exists dividends
(
    id               bigint generated always as identity
        constraint dividends_pkey1
            primary key,
    id_symbol        bigint                                 not null
        constraint dividend_symbol
            references symbols,
    dividend_type    varchar(2)                             not null,
    cash_amount      numeric                                not null,
    currency         varchar(3)                             not null,
    declaration_date date,
    ex_dividend_date date                                   not null,
    pay_date         date,
    record_date      date,
    frequency        integer                                not null,
    created          timestamp with time zone default now() not null,
    creator          varchar(20)                            not null,
    updated          timestamp with time zone,
    updater          varchar(20),
    unique (id_symbol, ex_dividend_date)
);


create table if not exists job_log
(
    id       bigint generated always as identity
        primary key,
    id_job   bigint                                 not null
        constraint job_log_fk
            references jobs,
    severity varchar(5)                             not null,
    msg      text                                   not null,
    created  timestamp with time zone default now() not null
);


create table if not exists splits
(
    id             bigint generated always as identity
        constraint splits_pkey1
            primary key,
    id_symbol      bigint                                 not null
        constraint split_symbol
            references symbols,
    split_from     bigint                                 not null,
    split_to       bigint                                 not null,
    execution_date date                                   not null,
    created        timestamp with time zone default now() not null,
    creator        varchar(20)                            not null,
    updated        timestamp with time zone,
    updater        varchar(20),
    unique (id_symbol, execution_date)
);


create table if not exists earnings_reports
(
    id                 bigint generated always as identity
        primary key,
    id_symbol          bigint                                 not null
        constraint er_symbol
            references symbols,
    report_date        date                                   not null,
    currency           varchar(3),
    eps                numeric,
    eps_surprise       numeric,
    revenue            numeric,
    revenue_surprise   numeric,
    guidance_direction varchar(20),
    created            timestamp with time zone default now() not null,
    creator            varchar(20)                            not null,
    updated            timestamp with time zone,
    updater            varchar(20),
    provider_info      jsonb,
    unique (id_symbol, report_date)
);

