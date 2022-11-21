from loaders.twitter_marketcurrents import Marketcurrents


def test_false_positive_guidance():
    account = Marketcurrents(Marketcurrents.account_name)

    tweet = "$TSN - Tyson Foods margin guidance raises analyst suspicion"
    assert (not account.parse_positive_guidance(tweet))

    tweet = "$DE - Moody's affirms Deere's A2 rating, raises outlook to positive"
    assert(account.parse_false_positive(tweet).groupdict())

    tweet = '$UCO $USO $DBO - Oil reverses gain as OPEC again cuts oil demand forecast'
    assert(not account.parse_negative_guidance(tweet))


def test_false_positive_earnings():
    account = Marketcurrents(Marketcurrents.account_name)

    tweet = "$TSSI - TSS trades lower after Q3 results, CEO departure announcement"
    assert (not account.parse_negative_earnings(tweet))

    tweet = "$DE $TITN - October seen as a strong month agricultural equipment sales" # fuzzy, earnings ind, false pos
    assert (not account.parse_positive_earnings(tweet))

    tweet = "$PVBC $BTC-USD - Provident Bancorp stock plunges as it estimates Q3 loss sparked by crypto slump"
    assert (not account.parse_negative_earnings(tweet))
    assert (account.parse_negative_guidance(tweet)[0] == 'estimates Q3 loss')

    tweet = "$NFLX - Netflix shares head north as BoA cites 'strong runway' for subscriber growth"
    assert(account.parse_false_positive(tweet).groupdict())

    tweet = "$JAGX - Jaguar trades lower despite Q3 revenue soaring 400%"
    assert(not account.parse_negative_earnings(tweet))  # lower despite

    tweet = "$FAMI - Farmmi secures high-volume order for export to Guam"
    assert(not account.parse_positive_earnings(tweet))  # higher, not high

    tweet = "$DIS - Disney World boosts prices as parks demand continues surge"
    assert(not account.parse_positive_earnings(tweet))

    tweet = "$EAD - Allspring Income Oppurtunities declines monthly dividend by -2.4% to $0.0535 /share"
    assert(not account.parse_negative_earnings(tweet))  # income declines not captured


def test_parse_false_positive():
    account = Marketcurrents(Marketcurrents.account_name)

    tweet = "$FXI $PGJ $EWH - China new home prices fall the most in over 7 years as persistent COVID-19 curbs"
    assert (account.parse_false_positive(tweet).groupdict())

    tweet = "$RAAS - Cloopen receives NYSE's grant of extension regarding delayed filing of 2021 annual report"
    assert (not account.parse_negative_earnings(tweet))

    tweet = "$EWU $FXB $EWUS - UK retail sales top estimates"
    assert (account.parse_false_positive(tweet).groupdict())

    tweet = '$BEAT - HeartBeam GAAP EPS of -$0.44'  # BEAT in the symbol)
    assert (not account.parse_positive_earnings(tweet))

    tweet = '$DDOG - Macro, consumer headwinds loom ahead of Datadog Q3 earnings'
    assert (account.parse_false_positive(tweet).groupdict())
    tweet = '$DDOG $REX Hot Stocks: afternoon update'
    assert (account.parse_false_positive(tweet).groupdict())
    tweet = '$DDOG Q2 Earnings Preview'
    assert (account.parse_false_positive(tweet).groupdict())
    tweet = '$DDOG Can Datadog show good Q3 results?'
    assert (account.parse_false_positive(tweet).groupdict())
    tweet = '$SPG - Simon Property likely to beat Q3 consensus amid winning streak for retail REITs'
    assert (account.parse_false_positive(tweet).groupdict())
    tweet = '$MAIN - Main Street Capital likely to go up after Q3 results on revenue beat, stronger capital position'
    assert (not account.parse_false_positive(tweet))

    tweet = '$MF - Missfresh regains compliance with Nasdaq minimum bid price requirement'  # miss in name
    assert (not account.parse_negative_earnings(tweet))

    tweet = '$SDIG - Stronghold Digital Mining reports mixed Q3 earnings; initiates FY23 guidance'  # strong in the name :)
    assert (not account.parse_positive_earnings(tweet))


def test_parse_earnings_indicator():
    account = Marketcurrents(Marketcurrents.account_name)

    tweet = "$HD - Home Depot hurdles Q3 expectations despite macro pressure, elevated inventory"
    assert (account.parse_earnings_indicator(tweet).groupdict()['earnings_indicator'].strip() == 'hurdles Q3 expectation')

    tweet = "$ENR - Energizer gains after posting strong organic sales"
    assert (account.parse_earnings_indicator(tweet).groupdict()['earnings_indicator'].strip() == 'after posting strong organic sales')

    tweet = '$TME - Tencent Music Entertainment jumps 30% on strong Q3 performance'
    assert (account.parse_earnings_indicator(tweet).groupdict()['earnings_indicator'].strip() == 'Q3 performance')

    tweet = "$CWCO - Consolidated Water stock dips 16% as Q3 net income falls"
    assert (account.parse_earnings_indicator(tweet).groupdict()['earnings_indicator'].strip() == 'Q3 net income')

    tweet = "$TTCF - Tattooed Chef shares tumbles about 15% on earnings disappointment, cash concerns"
    assert (account.parse_earnings_indicator(tweet).groupdict()['earnings_indicator'].strip() == 'earnings disappoint')

    tweet = "$IMNN - Imunon falls 4% on wider-than-expected loss"
    assert (account.parse_earnings_indicator(tweet).groupdict()['earnings_indicator'].strip() == 'wider-than-expected loss')

    tweet = "$SNDL - SNDL gains as cannabis retail drives Q3 growth"
    assert (account.parse_earnings_indicator(tweet).groupdict()['earnings_indicator'].strip() == 'Q3 growth')

    tweet = "$SANW - S&amp;W Seed Company tops earnings expectation, touts cost-saving efforts"
    assert (account.parse_earnings_indicator(tweet).groupdict()['earnings_indicator'].strip() == 'tops earnings expectation')

    tweet = "$HNST - Honest Company stock slides on larger than expected loss"
    assert (account.parse_earnings_indicator(tweet).groupdict()['earnings_indicator'].strip() == 'larger than expected loss')

    tweet = '$VCSA - Vacasa stock sinks ~38% as Q4 guidance disappoints; co sees softness in bookings'
    assert (account.parse_earnings_indicator(tweet).groupdict()['earnings_indicator'].strip() == 'Q4 guidance')

    tweet = "$PGEN - Precigen stock rises 16% as Q3 collaboration/licensing revenue surges"
    assert (account.parse_earnings_indicator(tweet).groupdict()['earnings_indicator'].strip() == 'Q3 collaboration/licensing revenue')

    tweet = "$SSYS - Stratasys cuts FY2022 outlook to include the impact of MakerBot divestiture"
    assert (account.parse_earnings_indicator(tweet).groupdict()['earnings_indicator'].strip() == 'FY2022 outlook')

    tweet = "$RKLB - Rocket Lab stock zooms over 20% on record revenue, narrower loss"
    assert (account.parse_earnings_indicator(tweet).groupdict()['earnings_indicator'].strip() == 'record revenue')

    tweet = "$BRLT - Brilliant Earth plunges 60% after slash in full-year outlook"
    assert (account.parse_earnings_indicator(tweet).groupdict()['earnings_indicator'].strip() == 'full-year outlook')

    tweet = "$HYPR - Hyperfine stock rises as Q3 device revenue surges, maintains FY22 outlook"
    assert (account.parse_earnings_indicator(tweet).groupdict()['earnings_indicator'].strip() == 'Q3 device revenue')

    tweet = "$AIRS - AirSculpt drops nearly 30% on 2022 forecast cut"
    assert (account.parse_earnings_indicator(tweet).groupdict()['earnings_indicator'].strip() == '2022 forecast')

    tweet = "$FNA - Paragon surges 11% as FY22 outlook raised despite forex impact"
    assert (account.parse_earnings_indicator(tweet).groupdict()['earnings_indicator'].strip() == 'FY22 outlook')

    tweet = "$MGNI - Magnite jumps 8% as third-quarter revenues, profits top views"
    assert (account.parse_earnings_indicator(tweet).groupdict()['earnings_indicator'].strip() == 'third-quarter revenues, profit')

    tweet = "$SPTN - SpartanNash guides Q3 revenue above the consensus, raises FY guidance"
    # But this was actually just guidance, 6 days before the report
    assert(account.parse_earnings_indicator(tweet).groupdict()['earnings_indicator'].strip() == 'Q3 revenue')

    tweet = '$KODK - Kodak shares tumble 21% on earnings decline in Q3'
    assert(account.parse_earnings_indicator(tweet).groupdict()['earnings_indicator'].strip() == 'decline in Q3')

    tweet = '$SFM - Sprouts Farmers Market stock surges on strong profit, sales forecasts'
    assert(account.parse_earnings_indicator(tweet).groupdict()['earnings_indicator'].strip() == 'strong profit')

    tweet = '$MSGE - MSG Entertainment stock drops over 13% to record low as higher costs drag earnings'
    assert(account.parse_earnings_indicator(tweet).groupdict()['earnings_indicator'].strip() == 'drag earnings')

    tweet = '$REAL - The RealReal offers mixed Q3 report, below consensus sales guide'
    assert(account.parse_earnings_indicator(tweet).groupdict()['earnings_indicator'].strip() == 'Q3 report')

    tweet = '$LMND - Lemonade Q4 guidance trails consensus; Q3 net loss ratio swells'
    assert(account.parse_earnings_indicator(tweet).groupdict()['earnings_indicator'].strip() == 'Q4 guidance')

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
    assert(account.parse_earnings_indicator(tweet).groupdict()['earnings_indicator'].strip() == 'topping some beaten-down estimate')


