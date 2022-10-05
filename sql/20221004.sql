ALTER TABLE symbols RENAME TO symbols_eod;

drop table if exists symbols;
create table if not exists symbols (
   symbol varchar(10) not null,
   exchange varchar(4) not null,
   active boolean default true,
   name varchar(300) not null,
   type varchar(20),
   currency varchar(10) not null,
   isin varchar(12),
   cik varchar(10),
   composite_figi varchar(12),
   share_class_figi varchar(12),
   provider_last_updated timestamptz,
   created timestamptz NOT NULL DEFAULT now(),
   creator varchar(20) not null,
   updated timestamptz,
   updater varchar(20),
   primary key (symbol, exchange, active),
   constraint symbol_exchange foreign key(exchange) references exchanges(operating_mic)
);

alter table symbols add column delisted timestamptz;