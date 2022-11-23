from loaders.earnings_reports_from_twitter import LoadEarningsReportsFromTwitter
from loaders.twitter_livesquawk import Livesquawk
from loaders.twitter_marketcurrents import Marketcurrents


def test_parse_tweet_nii():
    tweet = '$SAR - Saratoga Investment Non-GAAP NII of $0.58 beats by $0.07, total Investment Income of $21.85M beats by $1.95M'
    loader = LoadEarningsReportsFromTwitter(Marketcurrents(Marketcurrents.account_name))
    d = loader.parse_earnings_numbers(tweet)
    assert(d.get('eps_sign') is None)
    assert(d.get('eps_currency') == '$')
    assert(d.get('eps') == '0.58')
    assert(d.get('eps_surprise_direction') == 'beats')
    assert(d.get('eps_surprise_currency') == '$')
    assert(d.get('eps_surprise_amount') == '0.07')
    assert(d.get('revenue_currency') == '$')
    assert(d.get('revenue') == '21.85')
    assert(d.get('revenue_uom') == 'M')
    assert(d.get('revenue_surprise_direction') == 'beats')
    assert(d.get('revenue_surprise_currency') == '$')
    assert(d.get('revenue_surprise_amount') == '1.95')
    assert(d.get('revenue_surprise_uom') == 'M')


def test_parse_tweet_basic():
    tweet = '$BABB GAAP EPS of $0.02, revenue of $0.88M'
    loader = LoadEarningsReportsFromTwitter(Marketcurrents(Marketcurrents.account_name))
    d = loader.parse_earnings_numbers(tweet)
    assert(d.get('eps_sign') is None)
    assert(d.get('eps_currency') == '$')
    assert(d.get('eps') == '0.02')
    assert(d.get('eps_surprise_direction') is None)
    assert(d.get('eps_surprise_currency') is None)
    assert(d.get('eps_surprise_amount') is None)
    assert(d.get('revenue_currency') == '$')
    assert(d.get('revenue') == '0.88')
    assert(d.get('revenue_uom') == 'M')
    assert(d.get('revenue_surprise_direction') is None)
    assert(d.get('revenue_surprise_currency') is None)
    assert(d.get('revenue_surprise_amount') is None)
    assert(d.get('revenue_surprise_uom') is None)


def test_parse_tweet_with_surprises():
    tweet = '$TLRY $TLRY:CA - Tilray Non - GAAP EPS of -$0.08 misses by $0.01, revenue of $153M misses by $3.6M'
    loader = LoadEarningsReportsFromTwitter(Marketcurrents(Marketcurrents.account_name))
    d = loader.parse_earnings_numbers(tweet)
    assert(d.get('eps_sign') == '-')
    assert(d.get('eps_currency') == '$')
    assert(d.get('eps') == '0.08')
    assert(d.get('eps_surprise_direction') == 'misses')
    assert(d.get('eps_surprise_currency') == '$')
    assert(d.get('eps_surprise_amount') == '0.01')
    assert(d.get('revenue_currency') == '$')
    assert(d.get('revenue') == '153')
    assert(d.get('revenue_uom') == 'M')
    assert(d.get('revenue_surprise_direction') == 'misses')
    assert(d.get('revenue_surprise_currency') == '$')
    assert(d.get('revenue_surprise_amount') == '3.6')
    assert(d.get('revenue_surprise_uom') == 'M')


def test_parse_tweet_canadian():
    tweet = '$ATZAF $ATZ:CA - Aritzia&amp;nbsp; GAAP EPS of C$0.44, revenue of C$525.5M'
    loader = LoadEarningsReportsFromTwitter(Marketcurrents(Marketcurrents.account_name))
    d = loader.parse_earnings_numbers(tweet)
    assert(d.get('eps_sign') is None)
    assert(d.get('eps_currency') == 'C$')
    assert(d.get('eps') == '0.44')
    assert(d.get('eps_surprise_direction') is None)
    assert(d.get('eps_surprise_currency') is None)
    assert(d.get('eps_surprise_amount') is None)
    assert(d.get('revenue_currency') == 'C$')
    assert(d.get('revenue') == '525.5')
    assert(d.get('revenue_uom') == 'M')
    assert(d.get('revenue_surprise_direction') is None)
    assert(d.get('revenue_surprise_currency') is None)
    assert(d.get('revenue_surprise_amount') is None)
    assert(d.get('revenue_surprise_uom') is None)


