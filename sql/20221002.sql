alter table symbols add column updated timestamptz;

insert into exchange_acronyms (operating_mic, acronym) values
    ('NEOE', 'NEO') on conflict (operating_mic, acronym) do nothing;

alter table dividends drop constraint dividend_symbol,
    add constraint dividend_symbol foreign key(symbol, exchange, active) references symbols(symbol, exchange, active)
    on update cascade;

alter table splits drop constraint split_symbol,
    add constraint split_symbol foreign key(symbol, exchange, active) references symbols(symbol, exchange, active)
    on update cascade;

update symbols set active = false where updated is null;

