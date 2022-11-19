from __future__ import annotations
from datetime import datetime, timedelta

import model
import loaders.events_from_twitter as e
from loaders.loader_base import LoaderBase
from loaders.twitter_account import TwitterAccount
from loaders.twitter_livesquawk import Livesquawk  # noqa
from loaders.twitter_marketcurrents import Marketcurrents  # noqa
from model.events import Guidance, Event, EventType
from model.jobs import Provider
from model.symbols import Symbol
from utils.utils import Utils


class LoadGuidanceFromTwitter(LoaderBase):
    POSITIVE_GUIDANCE = 'positive_guidance'
    NEGATIVE_GUIDANCE = 'negative_guidance'

    def __init__(self, account):
        self.account: TwitterAccount = account
        super(LoadGuidanceFromTwitter, self).__init__()

    def parse_guidance(self, tweet_text: str) -> dict:
        parsed_guidance = {}

        positive_guidance = self.account.parse_positive_guidance(tweet_text)
        if positive_guidance:
            parsed_guidance |= {self.POSITIVE_GUIDANCE: positive_guidance}

        negative_guidance = self.account.parse_negative_guidance(tweet_text)
        if negative_guidance:
            parsed_guidance |= {self.NEGATIVE_GUIDANCE: negative_guidance}

        return parsed_guidance

    def update_guidance(self, guidance: Guidance, tweet_response: dict, match_dict: dict):
        self.update_guidance_fields(guidance, match_dict)
        self.update_reference_fields(guidance, tweet_response, match_dict)

    def update_guidance_fields(self, guidance: Guidance, match_dict: dict):
        guidance.parsed_positive = Utils.update_list_without_dups(guidance.parsed_positive,
                                                                  match_dict.get(self.POSITIVE_GUIDANCE))
        guidance.parsed_negative = Utils.update_list_without_dups(guidance.parsed_negative,
                                                                  match_dict.get(self.NEGATIVE_GUIDANCE))
        guidance.sentiment = 0
        if guidance.parsed_positive:
            guidance.sentiment += len(guidance.parsed_positive)
        if guidance.parsed_negative:
            guidance.sentiment -= len(guidance.parsed_negative)

        guidance.sentiment = min(guidance.sentiment, Guidance.max_guidance_sentiment)
        guidance.sentiment = max(guidance.sentiment, 0 - Guidance.max_guidance_sentiment)

    def update_reference_fields(self, guidance: Guidance, tweet_response: dict, match_dict: dict):
        tweet_info = e.LoadEventsFromTwitter.build_tweet_info_json(tweet_response, self.account.account_name)

        if self.POSITIVE_GUIDANCE in match_dict:
            tweet_info[self.POSITIVE_GUIDANCE] = match_dict[self.POSITIVE_GUIDANCE]
        if self.NEGATIVE_GUIDANCE in match_dict:
            tweet_info[self.NEGATIVE_GUIDANCE] = match_dict[self.NEGATIVE_GUIDANCE]

        e.LoadEventsFromTwitter.update_provider_info_json(guidance, tweet_info, tweet_response)

    def load(self, session: model.Session, tweet_response: dict, symbols: [Symbol]) -> Guidance | None:
        tweet_text: str = tweet_response["text"]
        parsed_guidance = self.parse_guidance(tweet_text)
        if not parsed_guidance:
            return

        print(f'INFO associated {symbols.keys()} and matched {parsed_guidance}')

        provider = 'Twitter_' + self.account.account_name
        report_date = datetime.strptime(tweet_response['created_at'], '%Y-%m-%dT%H:%M:%S.%fZ').date()
        guidance = Event.get_unique_by_symbols_and_date_range\
            (session, symbols, EventType.Guidance, report_date - timedelta(days=5), report_date + timedelta(days=5))
        if not guidance:
            guidance = Guidance(creator=Provider[provider], event_date=report_date)
            session.add(guidance)
            for key in symbols:
                guidance.symbols.append(symbols[key])

            self.update_guidance(guidance, tweet_response, parsed_guidance)
            self.records_added += 1
        else:
            if e.LoadEventsFromTwitter.should_update(guidance, provider):
                guidance.updated = datetime.now()
                guidance.updater = Provider[provider]
                self.update_guidance(guidance, tweet_response, parsed_guidance)
                self.records_updated += 1
        return guidance  # for testing