def test_trillions():
    tweet = '$SZKMF - Suzuki Motor Corporation GAAP EPS of ¥237.00, revenue of ¥2.22T'
    loader = LoadEarningsReportsFromTwitter(Marketcurrents(Marketcurrents.account_name))
    d = loader.parse_earnings_numbers(tweet)
    assert(d.get('revenue_currency') == '¥')
    assert(d.get('revenue') == '2.22')
    assert(d.get('revenue_uom') == 'T')


def test_parse_tweet_with_guidance():
    tweet = 'AngioDynamics Non-GAAP EPS of -$0.06 misses by $0.04, revenue of $81.5M misses by $1.93M, raises FY guidance'
    loader = LoadEarningsReportsFromTwitter(Marketcurrents(Marketcurrents.account_name))
    d = loader.parse_earnings_numbers(tweet)
    assert (d.get('eps_sign') == '-')
    assert(d.get('eps_currency') == '$')
    assert(d.get('eps') == '0.06')
    assert(d.get('eps_surprise_direction') == 'misses')
    assert(d.get('eps_surprise_currency') == '$')
    assert(d.get('eps_surprise_amount') == '0.04')
    assert(d.get('revenue_currency') == '$')
    assert(d.get('revenue') == '81.5')
    assert(d.get('revenue_uom') == 'M')
    assert(d.get('revenue_surprise_direction') == 'misses')
    assert(d.get('revenue_surprise_currency') == '$')
    assert(d.get('revenue_surprise_amount') == '1.93')
    assert(d.get('revenue_surprise_uom') == 'M')


def test_parse_tweet_with_space_after_currency():
    tweet = '$BLAH - Blah GAAP EPS of NOK 0.99, revenue of NOK 3.04B beats by NOK 20M'
    loader = LoadEarningsReportsFromTwitter(Marketcurrents(Marketcurrents.account_name))
    d = loader.parse_earnings_numbers(tweet)
    assert (d.get('eps_sign') is None)
    assert (d.get('eps_currency') == 'NOK')
    assert (d.get('eps') == '0.99')
    assert (d.get('revenue_currency') == 'NOK')
    assert (d.get('revenue') == '3.04')
    assert (d.get('revenue_uom') == 'B')


def test_parse_tweet_with_inconsistent_brazil_currency():
    tweet = '$CBD - Companhia Brasileira de Distribuio GAAP EPS of -R$1.10, revenue of $R4.27B'
    loader = LoadEarningsReportsFromTwitter(Marketcurrents(Marketcurrents.account_name))
    d = loader.parse_earnings_numbers(tweet)
    assert (d.get('eps_sign') == '-')
    assert (d.get('eps_currency') == 'R$')
    assert (d.get('eps') == '1.10')
    assert (d.get('revenue_currency') == '$R')
    assert (d.get('revenue') == '4.27')
    assert (d.get('revenue_uom') == 'B')


def parse_tweet_with_jpy_and_trillions():
    tweet = '$SZKMF - Suzuki Motor Corporation GAAP EPS of ¥237.00, revenue of ¥2.22T'
    loader = LoadEarningsReportsFromTwitter(Marketcurrents(Marketcurrents.account_name))
    d = loader.parse_earnings_numbers(tweet)
    assert (d.get('eps_currency') == '¥')
    assert (d.get('eps') == '237.00')
    assert (d.get('revenue_currency') == '¥')
    assert (d.get('revenue') == '2.22')
    assert (d.get('revenue_uom') == 'T')


def test_parse_tweet_with_bad_currency():
    tweet = '$SPOT - Spotify GAAP EPS of -€0.99 misses by v0.15, revenue of €3.04B beats by €20M'
    loader = LoadEarningsReportsFromTwitter(Marketcurrents(Marketcurrents.account_name))
    d = loader.parse_earnings_numbers(tweet)
    assert (d.get('eps_sign') == '-')
    assert (d.get('eps_currency') == '€')
    assert (d.get('eps') == '0.99')
    assert (d.get('eps_surprise_direction') == 'misses')
    assert (d.get('eps_surprise_currency') is None)
    assert (d.get('eps_surprise_amount') is None)
    assert (d.get('revenue_currency') == '€')
    assert (d.get('revenue') == '3.04')
    assert (d.get('revenue_uom') == 'B')
    assert (d.get('revenue_surprise_direction') == 'beats')
    assert (d.get('revenue_surprise_currency') == '€')
    assert (d.get('revenue_surprise_amount') == '20')
    assert (d.get('revenue_surprise_uom') == 'M')
    assert (d.get('positive_guidance') is None)


def test_parse_tweet_not_earnings():
    tweet = '$AZZ declares $0.17 dividend'
    loader = LoadEarningsReportsFromTwitter(Marketcurrents(Marketcurrents.account_name))
    d = loader.parse_earnings_numbers(tweet)
    assert(not d)


