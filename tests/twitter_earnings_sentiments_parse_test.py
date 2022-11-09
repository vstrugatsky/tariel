from loaders.earnings_reports_from_twitter import LoadEarningsReportsFromTwitter
from loaders.twitter_marketcurrents import Marketcurrents


def test_parse_false_positive():
    account = Marketcurrents(Marketcurrents.account_name)
    tweet = '$DDOG - Macro, consumer headwinds loom ahead of Datadog Q3 earnings'
    assert (account.parse_earnings_false_positive(tweet).groupdict())
    tweet = '$DDOG $REX Hot Stocks: afternoon update'
    assert (account.parse_earnings_false_positive(tweet).groupdict())
    tweet = '$DDOG Q2 Earnings Preview'
    assert (account.parse_earnings_false_positive(tweet).groupdict())
    tweet = '$DDOG Can Datadog show good Q3 results?'
    assert (account.parse_earnings_false_positive(tweet).groupdict())
    tweet = '$SPG - Simon Property likely to beat Q3 consensus amid winning streak for retail REITs'
    assert (account.parse_earnings_false_positive(tweet).groupdict())
    tweet = '$MAIN - Main Street Capital likely to go up after Q3 results on revenue beat, stronger capital position https://t.co/Cw7DgOo1Yv'
    assert (not account.parse_earnings_false_positive(tweet))

    tweet = '$MF - Missfresh regains compliance with Nasdaq minimum bid price requirement'
    assert (not account.parse_negative_earnings(tweet))


def test_parse_earnings_indicator():
    account = Marketcurrents(Marketcurrents.account_name)

    tweet = '$REAL - The RealReal offers mixed Q3 report, below consensus sales guide'
    assert(account.parse_earnings_indicator(tweet).groupdict()['earnings_indicator'].strip() == 'Q3 report')

    tweet = '$LMND - Lemonade Q4 guidance trails consensus; Q3 net loss ratio swells'
    assert(account.parse_earnings_indicator(tweet).groupdict()['earnings_indicator'].strip() == 'Q3 net loss')

    tweet = '$PEI - PREIT posts Q3 FFO loss, focuses on raising capital, paying down debt'
    assert(account.parse_earnings_indicator(tweet).groupdict()['earnings_indicator'].strip() == 'posts Q3')

    tweet = '$LTC - LTC Properties Q3 results mixed on rental income growth, higher expenses'
    assert(account.parse_earnings_indicator(tweet).groupdict()['earnings_indicator'].strip() == 'Q3 result')

    tweet = '$THS - TreeHouse Foods slides after margins disappoint despite higher pricing'
    assert(account.parse_earnings_indicator(tweet).groupdict()['earnings_indicator'].strip() == 'after margins')

    tweet = '$APRN - Blue Apron slides to all-time low after another unprofitable quarter, pulled guidance'
    assert(account.parse_earnings_indicator(tweet).groupdict()['earnings_indicator'].strip() == 'after another unprofitable')

    tweet = '$NEWT - Newtek Business Q3 adjusted NII climbs from a year ago, but falls short of consensus'
    assert(account.parse_earnings_indicator(tweet).groupdict()['earnings_indicator'].strip() == 'Q3 adjusted NII')

    tweet = '$CGJTF $CJT:CA - Cargojet posts stronger than expected profits, touts on-time performance'
    assert(account.parse_earnings_indicator(tweet).groupdict()['earnings_indicator'].strip() == 'posts stronger than expected profits')

    tweet = '$BRK.A $BRK.B - Berkshire Hathaway Q3 operating earnings slip by 20% Y/Y'
    assert(account.parse_earnings_indicator(tweet).groupdict()['earnings_indicator'].strip() == 'Q3 operating earnings')

    tweet = '$KPTI - Karyopharm surges as blood cancer drug drives sales in Q3, net loss narrows'
    assert(account.parse_earnings_indicator(tweet).groupdict()['earnings_indicator'].strip() == 'sales in Q3')

    tweet = '$FRG - Franchise Group plummets 14% after missing Q3 bottom line'
    assert (account.parse_earnings_indicator(tweet).groupdict()['earnings_indicator'].strip() == 'after missing Q3')

    tweet = '$NWL - Newell Brands gains after topping some beaten-down estimates'
    assert(account.parse_earnings_indicator(tweet).groupdict()['earnings_indicator'].strip() == 'topping some beaten-down estimates')


def test_parse_combos():
    account = Marketcurrents(Marketcurrents.account_name)
    tweet = '$EPR - EPR Properties stock jumps on higher year guidance, solid Q3 beat'
    assert (account.parse_earnings_indicator(tweet).groupdict()['earnings_indicator'])
    assert(account.parse_positive_guidance(tweet)[0] == 'higher year guidance')
    assert(account.parse_positive_earnings(tweet)[0] == 'Q3 beat')

    tweet = '$SXC - SunCoke Energy surges on strong Q3 results, EBITDA guidance'
    assert(account.parse_positive_guidance(tweet)[0] == 'strong Q3 results, EBITDA guidance')
    assert(account.parse_positive_earnings(tweet)[0] == 'strong Q3 results')

    tweet = '$OLED - Universal Display stock soars 15% on earnings beat despite weak near-term OLED demand'
    assert(account.parse_negative_earnings(tweet)[0] == 'weak')
    assert(account.parse_positive_earnings(tweet)[0] == 'earnings beat')

    tweet = '$MCHP - Microchip stock gain on FQ2 earnings beat and guiding outlook above consensus https://t.co/4QT91aHWIG'
    assert (account.parse_earnings_indicator(tweet).groupdict()['earnings_indicator'])
    assert(account.parse_positive_guidance(tweet)[0] == 'guiding outlook above')
    assert(account.parse_positive_earnings(tweet)[0] == 'earnings beat')

    tweet = '$CVS - CVS Health gains after guidance raise even as opioid charges trigger Q3 loss'
    assert (account.parse_earnings_indicator(tweet).groupdict()['earnings_indicator'])
    assert(account.parse_positive_guidance(tweet)[0] == 'guidance raise')
    assert(account.parse_negative_earnings(tweet)[0] == 'Q3 loss')

    tweet = '$MYGN - Myriad Genetics falls 19% after lowering full-year guidance, Q3 misses'
    assert (account.parse_earnings_indicator(tweet).groupdict()['earnings_indicator'])
    assert(account.parse_negative_guidance(tweet)[0] == 'lowering full-year guidance')
    assert(account.parse_negative_earnings(tweet)[0] == 'Q3 miss')

    tweet = '$LAZ - Lazard Q3 earnings beat as Financial Advisory strengthens, while AUM slump'
    assert (account.parse_earnings_indicator(tweet).groupdict()['earnings_indicator'])
    assert(account.parse_positive_earnings(tweet)[0] == 'earnings beat')
    assert(account.parse_positive_earnings(tweet)[1] == 'strength')
    assert(account.parse_negative_earnings(tweet)[0] == 'AUM slump')
    assert(not account.parse_positive_guidance(tweet))

    tweet = '$GBX - Greenbrier stock soars on big earnings beat, bullish forecast'
    assert (account.parse_earnings_indicator(tweet).groupdict()['earnings_indicator'])
    assert(account.parse_positive_earnings(tweet)[0] == 'earnings beat')
    assert(account.parse_positive_guidance(tweet)[0] == 'bullish forecast')

    tweet = '$BUD - Anheuser-Busch InBev shares gain sharply on Q3 profit beat, outlook boost https://t.co/gQm5oJEp1U'
    assert (account.parse_earnings_indicator(tweet).groupdict()['earnings_indicator'])
    assert(account.parse_positive_earnings(tweet)[0] == 'profit beat')
    assert(account.parse_positive_guidance(tweet)[0] == 'outlook boost')

    tweet = '$HUM - Humana trades higher on Q3 earnings beat, affirms FY22 outlook'
    assert (account.parse_earnings_indicator(tweet).groupdict()['earnings_indicator'])
    assert(account.parse_positive_earnings(tweet)[0] == 'earnings beat')
    assert(not account.parse_positive_guidance(tweet))

    tweet = '$MET - MetLife Q3 earnings beat as volume growth, higher rates offset lower PE returns'
    assert (account.parse_earnings_indicator(tweet).groupdict()['earnings_indicator'])
    assert(account.parse_positive_earnings(tweet)[0] == 'earnings beat')
    assert(account.parse_positive_earnings(tweet)[1] == 'volume grow')
    assert(account.parse_negative_earnings(tweet)[0] == 'lower PE return')

    tweet = '$VSTO - Vista Outdoor FQ2 2023 results beat estimates, co cuts FY sales, adj. EPS guidance'
    assert(account.parse_earnings_indicator(tweet).groupdict()['earnings_indicator'])
    assert(account.parse_positive_earnings(tweet)[0] == 'results beat')
    assert(account.parse_negative_guidance(tweet)[0] == 'cuts FY sales, adj. EPS guidance')

    tweet = '$OMCL - Omnicell stock crashes 32% as FY22 outlook slashed, Q3 sees headwinds'
    assert (account.parse_earnings_indicator(tweet).groupdict()['earnings_indicator'])
    assert (account.parse_negative_earnings(tweet)[0] == 'headwind')
    assert (account.parse_negative_guidance(tweet)[0] == 'outlook slashed')

    tweet = 'Donnelley Financial down ~17% on Q3 miss, lower-than-consensus Q4 guidance'
    assert (account.parse_earnings_indicator(tweet).groupdict()['earnings_indicator'])
    assert (account.parse_negative_earnings(tweet)[0] == 'Q3 miss')
    assert (account.parse_negative_guidance(tweet)[0] == 'lower-than-consensus Q4 guidance')

    tweet = '$SKT - Tanger Factory Outlet boosts guidance after Q3 FFO beats on higher occupancy, NOI'
    assert (account.parse_earnings_indicator(tweet).groupdict()['earnings_indicator'])
    assert (account.parse_positive_earnings(tweet)[0] == 'Q3 FFO beat')
    assert (account.parse_positive_guidance(tweet)[0] == 'boosts guidance')


