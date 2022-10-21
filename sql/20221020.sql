drop table if exists market_daily;
create table market_daily(
    id bigint generated always as identity primary key,
    id_symbol bigint not null,
    market_day date not null,
    price_close numeric,
    price_high numeric,
    price_low numeric,
    price_open numeric,
    num_transactions numeric,
    volume numeric,
    price_volume_weighted numeric,
    created timestamp with time zone default now() not null,
    creator varchar(20) not null,
    updated timestamptz,
    updater varchar(20),
    provider_info jsonb,
    unique(id_symbol, market_day),
    constraint md_symbol foreign key (id_symbol) references symbols(id)
);