def test_parse_tweet_pesos():
    tweet = '$BSMX - Banco Santander México GAAP EPS of Ps.1.21, revenue of Ps.23.64B'
    loader = LoadEarningsReportsFromTwitter(Marketcurrents(Marketcurrents.account_name))
    d = loader.parse_earnings_numbers(tweet)
    assert (d.get('eps_sign') is None)
    assert (d.get('eps_currency') == 'Ps.')
    assert (d.get('eps') == '1.21')
    assert (d.get('revenue_currency') == 'Ps.')
    assert (d.get('revenue') == '23.64')
    assert (d.get('revenue_uom') == 'B')


def test_parse_tweet_remnibi():
    tweet = '$RCON - Recon Technology GAAP EPS of RMB3.20, revenue of RMB83.8M'
    loader = LoadEarningsReportsFromTwitter(Marketcurrents(Marketcurrents.account_name))
    d = loader.parse_earnings_numbers(tweet)
    assert (d.get('eps_sign') is None)
    assert (d.get('eps_currency') == 'RMB')
    assert (d.get('eps') == '3.20')
    assert (d.get('revenue_currency') == 'RMB')
    assert (d.get('revenue') == '83.8')
    assert (d.get('revenue_uom') == 'M')


def test_parse_tweet_singaporean():
    tweet = '$MAPIF - Mapletree Industrial Trust Net income of S$130.32, revenue of S$175.51M beats by $61.37M'
    loader = LoadEarningsReportsFromTwitter(Marketcurrents(Marketcurrents.account_name))
    d = loader.parse_earnings_numbers(tweet)
    assert (d.get('eps_sign') is None)
    assert (d.get('eps_currency') is None)
    assert (d.get('eps') is None)
    assert (d.get('revenue_currency') == 'S$')
    assert (d.get('revenue') == '175.51')
    assert (d.get('revenue_uom') == 'M')


def test_parse_inline():
    tweet = '$NEWP $NUAG:CA - New Pacific Metals GAAP EPS of -$0.01 in-line'
    loader = LoadEarningsReportsFromTwitter(Marketcurrents(Marketcurrents.account_name))
    d = loader.parse_earnings_numbers(tweet)
    assert (d.get('eps_sign') == '-')
    assert (d.get('eps_currency') == '$')
    assert (d.get('eps') == '0.01')
    assert (d.get('eps_surprise_direction') == 'in-line')
    assert (d.get('eps_surprise_amount') is None)
    assert (d.get('revenue_currency') is None)
    assert (d.get('revenue') is None)
    assert (d.get('revenue_uom') is None)


def test_parse_II():
    tweet = '$NEWT - Newtek Business NII of $0.01 per share, TII of $23.6M'
    loader = LoadEarningsReportsFromTwitter(Marketcurrents(Marketcurrents.account_name))
    d = loader.parse_earnings_numbers(tweet)
    assert (d.get('eps_sign') is None)
    assert (d.get('eps_currency') == '$')
    assert (d.get('eps') == '0.01')
    assert (d.get('eps_surprise_direction') is None)
    assert (d.get('eps_surprise_amount') is None)
    assert (d.get('revenue_currency') == '$')
    assert (d.get('revenue') == '23.6')
    assert (d.get('revenue_uom') == 'M')


def test_parse_tweet_weird_euros():
    tweet = '$TRATF - Traton SE GAAP EPS of Є1.32, revenue of Є28.45B'
    loader = LoadEarningsReportsFromTwitter(Marketcurrents(Marketcurrents.account_name))
    d = loader.parse_earnings_numbers(tweet)
    assert (d.get('eps_sign') is None)
    assert (d.get('eps_currency') == 'Є')
    assert (d.get('eps') == '1.32')
    assert (d.get('revenue_currency') == 'Є')
    assert (d.get('revenue') == '28.45')
    assert (d.get('revenue_uom') == 'B')


def test_parse_tweet_livesquawk():
    tweet = '''
    $DAL Delta Airlines Q3 22 Earnings: \
      - Adj EPS $1.51 (est $1.54) \
      - Adj Revenue $12.84B (est $12.83B) \
      - Sees Q4 Adj EPS $1 To $1.25 (est $0.80) \
      - Raises Q4 EPS to $1.00
      '''
    loader = LoadEarningsReportsFromTwitter(Livesquawk(Livesquawk.account_name))
    d = loader.parse_earnings_numbers(tweet)
    assert(d.get('eps_sign') is None)
    assert(d.get('eps_currency') == '$')
    assert(d.get('eps') == '1.51')
    assert(d.get('eps_estimate_currency') == '$')
    assert(d.get('eps_estimate_amount') == '1.54')
    assert(d.get('revenue_currency') == '$')
    assert(d.get('revenue') == '12.84')
    assert(d.get('revenue_uom') == 'B')
    assert(d.get('revenue_estimate_currency') == '$')
    assert(d.get('revenue_estimate_amount') == '12.83')
    assert(d.get('revenue_estimate_uom') == 'B')


