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

    er = EarningsReport(creator=Provider['Twitter_Marketcurrents'], updater=None)
    provider = 'Twitter_Marketcurrents'
    assert(LoadEarningsReportsFromTwitter.should_update(er, provider) is True)

    er = EarningsReport(creator=Provider['Twitter_Livesquawk'], updater=None)
    provider = 'Twitter_Marketcurrents'
    assert(LoadEarningsReportsFromTwitter.should_update(er, provider) is True)

    er = EarningsReport(creator=Provider['Twitter_Livesquawk'], updater=Provider['Twitter_Livesquawk'])
    provider = 'Twitter_Marketcurrents'
    assert(LoadEarningsReportsFromTwitter.should_update(er, provider) is True)

    er = EarningsReport(creator=Provider['Twitter_Livesquawk'], updater=Provider['Twitter_Marketcurrents'])
    provider = 'Twitter_Livesquawk'
    assert(LoadEarningsReportsFromTwitter.should_update(er, provider) is False)


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
        cashtags = [{'start': 0, 'end': 4, 'tag': 'PPG'}]
        assert('PPG' in LoadEarningsReportsFromTwitter.associate_tweet_with_symbols(session, cashtags).keys())

        cashtags = [{'start': 0, 'end': 4, 'tag': 'SPY'},
                    {'start': 5, 'end': 9, 'tag': 'WMT'},
                    {'start': 10, 'end': 15, 'tag': 'AAPL'}]
        assert('SPY' in LoadEarningsReportsFromTwitter.associate_tweet_with_symbols(session, cashtags).keys())
        assert('WMT' in LoadEarningsReportsFromTwitter.associate_tweet_with_symbols(session, cashtags).keys())
        assert('AAPL' in LoadEarningsReportsFromTwitter.associate_tweet_with_symbols(session, cashtags).keys())
        assert(len(LoadEarningsReportsFromTwitter.associate_tweet_with_symbols(session, cashtags).keys()) == 3)

        cashtags = [{'start': 0, 'end': 4, 'tag': 'SPY'},
                    {'start': 5, 'end': 9, 'tag': 'SPY'}]
        assert('SPY' in LoadEarningsReportsFromTwitter.associate_tweet_with_symbols(session, cashtags).keys())
        assert(len(LoadEarningsReportsFromTwitter.associate_tweet_with_symbols(session, cashtags).keys()) == 1)

        cashtags = [{'start': 0, 'end': 4, 'tag': 'SPY'},
                    {'start': 5, 'end': 9, 'tag': 'SPYZZZ'}]
        assert('SPY' in LoadEarningsReportsFromTwitter.associate_tweet_with_symbols(session, cashtags).keys())
        assert(len(LoadEarningsReportsFromTwitter.associate_tweet_with_symbols(session, cashtags).keys()) == 1)

        cashtags = [{'start': 0, 'end': 4, 'tag': 'GFELF'},
                    {'start': 5, 'end': 9, 'tag': 'GLD'}]
        assert('GFELF' in LoadEarningsReportsFromTwitter.associate_tweet_with_symbols(session, cashtags).keys())
        assert('GLD' in LoadEarningsReportsFromTwitter.associate_tweet_with_symbols(session, cashtags).keys())
        assert(len(LoadEarningsReportsFromTwitter.associate_tweet_with_symbols(session, cashtags).keys()) == 2)

        cashtags = [{'start': 0, 'end': 4, 'tag': 'SPYZZZ'}]
        assert(not LoadEarningsReportsFromTwitter.associate_tweet_with_symbols(session, cashtags))

        cashtags = None
        assert(not LoadEarningsReportsFromTwitter.associate_tweet_with_symbols(session, cashtags))


def test_associate_tweet_with_symbols_duplicate():
    tweet = '$CPG $CPG:CA - Crescent Point Energy GAAP EPS of C$0.82, revenue of C$1.1B'
    cashtags = [{'start': 0, 'end': 4, 'tag': 'CPG'}, {'start': 5, 'end': 9, 'tag': 'CPG'}]
    with model.Session() as session:
        assert(len(LoadEarningsReportsFromTwitter.associate_tweet_with_symbols(session, cashtags, tweet).keys()) == 1)


