from __future__ import annotations
import re

from loaders.twitter_account import TwitterAccount
from model.currency import Currency
from utils.utils import Utils


class Marketcurrents(TwitterAccount):
    account_name = 'marketcurrents'

    def parse_eps(self, tweet_text: str):
        p = re.compile(r'''
           (EPS|EPADS|NII|EPADR|FFO)\ of\ (?P<eps_sign>-)?(?P<eps_currency>''' + Currency.format_for_regex() + r''')      
           \ ?(?P<eps>\d+\.\d+)
           \ ?(?P<eps_surprise_direction>misses|beats)?
           (\ by\ )?(?P<eps_surprise_currency>''' + Currency.format_for_regex() + r''')?
           \ ?(?P<eps_surprise_amount>\d+\.\d+)?
           ''', re.VERBOSE | re.IGNORECASE | re.DOTALL)
        return p.search(tweet_text)

    def parse_revenue(self, tweet_text: str):
        p = re.compile(r'''
           (revenue|TII|net\ interest\ income|investment\ income)\ of\ (?P<revenue_currency>''' + Currency.format_for_regex() + r''')
           \ ?(?P<revenue>\d+\.?\d*)
           (?P<revenue_uom>[MBK])
           \ ?(?P<revenue_surprise_direction>misses|beats)?
           (\ by\ )?(?P<revenue_surprise_currency>''' + Currency.format_for_regex() + r''')?
           \ ?(?P<revenue_surprise_amount>\d+\.?\d*)?
           (?P<revenue_surprise_uom>[MBK])?
        ''', re.VERBOSE | re.IGNORECASE | re.DOTALL)
        return p.search(tweet_text)

    def parse_earnings_indicator(self, tweet_text: str):
        p = re.compile(r'''
           (?P<earnings_indicator>
           \W(Q[1-4]|quarterly)\ (earnings|result|beat|miss|loss|revenue|profit|sales|sees)|
           \W(EPS|revenue)\ of|
           \W(expenses|costs|outflows)\ (plummet|improve|jump|rise|rose|increase|climb)|
           \W(posts|after|reports)\ .*Q[1-4]|
           \Wbeat|\Wmiss|\Wresults|(\Wsurpasses|\Wtop).+estimates)
           ''', re.VERBOSE | re.IGNORECASE | re.DOTALL)
        return p.search(tweet_text)

    def parse_earnings_false_positive(self, tweet_text: str):
        p = re.compile(r'''
           (?P<earnings_false_positive>
           \Wearnings\ preview|\?|\Whot\ stocks|\Wweek\ ahead|\Wday\ movers|\Wlikely\ to\ [beat|miss]|
           \W(ahead\ of)\ .*Q[1-4])
           ''', re.VERBOSE | re.IGNORECASE | re.DOTALL)
        return p.search(tweet_text)

    def parse_positive_earnings(self, tweet_text: str) -> [str or None]:
        sentiments: [str or None] = []
        p = re.compile(r'''
           (?P<positive_sentiment>
           \W(earnings|result(s)?|estimates|sales|income|volume|profit|AUM)\ (surpass|exceed|gain|beat|top|increase|boost|grow|rise|climb)|
           \W(revenue(s?)|profit(s?)|booking(s?)|cash\ flow)\ (soar|surpass|jump|surge|gain|climb)|
           \W(tops|topping|topped)\ .*(forecast|estimate)|
           \W(expenses|costs)\ (plummet|improve)|
           \W(high(er)?|strong|record|boosts)\ (Q[1-4]\ )?(sales|earnings|(annual\ )?revenue|margin|demand|profit|income|volume|pricing|consumption)|
           \Wlow(er)?\ (expenses|costs|outflows|loss)|
           \W(Q[1-4]\ )?((EPS|FFO|revenue)\ )?beat(?!e)|\Wcrush|\Wstrength|\Wstrong|\Wimproved|\Wtailwind)
           ''', re.VERBOSE | re.IGNORECASE | re.DOTALL)
        for i in p.finditer(tweet_text):
            sentiments.append(i.groupdict()["positive_sentiment"].strip())
        return sentiments

    def parse_negative_earnings(self, tweet_text: str) -> [str or None]:
        sentiments: [str] = []
        p = re.compile(r'''
           (?P<negative_sentiment>
           \W(earnings|revenue(s?)|profit(s?)|result(s)?|income|sales|volume|AUM|asset\ values)\ (slip|slump|fall|miss|decline|plummet|drop)|
           \Whigh(er)?\ (expenses|cost|outflows)|
           \W(expenses|costs|outflows)\ (jump|rise|rose|increase|climb)|
           \W(low(er)?|weak|missing)\ (Q[1-4]\ )?(sales|earnings|revenue|margin|demand|profit|income|volume|pricing|consumption|PE\ return|bottom\ line)|
           \W(Q[1-4]|credit)\ (loss|miss)|
           \Wweak|\Wheadwind|\Wdecline|\Wdelay|\Wcost\ overrun)
           ''', re.VERBOSE | re.IGNORECASE | re.DOTALL)
        for i in p.finditer(tweet_text):
            sentiments.append(i.groupdict()["negative_sentiment"].strip())
        return sentiments

    def parse_positive_guidance(self, tweet_text: str) -> [str or None]:
        sentiments: [str] = []
        p = re.compile(r'''
           (?P<positive_guidance>
           \W(forecast|guidance|outlook)\ (raise|boost)|
           \W(guides|guiding)\ .*(EPS|revenue|sales|income|outlook)\ .*(higher|above)|
           \W(raise[sd]|sweeten(s)?|increase(s)?|upward\ revision|hike(s)?|bullish|boost(s)?)\ .*(guidance|outlook|forecast|guide)|
           \Whigher\ (Q[1-4]|yearly|annual|quarterly|year)\ (guidance|outlook|forecast))
           ''', re.VERBOSE | re.IGNORECASE | re.DOTALL)
        for i in p.finditer(tweet_text):
            sentiments.append(i.groupdict()["positive_guidance"].strip())
        return sentiments

    def parse_negative_guidance(self, tweet_text: str) -> [str or None]:
        sentiments: [str] = []
        p = re.compile(r'''
           (?P<negative_guidance>
           \W(guidance|outlook|forecast)\ (widely\ )?(cut|slashed|misses|lower(ed)?|below)|
           \W(guides|guiding)\ .*((EPS|revenue)\. .*)?(below|lower)|
           \W(cut(s|ting)?|dim|lower(s|ed|ing)?|downward\ revision|slash(es|ed|ing)?)[- ].*(guidance|outlook|forecast|guide))
           ''', re.VERBOSE | re.IGNORECASE | re.DOTALL)
        for i in p.finditer(tweet_text):
            sentiments.append(i.groupdict()["negative_guidance"].strip())
        return sentiments

    def should_raise_parse_warning(self, tweet_text: str) -> bool:
        return False

    def parse_symbol_from_url_desc(self, url_desc) -> str | None:
        p = re.compile(r'''(\((?P<symbol>[A-Za-z\.\:]+)\))
            ''', re.VERBOSE | re.IGNORECASE | re.DOTALL)
        match = p.search(url_desc)
        return match.groupdict()['symbol'] if match else None

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