def test_parse_combos():
    account = Marketcurrents(Marketcurrents.account_name)

    tweet = "$SPB - Spectrum Brands trades lower after revenue miss, cautious outlook"
    assert(account.parse_negative_guidance(tweet)[0] == 'cautious outlook')
    assert(account.parse_negative_earnings(tweet)[0] == 'revenue miss')

    tweet = "$QUIK - QuickLogic trades down despite Q3 beat as revenue decreases Y/Y"
    assert(account.parse_positive_earnings(tweet)[0] == 'Q3 beat')
    assert(account.parse_negative_earnings(tweet)[0] == 'revenue decrease')

    tweet = '$BZH - Beazer Homes fiscal Q4 earnings top consensus even as selling prices drop'
    assert(account.parse_positive_earnings(tweet)[0] == 'earnings top')
    assert(account.parse_negative_earnings(tweet)[0] == 'prices drop')

    tweet = '$MQ - Marqeta expects slower Q4 revenue growth, while EBITDA margin seen to improve'
    assert(account.parse_negative_guidance(tweet)[0] == 'expects slower Q4 revenue growth')
    assert(account.parse_positive_guidance(tweet)[0] == 'margin seen to improve')
    assert(not account.parse_positive_earnings(tweet))  # we don't want revenue growth - preceded by "slower"

    tweet = "$HGV - Hilton Grand Vacations climbs 10% on raising FY outlook, and reporting Q3 beat"
    assert (account.parse_earnings_indicator(tweet).groupdict()['earnings_indicator'])
    assert(account.parse_positive_guidance(tweet)[0] == 'raising FY outlook')
    assert(account.parse_positive_earnings(tweet)[0] == 'Q3 beat')

    tweet = '$EPR - EPR Properties stock jumps on higher year guidance, solid Q3 beat'
    assert (account.parse_earnings_indicator(tweet).groupdict()['earnings_indicator'])
    assert(account.parse_positive_guidance(tweet)[0] == 'higher year guidance')
    assert(account.parse_positive_earnings(tweet)[0] == 'Q3 beat')

    tweet = '$WWW - Wolverine World Wide stock runs lower on earnings miss, pared guidance https://t.co/nfpaLShQN7'
    assert(account.parse_negative_guidance(tweet)[0] == 'pared guidance')
    assert(account.parse_negative_earnings(tweet)[0] == 'earnings miss')

    tweet = '$SXC - SunCoke Energy surges on strong Q3 results, EBITDA guidance'
    assert(account.parse_positive_guidance(tweet)[0] == 'strong Q3 results, EBITDA guidance')
    assert(account.parse_positive_earnings(tweet)[0] == 'strong Q3 results')

    tweet = '$OLED - Universal Display stock soars 15% on earnings beat despite weak near-term OLED demand'
    assert(account.parse_negative_earnings(tweet)[0] == 'weak near-term OLED demand')
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
    assert(account.parse_positive_earnings(tweet)[0] == 'Q3 earnings beat')
    assert(account.parse_negative_earnings(tweet)[0] == 'AUM slump')
    assert(not account.parse_positive_guidance(tweet))

    tweet = '$GBX - Greenbrier stock soars on big earnings beat, bullish forecast'
    assert (account.parse_earnings_indicator(tweet).groupdict()['earnings_indicator'])
    assert(account.parse_positive_earnings(tweet)[0] == 'earnings beat')
    assert(account.parse_positive_guidance(tweet)[0] == 'bullish forecast')

    tweet = '$BUD - Anheuser-Busch InBev shares gain sharply on Q3 profit beat, outlook boost https://t.co/gQm5oJEp1U'
    assert (account.parse_earnings_indicator(tweet).groupdict()['earnings_indicator'])
    assert(account.parse_positive_earnings(tweet)[0] == 'Q3 profit beat')
    assert(account.parse_positive_guidance(tweet)[0] == 'outlook boost')

    tweet = '$HUM - Humana trades higher on Q3 earnings beat, affirms FY22 outlook'
    assert (account.parse_earnings_indicator(tweet).groupdict()['earnings_indicator'])
    assert(account.parse_positive_earnings(tweet)[0] == 'Q3 earnings beat')
    assert(not account.parse_positive_guidance(tweet))

    tweet = '$MET - MetLife Q3 earnings beat as volume growth, higher rates offset lower PE returns'
    assert (account.parse_earnings_indicator(tweet).groupdict()['earnings_indicator'])
    assert(account.parse_positive_earnings(tweet)[0] == 'Q3 earnings beat')
    assert(account.parse_positive_earnings(tweet)[1] == 'volume grow')
    assert(account.parse_negative_earnings(tweet)[0] == 'lower PE return')

    tweet = '$VSTO - Vista Outdoor FQ2 2023 results beat estimates, co cuts FY sales, adj. EPS guidance'
    assert(account.parse_earnings_indicator(tweet).groupdict()['earnings_indicator'])
    assert(account.parse_positive_earnings(tweet)[0] == 'results beat')
    assert(account.parse_negative_guidance(tweet)[0] == 'cuts FY sales, adj. EPS guidance')

    tweet = '$OMCL - Omnicell stock crashes 32% as FY22 outlook slashed, Q3 sees headwinds'
    assert (account.parse_earnings_indicator(tweet).groupdict()['earnings_indicator'])
    assert (account.parse_negative_earnings(tweet)[0] == 'Q3 sees headwind')
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

    tweet = '$TSN - Tyson Foods projects ‘strong profitability’ in 2023 despite macro pressures'
    assert (account.parse_positive_guidance(tweet)[0] == 'projects ‘strong profit')
    assert (not account.parse_positive_earnings(tweet))

    tweet = "$LOW - Lowe’s shares lifted by earnings beat, raised forecast"
    assert (account.parse_positive_guidance(tweet)[0] == 'raised forecast')
    assert (account.parse_positive_earnings(tweet)[0] == 'earnings beat')

    tweet = '$COLD - Americold Realty Trust rises on upward revision to FY22 guidance'
    assert (account.parse_positive_guidance(tweet)[0] == 'upward revision to FY22 guidance')
    assert (not account.parse_positive_earnings(tweet))

    tweet = "$WSKEF $WKEY - WISeKey sees FY22 semiconductor revenue to $22.7M; FY23 revenues expected to grow over 40% Y/Y"
    assert (account.parse_positive_guidance(tweet)[0] == 'revenues expected to grow')
    assert (not account.parse_positive_earnings(tweet))

    tweet = "$SHLS - Shoals sizzles after raising low end of revenue guidance; Northland upgrades"
    assert (account.parse_positive_guidance(tweet)[0] == 'raising low end of revenue guidance')
    assert (not account.parse_positive_earnings(tweet))

    tweet = "$ONON - On Holding stock slides despite hiking sales outlook"
    assert (account.parse_positive_guidance(tweet)[0] == 'hiking sales outlook')
    assert (not account.parse_positive_earnings(tweet))

    tweet = '$DVA $FMS $OM - Outset Medical adds 39% after setting guidance ahead of consensus'
    assert (account.parse_positive_guidance(tweet)[0] == 'guidance ahead')
    assert (not account.parse_positive_earnings(tweet))

    tweet = '$TTM - Tata Motors expects strong improvements in EBIT and free cash flows in H2 FY23; to delist its ADSs from NYSE'
    assert (account.parse_positive_guidance(tweet)[0] == 'expects strong improvement')
    assert (not account.parse_positive_earnings(tweet))

    tweet = '$PFE $NVAX $MRNA - Pfizer raises outlook even as COVID vaccines sales drop 66% in Q3'
    assert (account.parse_positive_guidance(tweet)[0] == 'raises outlook')
    assert (account.parse_negative_earnings(tweet)[0] == 'sales drop')

    tweet = '$LPSN - LivePerson stock rises 9% as more upsells, WildHealth outperformance drive upbeat outlook'
    assert (account.parse_positive_guidance(tweet)[0] == 'upbeat outlook')
    assert (not account.parse_positive_earnings(tweet))

    tweet = '$BLNK - Blink Charging issues confident production outlook even as losses continue'
    assert (account.parse_positive_guidance(tweet)[0] == 'confident production outlook')
    assert (account.parse_negative_earnings(tweet)[0] == 'losses continue')

    tweet = "$KEYS - Keysight rises on Q4 earnings beat, sees Q1 result above estimates"
    assert (account.parse_positive_guidance(tweet)[0] == 'sees Q1 result above')
    assert (account.parse_positive_earnings(tweet)[0] == 'Q4 earnings beat')

    tweet = "$M - Macy’s stock surges on strong Q3 earnings, boost to bottom line guide"
    assert (account.parse_positive_guidance(tweet)[0] == 'boost to bottom line guide')
    assert (account.parse_positive_earnings(tweet)[0] == 'strong Q3 earnings')

    tweet = "$BBWI - Bath &amp; Body Works soars after lifting profit guidance"
    assert (account.parse_positive_guidance(tweet)[0] == 'lifting profit guidance')
    assert (not account.parse_positive_earnings(tweet))

    tweet = "$AQUA - Evoqua Water rallies after solid earnings beat, guidance tops expectations"
    assert(account.parse_positive_guidance(tweet)[0] == 'guidance tops')
    assert (account.parse_positive_earnings(tweet)[0] == 'earnings beat')

    tweet = '$SFM - Sprouts Farmers Market stock surges on strong profit, sales forecasts'
    assert(account.parse_positive_guidance(tweet)[0] == 'strong profit, sales forecast')
    assert (account.parse_positive_earnings(tweet)[0] == 'strong profit')

    tweet = '$DTM - DT Midstream reports Q3 earnings; raises FY22 and FY23 Adjusted EBITDA guidance'
    assert (account.parse_earnings_indicator(tweet).groupdict()['earnings_indicator'])
    assert(account.parse_positive_guidance(tweet)[0] == 'raises FY22 and FY23 Adjusted EBITDA guidance')
    assert (not account.parse_positive_earnings(tweet))

    tweet = '$FPRUF $FPRUY - Fraport AG reports Q3 results; expects to achieve upper range of full-year outlook'
    assert(account.parse_positive_guidance(tweet)[0] == 'upper range of full-year outlook')
    assert (not account.parse_positive_earnings(tweet))

    tweet = "$KSS - Kohl’s shares gain as Q3 earnings guided to be well above consensus, CEO quits"
    assert(account.parse_positive_guidance(tweet)[0] == 'guided to be well above')
    assert (not account.parse_positive_earnings(tweet))

    tweet = '$WMB - Williams sees full-year EBITDA near high end of guidance after strong Q3'
    assert(account.parse_positive_guidance(tweet)[0] == 'high end of guidance')
    assert (not account.parse_positive_earnings(tweet))

    tweet = '$TGLS - Tecnoglass beats top and bottom line, increases FY outlook'
    assert (account.parse_earnings_indicator(tweet).groupdict()['earnings_indicator'])
    assert(account.parse_positive_guidance(tweet)[0] == 'increases FY outlook')
    assert (account.parse_positive_earnings(tweet)[0] == 'beats top and bottom line')

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
    assert (account.parse_positive_earnings(tweet)[0] == 'Q3 estimates beat')

    tweet = '$GTLS - Chart Industries reports mixed Q3 earnings; narrows FY22 and issues FY23 guidance'
    assert (account.parse_earnings_indicator(tweet).groupdict()['earnings_indicator'])
    assert(not account.parse_positive_guidance(tweet))
    assert(not account.parse_positive_earnings(tweet))
    assert(not account.parse_negative_guidance(tweet))

    tweet = '$CL - Colgate-Palmolive reports mixed Q3 result, raises sales forecasts'  # earnings + => mixed but raises, earnings tweet mixed
    assert (account.parse_earnings_indicator(tweet).groupdict()['earnings_indicator'])
    assert(account.parse_positive_guidance(tweet)[0] == 'raises sales forecast')
    assert(not account.parse_negative_guidance(tweet))
    assert(not account.parse_positive_earnings(tweet))


