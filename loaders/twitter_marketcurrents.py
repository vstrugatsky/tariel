from __future__ import annotations
import re

from loaders.twitter_account import TwitterAccount
from model.currency import Currency
from utils.utils import Utils


class Marketcurrents(TwitterAccount):
    account_name = 'marketcurrents'

    def parse_eps(self, tweet_text: str):
        p = re.compile(r'''
           (EPS|EPADS|NII|EPADR|FFO)[ ]of[ ](?P<eps_sign>[-])?(?P<eps_currency>''' + Currency.format_for_regex() + r''')      
           [ ]?(?P<eps>\d+\.\d+)
           [ ]?(?P<eps_surprise_direction>misses|beats)?
           ([ ]by[ ])?(?P<eps_surprise_currency>''' + Currency.format_for_regex() + r''')?
           [ ]?(?P<eps_surprise_amount>\d+\.\d+)?
           ''', re.VERBOSE | re.IGNORECASE | re.DOTALL)
        return p.search(tweet_text)

    def parse_revenue(self, tweet_text: str):
        p = re.compile(r'''
           (revenue|investment[ ]income)[ ]of[ ](?P<revenue_currency>''' + Currency.format_for_regex() + r''')
           [ ]?(?P<revenue>\d+\.?\d*)
           (?P<revenue_uom>[MBK])
           [ ]?(?P<revenue_surprise_direction>misses|beats)?
           ([ ]by[ ])?(?P<revenue_surprise_currency>''' + Currency.format_for_regex() + r''')?
           [ ]?(?P<revenue_surprise_amount>\d+\.?\d*)?
           (?P<revenue_surprise_uom>[MBK])?
        ''', re.VERBOSE | re.IGNORECASE | re.DOTALL)
        return p.search(tweet_text)

    def parse_positive_earnings(self, tweet_text: str) -> [str or None]:
        sentiments: [str or None] = []
        p = re.compile(r'''
           (?P<positive_sentiment>
           \W(earnings|results|estimates)\ (surpass|exceed|gain|beat|top)|
           \W(revenue(s?)|profit(s?))\ (soar|surpass|jump)|
           \W(tops|topping|topped)\ .*(forecast|estimate)|
           \W(expenses|costs)\ (plummet|improve)|
           \W(high(er)?|strong)\ (sales|earnings|revenues|margins|demand|profit|income|volume|pricing|consumption)|
           \Wlow(er)?\ (expenses|costs)|\Wfree\ cash\ flow\ jump|
           \W(Q[1-4]\ )?((EPS|revenue)\ )?beat(?!e)|\Wboost|\Wstrength|\Wstrong|\Wtailwind|\Wraise[sd])
           ''', re.VERBOSE | re.IGNORECASE | re.DOTALL)
        for i in p.finditer(tweet_text):
            sentiments.append(i.groupdict()["positive_sentiment"])
        return sentiments

    def parse_negative_earnings(self, tweet_text: str) -> [str or None]:
        sentiments: [str] = []
        p = re.compile(r'''
           (?P<negative_sentiment>
           \W(earnings|revenue(s?)|profit(s?))\ (slip|fall|miss|decline|plummet)|
           \Whigh(er)?\ (expenses|cost)|
           \W(low(er)?|weak)\ (sales|earnings|revenues|margins|demand|profit|income|volume|pricing|consumption)|
           \W((Q[1-4]|credit)\ )?(loss|miss)|
           \Wweak|\Wheadwind|\Wlowered|\Wdecline|\Wdrop|\Wdelay|\Wcost\ overrun)
           ''', re.VERBOSE | re.IGNORECASE | re.DOTALL)
        for i in p.finditer(tweet_text):
            sentiments.append(i.groupdict()["negative_sentiment"])
        return sentiments

    def parse_positive_guidance(self, tweet_text: str) -> [str or None]:
        sentiments: [str] = []
        p = re.compile(r'''
           (?P<positive_guidance>
           \W(guidance|outlook)\ raised|
           \Wguides\ .*(EPS|revenue)\. .*(higher|above)|
           \W(raise[sd])\ .*(guidance|outlook))
           ''', re.VERBOSE | re.IGNORECASE | re.DOTALL)
        for i in p.finditer(tweet_text):
            sentiments.append(i.groupdict()["positive_guidance"])
        return sentiments

    def parse_negative_guidance(self, tweet_text: str) -> [str or None]:
        sentiments: [str] = []
        p = re.compile(r'''
           (?P<negative_guidance>
           \W(guidance|outlook)\ (cut|slashed|lower(ed)?|below)|
           \Wguides\ .*((EPS|revenue)\. .*)?(below|lower)|
           \W(cut|cuts|lowers|lowered|slashe[sd])\ .*(guidance|outlook))
           ''', re.VERBOSE | re.IGNORECASE | re.DOTALL)
        for i in p.finditer(tweet_text):
            sentiments.append(i.groupdict()["negative_guidance"])
        return sentiments

    def parse_guidance(self, tweet_text: str):
        p = re.compile(r'''
           (?P<guidance_1>raises|lowers|reaffirms|cuts|below)[ ]
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

        if not surprise_direction or not surprise_amount:
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
