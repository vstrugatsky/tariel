import re
import model
from loaders.earnings_reports_from_twitter import LoadEarningsReportsFromTwitter
from loaders.twitter_livesquawk import Livesquawk
from loaders.twitter_marketcurrents import Marketcurrents
from model.earnings_reports import EarningsReport
from model.jobs import Provider
from utils.utils import Utils


def test_should_update():
    er = EarningsReport(creator=Provider['Twitter_Livesquawk'], updater=None)
    provider = 'Twitter_Livesquawk'
    assert(LoadEarningsReportsFromTwitter.should_update(er, provider) is True)

    er = EarningsReport(creator=Provider['Twitter_Livesquawk'], updater=None)
    provider = 'Twitter_Livesquawk'
    assert(LoadEarningsReportsFromTwitter.should_update(er, provider) is True)

    er = EarningsReport(creator=Provider['Twitter_Livesquawk'], updater=None)
    provider = 'Twitter_Marketcurrents'
    assert(LoadEarningsReportsFromTwitter.should_update(er, provider) is False)

    er = EarningsReport(creator=Provider['Twitter_Livesquawk'], updater=Provider['Twitter_Livesquawk'])
    provider = 'Twitter_Marketcurrents'
    assert(LoadEarningsReportsFromTwitter.should_update(er, provider) is False)

    er = EarningsReport(creator=Provider['Twitter_Livesquawk'], updater=Provider['Twitter_Marketcurrents'])
    provider = 'Twitter_Livesquawk'
    assert(LoadEarningsReportsFromTwitter.should_update(er, provider) is True)


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


def test_determine_surprise_marketcurrents():
    loader = LoadEarningsReportsFromTwitter(Marketcurrents(Marketcurrents.account_name))

    match_dict = {'eps_surprise_direction': None, 'eps_surprise_amount': None, 'eps_surprise_uom': None}
    assert(loader.account.determine_surprise(match_dict=match_dict, metrics='eps') is None)

    match_dict = {'eps_surprise_direction': 'BAD', 'eps_surprise_amount': 0.01, 'eps_surprise_uom': None}
    assert (loader.account.determine_surprise(match_dict=match_dict, metrics='eps') is None)

    match_dict = {'eps_surprise_direction': 'beats', 'eps_surprise_amount': 0.01, 'eps_surprise_uom': None}
    assert (loader.account.determine_surprise(match_dict=match_dict, metrics='eps') == 0.01)

    match_dict = {'revenue_surprise_direction': 'MISSES', 'revenue_surprise_amount': 0.01, 'revenue_surprise_uom': 'm'}
    assert (loader.account.determine_surprise(match_dict=match_dict, metrics='revenue') == -10000)

    match_dict = {'revenue_surprise_direction': 'misses', 'revenue_surprise_amount': 64.24, 'revenue_surprise_uom': 'M'}
    assert (loader.account.determine_surprise(match_dict=match_dict, metrics='revenue') == -64240000)


def test_determine_surprise_livesquawk():
    loader = LoadEarningsReportsFromTwitter(Livesquawk(Livesquawk.account_name))
    match_dict = {'eps': '1.51', 'eps_estimate_amount': '1.54'}
    assert (loader.account.determine_surprise(match_dict=match_dict, metrics='eps') == -0.03)

    match_dict = {'revenue': '12.84', 'revenue_uom': 'b', 'revenue_estimate_amount': '12.83', 'revenue_estimate_uom': 'B'}
    assert (loader.account.determine_surprise(match_dict=match_dict, metrics='revenue') == 10000000)

    match_dict = {'revenue': '12.84', 'revenue_uom': None, 'revenue_estimate_amount': '12.83', 'revenue_estimate_uom': None}
    assert (loader.account.determine_surprise(match_dict=match_dict, metrics='revenue') == 10000000)


def test_apply_uom():
    assert(Utils.apply_uom(amount=0.07, uom=None) == 0.07)
    assert(Utils.apply_uom(0.07, 'Z') == 0.07)
    assert(Utils.apply_uom(0.07, 'k') == 70)
    assert(Utils.apply_uom(0.07, 'M') == 70000)
    assert(Utils.apply_uom(1.1, 'b') == 1100000000)
    assert(Utils.apply_uom(64.24, 'M') == 64240000)


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
    loader = LoadEarningsReportsFromTwitter(Marketcurrents(Marketcurrents.account_name))
    m: re.Match = loader.account.parse_tweet(tweet)
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
    loader = LoadEarningsReportsFromTwitter(Marketcurrents(Marketcurrents.account_name))
    m: re.Match = loader.account.parse_tweet(tweet)
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
    loader = LoadEarningsReportsFromTwitter(Marketcurrents(Marketcurrents.account_name))
    m: re.Match = loader.account.parse_tweet(tweet)
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
    loader = LoadEarningsReportsFromTwitter(Marketcurrents(Marketcurrents.account_name))
    m: re.Match = loader.account.parse_tweet(tweet)
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
    loader = LoadEarningsReportsFromTwitter(Marketcurrents(Marketcurrents.account_name))
    m: re.Match = loader.account.parse_tweet(tweet)
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
    loader = LoadEarningsReportsFromTwitter(Marketcurrents(Marketcurrents.account_name))
    m: re.Match = loader.account.parse_tweet(tweet)
    assert(m is None)