def test_parse_negative_guidance():
    account = Marketcurrents(Marketcurrents.account_name)

    tweet = '$APRN - Blue Apron slides to all-time low after another unprofitable quarter, pulled guidance'
    assert(account.parse_negative_guidance(tweet)[0] == 'pulled guidance')
    assert(account.parse_negative_earnings(tweet)[0] == 'unprofitable quarter')

    tweet = '$SENS - Senseonics Holdings shares dip on tightening FY2022 revenue outlook'
    assert (account.parse_negative_guidance(tweet)[0] == 'tightening FY2022 revenue outlook')

    tweet = '$VRNS - Varonis slashes guidance on macro, forex headwinds; stock tumbles 16% after the bell'
    assert (account.parse_negative_guidance(tweet)[0] == 'slashes guidance')
    assert (not account.parse_negative_earnings(tweet))

    tweet = '$DKNG - DraftKings stock dives nearly 20% on lackluster 2023 forecast'
    assert (account.parse_negative_guidance(tweet)[0] == 'lackluster 2023 forecast')

    tweet = '$TEAM - Atlassian plunges as Piper Sandler downgrades following guidance cut, slowing user growth'
    assert (account.parse_negative_guidance(tweet)[0] == 'guidance cut')

    tweet = '$KTOS - Kratos trims FY forecast on labor shortages, inflation woes'
    assert (account.parse_negative_guidance(tweet)[0] == 'trims FY forecast')

    tweet = '$SYNH - Syneos Health sheds 23% as outlook stands below consensus'
    assert (account.parse_negative_guidance(tweet)[0] == 'outlook stands below')

    tweet = "$KSS $LEVI - Kohl’s withdraws full-year guidance amid macro uncertainty, CEO transition"
    assert (account.parse_negative_guidance(tweet)[0] == 'withdraws full-year guidance')

    tweet = "$PLCE - Children’s Place stock plunges after pulling in full-year forecasts"
    assert (account.parse_negative_guidance(tweet)[0] == 'pulling in full-year forecast')

    tweet = "$BRLT - Brilliant Earth stock slumps after sales forecast falls short of expectations"
    assert (account.parse_negative_guidance(tweet)[0] == 'forecast falls')
    assert (not account.parse_negative_earnings(tweet))

    tweet = "$POWW - Ammo stock plummets 26% as outlook cut, proxy contest linked expenses to continue"
    assert (account.parse_negative_guidance(tweet)[0] == 'outlook cut')
    assert (not account.parse_negative_earnings(tweet))

    tweet = "$COOK - Traeger stock tumbles on underdone guidance"
    assert (account.parse_negative_guidance(tweet)[0] == 'underdone guidance')
    assert (not account.parse_negative_earnings(tweet))

    tweet = '$MQ - Marqeta expects slower Q4 revenue growth, while EBITDA margin seen to improve'
    assert (account.parse_negative_guidance(tweet)[0] == 'expects slower Q4 revenue growth')
    assert (account.parse_positive_guidance(tweet)[0] == 'margin seen to improve')
    assert (not account.parse_negative_earnings(tweet))

    tweet = '$TLS - Telos tanks 67% on full year guidance cut'
    assert (account.parse_negative_guidance(tweet)[0] == 'guidance cut')

    tweet = '$UPST - Upstart Q4 guidance disappoints as high interest rates crush loans demand'
    assert (account.parse_negative_guidance(tweet)[0] == 'guidance disappoint')
    assert (not account.parse_negative_earnings(tweet))

    tweet = '$NVAX - Novavax updated 2022 revenue guidance falls below consensus estimate'
    assert (account.parse_negative_guidance(tweet)[0] == 'guidance falls')
    assert (not account.parse_negative_earnings(tweet))

    tweet = '$PRTY - Party City stock plummets after cutting full-year forecasts'
    assert (account.parse_negative_guidance(tweet)[0] == 'cutting full-year forecast')
    assert (not account.parse_negative_earnings(tweet))

    tweet = '$QTWO - Q2 Holdings stock drops as macro headwinds dent year outlook, analysts cut'
    assert (account.parse_negative_guidance(tweet)[0] == 'dent year outlook')
    assert (not account.parse_negative_earnings(tweet))

    tweet = '$LYB - LyondellBasell paints a gloomy picture for current qtr, succumbing to high energy costs'
    assert (account.parse_negative_guidance(tweet)[0] == 'gloomy picture')
    assert (account.parse_negative_earnings(tweet)[0] == 'high energy costs')

    tweet = '$TTWO - Take-Two tumbles 11% as it cuts bookings view below expectations'
    assert (account.parse_negative_guidance(tweet)[0] == 'cuts bookings view')
    assert (not account.parse_negative_earnings(tweet))

    tweet  = '$OCUL - Ocular Therapeutix hits 52-week low after slashing revenue guidance'
    assert (account.parse_negative_guidance(tweet)[0] == 'slashing revenue guidance')
    assert (not account.parse_negative_earnings(tweet))

    tweet = '$UIS - Unisys plunges 40% after guidance cut'
    assert (account.parse_negative_guidance(tweet)[0] == 'guidance cut')
    assert (not account.parse_negative_earnings(tweet))

    tweet = "$WSM - Williams-Sonoma falls sharply after pulling FY24 guidance"
    assert (account.parse_negative_guidance(tweet)[0] == 'pulling FY24 guidance')
    assert (not account.parse_negative_earnings(tweet))

    tweet = "$SPB - Spectrum Brands trades lower after revenue miss, cautious outlook"
    assert (account.parse_negative_guidance(tweet)[0] == 'cautious outlook')
    assert (account.parse_negative_earnings(tweet)[0] == 'revenue miss')

    tweet = '$PEG - PSEG forecasts 2023 earnings below Wall Street consensus'
    assert (account.parse_negative_guidance(tweet)[0] == 'forecasts 2023 earnings below')
    assert (not account.parse_negative_earnings(tweet))

    tweet = '$OTLY - Oatly stock slides after missing Q3 expectations, slashing sales estimates'
    assert (account.parse_negative_guidance(tweet)[0] == 'slashing sales estimate')
    assert (account.parse_negative_earnings(tweet)[0] == 'missing Q3 expectation')

    tweet = '$VCSA - Vacasa stock sinks ~38% as Q4 guidance disappoints; co sees softness in bookings'
    assert (account.parse_negative_guidance(tweet)[0] == 'guidance disappoint')
    assert (account.parse_negative_guidance(tweet)[1] == 'sees softness in bookings')
    assert (not account.parse_negative_earnings(tweet))

    tweet = '$RDFN - Redfin issues soft Q4 revenue guidance, Q3 misses amid real estate slump'
    assert(account.parse_negative_guidance(tweet)[0] == 'soft Q4 revenue guidance')
    assert (account.parse_negative_earnings(tweet)[0] == 'Q3 miss')

    tweet = '$LMND - Lemonade Q4 guidance trails consensus; Q3 net loss ratio swells'
    assert(account.parse_negative_guidance(tweet)[0] == 'guidance trails')
    assert (account.parse_negative_earnings(tweet)[0] == 'Q3 net loss')

    tweet = '$REAL - The RealReal offers mixed Q3 report, below consensus sales guide'
    assert(account.parse_negative_guidance(tweet)[0] == 'below consensus sales guide')
    assert (not account.parse_negative_earnings(tweet))

    tweet = '$SOPH - SOPHiA Genetics reports Q3 earnings; FY22 revenue to be at the low-end of guidance'
    assert(account.parse_negative_guidance(tweet)[0] == 'low-end of guidance')
    assert (not account.parse_negative_earnings(tweet))

    tweet = '$STM - STMicroelectronics drops 7% on guiding Q4 revenue below consensus'
    assert (account.parse_earnings_indicator(tweet).groupdict()['earnings_indicator'])
    assert(not account.parse_negative_earnings(tweet))
    assert(account.parse_negative_guidance(tweet)[0] == 'guiding Q4 revenue below')

    tweet = '$PRLB - Proto Labs stock sinks 24% to decade-low as guidance widely misses estimates'
    assert (account.parse_earnings_indicator(tweet).groupdict()['earnings_indicator'])
    assert(not account.parse_negative_earnings(tweet))
    assert(account.parse_negative_guidance(tweet)[0] == 'guidance widely misses')

    tweet = '$MTUAF - MTU Aero Engines AG GAAP EPS of €1.74, revenue of €1.35B, FY22 guidance lowered'
    assert (account.parse_earnings_indicator(tweet).groupdict()['earnings_indicator'])
    assert(account.parse_negative_guidance(tweet)[0] == 'guidance lowered')
    assert (not account.parse_negative_earnings(tweet))

    tweet = '$LHX - L3Harris plunges after Q3 miss, full-year guidance cut'
    assert (account.parse_earnings_indicator(tweet).groupdict()['earnings_indicator'])
    assert(account.parse_negative_guidance(tweet)[0] == 'guidance cut')
    assert (account.parse_negative_earnings(tweet)[0] == 'Q3 miss')

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

    tweet = "$DOLE - Dole stock gains on Q3 profit beat, strong sales guidance"
    assert (account.parse_positive_earnings(tweet)[0] == 'Q3 profit beat')
    assert (len(account.parse_positive_earnings(tweet)) == 1)  # strong sales not considered because of guidance
    assert (account.parse_positive_guidance(tweet)[0] == 'strong sales guidance')

    tweet = "$M - Macy's beats consensus in Q3, raised FY2022 adjusted EPS outlook"
    assert (account.parse_positive_earnings(tweet)[0] == 'beats consensus')

    tweet = "$DSX - Diana Shipping sails through after upbeat Q3, declares dividends"
    assert (account.parse_positive_earnings(tweet)[0] == 'upbeat Q3')

    tweet = "$HUYA - Huya rises 32% on better-than-expected Q3 earnings"
    assert (account.parse_positive_earnings(tweet)[0] == 'better-than-expected Q3 earnings')

    tweet = '$EVTV - Envirotech Vehicles rises 9% on higher quarterly revenue'
    assert (account.parse_positive_earnings(tweet)[0] == 'higher quarterly revenue')

    tweet = "$SRAD - Sportradar soars after reporting first profit for U.S. business"
    assert(account.parse_positive_earnings(tweet)[0] == 'first profit')

    tweet = '$WKME - WalkMe rallies after 23% growth in subscription revenue leads earnings beat'
    assert(account.parse_positive_earnings(tweet)[0] == 'growth in subscription revenue')
    assert(account.parse_positive_earnings(tweet)[1] == 'earnings beat')

    tweet = '$NU - Nu Holdings stock jumps 13% as Q3 revenue beats consensus, earnings improve'
    assert(account.parse_positive_earnings(tweet)[0] == 'Q3 revenue beat')
    assert(account.parse_positive_earnings(tweet)[1] == 'earnings improve')

    tweet = "$MTTR - Matterport stock surges after record Q3 performance"
    assert(account.parse_positive_earnings(tweet)[0] == 'record Q3 performance')

    tweet = '$RMTI - Rockwell rises 9% on restructuring plans, narrow-than-expected Q3 loss'
    assert(account.parse_positive_earnings(tweet)[0] == 'narrow-than-expected Q3 loss')
    assert(not account.parse_negative_earnings(tweet))

    tweet = '$ALT - Altimmune rises 5.2% on smaller-than-expected Q3 loss'
    assert(account.parse_positive_earnings(tweet)[0] == 'smaller-than-expected Q3 loss')
    assert(not account.parse_negative_earnings(tweet))

    tweet = '$ANGI - ANGI climbs 11% after Q3 reports, topline sees 8% rise'
    assert(account.parse_positive_earnings(tweet)[0] == 'topline sees 8% rise')

    tweet = '$ABUS - Arbutus trades higher as Q3 net loss narrows, revenue grows on license deal'
    assert(not account.parse_negative_earnings(tweet))
    assert(account.parse_positive_earnings(tweet)[0] == 'loss narrow')
    assert(account.parse_positive_earnings(tweet)[1] == 'revenue grow')

    tweet = '$VNO - Vornado Realty Q3 revenue exceeds consensus, helped by same store NOI growth'
    assert(account.parse_positive_earnings(tweet)[0] == 'revenue exceed')

    tweet = '$CBOE - Cboe Global sees higher organic growth, less expenses in 2022 after Q3 beat'
    assert(account.parse_positive_earnings(tweet)[0] == 'higher organic growth')
    assert(account.parse_positive_earnings(tweet)[1] == 'less expenses')
    assert(account.parse_positive_earnings(tweet)[2] == 'Q3 beat')

    tweet = '$APO - Apollo Global Q3 earnings gain as inflows hold up, AUM rises'
    assert (account.parse_earnings_indicator(tweet).groupdict()['earnings_indicator'])
    assert(account.parse_positive_earnings(tweet)[0] == 'earnings gain')
    assert(account.parse_positive_earnings(tweet)[1] == 'AUM rise')

    tweet = '$ARCB - ArcBest reports Q3 earnings beat; on track to deliver record annual revenues in 2022'
    assert (account.parse_earnings_indicator(tweet).groupdict()['earnings_indicator'])
    assert(account.parse_positive_earnings(tweet)[0] == 'Q3 earnings beat')
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
    assert(account.parse_positive_earnings(tweet)[1] == 'crush results estimate')
    assert(not account.parse_negative_earnings(tweet))

    tweet = '$AFRAF - Air France-KLM savors recovering air travel which boosts Q3 revenue'
    assert (account.parse_earnings_indicator(tweet).groupdict()['earnings_indicator'])
    assert(account.parse_positive_earnings(tweet)[0] == 'boosts Q3 revenue')
    assert(not account.parse_negative_earnings(tweet))

    tweet = '$IMO $IMO:CA - Imperial Oil results surpass estimates as downstream strength continues'  # + surpass, strength
    assert (account.parse_earnings_indicator(tweet).groupdict()['earnings_indicator'])
    assert(account.parse_positive_earnings(tweet)[0] == 'results surpass')
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
    assert(account.parse_positive_earnings(tweet)[0] == 'beating Q3 consensus')
    assert(not account.parse_negative_earnings(tweet))

    tweet = '$TEX - Terex raised FY2022 EPS outlook range after 79% growth in Q3 and strong margins'  # Q3=earnings, raised, strong margins
    assert (account.parse_earnings_indicator(tweet).groupdict()['earnings_indicator'])
    assert(account.parse_positive_earnings(tweet)[0] == 'growth in Q3')
    assert(account.parse_positive_earnings(tweet)[1] == 'strong margin')
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
    assert (account.parse_positive_earnings(tweet)[0] == 'Q3 estimates beat')
    assert (not account.parse_negative_earnings(tweet))

    tweet = '$NEE $NEP - NextEra Energy posts Q3 beat; buys $1.1B landfill gas-to-electric portfolio'  # earnings +, repeats tweet
    assert (account.parse_earnings_indicator(tweet).groupdict()['earnings_indicator'])
    assert (account.parse_positive_earnings(tweet)[0] == 'Q3 beat')
    assert (not account.parse_negative_earnings(tweet))

    tweet = '$AON - Aon Q3 earnings beat as expenses plummet, free cash flow jump'  # earnings + although earnings tweet mixed
    assert (account.parse_earnings_indicator(tweet).groupdict()['earnings_indicator'])
    assert (account.parse_positive_earnings(tweet)[0] == 'Q3 earnings beat')
    assert (account.parse_positive_earnings(tweet)[1] == 'expenses plummet')
    assert (account.parse_positive_earnings(tweet)[2] == 'cash flow jump')
    assert (not account.parse_negative_earnings(tweet))

    tweet = '$SMP - Standard Motor Products reports Q3 earnings beat; updates FY22 guidance'  # reports beat => earnings +, no tweet
    assert (account.parse_earnings_indicator(tweet).groupdict()['earnings_indicator'])
    assert (account.parse_positive_earnings(tweet)[0] == 'Q3 earnings beat')
    assert (not account.parse_negative_earnings(tweet))

    tweet = '$NWL - Newell Brands gains after topping some beaten-down estimates'  # topping -> earnings, uvaga: beaten-down <> beat
    assert (account.parse_earnings_indicator(tweet).groupdict()['earnings_indicator'])
    assert (account.parse_positive_earnings(tweet)[0] == 'topping some beaten-down estimate')
    assert (not account.parse_negative_earnings(tweet))

    tweet = '$RNGR - Ranger Energy Services reports Q3 earnings beat; reaffirms FY22 capex guidance'  # + earnings, no tweet
    assert (account.parse_earnings_indicator(tweet).groupdict()['earnings_indicator'])
    assert (account.parse_positive_earnings(tweet)[0] == 'Q3 earnings beat')
    assert (not account.parse_positive_guidance(tweet))
    assert (not account.parse_negative_guidance(tweet))
    assert (not account.parse_negative_earnings(tweet))

    tweet = '$ABBV - AbbVie Non-GAAP EPS of $3.66 beats by $0.10, revenue of $14.81B misses by $130M, raises dividend by 5%'
    assert (account.parse_earnings_indicator(tweet).groupdict()['earnings_indicator'])
    assert (not account.parse_positive_earnings(tweet))
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
    assert (account.parse_positive_earnings(tweet)[0] == 'Q3 earnings beat')
    assert (not account.parse_positive_guidance(tweet))
    assert (not account.parse_negative_guidance(tweet))

    tweet = '$SNY $REGN - Sanofi Q3 sales boosted by Dupixent, Vaccines business; raises FY22 outlook again'  # miss this because of:
    assert (account.parse_earnings_indicator(tweet).groupdict()['earnings_indicator'])
    assert (account.parse_positive_earnings(tweet)[0] == 'sales boost')
    assert (account.parse_positive_guidance(tweet)[0] == 'raises FY22 outlook')

    tweet = '$SNY - Sanofi reports Q3 earnings beat; raises FY22 EPS guidance'  # Q3 earnings beat
    assert (account.parse_earnings_indicator(tweet).groupdict()['earnings_indicator'])
    assert (account.parse_positive_earnings(tweet)[0] == 'Q3 earnings beat')
    assert (account.parse_positive_guidance(tweet)[0] == 'raises FY22 EPS guidance')

    tweet = '$HIG - Hartford Financial Q3 earnings beat, helped by Commercial Lines, Group Benefits'  # earnings => repeats
    assert (account.parse_earnings_indicator(tweet).groupdict()['earnings_indicator'])
    assert (account.parse_positive_earnings(tweet)[0] == 'Q3 earnings beat')
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
    assert (account.parse_positive_earnings(tweet)[1] == 'strong quarterly sales')
    assert (len(account.parse_positive_earnings(tweet)) == 2)


