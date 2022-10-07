delete from dividends d where not exists(select 1 from symbols s where s.symbol = d.symbol and s.exchange = d.exchange
    and s.active = d.active); -- 44369 + 988
delete from splits d where not exists(select 1 from symbols s where s.symbol = d.symbol and s.exchange = d.exchange
   and s.active = d.active); -- 1244 + 116

alter table dividends drop constraint dividend_symbol,
add constraint dividend_symbol foreign key(symbol, exchange, active) references symbols(symbol, exchange, active)
on update cascade;

alter table splits drop constraint split_symbol,
add constraint split_symbol foreign key(symbol, exchange, active) references symbols(symbol, exchange, active)
on update cascade;