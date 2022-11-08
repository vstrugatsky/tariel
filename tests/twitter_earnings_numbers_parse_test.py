from loaders.earnings_reports_from_twitter import LoadEarningsReportsFromTwitter
from loaders.twitter_livesquawk import Livesquawk
from loaders.twitter_marketcurrents import Marketcurrents


def test_parse_tweet_nii():
    tweet = '$SAR - Saratoga Investment Non-GAAP NII of $0.58 beats by $0.07, total Investment Income of $21.85M beats by $1.95M'
    loader = LoadEarningsReportsFromTwitter(Marketcurrents(Marketcurrents.account_name))
    dict = loader.parse_earnings_numbers(tweet)
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
    loader = LoadEarningsReportsFromTwitter(Marketcurrents(Marketcurrents.account_name))
    dict = loader.parse_earnings_numbers(tweet)
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
    loader = LoadEarningsReportsFromTwitter(Marketcurrents(Marketcurrents.account_name))
    dict = loader.parse_earnings_numbers(tweet)
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
    loader = LoadEarningsReportsFromTwitter(Marketcurrents(Marketcurrents.account_name))
    dict = loader.parse_earnings_numbers(tweet)
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


def test_trillions():
    tweet = '$SZKMF - Suzuki Motor Corporation GAAP EPS of ¥237.00, revenue of ¥2.22T'
    loader = LoadEarningsReportsFromTwitter(Marketcurrents(Marketcurrents.account_name))
    dict = loader.parse_earnings_numbers(tweet)
    assert(dict.get('revenue_currency') == '¥')
    assert(dict.get('revenue') == '2.22')
    assert(dict.get('revenue_uom') == 'T')


def test_parse_tweet_with_guidance():
    tweet = 'AngioDynamics Non-GAAP EPS of -$0.06 misses by $0.04, revenue of $81.5M misses by $1.93M, raises FY guidance'
    loader = LoadEarningsReportsFromTwitter(Marketcurrents(Marketcurrents.account_name))
    dict = loader.parse_earnings_numbers(tweet)
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
    assert(dict.get('positive_guidance')[0] == 'raises FY guidance')


def test_parse_above_consensus():
    tweet = '$TCMD - Tactile Systems GAAP EPS of $0.11, revenue of $65.3M, FY22 guidance above consensus'
    loader = LoadEarningsReportsFromTwitter(Marketcurrents(Marketcurrents.account_name))
    dict = loader.parse_earnings_numbers(tweet)
    assert(dict.get('positive_guidance')[0] == 'guidance above')


def test_parse_tweet_with_space_after_currency():
    tweet = '$BLAH - Blah GAAP EPS of NOK 0.99, revenue of NOK 3.04B beats by NOK 20M'
    loader = LoadEarningsReportsFromTwitter(Marketcurrents(Marketcurrents.account_name))
    dict = loader.parse_earnings_numbers(tweet)
    assert (dict.get('eps_sign') is None)
    assert (dict.get('eps_currency') == 'NOK')
    assert (dict.get('eps') == '0.99')
    assert (dict.get('revenue_currency') == 'NOK')
    assert (dict.get('revenue') == '3.04')
    assert (dict.get('revenue_uom') == 'B')


def test_parse_tweet_with_inconsistent_brazil_currency():
    tweet = '$CBD - Companhia Brasileira de Distribuio GAAP EPS of -R$1.10, revenue of $R4.27B'
    loader = LoadEarningsReportsFromTwitter(Marketcurrents(Marketcurrents.account_name))
    dict = loader.parse_earnings_numbers(tweet)
    assert (dict.get('eps_sign') == '-')
    assert (dict.get('eps_currency') == 'R$')
    assert (dict.get('eps') == '1.10')
    assert (dict.get('revenue_currency') == '$R')
    assert (dict.get('revenue') == '4.27')
    assert (dict.get('revenue_uom') == 'B')


def parse_tweet_with_jpy_and_trillions():
    tweet = '$SZKMF - Suzuki Motor Corporation GAAP EPS of ¥237.00, revenue of ¥2.22T'
    loader = LoadEarningsReportsFromTwitter(Marketcurrents(Marketcurrents.account_name))
    dict = loader.parse_earnings_numbers(tweet)
    assert (dict.get('eps_currency') == '¥')
    assert (dict.get('eps') == '237.00')
    assert (dict.get('revenue_currency') == '¥')
    assert (dict.get('revenue') == '2.22')
    assert (dict.get('revenue_uom') == 'T')


def test_parse_tweet_with_bad_currency():
    tweet = '$SPOT - Spotify GAAP EPS of -€0.99 misses by v0.15, revenue of €3.04B beats by €20M'
    loader = LoadEarningsReportsFromTwitter(Marketcurrents(Marketcurrents.account_name))
    dict = loader.parse_earnings_numbers(tweet)
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
    assert (dict.get('positive_guidance') is None)


def test_parse_tweet_not_earnings():
    tweet = '$AZZ declares $0.17 dividend'
    loader = LoadEarningsReportsFromTwitter(Marketcurrents(Marketcurrents.account_name))
    dict = loader.parse_earnings_numbers(tweet)
    assert(not dict)


