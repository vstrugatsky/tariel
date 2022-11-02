alter table earnings_reports drop constraint if exists earnings_reports_provider_unique_id_key;
alter table earnings_reports drop column provider_unique_id;

update earnings_reports set provider_info = json_build_array(provider_info);
update earnings_reports set guidance_sentiment = 1 where provider_info[0]->>'tweet_text' like '%raise%';
update earnings_reports set guidance_sentiment = null where guidance_sentiment = 0;

update earnings_reports set earnings_sentiment = 2 where eps_surprise > 0 and revenue_surprise > 0; -- 330
update earnings_reports set earnings_sentiment = -2 where eps_surprise < 0 and revenue_surprise < 0; -- 85
update earnings_reports set earnings_sentiment = 0 where eps_surprise < 0 and revenue_surprise > 0; -- 89
update earnings_reports set earnings_sentiment = 0 where eps_surprise > 0 and revenue_surprise < 0; -- 93
update earnings_reports set earnings_sentiment = 1 where eps_surprise > 0 and (revenue_surprise = 0 or revenue_surprise is null); -- 29
update earnings_reports set earnings_sentiment = 1 where revenue_surprise > 0 and (eps_surprise = 0 or eps_surprise is null); -- 63
update earnings_reports set earnings_sentiment = -1 where eps_surprise < 0 and (revenue_surprise = 0 or revenue_surprise is null); -- 20
update earnings_reports set earnings_sentiment = -1 where revenue_surprise < 0 and (eps_surprise = 0 or eps_surprise is null); -- 26