def test_parse_tweet_livesquawk():
    tweet = '''
    $DAL Delta Airlines Q3 22 Earnings: \
      - Adj EPS $1.51 (est $1.54) \
      - Adj Revenue $12.84B (est $12.83B) \
      - Sees Q4 Adj EPS $1 To $1.25 (est $0.80)
      '''
    loader = LoadEarningsReportsFromTwitter(Livesquawk(Livesquawk.account_name))
    m: re.Match = loader.account.parse_tweet(tweet)
    assert(m.groupdict().get('eps_sign') is None)
    assert(m.groupdict().get('eps_currency') == '$')
    assert(m.groupdict().get('eps') == '1.51')
    assert(m.groupdict().get('eps_estimate_currency') == '$')
    assert(m.groupdict().get('eps_estimate_amount') == '1.54')
    assert(m.groupdict().get('revenue_currency') == '$')
    assert(m.groupdict().get('revenue') == '12.84')
    assert(m.groupdict().get('revenue_uom') == 'B')
    assert(m.groupdict().get('revenue_estimate_currency') == '$')
    assert(m.groupdict().get('revenue_estimate_amount') == '12.83')
    assert(m.groupdict().get('revenue_estimate_uom') == 'B')


def test_parse_tweet_livesquawk_without_uom():
    tweet = '''
    $UNH UnitedHealth Q3 22 Earnings: 
- EPS $5.55 (est $5.20) 
- Revenue $46.56 (est $45.54) 
- Sees FY EPS $ 20.85 To $21.05 (prev $20.45 To $20.95
'''
    loader = LoadEarningsReportsFromTwitter(Livesquawk(Livesquawk.account_name))
    m: re.Match = loader.account.parse_tweet(tweet)
    assert(m.groupdict().get('eps_sign') is None)
    assert(m.groupdict().get('eps_currency') == '$')
    assert(m.groupdict().get('eps') == '5.55')
    assert(m.groupdict().get('eps_estimate_currency') == '$')
    assert(m.groupdict().get('eps_estimate_amount') == '5.20')
    assert(m.groupdict().get('revenue_currency') == '$')
    assert(m.groupdict().get('revenue') == '46.56')
    assert(m.groupdict().get('revenue_uom') is None)
    assert(m.groupdict().get('revenue_estimate_currency') == '$')
    assert(m.groupdict().get('revenue_estimate_amount') == '45.54')
    assert(m.groupdict().get('revenue_estimate_uom') is None)

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
    tweet = '$UNTY - Unity Bancorp GAAP EPS of $0.93'
    tweet = '$THTX $TH:CA - Theratechnologies reports Q3 results, FY22 guidance is on track'
    tweet = '$RWT - Redwood Trust stock gains 5% after hours on preliminary Q3 results'
    tweet = 'NEWS: $INMD InMode Expects Record Third Quarter 2022 Revenue of $120.5M-$120.9M, Raising Full-Year 2022 Revenue Guidance to $445M-450M'
    tweet_acct = '@marketwirenews'
    tweet = '$UNH - UnitedHealth stock trades higher as revenue soars 12%, FY22 outlook raised again'
    tweet = '$PLUG - Plug Power plunges as full-year revenues seen missing guidance'

    tweet = '$WBA Walgreens Boots Q4 22 Earnings: \
        - Adj EPS $0.80 (est $0.77) \
        - Revenue $32.45B (est $32.28B) \
        - Sees 2023 Adj EPS $4.45 To $4.65 (est $4.51)'

    tweet = '$BLK BlackRock Q3 22 Earnings: \
            - Adj EPS $9.55 (est $7.03) \
            - Revenue $4.31B (est $4.33B) \
            - AUM $7.96T (est $8.27T)'

    tweet = '''
    $SCHW Charles Schwab Q3 22 Earnings:  
- Revenue: $5.5B (exp $5.41B)  
- Adj EPS: $1.10 (exp $1.05)
'''

    twwet = '''
    $BAC Bank Of America Q3 22 Earnings:  
- EPS: $0.81 (exp $0.77)  
- Investment Banking Rev: $1.17B (est $1.17B) 
- Trading Revenue Ex DVA: $4.1B (est $3.81B) 
- Revenue Net Of Interest Expense: $24.50B'''

    tweet = '''
    $BNY Bank of NY Mellon Q3 22 Earnings:  
- Revenue: $4.28B (exp $4.21B)  
- Adj EPS: $1.21 (exp $1.01)'''

    # DAL missing!!
