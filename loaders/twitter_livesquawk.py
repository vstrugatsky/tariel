from __future__ import annotations
from typing import Optional
from loaders.twitter_account import TwitterAccount
import re
from utils.utils import Utils


class Livesquawk(TwitterAccount):
    account_name = 'livesquawk'

    def parse_eps(self, tweet_text: str) -> Optional[re.Match]:
        p = re.compile(r'''
           EPS(:?)[ ](?P<eps_sign>[-])?(?P<eps_currency>C?[$])
           (?P<eps>\d+\.\d+)
           .+?
           (est|exp)[ ](?P<eps_estimate_currency>C?[$])?
           (?P<eps_estimate_amount>\d+\.\d+)?
           ''', re.VERBOSE | re.IGNORECASE | re.DOTALL)
        return p.search(tweet_text)

    def parse_revenue(self, tweet_text: str) -> Optional[re.Match]:
        p = re.compile(r'''
           Revenue(:?)[ ](?P<revenue_currency>C?[$])
           (?P<revenue>\d+\.?\d*)
           (?P<revenue_uom>[MBK])?
           .+?
           (est|exp)[ ](?P<revenue_estimate_currency>C?[$])?
           (?P<revenue_estimate_amount>\d+\.\d+)?
           (?P<revenue_estimate_uom>[MBK])?
           ''', re.VERBOSE | re.IGNORECASE | re.DOTALL)
        return p.search(tweet_text)

    def parse_tweet_v2(self, tweet_text: str) -> Optional[dict]:
        return_dict = {}
        eps_match: Optional[re.Match] = self.parse_eps(tweet_text)
        if eps_match:
            return_dict |= eps_match.groupdict()

        revenue_match: Optional[re.Match] = self.parse_revenue(tweet_text)
        if revenue_match:
            return_dict |= revenue_match.groupdict()
        return return_dict

    def parse_tweet(self, tweet_text: str) -> re.Match:
        # examples
        # tweet = 'LiveSquawk @LiveSquawk $DAL Delta Airlines Q3 22 Earnings: \
        #   - Adj EPS $1.51 (est $1.54) \
        #   - Adj Revenue $12.84B (est $12.83B) \
        #   - Sees Q4 Adj EPS $1 To $1.25 (est $0.80)'

        # tweet = '''
        #     $UNH UnitedHealth Q3 22 Earnings:
        # - EPS $5.55 (est $5.20)
        # - Revenue $46.56 (est $45.54)
        # - Sees FY EPS $ 20.85 To $21.05 (prev $20.45 To $20.95
        # '''
        p = re.compile(r'''
           EPS[ ](?P<eps_sign>[-])?(?P<eps_currency>C?[$])
           (?P<eps>\d+\.\d+)
           .+?
           (est|exp)[ ](?P<eps_estimate_currency>C?[$])?
           (?P<eps_estimate_amount>\d+\.\d+)?
           .+?
           Revenue[ ](?P<revenue_currency>C?[$])
           (?P<revenue>\d+\.?\d*)
           (?P<revenue_uom>[MBK])?
           .+?
           (est|exp)[ ](?P<revenue_estimate_currency>C?[$])?
           (?P<revenue_estimate_amount>\d+\.\d+)?
           (?P<revenue_estimate_uom>[MBK])?
           ''', re.VERBOSE | re.IGNORECASE | re.DOTALL)
        return p.search(tweet_text)

    def should_raise_parse_warning(self, tweet_text: str) -> bool:
        if 'Earnings:' in tweet_text:
            return True
        else:
            return False

    def determine_surprise(self, match_dict: dict, metrics: str) -> float | None:
        if metrics == 'eps':
            eps = float(match_dict.get('eps')) or None
            eps_estimate = float(match_dict.get('eps_estimate_amount')) or None
            return round(eps - eps_estimate, 2)
        elif metrics == 'revenue':
            revenue = float(match_dict.get('revenue')) or None
            revenue_estimate = float(match_dict.get('revenue_estimate_amount')) or None
            # default to billions if none - Livesquawk mainly covers large companies
            revenue_uom = match_dict.get('revenue_uom') or 'B'
            revenue_estimate_uom = match_dict.get('revenue_estimate_uom') or 'B'
            return round(
                Utils.apply_uom(revenue, revenue_uom) - Utils.apply_uom(revenue_estimate, revenue_estimate_uom), 2)

    def determine_revenue(self, match_dict: dict) -> float | None:
        # default to billions if none - Livesquawk mainly covers large companies
        revenue_uom = match_dict.get('revenue_uom') or 'B'
        return Utils.apply_uom(float(match_dict.get('revenue')), revenue_uom)
