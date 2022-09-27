alter table dividends add column created TIMESTAMP NOT NULL DEFAULT now();

set search_path = tariel;
drop table if exists splits;
create table if not exists splits (
     symbol varchar(10) not null,
     split_from bigint not null,
     split_to bigint not null,
     execution_date date not null,
     created TIMESTAMP NOT NULL DEFAULT now(),
     primary key (symbol, execution_date),
     constraint splits_symbol foreign key(symbol) references symbols(symbol));