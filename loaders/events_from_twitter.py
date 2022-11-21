from __future__ import annotations
import sys
from typing import Type
from datetime import datetime, timedelta

from fuzzywuzzy import fuzz
from sqlalchemy.orm.attributes import flag_modified

import model
import loaders.ers_from_twitter as er
import loaders.guidance_from_twitter as g
from loaders.loader_base import LoaderBase
from loaders.twitter_account import TwitterAccount
from loaders.twitter_livesquawk import Livesquawk  # noqa
from loaders.twitter_marketcurrents import Marketcurrents  # noqa
from model.job_log import MsgSeverity
from model.jobs import Provider, JobType
from model.symbols import Symbol
from model.events import Event
from utils.utils import Utils
from providers.twitter import Twitter


class LoadEventsFromTwitter(LoaderBase):
    def __init__(self, account):
        self.account: TwitterAccount = account
        super(LoadEventsFromTwitter, self).__init__()

    @staticmethod
    def build_tweet_info_json(tweet_response: dict, account_name: str) -> dict:
        return {
            'tweet_id': tweet_response['id'],
            'tweet_date': tweet_response['created_at'],
            'tweet_text': tweet_response['text'],
            'twitter_account': account_name + '(' + tweet_response['author_id'] + ')',
            'tweet_short_url': Utils.find_first_match("entities.urls[0].url", tweet_response),
            'tweet_expanded_url': Utils.find_first_match("entities.urls[0].expanded_url", tweet_response),
            'tweet_url_status': Utils.find_first_match("entities.urls[0].status", tweet_response),
            'tweet_url_title': Utils.find_first_match("entities.urls[0].title", tweet_response),
            'tweet_url_description': Utils.find_first_match("entities.urls[0].description", tweet_response),
        }

    @staticmethod
    def update_provider_info_json(event: Event, tweet_info: dict, tweet_response: dict):
        if event.provider_info:
            index = next((j for j, item in enumerate(event.provider_info) if item["tweet_id"] == tweet_response['id']), None)
            if index is None:
                event.provider_info.append(tweet_info)
            else:
                event.provider_info[index] = tweet_info
            flag_modified(event, "provider_info")
        else:
            event.provider_info = [tweet_info]

    def get_symbols_for_tweet(self, session: model.Session, tweet_response) -> dict | None:
        tweet_text = tweet_response["text"]
        cashtags = Twitter.get_cashtags(tweet_response)
        tweet_url_desc = Utils.find_first_match("entities.urls[0].description", tweet_response)
        symbols, eliminated_symbols = self.associate_tweet_with_symbols(session, cashtags, tweet_text, tweet_url_desc)
        if not symbols:
            msg = 'Cannot associate symbol with cashtags ' + str(cashtags)
            LoaderBase.write_log(session, self, MsgSeverity.WARN, msg)
            return None
        if eliminated_symbols:
            msg = 'Eliminated symbols based on fuzzy matching ' + str(eliminated_symbols) + ' in ' + tweet_text
            LoaderBase.write_log(session, self, MsgSeverity.INFO, msg)
        return symbols

    def associate_tweet_with_symbols(self, session: model.Session, cashtags, tweet_text, tweet_url_desc) -> (dict, dict):
        symbols: dict = {}
        if not cashtags:
            return symbols, {}
        for d in cashtags:
            tag = d.get('tag')
            if tag and ('$' + tag + ' ' in tweet_text or '$' + tag + ':CA' not in tweet_text):  # exclude Canadian tickers
                candidate_symbol: Symbol = Symbol.get_unique_by_ticker_and_country(session, tag, 'US')
                if candidate_symbol:
                    symbols[candidate_symbol.symbol] = candidate_symbol

        if len(symbols) > 1:
            return self.eliminate_spurious_symbols(session, tweet_text, tweet_url_desc, symbols)
        else:
            return symbols, {}

    def eliminate_spurious_symbols(self, session: model.Session, tweet_text, tweet_url_desc, symbols) -> (dict, dict):
        retained_symbols = {}
        eliminated_symbols = {}
        fuzz_ratios = {}
        max_ratio = 0
        for symbol in symbols:
            symbol_name = Symbol.get_name_by_id(session, symbols[symbol].id)
            fuzz_ratios[symbol] = fuzz.token_set_ratio(tweet_text, symbol_name)
            if fuzz_ratios[symbol] > max_ratio:
                max_ratio = fuzz_ratios[symbol]

        for symbol in fuzz_ratios:
            parsed_symbol = self.account.parse_symbol_from_url_desc(tweet_url_desc)
            if fuzz_ratios[symbol] >= max_ratio or symbol == parsed_symbol:
                retained_symbols[symbol] = symbols[symbol]
            else:
                eliminated_symbols[symbol] = fuzz_ratios[symbol]

        return retained_symbols, eliminated_symbols

    @staticmethod
    def should_update(e: Event, provider: str) -> bool:
        # Allow update if updater is the same as creator or if updater's priority is higher than creator's
        new_updater = Provider[provider]
        new_updater_priority = new_updater.value
        creator_priority = e.creator.value
        if new_updater_priority < creator_priority:
            return False
        if e.updater:
            updater_priority = e.updater.value
            if new_updater_priority < updater_priority:
                return False
        return True

    @classmethod
    def load(cls, tweet_response: dict, session: model.Session, method_params: dict):
        driver: LoadEventsFromTwitter = method_params.get('driver')
        account: TwitterAccount = driver.account
        tweet_text: str = tweet_response["text"]
        cashtags = Twitter.get_cashtags(tweet_response)
        print(f'TWEET {tweet_response["created_at"]} {tweet_text} {str(cashtags)}')
        if not cashtags:
            return

        if account.parse_false_positive(tweet_text):
            print(f'INFO false positive detected')
            return

        er.LoadERFromTwitter(account).load(session, tweet_response, driver)
        g.LoadGuidanceFromTwitter(account).load(session, tweet_response, driver)


if __name__ == '__main__':
    account_name = sys.argv[1] if len(sys.argv) > 1 else 'Marketcurrents'
    account_class: Type[TwitterAccount] = getattr(sys.modules['loaders.twitter_' + account_name.lower()], account_name)
    driver = LoadEventsFromTwitter(account_class(account_name))
    provider = 'Twitter_' + account_name
    backfill = False
    commit = True
    paginate = True
    max_results = 100
    if backfill:
        max_date = datetime.utcnow() - timedelta(days=6, hours=23)  # to not hit the 7 days issue
    else:
        max_date = Event.get_max_date(provider) or datetime.utcnow() - timedelta(days=6, hours=23)

    payload = {'query': 'from:' + driver.account.account_name,
               'start_time': max_date.strftime("%Y-%m-%dT%H:%M:%SZ")}

    driver.job_id = LoaderBase.start_job(
        provider=Provider[provider], job_type=JobType.Events,
        params=str(payload) + ' paginate: ' + str(paginate))

    Twitter.call_paginated_api(
        url=Twitter.url_prefix + '/tweets/search/recent',
        payload=payload | {'tweet.fields': 'created_at,author_id,entities', 'max_results': max_results},
        method=LoadEventsFromTwitter.load,
        method_params={'driver': driver},
        paginate=paginate, commit=commit, next_token=None)

    LoaderBase.finish_job(driver)
