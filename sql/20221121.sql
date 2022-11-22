-- convert from Earnings_Reports to Events
alter table events add column old_id bigint;
insert into events(old_id, event_type, event_date, currency, er_eps, er_eps_surprise, er_revenue, er_revenue_surprise,
                   sentiment, parsed_positive, parsed_negative,
                   created, creator, updated, updater, provider_info, data_quality_note)
select id, 'Earnings_Report', report_date, currency, eps, eps_surprise, revenue, revenue_surprise,
       earnings_sentiment, positive_earnings, negative_earnings,
       created, creator, updated, updater, provider_info, data_quality_note from earnings_reports
where (earnings_sentiment is not null and earnings_sentiment <> 0) or eps is not null or eps_surprise is not null
or revenue is not null or revenue_surprise is not null or positive_earnings is not null or negative_earnings is not null; -- 3968

insert into events(old_id, event_type, event_date,
                   sentiment, parsed_positive, parsed_negative,
                   created, creator, updated, updater, provider_info, data_quality_note)
select id, 'Guidance', report_date,
       guidance_sentiment, positive_guidance, negative_guidance,
       created, creator, updated, updater, provider_info, data_quality_note from earnings_reports
where positive_guidance is not null or negative_guidance is not null; -- 210

insert into event_symbols(id_symbol, id_event, created)
select id_symbol, e.id, ers.created
       from earnings_reports_symbols ers
       inner join events e on ers.id_earnings_report = e.old_id; -- 4264