def test_parse_tweet_livesquawk_without_uom():
    tweet = '''
    $UNH UnitedHealth Q3 22 Earnings: 
- EPS $5.55 (est $5.20) 
- Revenue $46.56 (exp $45.54) 
- Sees FY EPS $ 20.85 To $21.05 (prev $20.45 To $20.95
'''
    loader = LoadEarningsReportsFromTwitter(Livesquawk(Livesquawk.account_name))
    d = loader.parse_earnings_numbers(tweet)
    assert(d.get('eps_sign') is None)
    assert(d.get('eps_currency') == '$')
    assert(d.get('eps') == '5.55')
    assert(d.get('eps_estimate_currency') == '$')
    assert(d.get('eps_estimate_amount') == '5.20')
    assert(d.get('revenue_currency') == '$')
    assert(d.get('revenue') == '46.56')
    assert(d.get('revenue_uom') is None)
    assert(d.get('revenue_estimate_currency') == '$')
    assert(d.get('revenue_estimate_amount') == '45.54')
    assert(d.get('revenue_estimate_uom') is None)


def test_parse_tweet_livesquawk_revenue_first():
    tweet = '''
    $SCHW Charles Schwab Q3 22 Earnings:  
    - Revenue: $5.5B (exp $5.41B)  
    - Adj EPS: $1.10 (exp $1.05)'''
    loader = LoadEarningsReportsFromTwitter(Livesquawk(Livesquawk.account_name))
    d = loader.parse_earnings_numbers(tweet)
    assert (d.get('eps_sign') is None)
    assert (d.get('eps_currency') == '$')
    assert (d.get('eps') == '1.10')
    assert (d.get('eps_estimate_currency') == '$')
    assert (d.get('eps_estimate_amount') == '1.05')
    assert (d.get('revenue_currency') == '$')
    assert (d.get('revenue') == '5.5')
    assert (d.get('revenue_uom') == 'B')
    assert (d.get('revenue_estimate_currency') == '$')
    assert (d.get('revenue_estimate_amount') == '5.41')
    assert (d.get('revenue_estimate_uom') == 'B')


def test_parse_tweet_livesquawk_worded_estimated():
    tweet = '''
$UAL United Airlines Q3 22 Earnings: 
- Adj EPS: $2.81 (Estimate: $2.29) 
- Passenger Revenue: $11.65B (Estimate: $11.39B) 
- Sees Q4 Adj. Op Margin To Exceed 2019'''
    loader = LoadEarningsReportsFromTwitter(Livesquawk(Livesquawk.account_name))
    d = loader.parse_earnings_numbers(tweet)
    assert (d.get('eps_sign') is None)
    assert (d.get('eps_currency') == '$')
    assert (d.get('eps') == '2.81')
    assert (d.get('eps_estimate_currency') == '$')
    assert (d.get('eps_estimate_amount') == '2.29')
    assert (d.get('revenue_currency') == '$')
    assert (d.get('revenue') == '11.65')
    assert (d.get('revenue_uom') == 'B')
    assert (d.get('revenue_estimate_currency') == '$')
    assert (d.get('revenue_estimate_amount') == '11.39')
    assert (d.get('revenue_estimate_uom') == 'B')


def test_parse_tweet_livesquawk_worded_rev():
    tweet = '''
    $BX Blackstone Inc Q3 22 Earnings:  
- Total Segment Rev. $2.59B, Est. $2.51B 
- Aum $950.9B (est $966.82B) 
- Inflows $44.8B (est $60.49B) 
- Distributable Income/SHR $1.06 (est 99c)'''
    loader = LoadEarningsReportsFromTwitter(Livesquawk(Livesquawk.account_name))
    d = loader.parse_earnings_numbers(tweet)
    assert (d.get('eps_sign') is None)
    assert (d.get('eps_currency') is None)
    assert (d.get('eps') is None)
    assert (d.get('eps_estimate_currency') is None)
    assert (d.get('eps_estimate_amount') is None)
    assert (d.get('revenue_currency') == '$')
    assert (d.get('revenue') == '2.59')
    assert (d.get('revenue_uom') == 'B')
    assert (d.get('revenue_estimate_currency') == '$')
    assert (d.get('revenue_estimate_amount') == '2.51')
    assert (d.get('revenue_estimate_uom') == 'B')
