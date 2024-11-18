alter table earnings_reports
    alter column creator drop default,
    alter column creator set not null,
    alter column updater drop default,
    alter column updater set not null;

alter table earnings_reports
    drop constraint earnings_reports_pkey,
    add primary key(symbol_norgate, fiscal_date_ending, creator),
    drop column updater,
    add column provider_updated date null;