set search_path = tariel;

update pg_database set encoding = pg_char_to_encoding('UTF8') where datname = 'vs';

drop table if exists exchanges;
create table if not exists exchanges (
    eod_exchange_code VARCHAR(10) primary key,
    operating_mic varchar(20) null,
    name varchar(100) not null,
    country_name varchar(50) not null,
    country_iso2 varchar(2) not null,
    country_iso3 varchar(3) not null,
    currency varchar(10) not null,
    created TIMESTAMP NOT NULL DEFAULT now());

set search_path = tariel;
drop table if exists symbols;
create table if not exists symbols (
     symbol VARCHAR(10) not null,
     country_iso2 varchar(2) not null,
     eod_exchange varchar(10) not null,
     eod_name varchar(200) not null,
     eod_type varchar(20) not null,
     currency varchar(10) not null,
     isin varchar(12),
     created TIMESTAMP NOT NULL DEFAULT now(),
     primary key(symbol, country_iso2),
     FOREIGN KEY(country_iso2) REFERENCES countries(iso_code_2));

alter table symbols
    add column polygon_exchange varchar(10) null,
    add column polygon_name varchar(200) null,
    add column polygon_type varchar(20) null,
    add column polygon_active boolean,
    add column polygon_cik varchar(20) null,
    add column polygon_composite_figi varchar(20) null,
    add column polygon_share_class_figi varchar(20) null,
    add column polygon_last_updated_utc timestamptz null;

alter table symbols alter column eod_exchange drop not null,
    alter column eod_name drop not null,
    alter column eod_type drop not null;

