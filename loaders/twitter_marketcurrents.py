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
           \ ?(?P<eps_surprise_direction>misses|beats|in-line)?
           (\ by\ )?(?P<eps_surprise_currency>''' + Currency.format_for_regex() + r''')?
           \ ?(?P<eps_surprise_amount>\d+\.\d+)?
           ''', re.VERBOSE | re.IGNORECASE | re.DOTALL)
        return p.search(tweet_text)

    def parse_revenue(self, tweet_text: str):
        p = re.compile(r'''
           (revenue|TII|net\ interest\ income|investment\ income)\ of\ (?P<revenue_currency>''' + Currency.format_for_regex() + r''')
           \ ?(?P<revenue>\d+\.?\d*)
           (?P<revenue_uom>[KMBT])
           \ ?(?P<revenue_surprise_direction>misses|beats|in-line)?
           (\ by\ )?(?P<revenue_surprise_currency>''' + Currency.format_for_regex() + r''')?
           \ ?(?P<revenue_surprise_amount>\d+\.?\d*)?
           (?P<revenue_surprise_uom>[KMBT])?
        ''', re.VERBOSE | re.IGNORECASE | re.DOTALL)
        return p.search(tweet_text)

    def parse_earnings_indicator(self, tweet_text: str):
        p = re.compile(r'''
           (?P<earnings_indicator>
           \W(Q[1-4]|quarterly|((first|second|third|fourth)\ quarter))\ 
           ((operating|adjusted|net)\ )?(report|earnings|EPS|NII|FFO|EBITDA|result|beat|miss|loss|revenue|profit|sales|sees)|
           \W(earnings|result|beat|miss|loss|decline|increase|revenue|profit|sales)\ (in\ )?(Q[1-4]|((first|second|third|fourth)\ quarter))|
           \W(EPS|revenue)\ of|
           \W(loss|profit)\ (widens|narrows)|\W(strong|wide|narrow)\ (profit|loss)|
           \W(expenses|costs|outflows)\ (plummet|improve|jump|rise|rose|increase|climb)|
           \W(posts|after|reports)\ .*((un)?profit(s|able)?|earnings|margins|Q[1-4]|((first|second|third|fourth)\ quarter))|
           \Wbeat|\Wmiss|\Wresults|\Wdrag\ earnings|(\Wsurpasses|\Wtop).+estimates)
           ''', re.VERBOSE | re.IGNORECASE | re.DOTALL)
        return p.search(tweet_text)

    def parse_earnings_false_positive(self, tweet_text: str):
        p = re.compile(r'''
           (?P<earnings_false_positive>
           \Wearnings\ preview|\?|\Whot\ stocks|\Wstocks\ to\ watch|\Wweek\ ahead|\Wday\ movers|\Wlikely\ to\ [beat|miss]|
           \WQ[1-4]\ preview|
           \W(ahead\ of)\ .*(Q[1-4]|quarterly))
           ''', re.VERBOSE | re.IGNORECASE | re.DOTALL)
        return p.search(tweet_text)

    def parse_positive_earnings(self, tweet_text: str) -> [str or None]:
        sentiments: [str or None] = []
        p = re.compile(r'''
           (?P<positive_sentiment>
           \W(earnings|EPS|NII|FFO|EBITDA|result(s)?|estimates|sales|income|volume|profit|AUM|NAV|(top|bottom)\ ?line)
           \ (sees\ )?((\w+\W+){0,1})?(surpass|exceed|gain|beat|top|increase|boost|grow|rise|climb)|
           \W(revenue(s?)|profit(s?)|booking(s?)|cash\ flow)\ (soar|surpass|jump|surge|gain|grow|climb)|
           \W(top(s|ped|ping)|exceed(s|ed|ing))\ .*(forecast|estimate|consensus)|
           \W(expenses|costs)\ (plummet|improve)|
           \W(high(er)?|strong|record|boosts|premium)\ (Q[1-4]\ )?((annual|adjusted|operating|organic)\ )?(sales|earnings|EPS|NII|FFO|results|revenue|EBITDA|margin|demand|growth|profit|income|volume|pricing|consumption)|
           \W(low(er)?|less)\ (expenses|costs|outflows|loss)| 
           \W(loss)\ narrows|
           \W(Q[1-4]\ )?((EPS|FFO|revenue)\ )?beat(?!e)|\Wcrush|\Wstrength|\Wstrong|\Wimproved|\Wtailwind)
           ''', re.VERBOSE | re.IGNORECASE | re.DOTALL)
        for i in p.finditer(tweet_text):
            sentiments.append(i.groupdict()["positive_sentiment"].strip())
        return sentiments

    def parse_negative_earnings(self, tweet_text: str) -> [str or None]:
        sentiments: [str] = []
        p = re.compile(r'''
           (?P<negative_sentiment>
           \W(earnings|EPS|NII|TII|FFO|EBITDA|revenue(s?)|profit(s?)|result(s)?|(top|bottom)\ ?line|income|sales|volume|margins|AUM|NAV|asset\ value(s)?)
           \ (slip(ped)?|slump(ed)?|slide|fall|fell|(just\ )?miss(ed)?|decline(d)?|plummet(ed)?|drop(ped)?|trail(ed)?|loss|disappoint(ed)?)|
           \W(high(er)?|rising|rise\ in)\ (\w+\W)?(expense|costs|outflows)|
           \W(expenses|costs|outflows)\ (jump|rise|rose|increase|climb)|
           \W(low(er)?|weak(er)?|missing|misse[sd]|disappointing|dismal)\ (Q[1-4]\ )?
           (sales|result|earnings|EPS|NII|TII|FFO|revenue|margin|demand|profit|income|volume|pricing|consumption|book\ value|PE\ return|bottom\ line)|
           \W(Q[1-4]|credit)\ (net\ )?(loss|miss)(?!\Wnarrows)|
           \Wweak|\Wfall(s)?\ short|\Wloss\ widens|\Wheadwind|\Wdecline|\Wdelay|\Wcost\ overrun)
           ''', re.VERBOSE | re.IGNORECASE | re.DOTALL)
        for i in p.finditer(tweet_text):
            if i.groupdict()["negative_sentiment"].strip() not in sentiments:  # to eliminate 'weak' if say 'weaker demand' was already parsed
                sentiments.append(i.groupdict()["negative_sentiment"].strip())
        return sentiments

    def parse_positive_guidance(self, tweet_text: str) -> [str or None]:
        sentiments: [str] = []
        p = re.compile(r'''
           (?P<positive_guidance>
           \W(forecast|guidance|outlook)\ (raise|boost|above|higher|hike|increase)|
           \W(guide[sd]|guiding)\ .*((EPS|revenue|sales|income|outlook)\ .*)?(higher|above)|
           \W(raise[sd]|sweeten(s)?|increase(s)?|hike(s)?|boost(s)?)[- ]((\w+\W+){0,5})?(guidance|outlook|forecast|guide)|
           \W(upbeat|upward\ revision|upper\ range|bullish|bright|strong|raising)[- ]((\w+\W+){0,3})?(guidance|outlook|forecast|guide)|
           \Whigher\ (Q[1-4]|yearly|annual|quarterly|year)\ (guidance|outlook|forecast|guide)|
           \Whigh[ -]end\ of\ guidance)
           ''', re.VERBOSE | re.IGNORECASE | re.DOTALL)
        for i in p.finditer(tweet_text):
            sentiments.append(i.groupdict()["positive_guidance"].strip())
        return sentiments

    def parse_negative_guidance(self, tweet_text: str) -> [str or None]:
        sentiments: [str] = []
        p = re.compile(r'''
           (?P<negative_guidance>
           \W(guidance|outlook|forecast)\ (widely\ )?(cut|slashed|trails|misses|lower(ed)?|below)|
           \W(guide[sd]|guiding)\ .*((EPS|revenue|sales|income|outlook)\. .*)?(below|lower)|
           \W(cut(s|ting)?|pull(s|ed)|lower(s|ed|ing)|slash(es|ed|ing))[- ]((\w+\W+){0,5})?(guidance|outlook|forecast|guide)|
           \W(dim|weak|below|pared|lower|downward\ revision)[- ]((\w+\W+){0,3})?(guidance|outlook|forecast|guide)|
           \Wlow[ -]end\ of\ guidance)
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

        if surprise_direction and surprise_amount:
            if surprise_direction.lower() == 'misses':
                return Utils.apply_uom(0.0 - float(surprise_amount), surprise_uom)
            elif surprise_direction.lower() == 'beats':
                return Utils.apply_uom(float(surprise_amount), surprise_uom)
        if surprise_direction == 'in-line':
            return 0
        return None

    def determine_revenue(self, match_dict: dict) -> float | None:
        if not match_dict.get('revenue'):
            return None
        return Utils.apply_uom(match_dict.get('revenue'), match_dict.get('revenue_uom'))
