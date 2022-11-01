alter table earnings_reports add column guidance_sentiment numeric, add column earnings_sentiment numeric;
update earnings_reports set guidance_sentiment = 1 where guidance_direction = 'raises';
update earnings_reports set guidance_sentiment = -1 where guidance_direction in ('lowers', 'below');
alter table earnings_reports drop column guidance_direction;
