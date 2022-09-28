import requests
import model
from model.earnings_reports import EarningsReport
from model.symbols import Symbol
from datetime import datetime, timedelta
from jsonpath_ng import parse
import re
import unittest


def find_first_match(jsonpath, json):
    jsonpath_expr = parse(jsonpath)
    matches = jsonpath_expr.find(json)
    if len(matches) > 0:
        return matches[0].value
    else:
        return None

api_key = '5jVxQ7fmxfkoZ7ZCJLALNhQX7'
api_key_secret = 'dg0rQIF04VG2LL1IZm161MEOy9T8oLbkKWXDw4Agw1ILZlQokd'
bearer_token = 'AAAAAAAAAAAAAAAAAAAAABPogAEAAAAAByMCjcuMzPZwxBBPsVvcwQu8XhQ%3DwgMrQIkMpzwRQZz2cQUEfspZ17wxWSpldiyd5GSOxgvckfGjsg'

url_prefix = 'https://api.twitter.com/2'
account = 'marketcurrents'


def call_paginated_api(payload, paginate, backfill, next_token):
    if backfill:
        max_date = datetime.utcnow() - timedelta(days=7)
    else:
        max_date = EarningsReport.get_max_date() or datetime.utcnow() - timedelta(days=7)

    payload.update({'start_time': max_date.strftime("%Y-%m-%dT%H:%M:%SZ")})

    if next_token and paginate:  # first or last execution
        payload.update({'pagination_token': next_token})

    r = requests.get(url_prefix + '/tweets/search/recent',
                     params=payload,
                     headers={'Authorization': 'Bearer ' + bearer_token})

    print(f'INFO {datetime.utcnow()} {r.headers["content-type"]} {r.encoding} {r.url} \n Status={r.status_code}')
    if r.status_code != 200:
        exit(1)
    print(f'Meta={r.json()["meta"]}')
    next_token = r.json()["meta"].get("next_token", None)

    session = model.Session()
    count = 0
    while count < r.json()["meta"]["result_count"]:
        i = r.json()["data"][count]
        count += 1

        # print(f'{i["id"]} {i["created_at"]} {i["text"]} \n {i["entities"]}')
        print(f'Look for symbol in {i["entities"]["urls"][0]["description"]}')

        if '$EARNINGS' in i['text']:
            tweet_url_description = find_first_match("entities.urls[0].description", i)
            # e.g.
            # Ambarella press release (AMBA):
            # Q2 Non-GAAP EPS of $0.20 beats by $0.01.Revenue of $80.88M (+2.0% Y/Y) beats by $0.67M.
            # Gross margin on a non-GAAP basis for the second quarter of

            match = re.search(r'\([A-Z.]+\)', tweet_url_description)
            if match:
                symbol = match.group(0).strip("()")
                if Symbol.lookup_symbol(symbol, session):
                    print(f'Found match for {symbol}')
                else:
                    print(f'WARN could not find {symbol} in Symbols')
                    # NEXT: deal with exchanges, e.g.: CTRL:CA, AIP.U:CA, PUL:CA - use regex groups
                    continue
            else:
                print(f'WARN - Could not find symbol in tweet_url_description')

            earnings_report = EarningsReport(
                tweet_id=i['id'],
                tweet_date=i['created_at'],
                twitter_account=account,
                tweet_text=i['text'],
                tweet_short_url=find_first_match("entities.urls[0].url", i),
                tweet_expanded_url=find_first_match("entities.urls[0].expanded_url", i),
                tweet_url_status=find_first_match("entities.urls[0].status", i),
                tweet_url_title=find_first_match("entities.urls[0].title", i),
                tweet_url_description=find_first_match("entities.urls[0].description", i))
                # parsed_symbol = Column(String(10), ForeignKey("symbols.symbol"), nullable=True)
                # symbol_object = relationship("Symbol")
                # currency = Column(String(3))
                # eps = Column(Numeric)
                # eps_surprise = Column(Numeric)
                # revenue = Column(BigInteger)
                # revenue_surprise = Column(BigInteger)
                # guidance_direction = Column(String(20))
            session.merge(earnings_report)

    session.commit()
    session.close()
    if paginate and next_token:
        call_paginated_api(payload, paginate, backfill, next_token)


if __name__ == '__main__':
    payload = {'query': 'from:' + account + ' earnings',
               'max_results': 100,
               'tweet.fields': 'created_at,author_id,entities'}

    call_paginated_api(payload, False, True, None)


class TestSymbolInParensRegex(unittest.TestCase):
    def runTest(self):
        desc = '''
        Russia's Gazprom (OGZPY) said on Tuesday it earned a record net profit of 2.5T rubles ($41.75B) in H1 2022, 
        "despite sanctions pressure and an unfavorable"
        '''
        m = re.search(r'\([A-Z]+\)', desc)
        assert(m.group(0) == '(OGZPY)')
        with model.Session() as session:
            assert(Symbol.lookup_symbol(m.group(0).strip("()"), session))