def test_parse_positive_guidance():
    account = Marketcurrents(Marketcurrents.account_name)
    tweet = '$DTM - DT Midstream reports Q3 earnings; raises FY22 and FY23 Adjusted EBITDA guidance'
    assert (account.parse_earnings_indicator(tweet).groupdict()['earnings_indicator'])
    assert(account.parse_positive_guidance(tweet)[0] == 'raises FY22 and FY23 Adjusted EBITDA guidance')

    tweet = '$FPRUF $FPRUY - Fraport AG reports Q3 results; expects to achieve upper range of full-year outlook'
    assert(account.parse_positive_guidance(tweet)[0] == 'upper range of full-year outlook')

    tweet = "$KSS - Kohl’s shares gain as Q3 earnings guided to be well above consensus, CEO quits"
    assert(account.parse_positive_guidance(tweet)[0] == 'guided to be well above')

    tweet = '$WMB - Williams sees full-year EBITDA near high end of guidance after strong Q3 https://t.co/1K0FkavqfR'
    assert(account.parse_positive_guidance(tweet)[0] == 'high end of guidance')

    tweet = '$TGLS - Tecnoglass beats top and bottom line, increases FY outlook'
    assert (account.parse_earnings_indicator(tweet).groupdict()['earnings_indicator'])
    assert(account.parse_positive_guidance(tweet)[0] == 'increases FY outlook')

    tweet = '$CVEO - CVEO GAAP EPS of $0.32 misses by $0.02, revenue of $184.2M beats by $10.39M, raises FY guidance'
    assert (account.parse_earnings_indicator(tweet).groupdict()['earnings_indicator'])
    assert(account.parse_positive_guidance(tweet)[0] == 'raises FY guidance')

    tweet = '$KIM - Kimco Realty FFO of $0.41 beats by $0.02, revenue of $433.4M beats by $15.98M, raises FY FFO guidance'
    assert (account.parse_earnings_indicator(tweet).groupdict()['earnings_indicator'])
    assert(account.parse_positive_guidance(tweet)[0] == 'raises FY FFO guidance')

    tweet = '$FISV - Fiserv Non-GAAP EPS of $1.63 misses by $0.06, revenue of $4.52B beats by $210M, raises FY earning guidance'
    assert (account.parse_earnings_indicator(tweet).groupdict()['earnings_indicator'])
    assert(account.parse_positive_guidance(tweet)[0] == 'raises FY earning guidance')

    tweet = '$OPCH - Option Care Health GAAP EPS of $0.20 in-line, revenue of $1.02B beats by $23.72M, raised FY22 guidance'
    assert (account.parse_earnings_indicator(tweet).groupdict()['earnings_indicator'])
    assert(account.parse_positive_guidance(tweet)[0] == 'raised FY22 guidance')

    tweet = '$LIN - Linde Non-GAAP EPS of $3.10 beats by $0.17, revenue of $8.79B beats by $470M, raises FY Adj. EPS guidance'
    assert (account.parse_earnings_indicator(tweet).groupdict()['earnings_indicator'])
    assert(account.parse_positive_guidance(tweet)[0] == 'raises FY Adj. EPS guidance')

    tweet = '$HRI - Herc GAAP EPS of $3.36 misses by $0.28, revenue of $745.1M beats by $20.99M; raises FY adj. EBITDA guidance'
    assert (account.parse_earnings_indicator(tweet).groupdict()['earnings_indicator'])
    assert(account.parse_positive_guidance(tweet)[0] == 'raises FY adj. EBITDA guidance')

    tweet = '$INFY - Infosys GAAP EPS of $0.18 in-line, revenue of $4.55B beats by $110M, revises FY guidance'
    assert (account.parse_earnings_indicator(tweet).groupdict()['earnings_indicator'])
    assert(not account.parse_positive_guidance(tweet))
    assert(not account.parse_negative_guidance(tweet))

    tweet = '$COHU - Cohu rallies 15% on Q3 estimates beat, provides Q4 guidance'
    assert (account.parse_earnings_indicator(tweet).groupdict()['earnings_indicator'])
    assert(not account.parse_positive_guidance(tweet))
    assert(not account.parse_negative_guidance(tweet))

    tweet = '$GTLS - Chart Industries reports mixed Q3 earnings; narrows FY22 and issues FY23 guidance'
    assert (account.parse_earnings_indicator(tweet).groupdict()['earnings_indicator'])
    assert(not account.parse_positive_guidance(tweet))
    assert(not account.parse_negative_guidance(tweet))

    tweet = '$CL - Colgate-Palmolive reports mixed Q3 result, raises sales forecasts'  # earnings + => mixed but raises, earnings tweet mixed
    assert (account.parse_earnings_indicator(tweet).groupdict()['earnings_indicator'])
    assert(account.parse_positive_guidance(tweet)[0] == 'raises sales forecast')
    assert(not account.parse_negative_guidance(tweet))

    tweet = '$GTLS - Chart Industries reports mixed Q3 earnings; narrows FY22 and issues FY23 guidance'  # earnings, mixed, no tweet
    assert (account.parse_earnings_indicator(tweet).groupdict()['earnings_indicator'])
    assert(not account.parse_positive_earnings(tweet))
    assert(not account.parse_negative_earnings(tweet))
    assert(not account.parse_positive_guidance(tweet))
    assert(not account.parse_negative_guidance(tweet))


