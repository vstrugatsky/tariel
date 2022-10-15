from __future__ import annotations
from loaders.twitter_account import TwitterAccount
import re
from utils.utils import Utils


class Livesquawk(TwitterAccount):
    account_name = 'livesquawk'

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
           est[ ](?P<eps_estimate_currency>C?[$])?
           (?P<eps_estimate_amount>\d+\.\d+)?
           .+?
           Revenue[ ](?P<revenue_currency>C?[$])
           (?P<revenue>\d+\.?\d*)
           (?P<revenue_uom>[MBK])?
           .+?
           est[ ](?P<revenue_estimate_currency>C?[$])?
           (?P<revenue_estimate_amount>\d+\.\d+)?
           (?P<revenue_estimate_uom>[MBK])?
           ''', re.VERBOSE | re.IGNORECASE | re.DOTALL)
        return p.search(tweet_text)

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
