alter table symbols rename to symbols_polygon;

drop table if exists symbols;
create table if not exists symbols (
       id bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
       symbol varchar(10) not null,
       exchange varchar(4) not null,
       active boolean default true,
       delisted timestamptz,
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
       unique (symbol, exchange, active, delisted),
       constraint symbol_exchange foreign key(exchange) references exchanges(operating_mic)
);

alter table dividends rename to dividends_polygon;

create table if not exists dividends
(   id bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    id_symbol bigint not null,
    dividend_type varchar(2) not null,
    cash_amount numeric not null,
    currency varchar(3) not null,
    declaration_date date not null,
    ex_dividend_date date not null,
    pay_date date not null,
    record_date date not null,
    frequency integer not null,
    created timestamptz NOT NULL DEFAULT now(),
    creator varchar(20) not null,
    updated timestamptz,
    updater varchar(20),
    constraint dividend_symbol foreign key (id_symbol) references symbols,
    unique (id_symbol, ex_dividend_date)
);