def test_parse_negative_guidance():
    account = Marketcurrents(Marketcurrents.account_name)

    tweet = '$REAL - The RealReal offers mixed Q3 report, below consensus sales guide'
    assert(account.parse_negative_guidance(tweet)[0] == 'below consensus sales guide')

    tweet = '$SOPH - SOPHiA Genetics reports Q3 earnings; FY22 revenue to be at the low-end of guidance'
    assert(account.parse_negative_guidance(tweet)[0] == 'low-end of guidance')

    tweet = '$STM - STMicroelectronics drops 7% on guiding Q4 revenue below consensus https://t.co/XAQZTeeNY5'
    assert (account.parse_earnings_indicator(tweet).groupdict()['earnings_indicator'])
    assert(not account.parse_negative_earnings(tweet))
    assert(account.parse_negative_guidance(tweet)[0] == 'guiding Q4 revenue below')

    tweet = '$APRN - Blue Apron slides to all-time low after another unprofitable quarter, pulled guidance'
    assert(account.parse_negative_guidance(tweet)[0] == 'pulled guidance')

    tweet = '$PRLB - Proto Labs stock sinks 24% to decade-low as guidance widely misses estimates'
    assert (account.parse_earnings_indicator(tweet).groupdict()['earnings_indicator'])
    assert(not account.parse_negative_earnings(tweet))
    assert(account.parse_negative_guidance(tweet)[0] == 'guidance widely misses')

    tweet = '$MTUAF - MTU Aero Engines AG GAAP EPS of €1.74, revenue of €1.35B, FY22 guidance lowered'
    assert (account.parse_earnings_indicator(tweet).groupdict()['earnings_indicator'])
    assert(account.parse_negative_guidance(tweet)[0] == 'guidance lowered')

    tweet = '$LHX - L3Harris plunges after Q3 miss, full-year guidance cut'
    assert (account.parse_earnings_indicator(tweet).groupdict()['earnings_indicator'])
    assert(account.parse_negative_guidance(tweet)[0] == 'guidance cut')

    tweet = '$TNC - Tennant Non-GAAP EPS of $0.99 misses by $0.11, revenue of $262.9M misses by $24.27M, lowers FY earning guidance'
    assert (account.parse_earnings_indicator(tweet).groupdict()['earnings_indicator'])
    assert(account.parse_negative_guidance(tweet)[0] == 'lowers FY earning guidance')

    tweet = '$STX - Seagate Technology Non-GAAP EPS of $0.48 misses by $0.23, revenue of $2.04B misses by $70M, issues Q2 guidance below the consensus'
    assert (account.parse_earnings_indicator(tweet).groupdict()['earnings_indicator'])
    assert(account.parse_negative_guidance(tweet)[0] == 'guidance below')

    tweet = '$TXN - Texas Instruments GAAP EPS of $2.47 beats by $0.08, revenue of $5.24B beats by $100M, guides below Q4 consensus'
    assert (account.parse_earnings_indicator(tweet).groupdict()['earnings_indicator'])
    assert(account.parse_negative_guidance(tweet)[0] == 'guides below')