def test_parse_negative_sentiment():
    account = Marketcurrents(Marketcurrents.account_name)

    tweet = '$BLNK - Blink Charging issues confident production outlook even as losses continue'
    assert (account.parse_negative_earnings(tweet)[0] == 'losses continue')

    tweet = "$WB - Weibo dips 4% as revenue tumble spurs rare earnings miss"
    assert (account.parse_negative_earnings(tweet)[0] == 'revenue tumble')
    assert (account.parse_negative_earnings(tweet)[1] == 'earnings miss')

    tweet = "$KINS - Kingstone stock slips as inflationary pressure weigh on Q3 results; suspends dividend"
    assert (account.parse_negative_earnings(tweet)[0] == 'weigh on Q3 result')

    tweet = "$FUV - Arcimoto falls after reporting another quarterly loss"
    assert (account.parse_negative_earnings(tweet)[0] == 'quarterly loss')

    tweet = '$OTLY - Oatly stock slides after missing Q3 expectations, slashing sales estimates'
    assert (account.parse_negative_earnings(tweet)[0] == 'missing Q3 expectation')

    tweet = "$BABYF $BABY:CA - Else Nutrition shares plummet as mechanical malfunction mars Q3 results"
    assert(account.parse_negative_earnings(tweet)[0] == 'mars Q3 result')

    tweet = '$ASXC - Asensus misses on top line as revenues decline slightly year over year'
    assert(account.parse_negative_earnings(tweet)[0] == 'misses on top line')
    assert(account.parse_negative_earnings(tweet)[1] == 'revenues decline')

    tweet = '$STWD - Starwood Property Trust Q3 earnings just miss consensus amid choppy markets'
    assert(account.parse_negative_earnings(tweet)[0] == 'earnings just miss')

    tweet = "$DNMR - Danimer shares rise despite Q3 top and bottom line misses"
    assert(account.parse_negative_earnings(tweet)[0] == 'bottom line miss')

    tweet = '$MSGE - MSG Entertainment stock drops over 13% to record low as higher costs drag earnings'
    assert(account.parse_negative_earnings(tweet)[0] == 'higher costs')

    tweet = "$CGC $WEED:CA - Canopy Growth stock dips as Canada cannabis revenue slumps 27% in Q2, net loss widens"
    assert(account.parse_negative_earnings(tweet)[0] == 'revenue slump')
    assert(account.parse_negative_earnings(tweet)[1] == 'loss widen')

    tweet = "$MARA - Marathon Digital Q3 net loss nearly triples Y/Y, earnings and revenue miss"
    assert(account.parse_negative_earnings(tweet)[0] == 'Q3 net loss')
    assert(account.parse_negative_earnings(tweet)[1] == 'earnings and revenue miss')

    tweet = '$FNMA - Fannie Mae Q3 earnings slide as lower home prices lead to higher credit expense'
    assert(account.parse_negative_earnings(tweet)[0] == 'earnings slide')
    assert(account.parse_negative_earnings(tweet)[1] == 'higher credit expense')

    tweet = '$OESX - Orion Energy Systems reports FQ2 missed earnings; reaffirms 2H and updates FY23 guidance'
    assert(account.parse_negative_earnings(tweet)[0] == 'missed earnings')

    tweet = '$PEI - PREIT posts Q3 FFO loss, focuses on raising capital, paying down debt'
    assert(account.parse_negative_earnings(tweet)[0] == 'Q3 FFO loss')

    tweet = '$RCM - R1 RCM slumps 39% on dismal Q3 result, CEO change'
    assert(account.parse_negative_earnings(tweet)[0] == 'dismal Q3 result')

    tweet = '$USNZY $USNZ - High costs, low volumes weigh on miner Usiminas Q3 results'  # earnings -, high cost, low volumes
    assert (account.parse_earnings_indicator(tweet).groupdict()['earnings_indicator'])
    assert(account.parse_negative_earnings(tweet)[0].lower() == 'high costs')
    assert(account.parse_negative_earnings(tweet)[1] == 'weigh on miner Usiminas Q3 result')
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
    assert(account.parse_negative_earnings(tweet)[0] == 'Q3 EPS miss')
    assert(account.parse_negative_earnings(tweet)[1] == 'disappointing margin')
    assert(not account.parse_positive_earnings(tweet))

    tweet = '$SEM - Select Medical sinks ~21% after rise in costs and expenses leads to big Q3 profit miss'
    assert (account.parse_earnings_indicator(tweet).groupdict()['earnings_indicator'])
    assert (account.parse_negative_earnings(tweet)[0] == 'rise in costs')
    assert(account.parse_negative_earnings(tweet)[1] == 'Q3 profit miss')
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
    assert(account.parse_negative_earnings(tweet)[0] == 'weigh on result')
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
    assert(account.parse_negative_earnings(tweet)[0] == 'earnings decline')
    assert(account.parse_negative_earnings(tweet)[1] == 'asset values drop')
    assert(account.parse_negative_earnings(tweet)[2] == 'outflows rose')
    assert(not account.parse_positive_earnings(tweet))

    tweet = '$B - Barnes Group Q3 profit matches analyst estimates while revenue slips on forex'  # Q3 = earnings, slips -, matches =
    assert (account.parse_earnings_indicator(tweet).groupdict()['earnings_indicator'])
    assert(not account.parse_positive_earnings(tweet))
    assert(account.parse_negative_earnings(tweet)[0] == 'revenue slip')

    tweet = '$SJW - SJW reports Q3 earnings miss; reaffirms FY22 guidance'  # # earnings, = - miss, no tweet
    assert (account.parse_earnings_indicator(tweet).groupdict()['earnings_indicator'])
    assert(not account.parse_positive_guidance(tweet))
    assert(account.parse_negative_earnings(tweet)[0] == 'Q3 earnings miss')

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
    assert (len(account.parse_negative_earnings(tweet)) == 2)

    tweet = '$ORC - Orchid Island Capital posts Q3 loss on widening spreads after Fed rate hikes'  # earnings, repeats tweet
    assert (account.parse_earnings_indicator(tweet).groupdict()['earnings_indicator'])
    assert (account.parse_negative_earnings(tweet)[0] == 'Q3 loss')
    assert (len(account.parse_negative_earnings(tweet)) == 1)


