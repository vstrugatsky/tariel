drop table if exists earnings_calendar;
create table earnings_calendar(
symbol_norgate varchar(20) not null references symbols_norgate(symbol),
fiscal_date_ending date not null,
primary key(symbol_norgate, fiscal_date_ending),
report_date date not null,
estimate varchar(10),
currency varchar(3),
created timestamptz default current_timestamp,
creator varchar(20) default 'AlphaVantage',
updated timestamptz default current_timestamp,
updater varchar(20) default 'AlphaVantage');