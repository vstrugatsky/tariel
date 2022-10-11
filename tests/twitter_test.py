import re
from loaders.earnings_reports_from_twitter import LoadEarningsReportsFromTwitter
from model.earnings_reports import EarningsReport


def test_symbol_in_parens_regex():
    desc = '''
    Russia's Gazprom (OGZPY) said on Tuesday it earned a record net profit of 2.5T rubles ($41.75B) in H1 2022, 
    "despite sanctions pressure and an unfavorable"
    '''
    m = re.search(r'\([A-Z]+\)', desc)
    assert(m.group(0) == '(OGZPY)')


def test_parse_tweet():
    tweet = '$BABB GAAP EPS of $0.02, revenue of $0.88M'
    m: re.Match = LoadEarningsReportsFromTwitter.parse_tweet(tweet)
    assert(m.groupdict().get('eps_sign') is None)
    assert(m.groupdict().get('eps_currency') == '$')
    assert(m.groupdict().get('eps') == '0.02')
    assert(m.groupdict().get('eps_surprise_direction') is None)
    assert(m.groupdict().get('eps_surprise_currency') is None)
    assert(m.groupdict().get('eps_surprise_amount') is None)
    assert(m.groupdict().get('revenue_currency') == '$')
    assert(m.groupdict().get('revenue') == '0.88')
    assert(m.groupdict().get('revenue_uom') == 'M')
    assert(m.groupdict().get('revenue_surprise_direction') is None)
    assert(m.groupdict().get('revenue_surprise_currency') is None)
    assert(m.groupdict().get('revenue_surprise_amount') is None)
    assert(m.groupdict().get('revenue_surprise_uom') is None)

    tweet = '$TLRY $TLRY:CA - Tilray Non - GAAP EPS of -$0.08 misses by $0.01, revenue of $153M misses by $3.6M'
    m: re.Match = LoadEarningsReportsFromTwitter.parse_tweet(tweet)
    assert (m.groupdict().get('eps_sign') == '-')
    assert(m.groupdict().get('eps_currency') == '$')
    assert(m.groupdict().get('eps') == '0.08')
    assert(m.groupdict().get('eps_surprise_direction') == 'misses')
    assert(m.groupdict().get('eps_surprise_currency') == '$')
    assert(m.groupdict().get('eps_surprise_amount') == '0.01')
    assert(m.groupdict().get('revenue_currency') == '$')
    assert(m.groupdict().get('revenue') == '153')
    assert(m.groupdict().get('revenue_uom') == 'M')
    assert(m.groupdict().get('revenue_surprise_direction') == 'misses')
    assert(m.groupdict().get('revenue_surprise_currency') == '$')
    assert(m.groupdict().get('revenue_surprise_amount') == '3.6')
    assert(m.groupdict().get('revenue_surprise_uom') == 'M')

    tweet = '$AZZ declares $0.17 dividend'
    m = LoadEarningsReportsFromTwitter.parse_tweet(tweet)
    assert(m is None)

    tweet = 'AngioDynamics Non-GAAP EPS of -$0.06 misses by $0.04, revenue of $81.5M misses by $1.93M, reaffirms FY guidance'
    tweet = 'Tesco PLC Non-GAAP EPS of 10.67p, revenue of £28.18B'
    tweet = '$HELE - Helen of Troy Non-GAAP EPS of $2.27 beats by $0.06, revenue of $521.4M beats by $2.33M, updates FY guidance'
    tweet = '$SAR - Saratoga Investment Non-GAAP NII of $0.58 beats by $0.07, total Investment Income of $21.85M beats by $1.95M'