def test_parse_tweet_nii():
    tweet = '$SAR - Saratoga Investment Non-GAAP NII of $0.58 beats by $0.07, total Investment Income of $21.85M beats by $1.95M'
    account = Marketcurrents(Marketcurrents.account_name)
    dict = LoadEarningsReportsFromTwitter.parse_tweet(account, tweet)
    assert(dict.get('eps_sign') is None)
    assert(dict.get('eps_currency') == '$')
    assert(dict.get('eps') == '0.58')
    assert(dict.get('eps_surprise_direction') == 'beats')
    assert(dict.get('eps_surprise_currency') == '$')
    assert(dict.get('eps_surprise_amount') == '0.07')
    assert(dict.get('revenue_currency') == '$')
    assert(dict.get('revenue') == '21.85')
    assert(dict.get('revenue_uom') == 'M')
    assert(dict.get('revenue_surprise_direction') == 'beats')
    assert(dict.get('revenue_surprise_currency') == '$')
    assert(dict.get('revenue_surprise_amount') == '1.95')
    assert(dict.get('revenue_surprise_uom') == 'M')


def test_parse_tweet_basic():
    tweet = '$BABB GAAP EPS of $0.02, revenue of $0.88M'
    account = Marketcurrents(Marketcurrents.account_name)
    dict = LoadEarningsReportsFromTwitter.parse_tweet(account, tweet)
    assert(dict.get('eps_sign') is None)
    assert(dict.get('eps_currency') == '$')
    assert(dict.get('eps') == '0.02')
    assert(dict.get('eps_surprise_direction') is None)
    assert(dict.get('eps_surprise_currency') is None)
    assert(dict.get('eps_surprise_amount') is None)
    assert(dict.get('revenue_currency') == '$')
    assert(dict.get('revenue') == '0.88')
    assert(dict.get('revenue_uom') == 'M')
    assert(dict.get('revenue_surprise_direction') is None)
    assert(dict.get('revenue_surprise_currency') is None)
    assert(dict.get('revenue_surprise_amount') is None)
    assert(dict.get('revenue_surprise_uom') is None)


def test_parse_tweet_with_surprises():
    tweet = '$TLRY $TLRY:CA - Tilray Non - GAAP EPS of -$0.08 misses by $0.01, revenue of $153M misses by $3.6M'
    account = Marketcurrents(Marketcurrents.account_name)
    dict = LoadEarningsReportsFromTwitter.parse_tweet(account, tweet)
    assert(dict.get('eps_sign') == '-')
    assert(dict.get('eps_currency') == '$')
    assert(dict.get('eps') == '0.08')
    assert(dict.get('eps_surprise_direction') == 'misses')
    assert(dict.get('eps_surprise_currency') == '$')
    assert(dict.get('eps_surprise_amount') == '0.01')
    assert(dict.get('revenue_currency') == '$')
    assert(dict.get('revenue') == '153')
    assert(dict.get('revenue_uom') == 'M')
    assert(dict.get('revenue_surprise_direction') == 'misses')
    assert(dict.get('revenue_surprise_currency') == '$')
    assert(dict.get('revenue_surprise_amount') == '3.6')
    assert(dict.get('revenue_surprise_uom') == 'M')


def test_parse_tweet_canadian():
    tweet = '$ATZAF $ATZ:CA - Aritzia&amp;nbsp; GAAP EPS of C$0.44, revenue of C$525.5M'
    account = Marketcurrents(Marketcurrents.account_name)
    dict = LoadEarningsReportsFromTwitter.parse_tweet(account, tweet)
    assert(dict.get('eps_sign') is None)
    assert(dict.get('eps_currency') == 'C$')
    assert(dict.get('eps') == '0.44')
    assert(dict.get('eps_surprise_direction') is None)
    assert(dict.get('eps_surprise_currency') is None)
    assert(dict.get('eps_surprise_amount') is None)
    assert(dict.get('revenue_currency') == 'C$')
    assert(dict.get('revenue') == '525.5')
    assert(dict.get('revenue_uom') == 'M')
    assert(dict.get('revenue_surprise_direction') is None)
    assert(dict.get('revenue_surprise_currency') is None)
    assert(dict.get('revenue_surprise_amount') is None)
    assert(dict.get('revenue_surprise_uom') is None)


