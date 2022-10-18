from abc import ABC, abstractmethod


class TwitterAccount(ABC):
    def __init__(self, account_name):
        self.account_name = account_name

    @abstractmethod
    def parse_eps(self, tweet_text: str):
        pass

    @abstractmethod
    def parse_revenue(self, tweet_text: str):
        pass

    @abstractmethod
    def parse_guidance(self, tweet_text: str):
        pass

    @abstractmethod
    def should_raise_parse_warning(self, tweet_text: str) -> bool:
        pass

    @abstractmethod
    def determine_surprise(self, match_dict: dict, metrics: str):
        pass

    @abstractmethod
    def determine_revenue(self, match_dict: dict):
        pass