def test_mixed_or_neutral():
    account = Marketcurrents(Marketcurrents.account_name)

    tweet = "$SHLS - Shoals sizzles after raising low end of revenue guidance; Northland upgrades"
    assert(not account.parse_positive_earnings(tweet))
    assert(not account.parse_negative_earnings(tweet))
    assert(account.parse_positive_guidance(tweet)[0] == 'raising low end of revenue guidance')
    assert(not account.parse_negative_guidance(tweet))

    tweet = '$ZIM - ZIM stock gains after earnings beat; analysts unfazed by downbeat guidance'
    assert(account.parse_positive_earnings(tweet)[0] == 'earnings beat')
    assert(account.parse_negative_guidance(tweet)[0] == 'downbeat guidance')

    tweet = '$NOV - Oilwell equipment and tech provider NOV posts mixed Q3'
    assert (account.parse_earnings_indicator(tweet).groupdict()['earnings_indicator'])
    assert(not account.parse_positive_earnings(tweet))
    assert(not account.parse_negative_earnings(tweet))

    tweet = "$BHG - Bright Health Group reports Q3 mixed earnings; revises Fy22 guidance"
    assert (not account.parse_positive_guidance(tweet))

    tweet = '$DTM - DT Midstream reports Q3 earnings; raises FY22 and FY23 Adjusted EBITDA guidance'  # earnings + => raises
    assert (account.parse_earnings_indicator(tweet).groupdict()['earnings_indicator'])
    assert (not account.parse_positive_earnings(tweet))

    tweet = "$AMC - AMC Entertainment Q3 results beat estimates, co's adj. EBITDA loss widens"
    assert(account.parse_positive_earnings(tweet)[0] == 'Q3 results beat')
    assert(account.parse_negative_earnings(tweet)[0] == 'EBITDA loss')

    tweet = '$NCLH - Norwegian Cruise Lines sails to earnings beat, offers upbeat occupancy forecast'
    assert(account.parse_positive_earnings(tweet)[0] == 'earnings beat')
    assert(account.parse_positive_guidance(tweet)[0] == 'upbeat occupancy forecast')

    tweet = '$THS - TreeHouse Foods slides after margins disappoint despite higher pricing'
    assert(account.parse_positive_earnings(tweet)[0] == 'higher pricing')
    assert(account.parse_negative_earnings(tweet)[0] == 'margins disappoint')

    tweet = '$NEWT - Newtek Business Q3 adjusted NII climbs from a year ago, but falls short of consensus'
    assert(account.parse_positive_earnings(tweet)[0] == 'NII climb')
    assert(account.parse_negative_earnings(tweet)[0] == 'falls short of consensus')

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
    t = "$PTC - PTC buys ServiceMax in $1.46B deal to boost PLM portfolio"
    t = "$KKR - KKR looks to sell Westbrick Energy for as much as C$2B - report"
    t = "$FCPT - Four Corners Property announces $6.1M acquisition of Caliber Collision property"
    t = "$SCU - Sculptor Capital gains after board forms committee to explore potential interest"
    t = "$LGIQ - Logiq signs LOI to acquire PrivCo"
    t = "$IRM - Iron Mountain acquires XData Properties"
    t = "$WAB - Wabtec to acquire Super Metal"
    t = "$GLOB - Globant acquires Australia's digital commerce consultancy eWave expanding its footprint in several Asian countries"
    t = "$FSS - Federal Signal to acquire Blasters for $14M"
    t = "$MLAB - Mesa Labs acquires Belyntic’s peptide purification business"
    t = "$STRH - Star8 acquires technology integrator, Hyper 30 Data"
    t = "$PSHG - Performance Shipping to buy tanker vessel from third party for $43.8M"
    t = "$HQI - HireQuest to acquire franchises from executive search firm MRINetwork for $13.5M"
    t = "$CW - Curtiss-Wright acquires UK firm Keronite for $35M"
    t= "$ACN - Accenture to acquire data science company ALBERT"
    t = "$BV - BrightView acquires South Carolina commercial landscaping firm"
    t = "$AN $TRUE - AutoNation takes minority ownership stake in TrueCar"
    t = "$EARI - EARI Beverage Group acquires Madre Agave"
    t = "$VEGYF $CURUF $CUR:CA - Consolidated Uranium buys Virginia Energy Resources for C32.2M"
    t = "$IOSP $EMNSF $ELMTY - Elementis may be seeing takeover interest - report"
    t = "$SIEN - Norman Pessin reports at 5.7% stake in Sientra, stock climbs 10%"
    t = "$EL $PPRUF $PPRUY - Estee Lauder agrees to acquire Tom Ford in $2.8B deal"
    t = "$OSK - Oshkosh to acquire Italian manufacturing equipment firm Hinowa for €186M"
    t = "$TINV - SPAC Tiga shareholders approve merger with dating app Grindr"
    t = "$BG - UPL's Advanta Seeds and Bunge intends to acquire a 20% stake in SEEDCORP|HO"
    t = "$WTFC - Wintrust to acquire North American asset management units from Rothschild &amp; Co"
    t = "$INVVY $OPNT $IZQVF - Opiant surges 123% as Indivior set to acquire overdose therapy maker for $145M"
    t = "$URI - United Rentals to acquire equipment rental firm Ahern Rentals in ~$2B cash deal"
    t = "$UUUU $EFR:CA - Energy Fuels to sell Alta Mesa ISR project in $120M deal"
    t = "$PDCO - Patterson Companies to acquire Dairy Tech"
    t = '$CWH - Camping World to acquire RV dealership Ashley Outdoors'
    t = "$VNTR - Venator Materials surges on sale of iron ore business after wider Q3 loss"
    t = "$IBEX - Outsourcing company Ibex jumps 10% on report of takeover interest"
    t = "$TRI $TRI:CA - Thomson Reuters to acquire SurePrep for $500M in cash"
    t = "$AGBA - SPAC AGBA shareholders approve merger with China-focused fintech provider TAG"
    t = "$CBRE - CBRE buys lab systems support services provider Full Spectrum Group for $110M"
    t = "$OGFGF $OGFGY $BEP - Brookfield Renewable consortium leads $11.8B buyout offer for Australia's Origin Energy"
    t = '$GEF - Greif reaffirms annual guidance, announces Lee Container acquisition'
    t = '$GTLS - Chart Industries to acquire Howden for $4.4B'
    t = "$ELV - Elevance Health to acquire speciality pharmacy from CarepathRx"
    t = '$RADI - Radius Global jumps 13% on speculation of takeover interest'
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
    t = '$MRNA - Moderna Omicron boosters outperform, but with lower response to latest variant'
    t = "$MO $JUUL - Juul Labs gets lifeline to avoid bankruptcy, plans to cut 30% of workforce"
    t = "$DIS - Disney slips 7% as media side profits, revenue slip; subscribers top forecasts"

def news_pos():
    t = "$POST $BRBR - Post Holdings stock pricing actions promote stronger than expected profits"
    t = "$ALGT - Allegiant Travel Company reports more passengers in October, compared to pre-pandemic level"
    t = "$NCRA - Nocera rises 18% as it records $3M revenue in October from eel fish sales in Japan"
    t = "$GRFX - Graphex Group stock jumps 24% amid filing related to graphite processing JV"
    t = "$DIS - Disney World boosts prices as parks demand continues surge"
    t = "$PANW - Palo Alto Networks pops after Loop Capital upgrade"
    t = "$AZN $VTRS - Viatris wins court decision on AstraZeneca Symbicort patent"
    t = "$PSNY $PSNYW - Polestar stock drives higher after sales double from prior year"
    t = "$INCR $INCR.U:CA - InterCure reports record preliminary Q3 revenue of of C$39M"
    t = "$PEP $CELH $MNST - Celsius stock surges on strong sales, profit growth"
    t = '$WT - WisdomTree says organic growth accelerated to nearly 14% YTD through October'
    t = '$VVPR - VivoPower subsidiary surges 16% as Tembo enters supply agreement for EV conversion kits'
    tweet = '$BSTG - Regenerative therapy developer Biostage files for Nasdaq uplisting, $6M offering'  # +, uplisting
    t = '$CUBT - Curative Biotechnology refiles for NYSE uplisting, $8M offering'
    t = '$DASH - DoorDash stock pops over 10% as analysts applaud resilience to macro pressures'
    t = '$CHUY - Chuys stock charges higher on strong comparable sales, profit growth'
    t = '$STEM - Stem stock rises on strong Q3 bookings'
    t = '$FSLR - First Solar soars to 11-year high as analyst touts extraordinary backlog'
    t = '$LEG - Leggett &amp; Platt shares lifted as earnings exceed lowered expectations'
    t = '$AMZN $HD $SBUX - Home Depot workers vote against unionization in first store test'
    t = '$ORGS - Orgenesis jumps 26% on $50M investment from Metalmark Capital'