def test_parse_tweet_with_guidance_1():
    tweet = 'AngioDynamics Non-GAAP EPS of -$0.06 misses by $0.04, revenue of $81.5M misses by $1.93M, reaffirms FY guidance'
    account = Marketcurrents(Marketcurrents.account_name)
    dict = LoadEarningsReportsFromTwitter.parse_tweet(account, tweet)
    assert (dict.get('eps_sign') == '-')
    assert(dict.get('eps_currency') == '$')
    assert(dict.get('eps') == '0.06')
    assert(dict.get('eps_surprise_direction') == 'misses')
    assert(dict.get('eps_surprise_currency') == '$')
    assert(dict.get('eps_surprise_amount') == '0.04')
    assert(dict.get('revenue_currency') == '$')
    assert(dict.get('revenue') == '81.5')
    assert(dict.get('revenue_uom') == 'M')
    assert(dict.get('revenue_surprise_direction') == 'misses')
    assert(dict.get('revenue_surprise_currency') == '$')
    assert(dict.get('revenue_surprise_amount') == '1.93')
    assert(dict.get('revenue_surprise_uom') == 'M')
    assert(dict.get('guidance_1') == 'reaffirms')


def test_parse_tweet_with_space_after_currency():
    tweet = '$BLAH - Blah GAAP EPS of NOK 0.99, revenue of NOK 3.04B beats by NOK 20M'
    account = Marketcurrents(Marketcurrents.account_name)
    dict = LoadEarningsReportsFromTwitter.parse_tweet(account, tweet)
    assert (dict.get('eps_sign') is None)
    assert (dict.get('eps_currency') == 'NOK')
    assert (dict.get('eps') == '0.99')
    assert (dict.get('revenue_currency') == 'NOK')
    assert (dict.get('revenue') == '3.04')
    assert (dict.get('revenue_uom') == 'B')


def test_parse_tweet_with_bad_currency():
    tweet = '$SPOT - Spotify GAAP EPS of -€0.99 misses by v0.15, revenue of €3.04B beats by €20M'
    account = Marketcurrents(Marketcurrents.account_name)
    dict = LoadEarningsReportsFromTwitter.parse_tweet(account, tweet)
    assert (dict.get('eps_sign') == '-')
    assert (dict.get('eps_currency') == '€')
    assert (dict.get('eps') == '0.99')
    assert (dict.get('eps_surprise_direction') == 'misses')
    assert (dict.get('eps_surprise_currency') is None)
    assert (dict.get('eps_surprise_amount') is None)
    assert (dict.get('revenue_currency') == '€')
    assert (dict.get('revenue') == '3.04')
    assert (dict.get('revenue_uom') == 'B')
    assert (dict.get('revenue_surprise_direction') == 'beats')
    assert (dict.get('revenue_surprise_currency') == '€')
    assert (dict.get('revenue_surprise_amount') == '20')
    assert (dict.get('revenue_surprise_uom') == 'M')
    assert (dict.get('guidance_1') is None)


def test_parse_tweet_not_earnings():
    tweet = '$AZZ declares $0.17 dividend'
    account = Marketcurrents(Marketcurrents.account_name)
    dict = LoadEarningsReportsFromTwitter.parse_tweet(account, tweet)
    assert(dict is None)


def test_parse_tweet_livesquawk():
    tweet = '''
    $DAL Delta Airlines Q3 22 Earnings: \
      - Adj EPS $1.51 (est $1.54) \
      - Adj Revenue $12.84B (est $12.83B) \
      - Sees Q4 Adj EPS $1 To $1.25 (est $0.80) \
      - Raises Q4 EPS to $1.00
      '''
    account = Livesquawk(Livesquawk.account_name)
    dict = LoadEarningsReportsFromTwitter.parse_tweet(account, tweet)
    assert(dict.get('eps_sign') is None)
    assert(dict.get('eps_currency') == '$')
    assert(dict.get('eps') == '1.51')
    assert(dict.get('eps_estimate_currency') == '$')
    assert(dict.get('eps_estimate_amount') == '1.54')
    assert(dict.get('revenue_currency') == '$')
    assert(dict.get('revenue') == '12.84')
    assert(dict.get('revenue_uom') == 'B')
    assert(dict.get('revenue_estimate_currency') == '$')
    assert(dict.get('revenue_estimate_amount') == '12.83')
    assert(dict.get('revenue_estimate_uom') == 'B')
    assert(dict.get('guidance_1').lower() == 'raises')


def test_parse_tweet_livesquawk_without_uom():
    tweet = '''
    $UNH UnitedHealth Q3 22 Earnings: 
- EPS $5.55 (est $5.20) 
- Revenue $46.56 (exp $45.54) 
- Sees FY EPS $ 20.85 To $21.05 (prev $20.45 To $20.95
'''
    account = Livesquawk(Livesquawk.account_name)
    dict = LoadEarningsReportsFromTwitter.parse_tweet(account, tweet)
    assert(dict.get('eps_sign') is None)
    assert(dict.get('eps_currency') == '$')
    assert(dict.get('eps') == '5.55')
    assert(dict.get('eps_estimate_currency') == '$')
    assert(dict.get('eps_estimate_amount') == '5.20')
    assert(dict.get('revenue_currency') == '$')
    assert(dict.get('revenue') == '46.56')
    assert(dict.get('revenue_uom') is None)
    assert(dict.get('revenue_estimate_currency') == '$')
    assert(dict.get('revenue_estimate_amount') == '45.54')
    assert(dict.get('revenue_estimate_uom') is None)


