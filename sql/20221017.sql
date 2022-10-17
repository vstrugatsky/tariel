alter table earnings_reports alter column creator type varchar(30);
alter table earnings_reports alter column updater type varchar(30);

update earnings_reports set creator = 'Twitter_Marketcurrents', updater = 'Twitter_Marketcurrents'
where lower(provider_info->>'twitter_account') like 'marketcurrents%';

update earnings_reports set creator = 'Twitter_Livesquawk', updater = 'Twitter_Livesquawk'
where lower(provider_info->>'twitter_account') like 'livesquawk%';

alter table jobs alter column provider type varchar(30);