def news_neg():
    t = '$PBI - Pitney Bowes stock plummets after reporting e-commerce contraction'
    t = "$NOTV - Inotiv nears 52-week low as employees of suppliers face charges for illegally importing non-human primates into U.S."
    t = "$ZI - lZoomInfo plunges 25% as fears grow over cloud-software company's sales outlook"
    t = "$JPM - JPMorgan Chase credit card net charge-offs, delinquencies tick up in October"
    t = "$COF - Capital One stock falls as credit losses rise; BofA downgrades to Neutral"
    t = "$THO $WGO $LCII - Winnebago drops sharply after warning on near-term softening of RV market"
    t = "$C - Citibank credit card delinquency, charge-off rates continue rising in October"
    t = "$MMM $DD - 3M, Dupont sued by California AG over toxic 'forever chemicals'"
    t = "$APRN - Blue Apron stock plummets over 30% on dilution fears"
    t = '$OLPX - Olaplex stock slips on slowing sales, cautious forecast'
    t = '$META - Facebook to receive antitrust charges over Marketplace ads platform: report'
    t = '$COTY - Coty shares carry higher on strong fragrance, consumer beauty sales'
    t = "$VZLA $VZLA:CA - Vizsla Silver shares slump after C$20M bought deal offering"
    tweet = '$AHG - Akso Health gets Nasdaq notice for not complying with minimum bid price rule'  # -, not complying
    tweet = '$YMAB - Y-mAbs fails to win FDA AdCom backing for neuroblastoma therapy'  # -, fails to win FDA
    tweet = '$BX $KKR $APO - KKR, Apollo, Blackstone face Justice Department probe on influence over boards'  # - face probe
    tweet = '$COF - Capital One credit card delinquency, net charge-off rates climb in September'  # -, industry, delinquency climbs =>IGNORE
    tweet = '$ALRM $VVNT - https://t.co/LStNLDdfU5 stock slips 3% after the bell on licensing dispute with Vivint'  # news, licensing dispute
    t = '$AXL $MLSPF - American Axle sinks 18% after denying sales talks'
    t = '$DAL - Delta pilots vote ‘overwhelmingly in favor’ of strike authorization'
    t = '$GT - Goodyear Tire stock skids as cost inflation, currency concerns impact earnings'
    t = '$MRNS - Marinus Pharmaceuticals stock drops 19% aftermarket on proposed public offering'
    t = '$ATHX - Athersys tumbles 40% after the bell on proposed stock offering'
    t = '$VRM - Vroom sees sales plummet, adjusted EBITDA go negative in Q3'
    t = "$RBA $IAA $RBA:CA - Ritchie Bros. plunges 20% on IAA purchase, deal called a 'head-scratcher'"
    t = "$JUPW $JWAC - Jupiter Wellness stock falls 13% on plans to spin off Caring Brands"
    t = "$ARVL - Arrival stock plunges as it expects no revenue until 2024 with insufficient cash"
    t = "$WKHS - Workhorse stock sinks on wider than expected loss"

def dividends():
    t = "$SJT - San Juan Basin Royalty Trust halves dividend to $0.1719" # halves
    t = "$DVY $VYM $DGRO - FY dividends forecast upgraded after 'encouraging Q3'"
    t = "$BRMK - Broadmark Realty stock slumps after dividend slashed to cover distributable EPS"
    t = "$MLGF - Malaga Financial declares special 5% year-end stock dividend"
    t = "$SYZLF $SYZ:CA - Sylogist cuts dividend by 92% to C$0.01/share"
    t = "$OCSL - Oaktree Specialty Lending raises quarterly dividend by 5.9%"
    t = "$KINS - Kingstone stock slips as inflationary pressure weigh on Q3 results; suspends dividend"
    t = "$MAR - Marriott raises dividend by 33.3% to $0.40/share, boosts share buyback plan"
    tweet = '$TAIT - Taitron Components raises dividend by 11% to $0.05'  # +, raises dividend
    t = '$ABC - AmerisourceBergen increases dividend by ~5%'
    tweet = '$ZION - Zions declares $0.41 dividend, approves up to $50M buyback'  # + buyback
    tweet = 'Wells Fargo Multi-Sector Income Fund lowers dividend by 4.1%'  # -, lowers dividend
    tweet = '$FTAI - Fortress Transportation dividend declines by 10% to $0.30'  # - dividend declines
    t = "$HQH - Tekla Healthcare Investors declines quarterly dividend by -2.5% to $0.39/share"
    t = "$OLY:CA - Olympia Financial Group raises monthly cash dividend by 29%"
    t = '$ETO - Eaton Vance Tax-Advantaged Global Dividend Opportunities Fund dividend declines by 23.3% to $0.1374'
    t = '$CRF - Cornerstone Total Return Fund reduces monthly dividend'
    t = '$FLGMF $MHC.UN:CA - Flagship Communities Real Estate Investment Trust decreases dividend by ~92%'
    t = "National Research Corporation slashes dividend to $0.12"
    t = "$HVT - Haverty Furniture declares $0.28 quarterly, $1 special dividend"

def splits():
    t = "$DNRSF $DSLV:CA - Denarius Metals announces 10:1 share consolidation"
    t = "$SNES - SenesTech shoots 120% on reverse stock split"
    t = "$KTRA - Kintara Therapeutics to effect 1-for-50 reverse stock split"
    t = "$TRVN - Trevena slides 18% after the bell on 1-for-25 reverse stock split"
    t = '$KERN - Akerna announces 20-for-1 reverse stock split; shares down 19%'
    t = '$ONCS - OncoSec stock plummets 26% on 1-for-22 reverse stock split'
    t = '$BBLN - Babylon to execute 1-for-25 reverse share split'
    t = "$AMPE - Ampio Pharmaceuticals to implement 1-for-15 reverse stock split"
    t = '$TMBR - Timber Pharmaceuticals announces 1-for-50 reverse stock split'

def exec():
    t = "$RKT $RXT - Rackspace Technology appoints Bobby Molu as chief financial officer"
    t = "$V - Visa names president McInerney as new CEO, Kelly to become executive chairman"
    t = "$AMED - Amedisys CEO Chris Gerard leaves company, effective immediately"
    t = "$HCMLF $HCMLY - Holcim appoints Steffen Kindler as CFO"
    t = "$AVHHL $RCEL - AVITA Medical appoints Jim Corbett as CEO"
    t = "$TRTN - Michael Pearl is the new finance chief of Triton international"
    t = "$OFIX $SPNE - Orthofix, SeaSpine report John Bostjancic will serve as CFO for combined company"
    t = "$CWQXF $CWQXY - Castellum CFO Maria Strandberg steps down"
    t = "$MPZZF - MPC Container Ships appoints Moritz Fuhrmann as new CFO"
    t = "$KPLT - Katapult hires new finance chief"
    t = "$IPG - Interpublic Group promotes Cavallo to Global CEO of MullenLowe Grou"
    t = "$HUBG - Hub Group announces several leadership changes"
    t = "$MOG.A $MOG.B - Moog CEO John Scannell to retire"
    t = "$SGA - Saga Communications taps new CEO to lead after founder's death"
    t = "$CURO - CURO Group names Doug Clark as new CEO"
    t = "$SFLM - SFLMaven appoints new key person and to divest its operating subsidiary, SFLMaven of Florida"
    t = "$ENDMF $ENDR:CA - Enduro Metals names new president"
    t = "$GGAZF - Goldgroup Mining announces CEO departure"
    t = "$OBGRF $OGD:CA - Eric Alexandre to step down from helm of Orbit Garant Drilling"
    t = "$TSSI - TSS trades lower after Q3 results, CEO departure announcement"
    t = "$TER - Teradyne appoints CEO"
    t = "$QSR $QSR:CA - Patrick Doyle joins Restaurant Brands as executive chairman"
    t = "$MCG - Membership Collective CEO steps down"
    t = '$EVA - Enviva names Meth as next CEO; Keppler to become Executive Chairman'
    t = "$DUOT - Duos Technologies names Andrew Murphy as CFO"

def buyback():
    tweet = "$BFIN - BankFinancial adds 300,000 shares to existing share repurchase program"  # + repurchase
    t = "$LPRO - Open Lending launches up to $75M share repurchase program"
    t = "$RVSB - Riverview Bancorp to launch up to $2.5M stock repurchase program"
    t = "$PRI - Primerica launches $375M share buyback"
    t = "$LX - LexFintech stock climbs after new $20M stock buyback program, Q3 results"
    t = "$FUSB - First US Bancshares extends stock buyback program"
    t = "$DFS - Discover Financial stock perks up after stock buyback program resumes"
    t = "$OSG - Overseas Shipholding Group climbs 6% on share repurchase"
    t = "$GPI - Group 1 Automotive raises buyback authorization, dividend"
    t = "$CUEN - Cuentas stock rallies as company proposes buyback plan"
    t = "$TRIN $TRINL - Trinity Capital announces $25M stock repurchase program"
    t = "$TMO - Thermo Fisher Scientific announces $4B stock buyback program"
    t = "$UCBI - United Community Banks declares $0.22 dividend and authorizes $50M buyback"
    t = "$STLD - Steel Dynamics declares $0.34 dividend, additional $1.5B share buyback plan"
    t = "Steel Dynamics declares $0.34 dividend and authorizes $1.5B buyback"
    t = "$AEL - American Equity Investment Life announces additional $400M stock buyback"
    t = "$SNAL - Newly public Snail stock rallies 42% following buyback news after weak debut"
    t = "$TUYA - Tuya announces $50M stock buyback program"
    t = '$NILE $GIGA - BitNile to distribute ~7M Giga-tronics shares to stockholders'
    t = '$PSX - Phillips 66 plans to return $10B -$12B to shareholders by 2024 end'
    t = '$AMPH - Amphastar authorizes $50M buyback'
    t = '$LXU - LSB Industries prices offering of $14.35M shares and plans to repurchase 3.5M shares'
    t = '$OEC - Orion Engineered Carbons announces $50M share buyback program'
    t = '$DQ - Daqo New Energy announces $700M stock buyback program'
    t = '$LAD - Lithia &amp; Driveway boosts share repurchase authorization by $450M'
    t = '$GDL $GFELF $GDL:CA - Goodfellow to buy back stock via NCIB'
    t = '$ENVA - Enova International expands stock buyback program to $150M'
    t = "$HLT - Hilton raises stock repurchase authorization by $2.5B to $3.4B"

def guidance():
    t = "$AMED - Amedisys reaffirms FY22 guidance"