def test_parse_tweet_livesquawk_revenue_first():
    tweet = '''
    $SCHW Charles Schwab Q3 22 Earnings:  
    - Revenue: $5.5B (exp $5.41B)  
    - Adj EPS: $1.10 (exp $1.05)'''
    account = Livesquawk(Livesquawk.account_name)
    dict = LoadEarningsReportsFromTwitter.parse_tweet(account, tweet)
    assert (dict.get('eps_sign') is None)
    assert (dict.get('eps_currency') == '$')
    assert (dict.get('eps') == '1.10')
    assert (dict.get('eps_estimate_currency') == '$')
    assert (dict.get('eps_estimate_amount') == '1.05')
    assert (dict.get('revenue_currency') == '$')
    assert (dict.get('revenue') == '5.5')
    assert (dict.get('revenue_uom') == 'B')
    assert (dict.get('revenue_estimate_currency') == '$')
    assert (dict.get('revenue_estimate_amount') == '5.41')
    assert (dict.get('revenue_estimate_uom') == 'B')


def test_parse_tweet_livesquawk_worded_estimated():
    tweet = '''
$UAL United Airlines Q3 22 Earnings: 
- Adj EPS: $2.81 (Estimate: $2.29) 
- Passenger Revenue: $11.65B (Estimate: $11.39B) 
- Sees Q4 Adj. Op Margin To Exceed 2019'''
    account = Livesquawk(Livesquawk.account_name)
    dict = LoadEarningsReportsFromTwitter.parse_tweet(account, tweet)
    assert (dict.get('eps_sign') is None)
    assert (dict.get('eps_currency') == '$')
    assert (dict.get('eps') == '2.81')
    assert (dict.get('eps_estimate_currency') == '$')
    assert (dict.get('eps_estimate_amount') == '2.29')
    assert (dict.get('revenue_currency') == '$')
    assert (dict.get('revenue') == '11.65')
    assert (dict.get('revenue_uom') == 'B')
    assert (dict.get('revenue_estimate_currency') == '$')
    assert (dict.get('revenue_estimate_amount') == '11.39')
    assert (dict.get('revenue_estimate_uom') == 'B')


def test_parse_tweet_livesquawk_worded_rev():
    tweet = '''
    $BX Blackstone Inc Q3 22 Earnings:  
- Total Segment Rev. $2.59B, Est. $2.51B 
- Aum $950.9B (est $966.82B) 
- Inflows $44.8B (est $60.49B) 
- Distributable Income/SHR $1.06 (est 99c)'''
    account = Livesquawk(Livesquawk.account_name)
    dict = LoadEarningsReportsFromTwitter.parse_tweet(account, tweet)
    assert (dict.get('eps_sign') is None)
    assert (dict.get('eps_currency') is None)
    assert (dict.get('eps') is None)
    assert (dict.get('eps_estimate_currency') is None)
    assert (dict.get('eps_estimate_amount') is None)
    assert (dict.get('revenue_currency') == '$')
    assert (dict.get('revenue') == '2.59')
    assert (dict.get('revenue_uom') == 'B')
    assert (dict.get('revenue_estimate_currency') == '$')
    assert (dict.get('revenue_estimate_amount') == '2.51')
    assert (dict.get('revenue_estimate_uom') == 'B')


def test_evaluate_data_quality():
    er = EarningsReport(revenue_surprise=-100, revenue=50)
    assert('-100 too large' in LoadEarningsReportsFromTwitter.evaluate_data_quality((er)))

    er = EarningsReport(revenue_surprise=None, revenue=50)
    assert(None is LoadEarningsReportsFromTwitter.evaluate_data_quality((er)))

    er = EarningsReport(revenue_surprise=74, revenue=100)
    assert(None is LoadEarningsReportsFromTwitter.evaluate_data_quality((er)))

    er = EarningsReport(revenue_surprise=75, revenue=100)
    assert('75 too large' in LoadEarningsReportsFromTwitter.evaluate_data_quality((er)))
