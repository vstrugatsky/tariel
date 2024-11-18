alter table market_daily
    drop column provider_info,
    drop column updater,
    add column iv numeric null,
    add column pc_ratio numeric null,
    add column next_earnings text null,
    add column market_cap varchar(20) null,
    add column eps numeric null,
    add column shortable varchar(20) null,
    add column fee_rate numeric null,
    drop constraint market_daily_id_symbol_market_day_key,
    drop constraint market_daily_pkey,
    alter column creator set not null,
    add primary key(id_symbol, market_day, creator);

alter table market_daily
    alter column created type timestamptz,
    alter column created set default current_timestamp,
    alter column updated type timestamptz,
    alter column updated set default current_timestamp;