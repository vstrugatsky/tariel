from __future__ import annotations
from loaders.twitter_account import TwitterAccount
import re
from utils.utils import Utils


class Marketcurrents(TwitterAccount):
    account_name = 'marketcurrents'

    def parse_eps(self, tweet_text: str):
        p = re.compile(r'''
           (EPS|NII|EPADR|FFO)[ ]of[ ](?P<eps_sign>[-])?(?P<eps_currency>C[$]|[$]|€|₹|SEK)      
           (?P<eps>\d+\.\d+)
           [ ]?(?P<eps_surprise_direction>misses|beats)?
           ([ ]by[ ])?(?P<eps_surprise_currency>C[$]|[$]|€|₹|SEK)?
           (?P<eps_surprise_amount>\d+\.\d+)?
           ''', re.VERBOSE | re.IGNORECASE | re.DOTALL)
        return p.search(tweet_text)

    def parse_revenue(self, tweet_text: str):
        p = re.compile(r'''
           (revenue|investment[ ]income)[ ]of[ ](?P<revenue_currency>C[$]|[$]|€|₹|SEK)
           (?P<revenue>\d+\.?\d*)
           (?P<revenue_uom>[MBK])
           [ ]?(?P<revenue_surprise_direction>misses|beats)?
           ([ ]by[ ])?(?P<revenue_surprise_currency>C[$]|[$]|€|₹|SEK)?
           (?P<revenue_surprise_amount>\d+\.?\d*)?
           (?P<revenue_surprise_uom>[MBK])?
        ''', re.VERBOSE | re.IGNORECASE | re.DOTALL)
        return p.search(tweet_text)

    def parse_guidance(self, tweet_text: str):
        p = re.compile(r'''
           (?P<guidance_1>raises|lowers|reaffirms)
           ''', re.VERBOSE | re.IGNORECASE | re.DOTALL)
        return p.search(tweet_text)

    def should_raise_parse_warning(self, tweet_text: str) -> bool:
        return False

    def determine_surprise(self, match_dict: dict, metrics: str) -> float | None:
        if metrics == 'eps':
            surprise_direction = match_dict.get('eps_surprise_direction')
            surprise_amount = match_dict.get('eps_surprise_amount')
            surprise_uom = None
        elif metrics == 'revenue':
            surprise_direction = match_dict.get('revenue_surprise_direction')
            surprise_amount = match_dict.get('revenue_surprise_amount')
            surprise_uom = match_dict.get('revenue_surprise_uom')

        if not surprise_direction:
            return None
        if surprise_direction.lower() == 'misses':
            return Utils.apply_uom(0.0 - float(surprise_amount), surprise_uom)
        elif surprise_direction.lower() == 'beats':
            return Utils.apply_uom(float(surprise_amount), surprise_uom)
        else:
            return None

    def determine_revenue(self, match_dict: dict) -> float | None:
        if not match_dict.get('revenue'):
            return None
        return Utils.apply_uom(match_dict.get('revenue'), match_dict.get('revenue_uom'))