def test_parse_positive_sentiment():
    account = Marketcurrents(Marketcurrents.account_name)
    tweet = '$NOV - Oilwell equipment and tech provider NOV posts mixed Q3'
    assert (account.parse_earnings_indicator(tweet).groupdict()['earnings_indicator'])
    assert(not account.parse_positive_earnings(tweet))
    assert(not account.parse_negative_earnings(tweet))

    tweet = '$VNO - Vornado Realty Q3 revenue exceeds consensus, helped by same store NOI growth'
    assert(account.parse_positive_earnings(tweet)[0] == 'exceeds consensus')

    tweet = '$CBOE - Cboe Global sees higher organic growth, less expenses in 2022 after Q3 beat'
    assert(account.parse_positive_earnings(tweet)[0] == 'higher organic growth')
    assert(account.parse_positive_earnings(tweet)[1] == 'less expenses')
    assert(account.parse_positive_earnings(tweet)[2] == 'Q3 beat')

    tweet = '$APO - Apollo Global Q3 earnings gain as inflows hold up, AUM rises'
    assert (account.parse_earnings_indicator(tweet).groupdict()['earnings_indicator'])
    assert(account.parse_positive_earnings(tweet)[0] == 'earnings gain')
    assert(account.parse_positive_earnings(tweet)[1] == 'AUM rise')

    tweet = '$ARCB - ArcBest reports Q3 earnings beat; on track to deliver record annual revenues in 2022 https://t.co/8OXQGp9zil'
    assert (account.parse_earnings_indicator(tweet).groupdict()['earnings_indicator'])
    assert(account.parse_positive_earnings(tweet)[0] == 'earnings beat')
    assert(account.parse_positive_earnings(tweet)[1] == 'record annual revenue')

    tweet = '$ANET - Arista Networks posts record revenue, Q3 beat https://t.co/eTWui9mTEB'
    assert (account.parse_earnings_indicator(tweet).groupdict()['earnings_indicator'])
    assert(account.parse_positive_earnings(tweet)[0] == 'record revenue')
    assert(account.parse_positive_earnings(tweet)[1] == 'Q3 beat')

    tweet = '$IIPR - Innovative Industrial Properties Q3 revenue gains helped by acquisitions'
    assert (account.parse_earnings_indicator(tweet).groupdict()['earnings_indicator'])
    assert(account.parse_positive_earnings(tweet)[0] == 'revenue gain')

    tweet = '$TT - Booking surge in Americas aids Trane Technologies crush results estimates'
    assert (account.parse_earnings_indicator(tweet).groupdict()['earnings_indicator'])
    assert(account.parse_positive_earnings(tweet)[0] == 'Booking surge')
    assert(account.parse_positive_earnings(tweet)[1] == 'crush')
    assert(not account.parse_negative_earnings(tweet))

    tweet = '$AFRAF - Air France-KLM savors recovering air travel which boosts Q3 revenue'
    assert (account.parse_earnings_indicator(tweet).groupdict()['earnings_indicator'])
    assert(account.parse_positive_earnings(tweet)[0] == 'boosts Q3 revenue')
    assert(not account.parse_negative_earnings(tweet))

    tweet = '$IMO $IMO:CA - Imperial Oil results surpass estimates as downstream strength continues'  # + surpass, strength
    assert (account.parse_earnings_indicator(tweet).groupdict()['earnings_indicator'])
    assert(account.parse_positive_earnings(tweet)[0] == 'results surpass')
    assert(account.parse_positive_earnings(tweet)[1] == 'strength')
    assert(not account.parse_negative_earnings(tweet))

    tweet = '$SLCA - Strong pricing and growth support U.S. Silica Q3 beat.'  # + beat, strong # earnings
    assert (account.parse_earnings_indicator(tweet).groupdict()['earnings_indicator'])
    assert(account.parse_positive_earnings(tweet)[0].lower() == 'strong pricing')
    assert(account.parse_positive_earnings(tweet)[1] == 'Q3 beat')
    assert(not account.parse_negative_earnings(tweet))

    tweet = '$PFG - Principal Financial Group up on Q3 EPS beat'  # + beat # earnings, earnings tweet previous day no surprises
    assert (account.parse_earnings_indicator(tweet).groupdict()['earnings_indicator'])
    assert(account.parse_positive_earnings(tweet)[0] == 'Q3 EPS beat')
    assert(not account.parse_negative_earnings(tweet))

    tweet = '$DXCM - DexCom hits six-month high after Q3 beat'  # beat #earnings - no earning tweet
    assert (account.parse_earnings_indicator(tweet).groupdict()['earnings_indicator'])
    assert(account.parse_positive_earnings(tweet)[0] == 'Q3 beat')
    assert(not account.parse_negative_earnings(tweet))

    tweet = '$JKS - JinkoSolar sinks 5% despite beating Q3 consensus'  # mixed - sinks and beating
    assert (account.parse_earnings_indicator(tweet).groupdict()['earnings_indicator'])
    assert(account.parse_positive_earnings(tweet)[0] == 'beat')
    assert(not account.parse_negative_earnings(tweet))

    tweet = '$TEX - Terex raised FY2022 EPS outlook range after 79% growth in Q3 and strong margins'  # Q3=earnings, raised, strong margins
    assert (account.parse_earnings_indicator(tweet).groupdict()['earnings_indicator'])
    assert(account.parse_positive_earnings(tweet)[0] == 'strong margin')
    assert(account.parse_positive_guidance(tweet)[0] == 'raised FY2022 EPS outlook')
    assert(not account.parse_negative_earnings(tweet))

    tweet = '$RWT - Redwood Trust stock trades higher amid Q3 earnings gain'  # earnings +, gain
    assert (account.parse_earnings_indicator(tweet).groupdict()['earnings_indicator'])
    assert (account.parse_positive_earnings(tweet)[0] == 'earnings gain')
    assert (not account.parse_negative_earnings(tweet))

    tweet = '$KNSL - Kinsale stock rises 12% on Q3 beat as revenue soars 32%'  # earnings + soars
    assert (account.parse_earnings_indicator(tweet).groupdict()['earnings_indicator'])
    assert (account.parse_positive_earnings(tweet)[0] == 'Q3 beat')
    assert (account.parse_positive_earnings(tweet)[1] == 'revenue soar')
    assert (not account.parse_negative_earnings(tweet))

    tweet = '$COHU - Cohu rallies 15% on Q3 estimates beat, provides Q4 guidance'  # earnings + Q3 estimates beat - matches earnings the day before
    assert (account.parse_earnings_indicator(tweet).groupdict()['earnings_indicator'])
    assert (account.parse_positive_earnings(tweet)[0] == 'estimates beat')
    assert (not account.parse_negative_earnings(tweet))

    tweet = '$NEE $NEP - NextEra Energy posts Q3 beat; buys $1.1B landfill gas-to-electric portfolio'  # earnings +, repeats tweet
    assert (account.parse_earnings_indicator(tweet).groupdict()['earnings_indicator'])
    assert (account.parse_positive_earnings(tweet)[0] == 'Q3 beat')
    assert (not account.parse_negative_earnings(tweet))

    tweet = '$AON - Aon Q3 earnings beat as expenses plummet, free cash flow jump'  # earnings + although earnings tweet mixed
    assert (account.parse_earnings_indicator(tweet).groupdict()['earnings_indicator'])
    assert (account.parse_positive_earnings(tweet)[0] == 'earnings beat')
    assert (account.parse_positive_earnings(tweet)[1] == 'expenses plummet')
    assert (account.parse_positive_earnings(tweet)[2] == 'cash flow jump')
    assert (not account.parse_negative_earnings(tweet))

    tweet = '$SMP - Standard Motor Products reports Q3 earnings beat; updates FY22 guidance'  # reports beat => earnings +, no tweet
    assert (account.parse_earnings_indicator(tweet).groupdict()['earnings_indicator'])
    assert (account.parse_positive_earnings(tweet)[0] == 'earnings beat')
    assert (not account.parse_negative_earnings(tweet))

    tweet = '$NWL - Newell Brands gains after topping some beaten-down estimates'  # topping -> earnings, uvaga: beaten-down <> beat
    assert (account.parse_earnings_indicator(tweet).groupdict()['earnings_indicator'])
    assert (account.parse_positive_earnings(tweet)[0] == 'topping some beaten-down estimate')
    assert (not account.parse_negative_earnings(tweet))

    tweet = '$RNGR - Ranger Energy Services reports Q3 earnings beat; reaffirms FY22 capex guidance'  # + earnings, no tweet
    assert (account.parse_earnings_indicator(tweet).groupdict()['earnings_indicator'])
    assert (account.parse_positive_earnings(tweet)[0] == 'earnings beat')
    assert (not account.parse_positive_guidance(tweet))
    assert (not account.parse_negative_guidance(tweet))
    assert (not account.parse_negative_earnings(tweet))

    tweet = '$ABBV - AbbVie Non-GAAP EPS of $3.66 beats by $0.10, revenue of $14.81B misses by $130M, raises dividend by 5%'
    assert (account.parse_earnings_indicator(tweet).groupdict()['earnings_indicator'])
    assert (account.parse_positive_earnings(tweet)[0] == 'beat')
    assert (not account.parse_negative_earnings(tweet))
    assert (not account.parse_positive_guidance(tweet))
    assert (not account.parse_negative_guidance(tweet))

    tweet = '$CHD - Church &amp; Dwight tops estimates, points to strong consumption trends'  # tops => earnings +, no tweet
    assert (account.parse_earnings_indicator(tweet).groupdict()['earnings_indicator'])
    assert (account.parse_positive_earnings(tweet)[0] == 'tops estimate')
    assert (account.parse_positive_earnings(tweet)[1] == 'strong consumption')
    assert (not account.parse_negative_earnings(tweet))

    tweet = '$SLCA - U.S. Silica Holdings reports Q3 earnings beat; updates FY22 guidance'  # earnings +, no tweet
    assert (account.parse_earnings_indicator(tweet).groupdict()['earnings_indicator'])
    assert (account.parse_positive_earnings(tweet)[0] == 'earnings beat')
    assert (not account.parse_positive_guidance(tweet))
    assert (not account.parse_negative_guidance(tweet))

    tweet = '$SNY $REGN - Sanofi Q3 sales boosted by Dupixent, Vaccines business; raises FY22 outlook again'  # miss this because of:
    assert (account.parse_earnings_indicator(tweet).groupdict()['earnings_indicator'])
    assert (account.parse_positive_earnings(tweet)[0] == 'sales boost')
    assert (account.parse_positive_guidance(tweet)[0] == 'raises FY22 outlook')

    tweet = '$SNY - Sanofi reports Q3 earnings beat; raises FY22 EPS guidance'  # Q3 earnings beat
    assert (account.parse_earnings_indicator(tweet).groupdict()['earnings_indicator'])
    assert (account.parse_positive_earnings(tweet)[0] == 'earnings beat')
    assert (account.parse_positive_guidance(tweet)[0] == 'raises FY22 EPS guidance')

    tweet = '$HIG - Hartford Financial Q3 earnings beat, helped by Commercial Lines, Group Benefits'  # earnings => repeats
    assert (account.parse_earnings_indicator(tweet).groupdict()['earnings_indicator'])
    assert (account.parse_positive_earnings(tweet)[0] == 'earnings beat')
    assert (len(account.parse_positive_earnings(tweet)) == 1)
    assert (not account.parse_positive_guidance(tweet))

    tweet = '$JAKK - JAKKS Pacific stock jumps 17% after the bell as strong demand drives earnings beat'  # repeats but 17% and reinforces
    assert (account.parse_earnings_indicator(tweet).groupdict()['earnings_indicator'])
    assert (account.parse_positive_earnings(tweet)[0] == 'strong demand')
    assert (account.parse_positive_earnings(tweet)[1] == 'earnings beat')
    assert (len(account.parse_positive_earnings(tweet)) == 2)
    assert (not account.parse_positive_guidance(tweet))

    tweet = '$ALK $SKYW $DAL - SkyWest stock flies higher as quarterly profits surpass expectations'  # beat, no tweet, but 3 tickers ???
    assert (account.parse_earnings_indicator(tweet).groupdict()['earnings_indicator'])
    assert (account.parse_positive_earnings(tweet)[0] == 'profits surpass')
    assert (len(account.parse_positive_earnings(tweet)) == 1)
    assert (not account.parse_positive_guidance(tweet))

    tweet = '$CWST - Waste recycler Casella posts Q3 beat and raises forecast, shares spike'  # earnings => beat, raises, spike +3 earnings also positive
    assert (account.parse_earnings_indicator(tweet).groupdict()['earnings_indicator'])
    assert (account.parse_positive_earnings(tweet)[0] == 'Q3 beat')
    assert (len(account.parse_positive_earnings(tweet)) == 1)
    assert (account.parse_positive_guidance(tweet)[0] == 'raises forecast')

    tweet = '$LADR - Ladder Capital stock gains after Q3 results exceed analyst expectations'  # earnings + on exceed expectations but tweet has no surprises
    assert (account.parse_earnings_indicator(tweet).groupdict()['earnings_indicator'])
    assert (account.parse_positive_earnings(tweet)[0] == 'results exceed')
    assert (len(account.parse_positive_earnings(tweet)) == 1)
    assert (not account.parse_positive_guidance(tweet))

    tweet = '$GILD - Gilead Sciences raises full-year 2022 outlook following Q3 beats'  # earnings, + raises but repeats earnings
    assert (account.parse_earnings_indicator(tweet).groupdict()['earnings_indicator'])
    assert (account.parse_positive_earnings(tweet)[0] == 'Q3 beat')
    assert (len(account.parse_positive_earnings(tweet)) == 1)
    assert (account.parse_positive_guidance(tweet)[0] == 'raises full-year 2022 outlook')

    tweet = '$AAPL - Apple results top forecasts as iPhone, services lead strong quarterly sales'
    assert (account.parse_earnings_indicator(tweet).groupdict()['earnings_indicator'])
    assert (account.parse_positive_earnings(tweet)[0] == 'results top')
    assert (account.parse_positive_earnings(tweet)[1] == 'strong')
    assert (len(account.parse_positive_earnings(tweet)) == 2)


