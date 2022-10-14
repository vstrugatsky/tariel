import re
import model
from loaders.earnings_reports_from_twitter import LoadEarningsReportsFromTwitter


def test_determine_currency():
    assert(LoadEarningsReportsFromTwitter.determine_currency(eps_currency=None, revenue_currency=None) is None)
    assert(LoadEarningsReportsFromTwitter.determine_currency('$', None) == 'USD')
    assert(LoadEarningsReportsFromTwitter.determine_currency(None, '$') == 'USD')
    assert(LoadEarningsReportsFromTwitter.determine_currency('$', '$') == 'USD')


def test_determine_eps():
    # determine_eps(eps_sign: str | None, eps: str | None) -> float:
    assert(LoadEarningsReportsFromTwitter.determine_eps(eps_sign=None, eps=None) == 0)
    assert(LoadEarningsReportsFromTwitter.determine_eps(None, eps='0.67') == 0.67)
    assert(LoadEarningsReportsFromTwitter.determine_eps('-', eps='0.67') == -0.67)
    assert(LoadEarningsReportsFromTwitter.determine_eps('-', eps='1') == -1)


def test_determine_surprise():
    assert(LoadEarningsReportsFromTwitter.determine_surprise(surprise_direction=None, surprise_amount=0.01, surprise_uom=None) is None)
    assert(LoadEarningsReportsFromTwitter.determine_surprise('BAD', 0.01, None) is None)
    assert(LoadEarningsReportsFromTwitter.determine_surprise('beats', 0.01, None) == 0.01)
    assert(LoadEarningsReportsFromTwitter.determine_surprise('MISSES', 0.01, 'm') == -10000)
    assert(LoadEarningsReportsFromTwitter.determine_surprise('misses', 64.24, 'M') == -64240000)


def test_apply_uom():
    assert(LoadEarningsReportsFromTwitter.apply_uom(amount=0.07, uom=None) == 0.07)
    assert(LoadEarningsReportsFromTwitter.apply_uom(0.07, 'Z') == 0.07)
    assert(LoadEarningsReportsFromTwitter.apply_uom(0.07, 'k') == 70)
    assert(LoadEarningsReportsFromTwitter.apply_uom(0.07, 'M') == 70000)
    assert(LoadEarningsReportsFromTwitter.apply_uom(1.1, 'b') == 1100000000)
    assert(LoadEarningsReportsFromTwitter.apply_uom(64.24, 'M') == 64240000)


def test_associate_tweet_with_symbol():
    with model.Session() as session:
        text = '$PPG blah'
        cashtags = [{'start': 0, 'end': 4, 'tag': 'PPG'}]
        assert(LoadEarningsReportsFromTwitter.associate_tweet_with_symbol(session, cashtags, text).symbol == 'PPG')

        text = '$SPY $WMT $AAPL blah'
        cashtags = [{'start': 0, 'end': 4, 'tag': 'SPY'},
                    {'start': 5, 'end': 9, 'tag': 'WMT'},
                    {'start': 10, 'end': 15, 'tag': 'AAPL'}]
        assert(LoadEarningsReportsFromTwitter.associate_tweet_with_symbol(session, cashtags, text) is None)

        text = '$SPY $SPY:CA blah'
        cashtags = [{'start': 0, 'end': 4, 'tag': 'SPY'},
                    {'start': 5, 'end': 9, 'tag': 'SPY'}]
        assert(LoadEarningsReportsFromTwitter.associate_tweet_with_symbol(session, cashtags, text).symbol == 'SPY')

        text = '$SPY blah'
        cashtags = [{'start': 0, 'end': 4, 'tag': 'SPY'},
                    {'start': 5, 'end': 9, 'tag': 'SPYZZZ'}]
        assert(LoadEarningsReportsFromTwitter.associate_tweet_with_symbol(session, cashtags, text).symbol == 'SPY')

        cashtags = [{'start': 0, 'end': 4, 'tag': 'GFELF'},
                    {'start': 5, 'end': 9, 'tag': 'GLD'}]
        text = '$GFELF $GLD:CA blah blah'
        assert(LoadEarningsReportsFromTwitter.associate_tweet_with_symbol(session, cashtags, text).symbol == 'GFELF')

        cashtags = [{'start': 0, 'end': 4, 'tag': 'VLNS'},
                    {'start': 5, 'end': 9, 'tag': 'VLNS'}]
        text = '$VLNS $VLNS:CA blah blah'
        assert(LoadEarningsReportsFromTwitter.associate_tweet_with_symbol(session, cashtags, text).symbol == 'VLNS')

        cashtags = [{'start': 0, 'end': 4, 'tag': 'SPYZZZ'}]
        assert(LoadEarningsReportsFromTwitter.associate_tweet_with_symbol(session, cashtags, text) is None)

        cashtags = None
        assert(LoadEarningsReportsFromTwitter.associate_tweet_with_symbol(session, cashtags, text) is None)


