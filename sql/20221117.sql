set search_path = 'tariel';
drop type if exists event_type;
create type event_type as enum ('Earnings Report', 'Guidance', 'Dividend', 'Split');

drop table if exists events;
create table events(
    id bigint generated always as identity primary key,
    event_type event_type not null,
    event_date date not null,
    sentiment numeric,
    parsed_positive text[],
    parsed_negative text[],
    created timestamptz default now() not null,
    creator varchar(30) not null,
    updated timestamp with time zone,
    updater varchar(30),
    provider_info jsonb,
    data_quality_note text,
    currency varchar(3),
    er_eps numeric,
    er_eps_surprise numeric,
    er_revenue numeric,
    er_revenue_surprise numeric,
    div_percent_change numeric,
    split_from bigint,
    split_to bigint);

drop table if exists event_symbols;
create table event_symbols(
    id_symbol bigint,
    id_event bigint,
    created timestamptz default now() not null,
    constraint es_symbol foreign key (id_symbol) references symbols(id),
    constraint es_evt foreign key (id_event) references events(id),
    primary key(id_symbol, id_event)
);