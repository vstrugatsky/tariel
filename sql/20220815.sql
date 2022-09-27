set search_path = tariel;
drop table if exists symbol_types;
create table if not exists symbol_types (
    code varchar(10) not null primary key,
    asset_class varchar(10) not null,
    locale varchar(10) not null,
    description text,
    created TIMESTAMP NOT NULL DEFAULT now());

alter table symbols add column polygon_market varchar(10), add column polygon_locale varchar(2),
    add constraint sy_type foreign key(polygon_type) references symbol_types(code);

alter table symbols alter column polygon_type type varchar(10);

alter table symbols drop constraint symbols_pkey;
alter table symbols add primary key (symbol);
alter table symbols drop constraint symbols_country_iso2_fkey;
alter table symbols drop column country_iso2;
alter table symbols add column eod_country varchar(3) null;
alter table symbols add column eod_exchange_code varchar(6) null;
alter table symbols rename column isin to eod_isin;
alter table symbols drop constraint sy_type;

set search_path = tariel;
drop table if exists dividends;
create table if not exists dividends (
symbol varchar(10) not null,
dividend_type varchar(2) not null,
cash_amount numeric not null,
currency varchar(3) not null,
declaration_date date not null,
ex_dividend_date date not null,
pay_date date not null,
record_date date not null,
frequency int not null,
primary key (symbol, ex_dividend_date),
constraint sy_symbol foreign key(symbol) references symbols(symbol));