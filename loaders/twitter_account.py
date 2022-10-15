from abc import ABC, abstractmethod


class TwitterAccount(ABC):
    def __init__(self, account_name):
        self.account_name = account_name

    @abstractmethod
    def parse_tweet(self, tweet_text: str):
        pass

    @abstractmethod
    def determine_surprise(self, match_dict: dict, metrics: str):
        pass

    @abstractmethod
    def determine_revenue(self, match_dict: dict):
        pass