def test_parse_tweet_nii():
    tweet = '$SAR - Saratoga Investment Non-GAAP NII of $0.58 beats by $0.07, total Investment Income of $21.85M beats by $1.95M'
    m: re.Match = LoadEarningsReportsFromTwitter.parse_tweet(tweet)
    assert(m.groupdict().get('eps_sign') is None)
    assert(m.groupdict().get('eps_currency') == '$')
    assert(m.groupdict().get('eps') == '0.58')
    assert(m.groupdict().get('eps_surprise_direction') == 'beats')
    assert(m.groupdict().get('eps_surprise_currency') == '$')
    assert(m.groupdict().get('eps_surprise_amount') == '0.07')
    assert(m.groupdict().get('revenue_currency') == '$')
    assert(m.groupdict().get('revenue') == '21.85')
    assert(m.groupdict().get('revenue_uom') == 'M')
    assert(m.groupdict().get('revenue_surprise_direction') == 'beats')
    assert(m.groupdict().get('revenue_surprise_currency') == '$')
    assert(m.groupdict().get('revenue_surprise_amount') == '1.95')
    assert(m.groupdict().get('revenue_surprise_uom') == 'M')


def test_parse_tweet_basic():
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


def test_parse_tweet_with_surprises():
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


def test_parse_tweet_canadian():
    tweet = '$ATZAF $ATZ:CA - Aritzia&amp;nbsp; GAAP EPS of C$0.44, revenue of C$525.5M'
    m: re.Match = LoadEarningsReportsFromTwitter.parse_tweet(tweet)
    assert (m.groupdict().get('eps_sign') is None)
    assert(m.groupdict().get('eps_currency') == 'C$')
    assert(m.groupdict().get('eps') == '0.44')
    assert(m.groupdict().get('eps_surprise_direction') is None)
    assert(m.groupdict().get('eps_surprise_currency') is None)
    assert(m.groupdict().get('eps_surprise_amount') is None)
    assert(m.groupdict().get('revenue_currency') == 'C$')
    assert(m.groupdict().get('revenue') == '525.5')
    assert(m.groupdict().get('revenue_uom') == 'M')
    assert(m.groupdict().get('revenue_surprise_direction') is None)
    assert(m.groupdict().get('revenue_surprise_currency') is None)
    assert(m.groupdict().get('revenue_surprise_amount') is None)
    assert(m.groupdict().get('revenue_surprise_uom') is None)