def test_parse_negative_sentiment():
    account = Marketcurrents(Marketcurrents.account_name)

    tweet = "$MARA - Marathon Digital Q3 net loss nearly triples Y/Y, earnings and revenue miss"
    assert(account.parse_negative_earnings(tweet)[0] == 'Q3 net loss')
    assert(account.parse_negative_earnings(tweet)[1] == 'revenue miss')

    tweet = '$FNMA - Fannie Mae Q3 earnings slide as lower home prices lead to higher credit expense'
    assert(account.parse_negative_earnings(tweet)[0] == 'earnings slide')
    assert(account.parse_negative_earnings(tweet)[1] == 'higher credit expense')

    tweet = '$OESX - Orion Energy Systems reports FQ2 missed earnings; reaffirms 2H and updates FY23 guidance'
    assert(account.parse_negative_earnings(tweet)[0] == 'missed earnings')

    tweet = '$PEI - PREIT posts Q3 FFO loss, focuses on raising capital, paying down debt'
    assert(account.parse_negative_earnings(tweet)[0] == 'FFO loss')

    tweet = '$RCM - R1 RCM slumps 39% on dismal Q3 result, CEO change'
    assert(account.parse_negative_earnings(tweet)[0] == 'dismal Q3 result')

    tweet = '$USNZY $USNZ - High costs, low volumes weigh on miner Usiminas Q3 results'  # earnings -, high cost, low volumes
    assert (account.parse_earnings_indicator(tweet).groupdict()['earnings_indicator'])
    assert(account.parse_negative_earnings(tweet)[0].lower() == 'high costs')
    assert(account.parse_negative_earnings(tweet)[1] == 'low volume')
    assert(not account.parse_positive_earnings(tweet))

    tweet = '$ARLP - Alliance Resources tumbles after coal producer misses results consensus'
    assert(account.parse_negative_earnings(tweet)[0].lower() == 'misses result')

    tweet = '$BRK.A $BRK.B - Berkshire Hathaway Q3 operating earnings slip by 20% Y/Y'
    assert(account.parse_negative_earnings(tweet)[0].lower() == 'earnings slip')

    tweet = '$MITT - AG Mortgage Investment Q3 earnings reflect weaker book value, NII as macro woes bite'
    assert (account.parse_earnings_indicator(tweet).groupdict()['earnings_indicator'])
    assert(account.parse_negative_earnings(tweet)[0].lower() == 'weaker book value')
    assert(len(account.parse_negative_earnings(tweet)) == 1)

    tweet = '$TRUP - Trupanion trades at about 2-and-1/2-year low as Q3 EPS misses on disappointing margins'
    assert (account.parse_earnings_indicator(tweet).groupdict()['earnings_indicator'])
    assert(account.parse_negative_earnings(tweet)[0] == 'EPS miss')
    assert(account.parse_negative_earnings(tweet)[1] == 'disappointing margin')
    assert(not account.parse_positive_earnings(tweet))

    tweet = '$SEM - Select Medical sinks ~21% after rise in costs and expenses leads to big Q3 profit miss'
    assert (account.parse_earnings_indicator(tweet).groupdict()['earnings_indicator'])
    assert (account.parse_negative_earnings(tweet)[0] == 'rise in costs')
    assert(account.parse_negative_earnings(tweet)[1] == 'profit miss')
    assert(not account.parse_positive_earnings(tweet))

    tweet = '$BIGC - BigCommerce stock plunges 26% after lower margins widened losses in third quarter'
    assert (account.parse_earnings_indicator(tweet).groupdict()['earnings_indicator'])
    assert(account.parse_negative_earnings(tweet)[0] == 'lower margin')
    assert(not account.parse_positive_earnings(tweet))

    tweet = '$FRG - Franchise Group plummets 14% after missing Q3 bottom line'
    assert (account.parse_negative_earnings(tweet)[0] == 'missing Q3 bottom line')

    tweet = '$DBRG - DigitalBridge stock dips as Q3 property, interest expenses climb'
    assert (account.parse_earnings_indicator(tweet).groupdict()['earnings_indicator'])
    assert(account.parse_negative_earnings(tweet)[0] == 'expenses climb')
    assert(not account.parse_positive_earnings(tweet))

    tweet = '$CRTO - Criteo slides after lower profit margins, revenue miss'  # miss=earnings, slides, lower earnings tweet mixed
    assert (account.parse_earnings_indicator(tweet).groupdict()['earnings_indicator'])
    assert(account.parse_negative_earnings(tweet)[0].lower() == 'lower profit')
    assert(account.parse_negative_earnings(tweet)[1] == 'revenue miss')
    assert(not account.parse_positive_earnings(tweet))

    tweet = '$AWRE - Aware stock slides over 8% as macro headwinds, delayed orders weigh on results'  # results=earnings, - headwinds, weigh
    assert (account.parse_earnings_indicator(tweet).groupdict()['earnings_indicator'])
    assert(account.parse_negative_earnings(tweet)[0].lower() == 'headwind')
    assert(account.parse_negative_earnings(tweet)[1] == 'delay')
    assert(not account.parse_positive_earnings(tweet))

    tweet = '$TECK $TECK.B:CA - Teck Resources tumbles as Q3 loss, cost overruns spark analyst downgrades'  # results = Q3 loss, - overrun
    assert (account.parse_earnings_indicator(tweet).groupdict()['earnings_indicator'])
    assert(account.parse_negative_earnings(tweet)[0] == 'Q3 loss')
    assert(account.parse_negative_earnings(tweet)[1] == 'cost overrun')
    assert(not account.parse_positive_earnings(tweet))

    tweet = '$LMAT - LeMaitre stock slumps 16% amid Q3 miss, slashed outlook'  # earnings - Q3 miss, slashed outlook, earnings tweet mixed
    assert (account.parse_earnings_indicator(tweet).groupdict()['earnings_indicator'])
    assert(account.parse_negative_earnings(tweet)[0] == 'Q3 miss')
    assert(account.parse_negative_guidance(tweet)[0] == 'slashed outlook')
    assert(not account.parse_positive_earnings(tweet))

    tweet = '$AB - AllianceBernstein Q3 earnings declined as asset values dropped, outflows rose'  # earnings -, no tweet
    assert (account.parse_earnings_indicator(tweet).groupdict()['earnings_indicator'])
    assert(account.parse_negative_earnings(tweet)[0] == 'earnings declined')
    assert(account.parse_negative_earnings(tweet)[1] == 'asset values dropped')
    assert(account.parse_negative_earnings(tweet)[2] == 'outflows rose')
    assert(not account.parse_positive_earnings(tweet))

    tweet = '$B - Barnes Group Q3 profit matches analyst estimates while revenue slips on forex'  # Q3 = earnings, slips -, matches =
    assert (account.parse_earnings_indicator(tweet).groupdict()['earnings_indicator'])
    assert(not account.parse_positive_earnings(tweet))
    assert(account.parse_negative_earnings(tweet)[0] == 'revenue slip')

    tweet = '$SJW - SJW reports Q3 earnings miss; reaffirms FY22 guidance'  # # earnings, = - miss, no tweet
    assert (account.parse_earnings_indicator(tweet).groupdict()['earnings_indicator'])
    assert(not account.parse_positive_guidance(tweet))
    assert(account.parse_negative_earnings(tweet)[0] == 'earnings miss')

    tweet = '$EW - Edwards Lifesciences down 11% after Q3 misses, revised 2022 EPS guidance'  # earnings => miss, -, repeats earnings tweet, but 11% down may be signif
    assert (account.parse_earnings_indicator(tweet).groupdict()['earnings_indicator'])
    assert (account.parse_negative_earnings(tweet)[0] == 'Q3 miss')
    assert (not account.parse_positive_earnings(tweet))
    assert (not account.parse_positive_guidance(tweet))
    assert (not account.parse_negative_guidance(tweet))

    tweet = '$LHX - L3Harris plunges after Q3 miss, full-year guidance cut'  # earnings -> miss, guidance cut, repeats earnings
    assert (account.parse_earnings_indicator(tweet).groupdict()['earnings_indicator'])
    assert (account.parse_negative_earnings(tweet)[0] == 'Q3 miss')
    assert (account.parse_negative_guidance(tweet)[0] == 'guidance cut')

    tweet = '$COF - Capital One Q3 earnings fall short of consensus as provision for credit losses jumps'  # earnings also -credit losses
    assert (account.parse_earnings_indicator(tweet).groupdict()['earnings_indicator'])
    assert (account.parse_negative_earnings(tweet)[0] == 'earnings fall')
    assert (account.parse_negative_earnings(tweet)[1] == 'credit loss')
    assert (len(account.parse_negative_earnings(tweet)) == 2)

    tweet = '$ORC - Orchid Island Capital posts Q3 loss on widening spreads after Fed rate hikes'  # earnings, repeats tweet
    assert (account.parse_earnings_indicator(tweet).groupdict()['earnings_indicator'])
    assert (account.parse_negative_earnings(tweet)[0] == 'Q3 loss')
    assert (len(account.parse_negative_earnings(tweet)) == 1)


