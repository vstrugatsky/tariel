from __future__ import annotations
from typing import Optional
from datetime import datetime, timedelta

import model
import loaders.events_from_twitter as e
from loaders.loader_base import LoaderBase
from loaders.twitter_account import TwitterAccount
from loaders.twitter_livesquawk import Livesquawk  # noqa
from loaders.twitter_marketcurrents import Marketcurrents  # noqa
from model.job_log import MsgSeverity
from model.jobs import Provider
from model.currency import Currency
from model.events import EventType, Event, ER
from utils.utils import Utils


class LoadERFromTwitter(LoaderBase):
    POSITIVE_EARNINGS = 'positive_earnings'
    NEGATIVE_EARNINGS = 'negative_earnings'

    def __init__(self, account):
        self.account: TwitterAccount = account
        super(LoadERFromTwitter, self).__init__()

    def parse_earnings_numbers(self, tweet_text: str) -> dict:
        parsed_earnings = {}

        eps_match = self.account.parse_eps(tweet_text)
        if eps_match:
            parsed_earnings |= eps_match.groupdict()

        revenue_match = self.account.parse_revenue(tweet_text)
        if revenue_match:
            parsed_earnings |= revenue_match.groupdict()

        return parsed_earnings

    def parse_earnings_sentiments(self, tweet_text: str) -> dict:
        parsed_sentiments = {}

        positive_earnings = self.account.parse_positive_earnings(tweet_text)
        if positive_earnings:
            parsed_sentiments |= {self.POSITIVE_EARNINGS: positive_earnings}

        negative_earnings = self.account.parse_negative_earnings(tweet_text)
        if negative_earnings:
            parsed_sentiments |= {self.NEGATIVE_EARNINGS: negative_earnings}

        return parsed_sentiments

    @classmethod
    def determine_currency(cls, eps_currency, revenue_currency) -> str | None:
        currency = eps_currency if eps_currency else revenue_currency
        return Currency.currencies.get(currency, None)

    @classmethod
    def determine_eps(cls, eps_sign: str | None, eps: str | None) -> float | None:
        if eps_sign == '-':
            return 0.0 - float(eps)
        else:
            return float(eps) if eps else None

    @classmethod
    def evaluate_data_quality(cls, er: ER) -> Optional[str]:
        if er.revenue_surprise and er.revenue and (abs(er.revenue_surprise) / er.revenue) >= 0.75:
            return 'Revenue surprise ' + str(er.revenue_surprise) + ' too large for revenue=' + str(er.revenue)
        else:
            return None

    def update_er(self, er: ER, tweet_response: dict, match_dict: dict):
        self.update_earnings_fields(er, match_dict)
        self.update_sentiment_fields(er)
        self.update_reference_fields(er, tweet_response, match_dict)
        er.data_quality_note = self.evaluate_data_quality(er)

    def update_earnings_fields(self, er: ER, match_dict: dict):
        if not er.currency:
            er.currency = self.determine_currency(match_dict.get('eps_currency'), match_dict.get('revenue_currency'))

        if not er.eps or match_dict.get('eps'):
            er.eps = self.determine_eps(match_dict.get('eps_sign'), match_dict.get('eps'))
        if not er.revenue or match_dict.get('revenue'):
            er.revenue = self.account.determine_revenue(match_dict)

        if not er.eps_surprise:
            er.eps_surprise = self.account.determine_surprise(match_dict, 'eps')
        if not er.revenue_surprise:
            er.revenue_surprise = self.account.determine_surprise(match_dict, 'revenue')

        er.parsed_positive = Utils.update_list_without_dups(er.parsed_positive, match_dict.get(self.POSITIVE_EARNINGS))
        er.parsed_negative = Utils.update_list_without_dups(er.parsed_negative, match_dict.get(self.NEGATIVE_EARNINGS))

    @classmethod
    def update_sentiment_fields(cls, er: ER):
        er.sentiment = 0  # Recalc from the beginning

        if er.eps_surprise and er.eps_surprise > 0:
            er.sentiment += 1
        if er.eps_surprise and er.eps_surprise < 0:
            er.sentiment -= 1
        if er.revenue_surprise and er.revenue_surprise > 0:
            er.sentiment += 1
        if er.revenue_surprise and er.revenue_surprise < 0:
            er.sentiment -= 1

        if er.parsed_positive:
            er.sentiment += len(er.parsed_positive)
        if er.parsed_negative:
            er.sentiment -= len(er.parsed_negative)

        er.sentiment = min(er.sentiment, ER.max_earnings_sentiment)
        er.sentiment = max(er.sentiment, 0 - ER.max_earnings_sentiment)

    def update_reference_fields(self, er: ER, tweet_response: dict, match_dict: dict):
        tweet_info = e.LoadEventsFromTwitter.build_tweet_info_json(tweet_response, self.account.account_name)

        if self.POSITIVE_EARNINGS in match_dict:
            tweet_info[self.POSITIVE_EARNINGS] = match_dict[self.POSITIVE_EARNINGS]
        if self.NEGATIVE_EARNINGS in match_dict:
            tweet_info[self.NEGATIVE_EARNINGS] = match_dict[self.NEGATIVE_EARNINGS]

        e.LoadEventsFromTwitter.update_provider_info_json(er, tweet_info, tweet_response)

    def warn_if_needed(self, tweet_text: str, driver: e.LoadEventsFromTwitter, session: model.Session):
        if self.account.should_raise_parse_warning(tweet_text):
            msg = 'Failed to parse likely earnings numbers or sentiments from ' + tweet_text
            LoaderBase.write_log(session, driver, MsgSeverity.WARN, msg)

    def load(self, session: model.Session, tweet_response: dict, driver: e.LoadEventsFromTwitter) -> ER | None:
        tweet_text: str = tweet_response["text"]
        parsed_earnings = self.parse_earnings_numbers(tweet_text)
        if not parsed_earnings:
            earnings_indicator = self.account.parse_simple_earnings_indicator(tweet_text)
            if not earnings_indicator:
                print(f'INFO cannot parse earnings numbers or indicator from {tweet_text}')
                return
            else:
                parsed_earnings = self.parse_earnings_sentiments(tweet_text)
                if not parsed_earnings:
                    indicator_text = earnings_indicator.groupdict()['earnings_indicator'].strip()
                    print(f'INFO cannot parse earnings sentiments from {tweet_text} despite indicator {indicator_text}')
                    self.warn_if_needed(tweet_text, driver, session)
                    return

        symbols = driver.get_symbols_for_tweet(session, tweet_response)
        if not symbols:
            return

        print(f'INFO associated {symbols.keys()} and matched {parsed_earnings}')
        provider = 'Twitter_' + self.account.account_name
        report_date = datetime.strptime(tweet_response['created_at'], '%Y-%m-%dT%H:%M:%S.%fZ').date()
        er = Event.get_unique_by_symbols_and_date_range(session, symbols, EventType.Earnings_Report,
                                                        start_date=report_date - timedelta(days=5),
                                                        end_date=report_date + timedelta(days=5))
        if not er:
            er = ER(creator=Provider[provider], event_date=report_date)
            session.add(er)
            for key in symbols:
                er.symbols.append(symbols[key])

            self.update_er(er, tweet_response, parsed_earnings)
            driver.records_added += 1
        else:
            if e.LoadEventsFromTwitter.should_update(er, provider):
                er.updated = datetime.now()
                er.updater = Provider[provider]
                self.update_er(er, tweet_response, parsed_earnings)
                driver.records_updated += 1
        return er  # for testing
