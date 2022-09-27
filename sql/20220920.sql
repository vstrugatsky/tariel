drop table if exists exchange_acronyms;
create table if not exists exchange_acronyms (
operating_mic varchar(4) not null,
acronym varchar(30) not null unique,
created timestamptz not null default now(),
primary key (operating_mic, acronym),
constraint acronym_operating_mic foreign key(operating_mic) references exchanges(operating_mic));

insert into exchange_acronyms (operating_mic, acronym) values
('XTSE', 'TO'), ('XTSX', 'V'), ('XNAS', 'NASDAQ'), ('XCBO', 'BATS'),
('XNYS', 'NYSE'), ('XNYS', 'NYSE MKT'), ('XNYS', 'NYSE ARCA'), ('XNYS', 'AMEX'),
('OTCM', 'OTCMKTS'), ('OTCM', 'OTCGREY'), ('OTCM', 'OTCCE'),('OTCM', 'OTCQX'), ('OTCM', 'OTCQB'), ('OTCM', 'PINK')
on conflict (operating_mic, acronym) do nothing;

insert into symbols
select symbol, (select operating_mic from exchange_acronyms where acronym = sp.eod_exchange),
true, eod_name, eod_type, currency, eod_isin from symbols_polygon sp
where eod_exchange is not null and sp.eod_exchange in (select acronym from exchange_acronyms) -- excludes 'NMFQS' ;

alter table dividends add column exchange varchar(4);
update dividends d set exchange = (select exchange from symbols s where s.symbol = d.symbol);
delete from dividends where exchange is null;
alter table dividends alter column exchange set not null;
alter table dividends add column active boolean not null default true;
alter table dividends drop constraint sy_symbol,
    add constraint dividend_symbol foreign key(symbol, exchange, active) references symbols(symbol, exchange, active);
alter table dividends drop constraint dividends_pkey, add primary key(symbol, exchange, active, ex_dividend_date);

alter table splits add column exchange varchar(4);
update splits d set exchange = (select exchange from symbols s where s.symbol = d.symbol);
delete from splits where exchange is null;
alter table splits alter column exchange set not null;
alter table splits add column active boolean not null default true;
alter table splits drop constraint splits_symbol,
                      add constraint split_symbol foreign key(symbol, exchange, active) references symbols(symbol, exchange, active);
alter table splits drop constraint splits_pkey, add primary key(symbol, exchange, active, execution_date);

drop table if exists earnings_reports;
create table if not exists earnings_reports (
    symbol varchar(10) not null,
    exchange varchar(4) not null,
    active boolean not null default true,
    report_date date not null, -- get from tweet_date
    currency varchar(3),
    eps numeric,
    eps_surprise numeric,
    revenue numeric,
    revenue_surprise numeric,
    guidance_direction varchar(20),
    created timestamptz not null default now(),
    tweet_id bigint,
    tweet_date timestamp,
    twitter_account varchar(15),
    tweet_text text,
    tweet_short_url varchar(23),
    tweet_expanded_url text,
    tweet_url_status numeric,
    tweet_url_title text,
    tweet_url_description text,
    primary key (symbol, exchange, active, report_date),
    constraint earnings_symbol foreign key(symbol, exchange, active) references symbols(symbol, exchange, active));