def test_mixed_or_neutral():
    account = Marketcurrents(Marketcurrents.account_name)
    tweet = '$DTM - DT Midstream reports Q3 earnings; raises FY22 and FY23 Adjusted EBITDA guidance'  # earnings + => raises
    assert (account.parse_earnings_indicator(tweet).groupdict()['earnings_indicator'])
    assert (not account.parse_positive_earnings(tweet))

    tweet = "$AMC - AMC Entertainment Q3 results beat estimates, co's adj. EBITDA loss widens"
    assert(account.parse_positive_earnings(tweet)[0] == 'results beat')
    assert(account.parse_negative_earnings(tweet)[0] == 'EBITDA loss')

    tweet = '$NCLH - Norwegian Cruise Lines sails to earnings beat, offers upbeat occupancy forecast'
    assert(account.parse_positive_earnings(tweet)[0] == 'earnings beat')
    assert(account.parse_positive_guidance(tweet)[0] == 'upbeat occupancy forecast')

    tweet = '$THS - TreeHouse Foods slides after margins disappoint despite higher pricing'
    assert(account.parse_positive_earnings(tweet)[0] == 'higher pricing')
    assert(account.parse_negative_earnings(tweet)[0] == 'margins disappoint')

    tweet = '$NEWT - Newtek Business Q3 adjusted NII climbs from a year ago, but falls short of consensus'
    assert(account.parse_positive_earnings(tweet)[0] == 'NII climb')
    assert(account.parse_negative_earnings(tweet)[0] == 'falls short')

    tweet = '$NEXA - Nexa Resources reports Q3 mixed earnings; reaffirms FY22 capex guidance'  # earnings, = mixed, reaffirms, no tweet
    assert (account.parse_earnings_indicator(tweet).groupdict()['earnings_indicator'])
    assert (not account.parse_positive_earnings(tweet))
    assert (not account.parse_negative_earnings(tweet))
    assert (not account.parse_positive_guidance(tweet))
    assert (not account.parse_negative_guidance(tweet))

    tweet = '$LTC - LTC Properties Q3 results mixed on rental income growth, higher expenses'  # mixed, repeats mixed info in tweet, +growth -expenses
    assert (account.parse_earnings_indicator(tweet).groupdict()['earnings_indicator'])
    assert (account.parse_negative_earnings(tweet)[0] == 'higher expense')
    assert (account.parse_positive_earnings(tweet)[0] == 'income grow')


def acq():
    t = '$BEP $NEP $BEP.UN:CA - Brookfield Renewable to buy U.S.-based Scout Clean Energy in $1B deal'
    t = "$ATKR - Atkore acquires Elite Polymer Solutions for $91.6M to boost HDPE conduit portfolio"
    t = '$SJI $ZEN - Zendesk drops on no apparent news amid private equity takeover'
    t = '$BZUN - Baozun acquires Gap Greater China in an all-cash transaction'
    t = '$BRKR - Bruker acquires neurotechnology company Inscopix'
    t = '$SHW - Sherwin-Williams acquires German wood coatings companies'
    t = '$ACHC - Acadia Healthcare announces new acquisition in Georgia to target opioid abuse'
    t = '$PKBO - Peak Bio stock rallies 140% after two days of losses following SPAC merger'
    t = "$ACIW - ACI Worldwide ticks higher on speculation it could be sale target with interim CEO "
    t = '$OYST $VTRS - Viatris to acquire Oyster Point Pharma for $11/share in cash'
    t = '$VLDR $OUST - Velodyne, Ouster propose to merge in all-stock deal'
    t = '$RBA $IAA $RBA:CA - Ritchie Bros. to acquire IAA in $7.3B stock and cash deal'
    t = '$IAA - IAA Non-GAAP EPS of $0.45 misses by $0.05, revenue of $497.5M beats by $20.89M, to be acquired by Ritchie Bros. in stock and cash deal of $7.3B'
    t = '$UNH $LHCG - LHC Group gains on report sale to UnitedHealth may close next month'

def mixed():
    t = '$BLNK - Blink Charging issues confident production outlook even as losses continue'
    t = "$DIS - Disney slips 7% as media side profits, revenue slip; subscribers top forecasts"