def listing():
    tweet = '$PME - Chinese fisher Pingtan gets Nasdaq minimum bid compliance notice'  # - compliance notice
    tweet = '$WNW - Meiwu Technology regains compliance with Nasdaq minimum bid price requirement'
    t = "$HFFG - HF Foods gets another non-compliance letter from Nasdaq"
    t = "$AMPED - Ampio Pharmaceuticals announces NYSE American removal of trading suspension"
    t = "$GOTU - Gaotu Techedu receives NYSE non-compliance letter"
    t = "$UCL - uCloudlink regains compliance with Nasdaq listing rules"
    t = "$MOXC - Moxian (BVI) gets non-compliance from Nasdaq regarding minimum bid price"
    t = "$MF - Missfresh once again in compliance with Nasdaq filing rules"
    t = "$ARAV - Aravive regains compliance with Nasdaq minimum bid price requirement"
    t = "$STRY - NYSE notifies Starry of non-compliance with minimum bid price requirement"
    t = "$NLSP - NLS Pharma rises 9% on approval from Nasdaq to continue listing"
    t = "$QNGY - Quanergy Systems intends to appeal NYSE's delisting decision"
    t = '$HOTH - Hoth Therapeutics regains compliance with Nasdaq listing rules'
    t = '$CYTO - Altamira Therapeutics regains listing compliance with Nasdaq'
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
    t = "$H $HZN - Horizon Global gets NYSE notice for listing deficiency"
    t = "$CEI - Camber Energy gets non-compliance letter from NYSE American"
    t = "$KLR - NYSE sends minimum bid price requirement-related notice to Kaleyra"
    t = "$UPC - Nasdaq notifies Universe Pharmaceuticals on regaining compliance with minimum price requirement"

def wins():
    t = "$BVNKF $BVNRY $BAVN - Bavarian Nordic to supply up to 2M doses of monkeypox vaccine to EU"
    t = "$DSX - Diana Shipping signs time charter deals for m/v DSI Aquila, m/v Houston"
    t = "$ESLT - Elbit Systems secures $200M contract to supply helicopter self-protection suits to a country in Asia-Pacific"
    t = "$F $ROK - Ford selects Rockwell to drive EV program"
    t = "$BW - Babcock &amp; Wilcox wins $24M+ contract"
    t = "$BLDP $BLDP:CA - Ballard Power's repeat customer orders 25 engines"
    t = "$MDGS $PRZO - ParaZero Technologies secures SafeAir safety systems' order: Medigus"
    t = "$GD - General Dynamics awarded $181.98M contract by Navy"
    t = "$BAESF - BAE Systems awarded $153.74M modification contract"
    t = "HEXO $ETRGF $ENTG:CA - Hexo signs 3-year cannabis supply deal with Entourage Health"
    t = "$SMID - Smith-Midland gets $7.7M contract from North Carolina Dept of Transportation"
    t = "$DARE - Daré gets Gates Foundation grant to develop Hydrogel tech for use in vaginal health"
    t = "$TYL - Tyler Technologies bags $54M agreement for US Department of State"
    t = "$CVEO - Civeo gets five-year contract renewal for integrated services in Australia"
    t = "$GVA - Granite JV bags more contracts for bridge rehabilitation project in Sacramento"
    t = "$FAMI - Farmmi secures high-volume order for export to Guam"
    t = "$TEDU - Tarena International gets added in China's list of approved education providers"
    t = "$CYN - Cyngn shares surges on signing contract to deploy autonomous industrial vehicles for U.S. Continental"
    t = "$BEEM - Beam Global gets a $29.4M order from TechFlow"
    t = "$STRL - Sterling Infrastructure unit gets $20M contract from US Customs &amp; Border Protection"
    t = "$BW - Babcock &amp; Wilcox secures over $42M upgrade and maintenance project"
    t = "$SAIC - Science Applications International wins $757M U.S. Army contract"
    t = "$NVEE - NV5 Global bags $15M cultural resources contract"
    t = "$DM - Desktop Metal bags $2M contract from US Dept of Veterans Affairs"
    t = "$ALLG - Allego inks first long-term PPA for renewable power"
    t = "$LEU - Centrus Energy wins first U.S. award to make next-generation nuclear fuel"
    t = "$ORN - Orion Group announces over $40M contract award"
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
    t = "$GCI - Gannett launches new round of layoffs in news"
    t = "$CVNA - Carvana slides after confirming plan to lay off 8% of workforce"
    t = "$ROKU - Roku cutting jobs by 5% to slow 2023 expense growth"
    t = "$TWTR $TSLA $SPACE - Fired SpaceX employees claim unfair labor practices, call out Elon Musk"
    t = "$TCEHY - Tencent reportedly begins new round of layoffs"
    t = "$ILMN - Illumina to shed 5% of global headcount"
    t = "$TCDA - Tricida to lay off ~60% of employees following strategic review announcement"
    t = "$FDX - FedEx to furlough freight workers through holiday season"
    t = '$META - Meta to cut 11,000 jobs, affirms revenue outlook'
    t = '$ZEN - Zendesk cuts ~300 jobs globally - SEC filing'
    t = '$X - U.S. Steel reaches tentative deal with steelworkers union, includes 5% base wage hike'
    t = '$META - Meta Platforms shares rise with big layoffs expected this week'
    t = '$RAMP - LiveRamp announces 10% workforce reduction, downsizes real estate footprint'

def patent():
    t = "$AVDL $JAZZ - Avadel Pharmaceuticals jumps on patent decision in dispute with Jazz Pharma"
    t = "$BEAT - HeartBeam receives patent for ECG smartwatch for detection of heart attacks"

def pharma_pos():
    tweet = '$PHGUF $PHAR - Pharming gets EMA accelerated review of leniolisib for rare immunodeficiency disorder'  # + => accelerated review
    tweet = '$OTLK - FDA accepts Outlook Therapeutics biologics license application for wet AMD drug'
    t = "$PDSB - PDS Biotech surges 22% as drug shows response in cervical cancer patients in phase 2 trial"
    t = "$BHC $BHC:CA - Bausch Health up 11% after draft FDA guidance makes it harder for Xifaxan generics"
    t = "$NWBO - Northwest achieves positive phase 3 results for glioblastoma candidate; shares rise 24%"
    t = "$ISEE - IVERIC bio gets FDA breakthrough therapy designation for geographic atrophy treatment"
    t = "$PRVB - Provention Bio's type 1 diabetes med teplizumab wins FDA approval"
    t = "$SNY - Sanofi's rare blood disorder drug Enjaymo gets approval in EU"
    t = "$MGNX $PRVB - MacroGenics to get $60M milestone from Provention as FDA approves diabetes drug Tzield"
    t = "$LLY $SNY $VTRS - Lilly's interchangeable insulin biosimilar to Sanofi's Lantus gets FDA approval"
    t = "$PFE $BNTX - Pfizer, BioNTech Omicron BA.4/BA.5 bivalent booster shot shows response vs emerging subvariants"
    t = "$KMPH - FDA awards Orphan Drug Designation to Kempharm for idiopathic hypersomnia candidate"
    t = "$NVAX - Novavax trades higher as COVID vaccine gets approval in Canada as booster"
    t = "$REVB - Revelation biosciences says REVTx-300 significantly reduced collagen deposition in preclinical model"
    t = "$ASND - Ascendis, Visen' once-weekly growth hormone drug beats daily hGH in Chinese patients in trial"
    t = "$ALPMF $ALPMY - Astellas zolbetuximab shows survival benefit, meets main goal in gastric cancer trial"
    t = "$BGNE - BeiGene Brukinsa gets approval in EU for expanded use in leukemia"
    t = "$PTCT - PTC Therapeutics gene therapy Upstaza for rare neuromuscular disorder gets approval in UK"
    t = "$REGN $CTMX - CytomX surges 26% on license deal with Regeneron to develop cancer drugs"
    t = "$RDHL - RedHill Biopharma rises 6% on positive data from opaganib for nuclear radiation injury"
    t = "$ARQT - Arcutis' psoriasis cream Zoryve added to Express Scripts national formularies"
    t = "$LIVN - LivaNova receives FDA clearance for extracorporeal membrane oxygenation for LifeSPARC"
    t = "$ARDX - Ardelyx soars 40% following FDA advisory panel endorsement of kidney disease drug tenapanor"
    t = "$PFE $DSKYF $DSNKY - Daiichi Sankyo mRNA COVID vaccine meets main goal in trial as booster shot"
    t = "$RHHBY $IMGN $RHHBF - Roche's Ventana test gets FDA approval for use with ovarian cancer drug Elahere"
    t = "$RHHBY $RHHBF - Roche monkeypox test authorized by US FDA"
    t = "$ANIP - ANI Pharmaceuticals launches generic antibiotic trimethoprim with FDA approval in bag"
    t = "$ABBV - AbbVie's migraine med Ubrelvy approved in Canada"
    t = "$INBX - Inhibrx's drug for rare bone cancer shows promise in ongoing phase 1 study"
    t = "$LUMO - Lumos growth hormone deficiency candidate meets expectations in mid-stage trials"
    t = "$PLX - Protalix stock rises on on FDA refiling for Fabry disease drug PRX–102"
    t = "$INMB - INmune receives green signal from Canada to begin trial of XPro1595 in mild Alzheimer’s Disease"
    t = "$APGN - Apexigen stock jumps 14% as cancer drug sotigalimab shows promise in phase 2 study"
    t = "$AGEN - Agenus spikes on Phase 1 data for cancer candidates"
    t = "$BTAI - BioXcel stock soars 17% as lead drug Igalmi starts to bring in revenue"
    t = "$TAK - Takeda's blood clot disorder therapy gets EMA panel nod for expanded use"
    t = "$TAK - Takeda Livtencity gets approval in EU for cytomegalovirus infection in transplant patients"
    t = "$AGIO - Agios granted EU approval for Pyrukynd in pyruvate kinase deficiency"
    t = "$SNY - Sanofi's heart disease therapy DuoPlavin gets EU drug regulator's nod for expanded approval"
    t = "$SNY - Sanofi's heart drugs get EMA panel nod for expanded use"
    t = "$AZN - AstraZeneca gets China drug regulator's review for expanded use of Soliris"
    t = "$AZN - AstraZeneca Imjudo, Imfinzi combo approved for non–small cell lung cancer"
    t = "$MRK $AZN - AstraZeneca/Merck's Lynparza gets EMA panel's greenlight for expanded use in prostate cancer"
    t = "$AZN $DSKYF $DSNKY - Daiichi Sankyo wins EU backing for Enhertu in gastric cancer"
    t = "$RHHBY $RHHBF - Roche influenza therapy Xofluza gets EMA committee nod for use in children"
    t = "$IMMX - Immix Biopharma gets review board nod to enroll kids in upcoming cancer therapy trial"
    t = "$JNJ - J&amp;J analysis: Early Tremfya efficacy in psoriatric arthritis can predict long-term response"
    t = "$IPSEF $IPSEY - Ipsen Onivyde combo meets trial's survival goal in untreated pancreatic cancer patients"
    t = '$IPSEF $IPSEY $MACK - Merrimack jumps 183% as partner Ipsen says pancreatic cancer trial met main goal'
    t = '$NRXP - NRx Pharma announces commercial production of drug targeted at suicidal depression'
    t = '$CLSD - Clearside stock rises as CLS-AX shows promise in early-stage study in eye disorder'
    t = '$PFE $BNTX - Pfizer/BioNTech win U.K. nod for second Omicron booster'
    t = '$PFE $NVAX $BNTX - Novavax COVID-19 shot authorized as booster in UK'
    t = '$IMMP - Immutep gets patents in Japan, South Korea linked to immunotherapy eftilagimod'
    t = '$VERU $BIOVF - Sobi wins FDA nod for COVID-19 therapy'
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
    tweet = '$SBHMY $FSTX - F-star Therapeutics drops amid concern about CFIUS approval for Sino-Biopharma'  # - drops, can't use 'approval' on its own
    t = "$INO - Inovio ends development of candidates for Lassa fever and Middle East Respiratory Syndrome"
    t = "$EDIT - Editas pausing enrollment of blindness drug trial to find partner; shares down 15%"
    t = "$STSA - Satsuma cut to neutral at Mizuho following migraine drug failure"
    t = "$MNPR - Monopar stock falls 20% amid preliminary phase 1 data for cancer drug camsirubicin"
    t = "$BIIB $RHHBY $ESALY - Roche faces another setback in Alzheimer's as gantenerumab fails 2 phase 3 trials"
    t = "$SLS - SELLAS falls 39% on delay for key milestone for cancer drug"
    t = "$BMRN $ASND - Ascendis falls after reporting Phase 2 data for achondroplasia candidate"
    t = '$MDT - Medtronic says trial for renal denervation system did not meet main goal in hypertension'
    t = "$OMER - Omeros appeal of FDA Complete Response Letter on narsoplimab denied; shared down 7%"
    t = '$VERV - Verve sheds 22% as FDA holds trial application for gene editing drug'
    t = '$GSK - GSK barred from bulk drug purchasing program in China for 18 months'
    t = '$ABBV - AbbVie candidate for postoperative atrial fibrillation fails in mid-stage trial'
    t = "$GSK $BMY - GSK's blood cancer therapy Blenrep fails to meet main goal in phase 3 study"
    t = "$OMER - Omeros downgraded at Bank of America after FDA snub for narsoplimab appeal"

