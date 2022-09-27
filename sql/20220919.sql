set search_path = tariel;

ALTER TABLE exchanges RENAME TO exchanges_eod;

drop table if exists market_identifier_codes_iso_10383;
drop type iso_10383_mic_type, iso_10383_status;
create type iso_10383_mic_type as enum ('OPRT', 'SGMT');
create type iso_10383_status as enum ('ACTIVE', 'MODIFIED', 'DELETED');

create table if not exists market_identifier_codes_iso_10383 (
mic varchar(4) not null primary key,
operating_mic varchar(4) not null,
market_type iso_10383_mic_type not null,
name text not null,
legal_entity_name text null,
lei varchar(20) null,
market_category varchar(4) null,
acronym varchar(30), -- create separate table to support multiple
iso_country_code varchar(2) not null,
city text not null,
website text,
status iso_10383_status not null,
date_created_iso_8601 varchar(8) not null,
date_modified_iso_8601 varchar(8) not null,
date_validated_iso_8601 varchar(8) null,
date_expiry_iso_8601 varchar(8) null,
comments text,
constraint iso_10383_country foreign key(iso_country_code) references countries(iso_code_2));

copy market_identifier_codes_iso_10383
    from '/Users/vs/Downloads/ISO10383_MIC_NewFormat.csv'
    -- https://www.iso20022.org/sites/default/files/ISO10383_MIC/ISO10383_MIC_NewFormat.csv
    WITH (FORMAT csv, DELIMITER ',', HEADER)
    WHERE iso_country_code <> 'ZZ';

drop table if exists exchanges;
create table if not exists exchanges (
    operating_mic varchar(4) not null primary key,
    name text not null,
    acronym varchar(30), -- create separate table to support multiple
    iso_country_code varchar(2) not null,
    created timestamptz NOT NULL DEFAULT now(),
    constraint exchange_country foreign key(iso_country_code) references countries(iso_code_2));

insert into exchanges
select operating_mic, name, acronym, iso_country_code from market_identifier_codes_iso_10383
where status <> 'DELETED' and market_type = 'OPRT';

ALTER TABLE symbols RENAME TO symbols_polygon;
ALTER TABLE symbol_types RENAME TO symbol_types_polygon;

create index exchange_acronym on exchanges(acronym);

drop table if exists symbols;
create table if not exists symbols (
    symbol varchar(10) not null,
    exchange varchar(4) not null,
    active boolean default true,
    name varchar(200) not null,
    type varchar(20) not null,
    currency varchar(10) not null,
    isin varchar(12),
    created timestamptz NOT NULL DEFAULT now(),
    primary key (symbol, exchange, active),
    constraint symbol_exchange foreign key(exchange) references exchanges(operating_mic)
);
