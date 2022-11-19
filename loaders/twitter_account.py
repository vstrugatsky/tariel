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
    def parse_positive_earnings(self, tweet_text: str):
        pass

    @abstractmethod
    def parse_negative_earnings(self, tweet_text: str):
        pass

    @abstractmethod
    def parse_earnings_indicator(self, tweet_text: str):
        pass

    @abstractmethod
    def parse_false_positive(self, tweet_text: str):
        pass

    @abstractmethod
    def parse_positive_guidance(self, tweet_text: str):
        pass

    @abstractmethod
    def parse_negative_guidance(self, tweet_text: str):
        pass

    @abstractmethod
    def parse_symbol_from_url_desc(self, tweet_text: str):
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