def bankruptcy():
    t = "$FSRD - Cloud manufacturing firm Fast Radius slides after establishing timeline for Chapter 11 sale process"
    t = '$FSRD - Fast Radius announces Chapter 11 filing to complete its marketing and sale process'

def insider():
    t = "$MC - Moelis slumps after top brass dumps stock"
    t = "$NN - NextNav's executive leaders sell ~796,000 shares"
    t = "$VTRS - DOJ, SEC charge Viatris executive with insider trading; co says he is on leave of absence"

def offerings():
    t = '$FAT - FAT Brands slides after withdrawing stock offering'
    t = '$ROIV - Roivant Sciences falls 7% after hours on $150M stock offering'
    t = "$SAVA - Cassava Sciences down 9% following $50M registered direct offering"
    t = "$VERX - Vertex falls 6% postmarket on proposed secondary stock offering"
    t = "$GTHX - G1 Therapeutics stock slides on pricing $50.05M stock offering"
    t = "$RAPT - RAPT Therapeutics announces $75M stock offering"
    t = "$RAPT - RAPT Therapeutics stock slide on pricing ~$75M stock offering"
    t = "$QFIN - 360 DigiTech dips on commencing global offering"
    t = "$LAUR - Laureate Education prices underwritten secondary offering of 32.8M shares"
    t = "$INM $IN:CA - InMed Pharmaceuticals dips after pricing ~$6M private offering"
    t = "$LILM - Lilium dips after announcing pricing of $119M fundraising"
    t = "$TFFP - TFF Pharma slips 22% on $10.68M public offering"
    t = "$TFFP - TFF Pharmaceuticals tumbles 25% after hours on proposed stock offering"
    t = "$BNOEF $BNOX - Bionomics slides on pricing ADS offering at $7.80"
    t = "$ORA - Ormat slumps 9% as stockholder Orix prices offering to sell $337.5M shares"
    t = "$DZSI - DZS falls 8% after hours on proposed stock offering"
    t = "$ECVT - Ecovyst prices upsized 17.5M secondary offering at $8.25/share"
    t = "$CRSR - Corsair Gaming slides after pricing $75M stock offering"
    t = "$ENV - Envestnet prices upsized $500M convertible notes offering"
    t = "$DXR - Daxor to raise $2M in stock offering"
    t = "$CSWC - Capital Southwest dips after pricing ~$38.2M stock offering"
    t = "$CMNDF - Psychedelic drug developer Clearmind stock slides following uplisting, $8M offering"
    t = "$DNA - Ginkgo Bioworks falls over 5% postmarket on $100M stock offering"
    t = "$ASLE - AerSale dips 5% after hours on secondary stock offering"
    t = "$CCL $CUK - Carnival stock slides 11% after the bell on $1B senior note offering"
    t = "$CCL $CUK $CUKPF - Carnival Corporation shares slide on pricing $1B debt offering for refinancing 2024 maturities"
    t = "$URI - United Rentals to raise $1.5B of 6.00% senior secured notes due 2029 in a private offering"
    t = "$OKE - ONEOK prices $750M senior notes offering"
    t = "$WOLF $BWA - Wolfspeed dips on $1.3B convertible notes offering"
    t = "$LAUR - Laureate Education dips on stock offering by sellers"
    t = "$BKD - Brookdale Senior Living dips on offering of tangible equity unit"
    t = "$CRSR - Corsair Gaming slides ~10% after the bell on $75M stock offering"
    t = "$DXR - Daxor tumbles 11% aftermarket on proposed stock offering"
    t = "$ESAB - ESAB launches underwritten offering of 6M shares"
    t = "$SRGA - Surgalign Holdings to raise $12M in direct stock offering"
    t = "$CDZI - Cadiz announces $10M direct placement"
    t = "$REXR - Rexford Industrial announces stock offering of 11.5M shares"
    t = "$REXR $REXR.PB $REXR.PC - Rexford Industrial Realty prices 11.5M stock offering at $56.00/share"
    t = "$RLYB - Rallybio prices $50M securities offering"
    t = "$ALIT - Alight announces 20M secondary stock offering, expands partner network"
    t = "$ATAT - Atour Lifestyle prices $52.3M IPO of ADSs"
    t = "$CGTX - Cognition Therapeutics prices $6M public offering"
    t = "$DV - DoubleVerify Holdings prices $260.40M secondary stock offering"
    t = "$ALTD - Sports education provider Altitude proposes $10M offering, Nasdaq uplisting"
    t = '$ZTS - Zoetis prices $1.35B senior note offering'
    t = '$HUM - Humana prices $1.23B debt offering'
    t = '$ROIV - Roivant Sciences stock dips on pricing stock offering'
    t = '$MRNS - Marinus Pharmaceuticals shares slide 18% on $60M securities offering'
    t = '$CAH - Cardinal Health files for mixed shelf offering'
    t = '$BXP - Boston Properties prices $750M offering of green bonds'

# Industry, auto peer detection
def industry():
    t = "$BIDU $BABA $JD - Alibaba slips on Q3 sales miss, Chinese tech stocks stutter"
    t = "$DB $MOS $DBA - Wheat leads grains lower as UN says Black Sea deal will continue"
    t = "$TGT $MAT $HAS - Toy stocks slump after Target warns holiday season demand could disappoint"
    t = "$AMZN $TDOC $HIMS - Amazon Clinic seen putting pressure on telehealth providers Him &amp; Hers Health, Teladoc"
    t = "$SQM $ALB $LAC - Lithium stocks slammed on talk of Chinese cutbacks, negative analyst note"
    t = "$SPWR $FSLR $TAN - Sunrun leads solar stocks higher as Deutsche Bank lauds strong U.S. presence"
    t = "$THO $WGO $LCII - Winnebago drops sharply after warning on near-term softening of RV market"
    t = "$DSX $EGLE $GOGL - Golden Ocean drags down shipping stocks after soft Q3 results"
    t = "$AMD $INTC $STX - Micron leads semiconductors lower as new capex cuts set to come next year"
    t = "$NAVI $SLM $NNI - Court keeps block on Biden's student loan debt forgiveness in place"
    t = 'LII $JCI $WSO - U.S. shipments of heat pumps jumped 27% in September amid broader slump'
    t = '$UNG $FCG $UNL - Natural gas trims gains as Freeport LNG likely to extend outage'
    t = "$BIIB $RHHBY $LLY - Cassava, Biogen lead Alzheimer's stocks higher following Roche's gantenerumab setback"
    t = "$EIX $SRE $PCG - Sunrun, others solars rip after California regulators lessen impact of solar subsidy rollback"
    t = "$KBH $TOL $PHM - Lennar, Pultegroup lead homebuilder stock surge after inflation pace slows"
    t = "$VMI - Valmont Industries secures nationwide drone waiver from FAA"
    t = "$UCO $USO $DBO - U.S. drilling rig count jumps in latest Baker Hughes report"
    t = "$UNH $CI $ELV - Health insurers plunge on above average volumes"
    t = "$XLV $AMGN $JNJ - Healthcare stocks fall across the board as traders move out of defensive sectors"
    t = "$WIX $GDDY $SQSP - GoDaddy, Wix and SquareSpace seeing 'massive' opportunity for website building"
    t = "$TSLA $BLNK $DRIV - XPeng, Arrival and Canoo lead big gains in the electric vehicle sector"
    t = "$AMD $INTC $TXN - Semiconductor stocks fall with Nvidia, AMD leading decline as Intel unveils new Xeon chips"
    t = '$EDU $TAL - Chinese education stocks slip on further regulation fears'
    t = '$SMH $PSI $INTC - Global semiconductors sales drop 3% in Q3 202'
    t = '$GTN $APO $GTN.A - Tegna falls as peer Gray Television plunges post results; Standard General refutes job cut claims'
    t = '$LI $NIO $XPEV - Chinese EV stocks jump on signal of Zero-COVID reconsideration'
    t = '$ARKG $ARKQ $ARKW - SARK, the anti-Cathie Wood ETF, has returned over 100% in its first year of trading'
    t = '$SWBI $RGR $SPWH - Election day means traders are watching firearm-related stocks for any recoil action'
    t = '$RCL $CCL $NCLH - Cruise stocks push higher after positive report from Norwegian'

def spac():
    t = "$GRND - Newly public Grindr stock soars as high as 515% following SPAC merger (update)"
    t = "$PUCK - SPAC Goal Acquisitions to merge with French fintech provider Digital Virgo"
    t = "$NWTN - Dubai-based EV maker NWTN stock tumbles for second day following SPAC merger"
    t = "$MJWL $OTEC $OTECU - Majic Wheels to merge with SPAC OceanTech Acquisitions in $200M deal"
    t = "$PRBM.U $PRBM $PRBMW - Energy harvesting firm EnOcean to go public via merger with SPAC Parabellum"

def activist():
    t = '$HZNP - Horizon Therapeutics ticks higher amid speculation of activist investor'
    t = "$MMM - 3M viewed as potential activist target after 13F filing"
    t = '$AIM - AIM Immunotech says court denies activist request on board nominees'

def ipo():
    t = "$SNAL - Game developer Snail stock tumbles 55% following downsized $15M IPO"
    t = "$ASPI $SNAL - ASP Isotopes stock drops 32% following downsized $5M IPO"
    t = "$ACRV - Acrivon stock rises modestly following $94M IPO, shares price below range"

def short():
    t = "$TWST - Twist Biosciences plunges 26% after new short report from Scorpion Capital"

def recalls():
    t = "$TSLA - Tesla recalls nearly 30K vehicles due to air bag issue"
