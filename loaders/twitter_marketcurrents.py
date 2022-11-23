from __future__ import annotations
# import re
import regex as re

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

    def parse_simple_earnings_indicator(self, tweet_text: str):
        p = re.compile(r'''
           (?P<earnings_indicator>
           \W(F?Q[1-4]|quarter(ly)?|earnings|results|posts|loss(es)?|profit(s)?|miss(es)?|beat(s)?|tops|
           after\ (reporting|posting|topping)|(EPS|revenue)\ of)(\W|$))
           ''', re.VERBOSE | re.IGNORECASE | re.DOTALL)
        return p.search(tweet_text)

    def parse_false_positive(self, tweet_text: str):
        p = re.compile(r'''
           (?P<earnings_false_positive>
           \Wearnings\ preview|\?|\Whot\ stocks|\Wstocks\ to\ watch|\Wweek\ ahead|\Wday\ movers|\Wlikely\ to\ [beat|miss]|
           \WQ[1-4]\ preview|\Wgoes\ ex-dividend|\WETF|
           \W(UK|China(['’]s)?|US|EU)\ (January|February|March|April|May|June|July|August|September|October|November|December|retail|(new\ )?home\ prices)|
           \W(ahead\ of)\ .*(Q[1-4]|quarterly))
           ''', re.VERBOSE | re.IGNORECASE | re.DOTALL)
        return p.search(tweet_text)

    def parse_positive_earnings(self, tweet_text: str) -> [str or None]:
        sentiments: [str or None] = []
        p = re.compile(r'''(?P<positive_sentiment>
           (?<!slower\ Q[1-4])
           \W(earnings|EPS|NII|FFO|EBITDA|result(s)?|estimates|sales|income|volume|profit(s)?|AUM|NAV|revenue(s)?|cash\ flow|booking(s)?|(top|bottom)\ ?line)
           \ (?!(guidance|outlook|guide|forecast|expect))((\w+\W+){0,2}?)?
           (beat|boost|climb|crush|exceed|gain|grow|increase|improve|jump|rise|soar|surge|surpass|top)|
           
           (?<!(projects|estimates|predicts|forecasts|expects)\W+)
           \W(higher(?!\ (on|as|after|ahead|amid|costs|despite|expenses|outflows|loss)\W)
           |strong(er)?|better|soaring|upbeat|record|boost(ed|s)|drives|drove|premium|growth)
           \W(than\Wexpected\W)?((Q[1-4]|quarterly)\ )?(?!(guidance|outlook|guide|forecast|projection)\W)
           ((\w+\W+){0,3}?)?
           (sales|earnings|EPS|NII|FFO|performance|results|revenue|EBITDA|margin|demand|growth|profit|income|volume|pricing|consumption)
           (?!\W(guidance|outlook|guide|forecast|projection))|
           
           (?<!(guidance|outlook|guide|forecast)(\ widely)?)
           \W(top(s|ped|ping)|exceed(s|ed|ing)|crush(es|ed|ing)?|beat(s|ing)|boost(s|ing))
           \ .*(forecast|estimate|consensus|expectation|top[-\ ]line|bottom[-\ ]line)|
           
           \W(expenses|costs|outflows|loss)\ (plummet|improve|narrow)|      
           \W(low(er)?|less|small(er)?|narrow(er)?|improv(ed|ing))\W(than\Wexpected\W)?(Q[1-4]\W)?((\w+\W+){0,1}?)?(expenses|costs|outflows|loss)| 
           
           (?<!estimates|forecasts|projects|expects|sees)\W(Q[1-4]|quarterly)\ ((\w+\W+){0,1}?)?(beat)|
           (?<!estimates|forecasts|projects|expects|sees)\W(beating|upbeat|growth\ in)\ (Q[1-4]|quarter)|
           
           \W(first|surprise)\ profit)''', re.VERBOSE | re.IGNORECASE | re.DOTALL)
        for i in p.finditer(tweet_text):
            sentiments.append(i.groupdict()["positive_sentiment"].strip())
        return sentiments

    def parse_negative_earnings(self, tweet_text: str) -> [str or None]:
        sentiments: [str] = []
        p = re.compile(r'''(?P<negative_sentiment>
           \W(earnings|EPS|NII|TII|FFO|EBITDA|revenue(s?)|profit(s?)|result(s)?|price(s)?|(top|bottom)\ ?line|income|sales|volume|margins|shipments|AUM|NAV|asset\ value(s)?)
           \ (?!(guidance|outlook|guide|forecast|expect))((\w+\W+){0,2}?)?
           (slip|slump|slide|decrease|tumble|fall|fell|miss|decline|plummet|drop|trail|loss|disappoint)|
           
           (?<!(projects|estimates|predicts|forecasts)\W+)
           \W(lower(?!\ (on|as|after|ahead|amid|costs|despite|expenses|outflows|loss)\W)
           |weak(er)?|mar(s|red)|miss(es|ed|ing)?(\ on)?|weigh(s)?(\ on)?|disappointing|plunging|downbeat|dismal)
           \W(than\Wexpected\W)?((Q[1-4]|quarterly)\ )?(?!(guidance|outlook|guide|forecast|projection)\W)
           ((\w+\W+){0,3}?)?
           (sales|result|earnings|expectation|EPS|NII|TII|FFO|revenue|margin|shipment|demand|profit|income|volume|pricing|consumption|book\ value|PE\ return|(top|bottom)\ ?line)|
           
           (?<!(guidance|outlook|guide|forecast)(\ widely)?)
           \W(fall(s|ing)?|fell|miss(es|ed|ing)?)\ .*(forecast|estimate|consensus|expectation|top[-\ ]line|bottom[-\ ]line)|
            
           (?<!estimates|expects|sees|forecasts|projects)
           \W(high(er)?|wide(ning|r)|rising|rise\ in)\W(than\Wexpected\W)?(Q[1-4]\W)?((\w+\W+){0,1}?)?(expense|costs|outflows|loss)|
           
           (?<!(smaller|narrow(er)?)([-\ ]than[-\ ]expected)?)(?<!estimates|expects|sees|forecasts|projects)
           \W(Q[1-4]|quarterly)\ ((\w+\W+){0,1}?)?(loss|miss|headwind)(?!\Wnarrows)|
           
           \W(expenses|costs|outflows|loss(es)?)\ (jump|rise|rose|increase|climb|widen|continue)|
           
           \Wcost\ overrun|\Wexcess\ inventory|\Wunprofitable\ quarter)''', re.VERBOSE | re.IGNORECASE | re.DOTALL)
        for i in p.finditer(tweet_text):
            if i.groupdict()["negative_sentiment"].strip() not in sentiments:  # to eliminate 'weak' if say 'weaker demand' was already parsed
                sentiments.append(i.groupdict()["negative_sentiment"].strip())
        return sentiments

    def parse_positive_guidance(self, tweet_text: str) -> [str or None]:
        sentiments: [str] = []
        p = re.compile(r'''
           (?P<positive_guidance>
           \W(forecast|guidance|outlook|guide)\ (raise(?!s)|boost|above|ahead|higher|hike|increase|lift|sweeten|top[s|ped])|
           
           \W(guide[sd]|guiding|sees|forecasts|projects)\ .*
           ((EPS|revenue|sales|income|outlook|growth|profit|result|margin|(top|bottom)[-\ ]line)\ .*)?(higher|above|ahead)|
           
           \W(rais(es|ed|ing)|sweeten(s|ed|ing)|lift(s|ed|ing)?|increas(es|ed|ing)|hik(es|ed|ing)|boost(s|ed|ing)?)[-\ ]
           (?!by\W)((\w+\W+){0,5}?)?(guidance|outlook|forecast|guide|estimate)(?!\ to\ positive)|
           
           (?<!\W(cut(s|ting)?|trim(s|med|ming)|tighten(s|ed|ing)|withdraw(s|ed|ing)|pull(s|ed|ing)|lower(s|ed|ing)|dent(s)?|slash(es|ed|ing)))
           \W(upbeat|upward\ revision|upper[\ -]range|bullish|confident|bright|strong|above[\ -]consensus|ahead|higher|high[\ -]end)[- ]
           ((\w+\W+){0,3}?)?(guidance|outlook|forecast|guide)|
           
           \W(expects|sees|estimates|projects|forecasts)\W+(faster|higher|strong(er)?|improv(ing|ed))
           \ ((\w+\W+){0,2}?)(EPS|revenue|sales|income|outlook|growth|profit|result|improvement|margin(top|bottom)[-\ ]line)|
           
           \W(expects|sees|estimates|projects|forecasts)\ ((\w+\W+){0,2}?)?(Q[1-4]|quarterly|yearly)\ ((\w+\W+){0,1}?)?(profit|beat)|
           
           \W(growth|profit|sales|result(s)?|revenue(s)?|EPS|income|(top|bottom)[-\ ]line|margin(s)?)
           \ (seen|expected)\ to\ (rise|grow|improve|increase))
           ''', re.VERBOSE | re.IGNORECASE | re.DOTALL)
        for i in p.finditer(tweet_text):
            sentiments.append(i.groupdict()["positive_guidance"].strip())
        return sentiments

    def parse_negative_guidance(self, tweet_text: str) -> [str or None]:
        sentiments: [str] = []
        p = re.compile(r'''
           (?P<negative_guidance>
           \W(guidance|outlook|forecast|guide)\ ((widely|stands)\ )?(cut|slashed|trimmed|trails|misses|falls|disappoint|lower(ed)?|below)|
           
           \W(guide[sd]|guiding|sees|forecasts|projects)\ .*
           ((EPS|earnings|revenue|sales|income|outlook|growth|profit|margin|(top|bottom)[-\ ]line)\. .*)?(below|lower)|
           
           \W(cut(s|ting)?|trim(s|med|ming)?|tighten(s|ed|ing)|withdraw(s|ed|ing)|pull(s|ed|ing)|lower(s|ed|ing)|dent(s)?|slash(es|ed|ing)?)[- ]
           ((\w+\W+){0,5})?(guidance|outlook|forecast|guide|estimate|view)|
           
           (?<!\W(rais(es|ed|ing)|sweeten(s|ed|ing)|lift(s|ed|ing)|increas(es|ed|ing)|hik(es|ed|ing)|boost(s|ed|ing)?))
           \W(dim|weak|soft|underdone|lackluster|cautious|below\ consensus|pared|gloomy|bearish|lower|low[\ -]end|downbeat|disappoint(ing)?|dismal|downward\ revision)[- ]
           ((\w+\W+){0,3})?(guidance|outlook|forecast|guide|picture|view)|
           
           \W(expects|sees|estimates|projects|forecasts)\ (slow(er)?|low(er)?|weak(er)?|soft(ness|er)?)
           \ ((\w+\W+){0,2})(EPS|revenue|sales|income|outlook|growth|profit|margin|bookings)|
           
           \W(expects|sees|estimates|projects|forecasts)\ ((\w+\W+){0,2}?)?(Q[1-4]|quarterly|yearly)\ ((\w+\W+){0,1}?)?(loss|miss)|
           
           \W(EPS|revenue|sales|income|outlook|growth|(top|bottom)[-\ ]line|profit|margin(s)?)\ seen to\ (fall|worsen|decrease|weaken|soften|slow))
           ''', re.VERBOSE | re.IGNORECASE | re.DOTALL)
        for i in p.finditer(tweet_text):
            sentiments.append(i.groupdict()["negative_guidance"].strip())
        return sentiments

    def parse_analyst(self, tweet_text: str):
        p = re.compile(r'''
           \W(?P<analyst>
           (Morgan\ Stanley|Bank\ of\ America|BofA|Citigroup|Moody(\Ws)?|Wedbush|Northland|Loop\ Capital|Piper\ Sandler))
           (\W|$)
           ''', re.VERBOSE | re.IGNORECASE | re.DOTALL)
        if p.search(tweet_text):
            return p.search(tweet_text).groupdict()["analyst"]

    def parse_analyst_positive(self, tweet_text: str) -> [str or None]:
        sentiments: [str] = []
        p = re.compile(r'''(?P<positive_analyst>
           \W(upgrade(s|d)?|raise(s|d)?)(\Woutlook)?(\Wto)?((\W\w+){0,1})?(\W|$))
           ''', re.VERBOSE | re.IGNORECASE | re.DOTALL)
        for i in p.finditer(tweet_text):
            sentiments.append(i.groupdict()["positive_analyst"].strip())
        return sentiments

    def parse_analyst_negative(self, tweet_text: str) -> [str or None]:
        sentiments: [str] = []
        p = re.compile(r'''(?P<negative_analyst>
           \W(downgrade(s|d)?|cut(s)?|slashe(s|d))(\Woutlook)?(\Wto)?((\W\w+){0,1})?(\W|$))
           ''', re.VERBOSE | re.IGNORECASE | re.DOTALL)
        for i in p.finditer(tweet_text):
            sentiments.append(i.groupdict()["negative_analyst"].strip())
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
