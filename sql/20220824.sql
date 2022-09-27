set search_path = tariel;
drop table if exists twitter_earnings_reports;
create table if not exists twitter_earnings_reports (
  tweet_id bigint not null primary key,
  tweet_date TIMESTAMP NOT NULL,
  twitter_account varchar(15) not null,
  tweet_text text NOT NULL,
  tweet_short_url varchar(23) null,
  tweet_expanded_url text null,
  tweet_url_status numeric null,
  tweet_url_title text null,
  tweet_url_description text null,
  parsed_symbol varchar(10) null,
  currency varchar(3) null,
  eps decimal,
  eps_surprise decimal,
  revenue decimal,
  revenue_surprise decimal,
  guidance_direction varchar(20),
  created TIMESTAMPTZ NOT NULL DEFAULT now(),
  constraint twitter_symbol foreign key(parsed_symbol) references symbols(symbol));

alter table api_requests alter issued type TIMESTAMPTZ USING issued at time zone 'utc';
alter table exchanges alter created type TIMESTAMPTZ USING created at time zone 'utc';
alter table symbols alter created type TIMESTAMPTZ;
alter table symbol_types alter created type TIMESTAMPTZ;
alter table dividends alter created type TIMESTAMPTZ;
alter table splits alter created type TIMESTAMPTZ;