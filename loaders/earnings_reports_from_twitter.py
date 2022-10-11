from __future__ import annotations
import model
from datetime import date, datetime, timedelta
from model.symbols import Symbol
from model.earnings_reports import EarningsReport
from loaders.loader_base import LoaderBase
from jsonpath_ng import parse
import re
from providers.twitter import Twitter


class LoadEarningsReportsFromTwitter:

    @staticmethod
    def lookup_currency(symbol: str) -> str | None:
        if symbol == '$':
            return 'USD'
        else:
            return None

    @staticmethod
    def parse_tweet(tweet_text: str) -> re.Match:
        p = re.compile(r'''
           EPS[ ]of[ ](?P<eps_sign>[-])?(?P<eps_currency>[$])      
           (?P<eps>\d+\.\d+)
           [ ]?(?P<eps_surprise_direction>misses|beats)?
           ([ ]by[ ])?(?P<eps_surprise_currency>[$])?
           (?P<eps_surprise_amount>\d+\.\d+)?
           .+
           revenue[ ]of[ ](?P<revenue_currency>[$])
           (?P<revenue>\d+\.?\d*)
           (?P<revenue_uom>[MBK])
           [ ]?(?P<revenue_surprise_direction>misses|beats)?
           ([ ]by[ ])?(?P<revenue_surprise_currency>[$])?
           (?P<revenue_surprise_amount>\d+\.?\d*)?
           (?P<revenue_surprise_uom>[MBK])?
           ''', re.VERBOSE | re.IGNORECASE)
        return p.search(tweet_text)

    @staticmethod
    def load(i: dict, session: model.Session, method_params: dict):
        print(i['created_at'] + ' ' + i['text'])
        # $BABB GAAP EPS of $0.02, revenue of $0.88M
        # $AZZ - AZZ declares $0.17 dividend
        # $RL $PVH $HBI - Levi Strauss earnings miss sends apparel stocks lower
        # $CVS $HUM $CANO - Cano Health jumps 10 % on report CVS in exclusive talks to acquire
        # $YASKY - YASKAWA Electric reports 1H results
        # $PGR - Progressive upgraded to Buy at Jefferies on widening margins, NII gains
        # $TSM - Taiwan Semiconductor reports 36 % revenue growth in September
        # $HZNP - Horizon Therapeutics cuts FY adj.EBITDA guidance to reflect new milestone related expense
        # $SACH - Sachem Capital to repurchase up to $7.5 M of shares
        # $TLRY $TLRY:CA - Tilray posts Q1 miss for fiscal 2023 as topline contracts
        # $TLRY $TLRY:CA - Tilray Non - GAAP EPS of -$0.08 misses by $0.01, revenue of $153.21M misses by $3.64M
        # $ASIX - AdvanSix expects Q3 adjusted EBITDA of $31M -$34M
        # $MTYFF $MTY:CA - MTY Food Group GAAP EPS of $0.92, revenue of $171.54M
        # $MTRX - Matrix Service Non - GAAP EPS of -$0.52 misses by $0.22, revenue of $200.7 M beats by $18.86M
        # $IMOS - ChipMOS' Q3 revenue down 26.6% Y/Y
        # $SSNLF $SSNNF - Samsung Electronics sees bleak Q3 operating profit KRW10.8T vs. KRW12.1T consensus as demand for memory chips dip
        # $GRRR - Gorilla Technology Group GAAP EPS of -$0.29, revenue of $13.8M
        # $IDT - IDT Corporation Non - GAAP EPS of $0.70, revenue of $329M
        # $NRIX - Nurix Therapeutics GAAP EPS of -$0.90 beats by $0.07, revenue of $10.79 M misses by $1.29M
        # $LEVI - Levi Strauss Non - GAAP EPS of $0.40 beats by $0.03, revenue of $1.52B misses by $80M
        # $EDUC - Educational Development reports Q2 results
        # $ANGO - AngioDynamics Non - GAAP EPS of -$0.06 misses by $0.04, revenue of $81.5 M misses by $1.93 M, reaffirms FY guidance
        # $TROX $CC $VNTR - Venator plunges after warning of TiO2 sales weakness
        # $MKC - McCormick & Company notches in -line, reaffirms outlook
        # $MKC - McCormick Non - GAAP EPS of $0.69 misses by $0.03, revenue of $1.6B beats by $10M
        # $PPG - PPG cuts earnings guidance on expected soft demand from Europe
        # $FIVN - Five9 guides Q3 earnings above consensus estimates, names new CEO
        # $SPY $WMT $AAPL - Earnings season kicks off with gloomy expectation
        # $MACE - Mace Security completes restructuring, Q3 adj. earnings now positive
        # $CAG - ConAgra Brands shares boosted by earnings beat, reaffirmed full-year forecast
        # AngioDynamics Q1 2023 Earnings Preview
        # $MKC - McCormick Q3 2022 Earnings Preview
        # $RPM - RPM International on the rise after sold earnings beat
        # $LW - Lamb Weston Holdings rises above earnings expectations, reaffirms guidance
        # $TJX $DECK $DKS - Watch these retail stocks for earnings jolts
        # $AEP - AEP narrows 2022 earnings guidance, issues in-line 2023 outlook
        m = LoadEarningsReportsFromTwitter.parse_tweet(i['text'])
        if m:
            print(m.groupdict())

        if '$EARNINGS' in i['text']:
            tweet_url_description = LoadEarningsReportsFromTwitter.find_first_match("entities.urls[0].description", i)
            # e.g.
            # Ambarella press release (AMBA):
            # Q2 Non-GAAP EPS of $0.20 beats by $0.01.Revenue of $80.88M (+2.0% Y/Y) beats by $0.67M.
            # Gross margin on a non-GAAP basis for the second quarter of

            match = re.search(r'\([A-Z.]+\)', tweet_url_description)
            if match:
                symbol = match.group(0).strip("()")
                print('matched symbol=' + symbol)
        #         if Symbol.lookup_symbol(symbol, session):
        #             print(f'Found match for {symbol}')
        #         else:
        #             print(f'WARN could not find {symbol} in Symbols')
        #             # NEXT: deal with exchanges, e.g.: CTRL:CA, AIP.U:CA, PUL:CA - use regex groups
        #             return
            else:
                print(f'WARN - Could not find symbol in tweet_url_description')
                return

        #     earnings_report = EarningsReport(
        #         tweet_id=i['id'],
        #         tweet_date=i['created_at'],
        #         twitter_account=Twitter.account,
        #         tweet_text=i['text'],
        #         tweet_short_url=find_first_match("entities.urls[0].url", i),
        #         tweet_expanded_url=find_first_match("entities.urls[0].expanded_url", i),
        #         tweet_url_status=find_first_match("entities.urls[0].status", i),
        #         tweet_url_title=find_first_match("entities.urls[0].title", i),
        #         tweet_url_description=find_first_match("entities.urls[0].description", i))
            # parsed_symbol = Column(String(10), ForeignKey("symbols.symbol"), nullable=True)
            # symbol_object = relationship("Symbol")
            # currency = Column(String(3))
            # eps = Column(Numeric)
            # eps_surprise = Column(Numeric)
            # revenue = Column(BigInteger)
            # revenue_surprise = Column(BigInteger)
            # guidance_direction = Column(String(20)

    @staticmethod
    def find_first_match(jsonpath, json):
        jsonpath_expr = parse(jsonpath)
        matches = jsonpath_expr.find(json)
        if len(matches) > 0:
            return matches[0].value
        else:
            return None


if __name__ == '__main__':
    backfill = True
    commit = False
    paginate = True
    max_results = 100
    if backfill:
        max_date = datetime.utcnow() - timedelta(days=7)
    else:
        max_date = EarningsReport.get_max_date() or datetime.utcnow() - timedelta(days=7)

    payload = {'query': 'from:' + Twitter.account,  # + ' earnings',
               'max_results': max_results,
               'start_time': max_date.strftime("%Y-%m-%dT%H:%M:%SZ"),
               'tweet.fields': 'created_at,author_id,entities'}

    Twitter.call_paginated_api(
        url=Twitter.url_prefix + '/tweets/search/recent',
        payload=payload,
        method=LoadEarningsReportsFromTwitter.load, method_params={},
        paginate=paginate, commit=commit, next_token=None)