def news_pos():
    t = '$VVPR - VivoPower subsidiary surges 16% as Tembo enters supply agreement for EV conversion kits'
    tweet = '$BSTG - Regenerative therapy developer Biostage files for Nasdaq uplisting, $6M offering'  # +, uplisting
    t = '$CUBT - Curative Biotechnology refiles for NYSE uplisting, $8M offering'
    tweet = '$BFIN - BankFinancial adds 300,000 shares to existing share repurchase program'  # + repurchase
    tweet = '$OTLK - FDA accepts Outlook Therapeutics biologics license application for wet AMD drug'  # +, FDA accepts
    tweet = '$PHGUF $PHAR - Pharming gets EMA accelerated review of leniolisib for rare immunodeficiency disorder'  # + => accelerated review
    t = '$DASH - DoorDash stock pops over 10% as analysts applaud resilience to macro pressures'
    t = '$CHUY - Chuys stock charges higher on strong comparable sales, profit growth'
    t = '$COLD - Americold Realty Trust rises on upward revision to FY22 guidance'
    t = '$HZNP - Horizon Therapeutics ticks higher amid speculation of activist investor' # activist investor
    t = '$STEM - Stem stock rises on strong Q3 bookings'
    t = '$FSLR - First Solar soars to 11-year high as analyst touts extraordinary backlog'
    t = '$LEG - Leggett &amp; Platt shares lifted as earnings exceed lowered expectations'
    t = '$AMZN $HD $SBUX - Home Depot workers vote against unionization in first store test'
    t = '$ORGS - Orgenesis jumps 26% on $50M investment from Metalmark Capital'

def news_neg():
    t = '$COTY - Coty shares carry higher on strong fragrance, consumer beauty sales'
    t = '$FAT - FAT Brands slides after withdrawing stock offering'
    t = "$VZLA $VZLA:CA - Vizsla Silver shares slump after C$20M bought deal offering"
    tweet = '$AHG - Akso Health gets Nasdaq notice for not complying with minimum bid price rule'  # -, not complying
    tweet = '$YMAB - Y-mAbs fails to win FDA AdCom backing for neuroblastoma therapy'  # -, fails to win FDA
    tweet = '$PME - Chinese fisher Pingtan gets Nasdaq minimum bid compliance notice'  # - compliance notice
    tweet = '$WNW - Meiwu Technology regains compliance with Nasdaq minimum bid price requirement'  # + regains compliance
    tweet = '$BX $KKR $APO - KKR, Apollo, Blackstone face Justice Department probe on influence over boards'  # - face probe
    tweet = '$SBHMY $FSTX - F-star Therapeutics drops amid concern about CFIUS approval for Sino-Biopharma'  # - drops, can't use 'approval' on its own
    tweet = '$COF - Capital One credit card delinquency, net charge-off rates climb in September'  # -, industry, delinquency climbs =>IGNORE
    tweet = '$ALRM $VVNT - https://t.co/LStNLDdfU5 stock slips 3% after the bell on licensing dispute with Vivint'  # news, licensing dispute
    t = '$KTOS - Kratos trims FY forecast on labor shortages, inflation woes'
    t = '$SYNH - Syneos Health sheds 23% as outlook stands below consensus'
    t = '$AXL $MLSPF - American Axle sinks 18% after denying sales talks'
    t = '$DKNG - DraftKings stock dives nearly 20% on lackluster 2023 forecast'
    t = '$TEAM - Atlassian plunges as Piper Sandler downgrades following guidance cut, slowing user growth'
    t = '$DAL - Delta pilots vote ‘overwhelmingly in favor’ of strike authorization'
    t = '$GT - Goodyear Tire stock skids as cost inflation, currency concerns impact earnings'
    t = '$VRNS - Varonis slashes guidance on macro, forex headwinds; stock tumbles 16% after the bell'
    t = '$MRNS - Marinus Pharmaceuticals stock drops 19% aftermarket on proposed public offering'
    t = '$ATHX - Athersys tumbles 40% after the bell on proposed stock offering'
    t = '$VRM - Vroom sees sales plummet, adjusted EBITDA go negative in Q3'
    t = '$ROIV - Roivant Sciences falls 7% after hours on $150M stock offering'
    t = "$RBA $IAA $RBA:CA - Ritchie Bros. plunges 20% on IAA purchase, deal called a 'head-scratcher'"
    t = "$JUPW $JWAC - Jupiter Wellness stock falls 13% on plans to spin off Caring Brands"
    t = "$ARVL - Arrival stock plunges as it expects no revenue until 2024 with insufficient cash"
    t = "$WKHS - Workhorse stock sinks on wider than expected loss"

def dividends():
    t = "$AMPE - Ampio Pharmaceuticals to implement 1-for-15 reverse stock split"
    tweet = '$TMBR - Timber Pharmaceuticals announces 1-for-50 reverse stock split'
    tweet = '$TAIT - Taitron Components raises dividend by 11% to $0.05'  # +, raises dividend
    t = '$ABC - AmerisourceBergen increases dividend by ~5%'
    tweet = '$ZION - Zions declares $0.41 dividend, approves up to $50M buyback'  # + buyback
    tweet = 'Wells Fargo Multi-Sector Income Fund lowers dividend by 4.1%'  # -, lowers dividend
    tweet = '$FTAI - Fortress Transportation dividend declines by 10% to $0.30'  # - dividend declines
    t = '$ETO - Eaton Vance Tax-Advantaged Global Dividend Opportunities Fund dividend declines by 23.3% to $0.1374'
    t = '$CRF - Cornerstone Total Return Fund reduces monthly dividend'
    t = '$KERN - Akerna announces 20-for-1 reverse stock split; shares down 19%'
    t = '$ONCS - OncoSec stock plummets 26% on 1-for-22 reverse stock split'

def buyback():
    t = '$AMPH - Amphastar authorizes $50M buyback'
    t = '$LXU - LSB Industries prices offering of $14.35M shares and plans to repurchase 3.5M shares'
    t = '$OEC - Orion Engineered Carbons announces $50M share buyback program'
    t = '$DQ - Daqo New Energy announces $700M stock buyback program'
    t = '$LAD - Lithia &amp; Driveway boosts share repurchase authorization by $450M'
    t = '$GDL $GFELF $GDL:CA - Goodfellow to buy back stock via NCIB'
    t = '$ENVA - Enova International expands stock buyback program to $150M'

# Political
t = '$TWTR $DWAC - Trump SPAC Digital World surges 24% as former President suggests he might run in 2024'

def guidance():
    t = '$UPST - Upstart Q4 guidance disappoints as high interest rates crush loans demand'
    t = '$NVAX - Novavax updated 2022 revenue guidance falls below consensus estimate'
    t = '$PRTY - Party City stock plummets after cutting full-year forecasts'  # although right when earnings
    t = '$QTWO - Q2 Holdings stock drops as macro headwinds dent year outlook, analysts cut'
    tweet = '$LYB - LyondellBasell paints a gloomy picture for current qtr, succumbing to high energy costs'
    t = '$PBI - Pitney Bowes stock plummets after reporting e-commerce contraction'  # -, gloomy
    t = '$PFE $NVAX $MRNA - Pfizer raises outlook even as COVID vaccines sales drop 66% in Q3'
    t = '$TTWO - Take-Two tumbles 11% as it cuts bookings view below expectations'
    t = '$OCUL - Ocular Therapeutix hits 52-week low after slashing revenue guidance'
    t = '$UIS - Unisys plunges 40% after guidance cut'   # earnings related but not linked
    t = '$LPSN - LivePerson stock rises 9% as more upsells, WildHealth outperformance drive upbeat outlook'

