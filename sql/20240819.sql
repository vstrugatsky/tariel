drop table if exists symbols_norgate;
create table symbols_norgate(
symbol varchar(20) primary key,
name varchar(300) not null,
exchange varchar(100),
delisted date,
type varchar(5) not null default 'Stock',
currency varchar(3) not null default 'USD',
created timestamptz default current_timestamp,
creator varchar(20) default 'Norgate',
updated timestamptz default current_timestamp,
updater varchar(20) default 'Norgate');

drop table if exists earnings_reports_symbols;

drop table if exists earnings_reports;
create table earnings_reports(
symbol_norgate varchar(20) not null references symbols_norgate(symbol),
fiscal_date_ending date not null,
primary key(symbol_norgate, fiscal_date_ending),
reported_date date,
report_time varchar(20),
created timestamptz default current_timestamp,
creator varchar(20) default 'AlphaVantage',
updated timestamptz default current_timestamp,
updater varchar(20) default 'AlphaVantage');