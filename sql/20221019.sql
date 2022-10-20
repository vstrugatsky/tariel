drop table if exists earnings_reports_symbols;
create table earnings_reports_symbols(
    id_symbol bigint not null,
    id_earnings_report bigint not null,
    created timestamptz not null default now(),
    constraint ers_symbol foreign key (id_symbol) references symbols(id),
    constraint ers_er foreign key (id_earnings_report) references earnings_reports(id),
    primary key(id_symbol, id_earnings_report)
);

insert into earnings_reports_symbols (id_symbol, id_earnings_report)
select er.id_symbol, er.id from earnings_reports er;

alter table earnings_reports add column provider_unique_id varchar(200);
update earnings_reports set provider_unique_id = provider_info->>'tweet_id';
alter table earnings_reports alter column provider_unique_id set not null;
alter table earnings_reports add unique (provider_unique_id);
alter table earnings_reports drop constraint earnings_reports_id_symbol_report_date_key;
alter table earnings_reports alter column id_symbol drop not null;

alter table earnings_reports drop column id_symbol;