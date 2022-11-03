from __future__ import annotations
import re
from typing import Optional

from loaders.twitter_account import TwitterAccount
from model.currency import Currency
from utils.utils import Utils


class Livesquawk(TwitterAccount):
    account_name = 'livesquawk'

    def parse_earnings_indicator(self, tweet_text: str):
        pass

    def parse_earnings_false_positive(self, tweet_text: str):
        pass

    def parse_positive_earnings(self, tweet_text: str):
        pass

    def parse_negative_earnings(self, tweet_text: str):
        pass

    def parse_positive_guidance(self, tweet_text: str):
        pass

    def parse_negative_guidance(self, tweet_text: str):
        pass

    def parse_eps(self, tweet_text: str) -> Optional[re.Match]:
        p = re.compile(r'''
           (EPS|EPADS|NII|EPADR|FFO)(:?)\ (?P<eps_sign>-)?(?P<eps_currency>''' + Currency.format_for_regex() + r''')
           \ ?(?P<eps>\d+\.\d+)
           .+?
           (est|exp|estimate)[:.]?\ (?P<eps_estimate_currency>''' + Currency.format_for_regex() + r''')?
           \ ?(?P<eps_estimate_amount>\d+\.\d+)?
           ''', re.VERBOSE | re.IGNORECASE | re.DOTALL)
        return p.search(tweet_text)

    def parse_revenue(self, tweet_text: str) -> Optional[re.Match]:
        p = re.compile(r'''
           (Revenue|Rev.):?\ (?P<revenue_currency>''' + Currency.format_for_regex() + r''')
           \ ?(?P<revenue>\d+\.?\d*)
           (?P<revenue_uom>[MBK])?
           .+?
           (est|exp|estimate)[:.]?\ (?P<revenue_estimate_currency>''' + Currency.format_for_regex() + r''')?
           \ ?(?P<revenue_estimate_amount>\d+\.\d+)?
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
            eps = match_dict.get('eps')
            eps_estimate = match_dict.get('eps_estimate_amount')
            if eps and eps_estimate:
                return round(float(eps) - float(eps_estimate), 2)
            else:
                return None
        elif metrics == 'revenue':
            revenue = match_dict.get('revenue')
            revenue_estimate = match_dict.get('revenue_estimate_amount')
            # default to billions if none - Livesquawk mainly covers large companies
            revenue_uom = match_dict.get('revenue_uom') or 'B'
            revenue_estimate_uom = match_dict.get('revenue_estimate_uom') or 'B'
            if revenue and revenue_estimate:
                return round(Utils.apply_uom(revenue, revenue_uom) -
                             Utils.apply_uom(revenue_estimate, revenue_estimate_uom), 2)
            else:
                return None

    def determine_revenue(self, match_dict: dict) -> float | None:
        # default to billions if none - Livesquawk mainly covers large companies
        if not match_dict.get('revenue'):
            return None
        revenue_uom = match_dict.get('revenue_uom') or 'B'
        return Utils.apply_uom(match_dict.get('revenue'), revenue_uom)
