alter table earnings_calendar
    alter column creator drop default,
    alter column creator set not null,
    alter column updater drop default,
    alter column updater set not null;

alter table earnings_calendar
    drop constraint earnings_calendar_pkey,
    add primary key(symbol_norgate, fiscal_date_ending, creator),
    drop column updater,
    add column provider_updated date null,
    add column report_time varchar(20) null check(report_time in ('before open', 'after close', 'during'));

ALTER TABLE earnings_calendar
    DROP CONSTRAINT earnings_calendar_report_time_check,
    add constraint report_time_check check(report_time in ('BEFORE_OPEN', 'AFTER_CLOSE', 'DURING'));

drop table if exists earnings_confirmed;
create table earnings_confirmed(
  symbol_norgate varchar(20) not null references symbols_norgate(symbol),
  report_date date not null,
  creator varchar(20) not null,
  primary key(symbol_norgate, report_date, creator),
  report_time varchar(20),
  report_when varchar(20),
  publication_date date,
  publication_title text,
  publication_url text,
  created timestamptz default current_timestamp,
  updated timestamptz default current_timestamp);