def test_parse_tweet_pesos():
    tweet = '$BSMX - Banco Santander México GAAP EPS of Ps.1.21, revenue of Ps.23.64B'
    loader = LoadEarningsReportsFromTwitter(Marketcurrents(Marketcurrents.account_name))
    dict = loader.parse_earnings_numbers(tweet)
    assert (dict.get('eps_sign') is None)
    assert (dict.get('eps_currency') == 'Ps.')
    assert (dict.get('eps') == '1.21')
    assert (dict.get('revenue_currency') == 'Ps.')
    assert (dict.get('revenue') == '23.64')
    assert (dict.get('revenue_uom') == 'B')


def test_parse_tweet_remnibi():
    tweet = '$RCON - Recon Technology GAAP EPS of RMB3.20, revenue of RMB83.8M'
    loader = LoadEarningsReportsFromTwitter(Marketcurrents(Marketcurrents.account_name))
    dict = loader.parse_earnings_numbers(tweet)
    assert (dict.get('eps_sign') is None)
    assert (dict.get('eps_currency') == 'RMB')
    assert (dict.get('eps') == '3.20')
    assert (dict.get('revenue_currency') == 'RMB')
    assert (dict.get('revenue') == '83.8')
    assert (dict.get('revenue_uom') == 'M')


def test_parse_tweet_singaporean():
    tweet = '$MAPIF - Mapletree Industrial Trust Net income of S$130.32, revenue of S$175.51M beats by $61.37M'
    loader = LoadEarningsReportsFromTwitter(Marketcurrents(Marketcurrents.account_name))
    dict = loader.parse_earnings_numbers(tweet)
    assert (dict.get('eps_sign') is None)
    assert (dict.get('eps_currency') is None)
    assert (dict.get('eps') is None)
    assert (dict.get('revenue_currency') == 'S$')
    assert (dict.get('revenue') == '175.51')
    assert (dict.get('revenue_uom') == 'M')


def test_parse_inline():
    tweet = '$NEWP $NUAG:CA - New Pacific Metals GAAP EPS of -$0.01 in-line'
    loader = LoadEarningsReportsFromTwitter(Marketcurrents(Marketcurrents.account_name))
    dict = loader.parse_earnings_numbers(tweet)
    assert (dict.get('eps_sign') == '-')
    assert (dict.get('eps_currency') == '$')
    assert (dict.get('eps') == '0.01')
    assert (dict.get('eps_surprise_direction') == 'in-line')
    assert (dict.get('eps_surprise_amount') is None)
    assert (dict.get('revenue_currency') is None)
    assert (dict.get('revenue') is None)
    assert (dict.get('revenue_uom') is None)


def test_parse_II():
    tweet = '$NEWT - Newtek Business NII of $0.01 per share, TII of $23.6M'
    loader = LoadEarningsReportsFromTwitter(Marketcurrents(Marketcurrents.account_name))
    dict = loader.parse_earnings_numbers(tweet)
    assert (dict.get('eps_sign') is None)
    assert (dict.get('eps_currency') == '$')
    assert (dict.get('eps') == '0.01')
    assert (dict.get('eps_surprise_direction') is None)
    assert (dict.get('eps_surprise_amount') is None)
    assert (dict.get('revenue_currency') == '$')
    assert (dict.get('revenue') == '23.6')
    assert (dict.get('revenue_uom') == 'M')


def test_parse_tweet_weird_euros():
    tweet = '$TRATF - Traton SE GAAP EPS of Є1.32, revenue of Є28.45B'
    loader = LoadEarningsReportsFromTwitter(Marketcurrents(Marketcurrents.account_name))
    dict = loader.parse_earnings_numbers(tweet)
    assert (dict.get('eps_sign') is None)
    assert (dict.get('eps_currency') == 'Є')
    assert (dict.get('eps') == '1.32')
    assert (dict.get('revenue_currency') == 'Є')
    assert (dict.get('revenue') == '28.45')
    assert (dict.get('revenue_uom') == 'B')


def test_parse_tweet_livesquawk():
    tweet = '''
    $DAL Delta Airlines Q3 22 Earnings: \
      - Adj EPS $1.51 (est $1.54) \
      - Adj Revenue $12.84B (est $12.83B) \
      - Sees Q4 Adj EPS $1 To $1.25 (est $0.80) \
      - Raises Q4 EPS to $1.00
      '''
    loader = LoadEarningsReportsFromTwitter(Livesquawk(Livesquawk.account_name))
    dict = loader.parse_earnings_numbers(tweet)
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


def test_parse_tweet_livesquawk_without_uom():
    tweet = '''
    $UNH UnitedHealth Q3 22 Earnings: 
- EPS $5.55 (est $5.20) 
- Revenue $46.56 (exp $45.54) 
- Sees FY EPS $ 20.85 To $21.05 (prev $20.45 To $20.95
'''
    loader = LoadEarningsReportsFromTwitter(Livesquawk(Livesquawk.account_name))
    dict = loader.parse_earnings_numbers(tweet)
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
    loader = LoadEarningsReportsFromTwitter(Livesquawk(Livesquawk.account_name))
    dict = loader.parse_earnings_numbers(tweet)
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
    loader = LoadEarningsReportsFromTwitter(Livesquawk(Livesquawk.account_name))
    dict = loader.parse_earnings_numbers(tweet)
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
    loader = LoadEarningsReportsFromTwitter(Livesquawk(Livesquawk.account_name))
    dict = loader.parse_earnings_numbers(tweet)
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