def test_parse_tweet_with_guidance_1():
    tweet = 'AngioDynamics Non-GAAP EPS of -$0.06 misses by $0.04, revenue of $81.5M misses by $1.93M, reaffirms FY guidance'
    m: re.Match = LoadEarningsReportsFromTwitter.parse_tweet(tweet)
    assert (m.groupdict().get('eps_sign') == '-')
    assert(m.groupdict().get('eps_currency') == '$')
    assert(m.groupdict().get('eps') == '0.06')
    assert(m.groupdict().get('eps_surprise_direction') == 'misses')
    assert(m.groupdict().get('eps_surprise_currency') == '$')
    assert(m.groupdict().get('eps_surprise_amount') == '0.04')
    assert(m.groupdict().get('revenue_currency') == '$')
    assert(m.groupdict().get('revenue') == '81.5')
    assert(m.groupdict().get('revenue_uom') == 'M')
    assert(m.groupdict().get('revenue_surprise_direction') == 'misses')
    assert(m.groupdict().get('revenue_surprise_currency') == '$')
    assert(m.groupdict().get('revenue_surprise_amount') == '1.93')
    assert(m.groupdict().get('revenue_surprise_uom') == 'M')
    assert(m.groupdict().get('guidance_1') == 'reaffirms')


def test_parse_tweet_not_earnings():
    tweet = '$AZZ declares $0.17 dividend'
    m = LoadEarningsReportsFromTwitter.parse_tweet(tweet)
    assert(m is None)

    tweet = 'AngioDynamics Non-GAAP EPS of -$0.06 misses by $0.04, revenue of $81.5M misses by $1.93M, reaffirms FY guidance'
    tweet = 'Tesco PLC Non-GAAP EPS of 10.67p, revenue of £28.18B'
    tweet = '$HELE - Helen of Troy Non-GAAP EPS of $2.27 beats by $0.06, revenue of $521.4M beats by $2.33M, updates FY guidance'
    tweet = '$ORC - Orchid Island Capital provides prelim Q3 numbers'
    tweet = '$TWO - Two Harbors Investment dips 4% on prelim FQ3 numbers'
    tweet = '$QDEL - QuidelOrtho forecasts strong Q3 revenue above estimates, shares rise ~6% after hours'
    tweet = '$RYAAY $DLAKY $EJTTF - Strong forecasts from IAG, easyJet send European airline stocks soaring'
    tweet = '$INO - Inovio reports positive phase 1/2 results for recurrent respiratory papillomatosis drug'
    tweet = '$KMX $AN $ABG - Carvana stock crashes as used auto prices continue to decline'
    tweet = '$INFY - Infosys GAAP EPS of $0.18 in-line, revenue of $4.55B beats by $110M, revises FY guidance'
    tweet = '$INMD - InMode gains after setting strong-than-anticipated Q3 pre-results, guidance'
    tweet = '$PCRX - Pacira BioSciences guides Q3 revenue below consensus'
    tweet = '$BKSC - Bank of South Carolina GAAP EPS of $0.33'
    tweet = '$THTX $TH:CA - Theratechnologies reports Q3 results, FY22 guidance is on track'
    tweet = '$RWT - Redwood Trust stock gains 5% after hours on preliminary Q3 results'
    tweet = 'NEWS: $INMD InMode Expects Record Third Quarter 2022 Revenue of $120.5M-$120.9M, Raising Full-Year 2022 Revenue Guidance to $445M-450M'
    tweet_acct = '@marketwirenews'


    # @LiveSquawk
    tweet = 'LiveSquawk @LiveSquawk $DAL Delta Airlines Q3 22 Earnings: \
      - Adj EPS $1.51 (est $1.54) \
      - Adj Revenue $12.84B (est $12.83B) \
      - Sees Q4 Adj EPS $1 To $1.25 (est $0.80)'

    tweet = '$WBA Walgreens Boots Q4 22 Earnings: \
        - Adj EPS $0.80 (est $0.77) \
        - Revenue $32.45B (est $32.28B) \
        - Sees 2023 Adj EPS $4.45 To $4.65 (est $4.51)'

    tweet = '$BLK BlackRock Q3 22 Earnings: \
            - Adj EPS $9.55 (est $7.03) \
            - Revenue $4.31B (est $4.33B) \
            - AUM $7.96T (est $8.27T)'

    # DAL missing!!

