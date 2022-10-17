from __future__ import annotations
from loaders.twitter_account import TwitterAccount
import re

from utils.utils import Utils


class Marketcurrents(TwitterAccount):
    account_name = 'marketcurrents'

    def parse_tweet_v2(self, tweet_text: str):
        pass

    def parse_tweet(self, tweet_text: str) -> re.Match:
        p = re.compile(r'''
           (EPS|NII)[ ]of[ ](?P<eps_sign>[-])?(?P<eps_currency>C?[$])      
           (?P<eps>\d+\.\d+)
           [ ]?(?P<eps_surprise_direction>misses|beats)?
           ([ ]by[ ])?(?P<eps_surprise_currency>C?[$])?
           (?P<eps_surprise_amount>\d+\.\d+)?
           .+
           (revenue|investment[ ]income)[ ]of[ ](?P<revenue_currency>C?[$])
           (?P<revenue>\d+\.?\d*)
           (?P<revenue_uom>[MBK])
           [ ]?(?P<revenue_surprise_direction>misses|beats)?
           ([ ]by[ ])?(?P<revenue_surprise_currency>C?[$])?
           (?P<revenue_surprise_amount>\d+\.?\d*)?
           (?P<revenue_surprise_uom>[MBK])?
           ([,;]?[ ]?(?P<guidance_1>reaffirms|updates|raises|ups|lowers|revises).+guidance)?
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
        return Utils.apply_uom(float(match_dict.get('revenue')), match_dict.get('revenue_uom'))