def listing():
    t = '$NILE - BitNile receives NYSE American non-compliance notice'
    t = '$VNTR - Venator gets listing deficiency letter from NYSE'
    t = '$SWVL - Swvl gets Nasdaq minimum bid price deficiency notice'
    t = '$TISI - Team receives continued listing notice from NYSE'
    t = '$STAB - Statera Biopharma granted continued listing on Nasdaq'  # + -> granted continued listing
    t = '$BROG - Brooge Energy gets Nasdaq staff determination letter'
    t = '$HEPS - Hepsiburada receives non-compliance letter from the Nasdaq'
    t = '$ANPC - AnPac gets till Nov 23 to meet Nasdaq listing rule'
    t = '$ZHYBF - Neurological products marketer Zhong Yuan seeks Nasdaq uplisting, $15M offering'
    t = '$IRNT - IronNet receives NYSE notice for non-compliance'
    t = '$WPRT $WPRT:CA - Westport gets notice for listing deficiency in U.S'
    t = '$SXTC - China SXT Pharmaceuticals receives Nasdaq notice for non-compliance'
    t = '$NESR - National Energy Services Reunited receives potential delisting notice from Nasdaq'
    t = '$GLS $GLS.WS - Gelesis receives NYSE notice of non-compliance'

def wins():
    t = '$GBLTF $GBLT:CA - GBLT receives over $1.1M additional order from an international retailer'
    t = '$HIHO - Highway Holdings receives new order from Fortune 500 customer'
    t = '$HWNI - High Wire bags $1.8M government phone deployment contract'
    t = '$LIQT - LiqTech secures order for Denmark metal processing industry'
    t = '$GVP - GSE Solutions climbs 11% on contract expansion worth $3M'
    t = '$LMT - Lockheed Martin secures $765M Naval Air Systems contract'
    t = '$KBR - KBR secures contract from Indian chemicals firm'
    t = '$GE - General Electric bags $1.09B Naval Supply Systems contract'
    t = '$PSN - Parsons bags $28M order to investigate PFAS impact at Army National Guard facilities'
    t = '$AEHR - Aehr wins $4.4M worth orders for WaferPak full wafer contactors'
    t = '$ACM - AECOMs venture wins contract for New Jersey light rail project'
    t = '$DEN - Denbury wins carbon transport, storage deal for planned clean hydrogen plant'
    t = '$ABSSF $BOS:CA - AirBoss of America receives $40.6M in orders for Husky 2G vehicles'
    t = '$LGIQ - Logiq signs client services contract, expected to generate $2M-$3M/month'
    t = '$APD - Air Products bags government funding for hydrogen energy complex in Alberta'

def labor():
    t = '$ZEN - Zendesk cuts ~300 jobs globally - SEC filing'
    t = '$X - U.S. Steel reaches tentative deal with steelworkers union, includes 5% base wage hike'
    t = '$META - Meta Platforms shares rise with big layoffs expected this week'
    t = '$RAMP - LiveRamp announces 10% workforce reduction, downsizes real estate footprint'

def pharma_pos():
    t = '$GLTO - Galecto stock rises 12% as GB1211 shows efficacy in liver disease patients in trial'
    t = '$OTLC - Oncotelic files with FDA to start trial of OT-101 for brain tumor in children'
    t = '$NVAX - Novavax says Phase 3 data support booster effect of COVID-19 shot against Omicron'
    t = '$PFE - Pfizer COVID-19 pill cuts risk of long COVID by 26% - study'
    t = '$ICCM - IceCure soars 44% as ProSense system for breast cancer gets Medicare payment group'
    t = '$MRNA - Moderna second bivalent COVID booster authorized in Canada'
    t = '$LLY - Eli Lilly heart disease therapy meets main goal in Phase 3 kidney disease trial'
    t = '$PFE $BNTX - Pfizer/BioNTech Omicron booster is safe despite bubble formation – Swissmedic'
    t = '$PFE $BNTX - Pfizer, BioNTech gain as updated data supports use of Omicron booster in adults'
    t = '$BMY $BCAB - BioAtla soars 47% as drug shows response in lung cancer patients in trial'
    t = '$ABMD - Abiomed Impella RP Flex gets FDA approval to treat right heart failure'
    t = '$ENSC - Ensysce says oxycodone formulation indicated potential for abuse deterrence'
    t = '$SBHMY $FSTX - F-star Therapeutics falls for a second day as CFIUS deadline set to expire'
    t = '$RVPH - Reviva issues enrollment update on pivotal trial for lead candidate'
    t = '$TAK $MRNA - Modernas Omicron BA.4-5 targeting booster shot gets approval in Japan'
    t = '$SNY $LCI - Lannett gains on patent deal for biosimilar insulin device'
    t = '$RHHBY $RHHBF $AFMD - Affimed gains 22% after updating Phase 1/2 data for tumor candidate'
    t = '$ABVC - ABVC Biopharma stock rises on upcoming US patent for ABV-1504 to treat depression'
    t = "$GMDA - Gamida's rises 5% after cell therapy candidate GDA-501 shows promising antitumor activity against HER2+ cancers"
    t = '$RLYB - Rallybio sees positive results in phase 1 trial of complement-mediated diseases candidate'
    t = '$AVXL - Anavex therapy for Fragile X syndrome gets FDA orphan drug status'
    t = '$RHHBY $IONS $RHHBF - Ionis, Roche kidney disease drug meets main goal in mid-stage study'
    t = "$AMGN - Amgen's olpasiran cuts cholesterol levels by 95% in heart disease patients in trial"
    t = "$RETA - Reata rises 15% as omaveloxolone moves ahead in FDA review process; plans EU filing"

def pharma_neg():
    t = '$MDT - Medtronic says trial for renal denervation system did not meet main goal in hypertension'
    t = "$OMER - Omeros appeal of FDA Complete Response Letter on narsoplimab denied; shared down 7%"
    t = '$VERV - Verve sheds 22% as FDA holds trial application for gene editing drug'
    t = '$GSK - GSK barred from bulk drug purchasing program in China for 18 months'
    t = '$ABBV - AbbVie candidate for postoperative atrial fibrillation fails in mid-stage trial'
    t = "$GSK $BMY - GSK's blood cancer therapy Blenrep fails to meet main goal in phase 3 study"
    t = "$OMER - Omeros downgraded at Bank of America after FDA snub for narsoplimab appeal"

def bankruptcy():
    t = '$FSRD - Fast Radius announces Chapter 11 filing to complete its marketing and sale process'

def offerings():
    t = '$ZTS - Zoetis prices $1.35B senior note offering'
    t = '$HUM - Humana prices $1.23B debt offering'
    t = '$ROIV - Roivant Sciences stock dips on pricing stock offering'
    t = '$MRNS - Marinus Pharmaceuticals shares slide 18% on $60M securities offering'
    t = '$CAH - Cardinal Health files for mixed shelf offering'
    t = '$BXP - Boston Properties prices $750M offering of green bonds'

# Industry, auto peer detection
def industry():
    t = '$SMH $PSI $INTC - Global semiconductors sales drop 3% in Q3 202'
    t = '$GTN $APO $GTN.A - Tegna falls as peer Gray Television plunges post results; Standard General refutes job cut claims'
    t = '$LI $NIO $XPEV - Chinese EV stocks jump on signal of Zero-COVID reconsideration'
    t = '$ARKG $ARKQ $ARKW - SARK, the anti-Cathie Wood ETF, has returned over 100% in its first year of trading'
    t = '$SWBI $RGR $SPWH - Election day means traders are watching firearm-related stocks for any recoil action'
    t = '$RCL $CCL $NCLH - Cruise stocks push higher after positive report from Norwegian'

# Activism
t = '$AIM - AIM Immunotech says court denies activist request on board nominees'

