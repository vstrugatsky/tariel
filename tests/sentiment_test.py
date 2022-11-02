from loaders.twitter_marketcurrents import Marketcurrents


def test_parse_guidance():
    account = Marketcurrents(Marketcurrents.account_name)
    tweet = '$DTM - DT Midstream reports Q3 earnings; raises FY22 and FY23 Adjusted EBITDA guidance'
    assert(account.parse_positive_guidance(tweet)[0].strip() == 'raises FY22 and FY23 Adjusted EBITDA guidance')

    tweet = '$CVEO - CVEO GAAP EPS of $0.32 misses by $0.02, revenue of $184.2M beats by $10.39M, raises FY guidance'
    assert(account.parse_positive_guidance(tweet)[0].strip() == 'raises FY guidance')

    tweet = '$KIM - Kimco Realty FFO of $0.41 beats by $0.02, revenue of $433.4M beats by $15.98M, raises FY FFO guidance'
    assert(account.parse_positive_guidance(tweet)[0].strip() == 'raises FY FFO guidance')

    tweet = '$FISV - Fiserv Non-GAAP EPS of $1.63 misses by $0.06, revenue of $4.52B beats by $210M, raises FY earning guidance'
    assert(account.parse_positive_guidance(tweet)[0].strip() == 'raises FY earning guidance')

    tweet = '$OPCH - Option Care Health GAAP EPS of $0.20 in-line, revenue of $1.02B beats by $23.72M, raised FY22 guidance'
    assert(account.parse_positive_guidance(tweet)[0].strip() == 'raised FY22 guidance')

    tweet = '$LIN - Linde Non-GAAP EPS of $3.10 beats by $0.17, revenue of $8.79B beats by $470M, raises FY Adj. EPS guidance'
    assert(account.parse_positive_guidance(tweet)[0].strip() == 'raises FY Adj. EPS guidance')

    tweet = '$HRI - Herc GAAP EPS of $3.36 misses by $0.28, revenue of $745.1M beats by $20.99M; raises FY adj. EBITDA guidance'
    assert(account.parse_positive_guidance(tweet)[0].strip() == 'raises FY adj. EBITDA guidance')

    tweet = '$MTUAF - MTU Aero Engines AG GAAP EPS of €1.74, revenue of €1.35B, FY22 guidance lowered'
    assert(account.parse_negative_guidance(tweet)[0].strip() == 'guidance lowered')

    tweet = '$LHX - L3Harris plunges after Q3 miss, full-year guidance cut'
    assert(account.parse_negative_guidance(tweet)[0].strip() == 'guidance cut')

    tweet = '$TNC - Tennant Non-GAAP EPS of $0.99 misses by $0.11, revenue of $262.9M misses by $24.27M, lowers FY earning guidance'
    assert(account.parse_negative_guidance(tweet)[0].strip() == 'lowers FY earning guidance')

    tweet = '$STX - Seagate Technology Non-GAAP EPS of $0.48 misses by $0.23, revenue of $2.04B misses by $70M, issues Q2 guidance below the consensus'
    assert(account.parse_negative_guidance(tweet)[0].strip() == 'guidance below')

    tweet = '$TXN - Texas Instruments GAAP EPS of $2.47 beats by $0.08, revenue of $5.24B beats by $100M, guides below Q4 consensus'
    assert(account.parse_negative_guidance(tweet)[0].strip() == 'guides below')

    tweet = '$AEP - American Electric Power Non-GAAP EPS of $1.62 beats by $0.06, revenue of $5.5B beats by $750M, reaffirms FY earning guidance'
    assert(not account.parse_positive_guidance(tweet))
    assert(not account.parse_negative_guidance(tweet))

    tweet = '$INFY - Infosys GAAP EPS of $0.18 in-line, revenue of $4.55B beats by $110M, revises FY guidance'
    assert(not account.parse_positive_guidance(tweet))
    assert(not account.parse_negative_guidance(tweet))

    tweet = '$COHU - Cohu rallies 15% on Q3 estimates beat, provides Q4 guidance'
    assert(not account.parse_positive_guidance(tweet))
    assert(not account.parse_negative_guidance(tweet))

    tweet = '$GTLS - Chart Industries reports mixed Q3 earnings; narrows FY22 and issues FY23 guidance'
    assert(not account.parse_positive_guidance(tweet))
    assert(not account.parse_negative_guidance(tweet))

    tweet = '$CL - Colgate-Palmolive reports mixed Q3 result, raises sales forecasts'  # earnings + => mixed but raises, earnings tweet mixed
    assert(account.parse_positive_guidance(tweet)[0].strip() == 'raises sales forecast')
    assert(not account.parse_negative_guidance(tweet))

    tweet = '$GTLS - Chart Industries reports mixed Q3 earnings; narrows FY22 and issues FY23 guidance'  # earnings, mixed, no tweet
    assert(not account.parse_positive_earnings(tweet))
    assert(not account.parse_negative_earnings(tweet))
    assert(not account.parse_positive_guidance(tweet))
    assert(not account.parse_negative_guidance(tweet))


def test_parse_positive_sentiment():
    account = Marketcurrents(Marketcurrents.account_name)
    tweet = '$NOV - Oilwell equipment and tech provider NOV posts mixed Q3'
    assert(not account.parse_positive_earnings(tweet))
    assert(not account.parse_negative_earnings(tweet))

    tweet = '$AFRAF - Air France-KLM savors recovering air travel which boosts Q3 revenue'
    assert(account.parse_positive_earnings(tweet)[0].strip() == 'boost')
    assert(not account.parse_negative_earnings(tweet))

    tweet = '$IMO $IMO:CA - Imperial Oil results surpass estimates as downstream strength continues'  # + surpass, strength
    assert(account.parse_positive_earnings(tweet)[0].strip() == 'results surpass')
    assert(account.parse_positive_earnings(tweet)[1].strip() == 'strength')
    assert(not account.parse_negative_earnings(tweet))

    tweet = '$SLCA - Strong pricing and growth support U.S. Silica Q3 beat.'  # + beat, strong # earnings
    assert(account.parse_positive_earnings(tweet)[0].strip().lower() == 'strong pricing')
    assert(account.parse_positive_earnings(tweet)[1].strip() == 'Q3 beat')
    assert(not account.parse_negative_earnings(tweet))

    tweet = '$PFG - Principal Financial Group up on Q3 EPS beat'  # + beat # earnings, earnings tweet previous day no surprises
    assert(account.parse_positive_earnings(tweet)[0].strip() == 'Q3 EPS beat')
    assert(not account.parse_negative_earnings(tweet))

    tweet = '$DXCM - DexCom hits six-month high after Q3 beat'  # beat #earnings - no earning tweet
    assert(account.parse_positive_earnings(tweet)[0].strip() == 'Q3 beat')
    assert(not account.parse_negative_earnings(tweet))

    tweet = '$JKS - JinkoSolar sinks 5% despite beating Q3 consensus'  # mixed - sinks and beating
    assert(account.parse_positive_earnings(tweet)[0].strip() == 'beat')
    assert(not account.parse_negative_earnings(tweet))

    tweet = '$TEX - Terex raised FY2022 EPS outlook range after 79% growth in Q3 and strong margins'  # Q3=earnings, raised, strong margins
    assert(account.parse_positive_earnings(tweet)[0].strip() == 'strong margins')
    assert(account.parse_positive_guidance(tweet)[0].strip() == 'raised FY2022 EPS outlook')
    assert(not account.parse_negative_earnings(tweet))

    tweet = '$RWT - Redwood Trust stock trades higher amid Q3 earnings gain'  # earnings +, gain
    assert (account.parse_positive_earnings(tweet)[0].strip() == 'earnings gain')
    assert (not account.parse_negative_earnings(tweet))

    tweet = '$KNSL - Kinsale stock rises 12% on Q3 beat as revenue soars 32%'  # earnings + soars
    assert (account.parse_positive_earnings(tweet)[0].strip() == 'Q3 beat')
    assert (account.parse_positive_earnings(tweet)[1].strip() == 'revenue soar')
    assert (not account.parse_negative_earnings(tweet))

    tweet = '$COHU - Cohu rallies 15% on Q3 estimates beat, provides Q4 guidance'  # earnings + Q3 estimates beat - matches earnings the day before
    assert (account.parse_positive_earnings(tweet)[0].strip() == 'estimates beat')
    assert (not account.parse_negative_earnings(tweet))

    tweet = '$NEE $NEP - NextEra Energy posts Q3 beat; buys $1.1B landfill gas-to-electric portfolio'  # earnings +, repeats tweet
    assert (account.parse_positive_earnings(tweet)[0].strip() == 'Q3 beat')
    assert (not account.parse_negative_earnings(tweet))

    tweet = '$AON - Aon Q3 earnings beat as expenses plummet, free cash flow jump'  # earnings + although earnings tweet mixed
    assert (account.parse_positive_earnings(tweet)[0].strip() == 'earnings beat')
    assert (account.parse_positive_earnings(tweet)[1].strip() == 'expenses plummet')
    assert (account.parse_positive_earnings(tweet)[2].strip() == 'cash flow jump')
    assert (not account.parse_negative_earnings(tweet))

    tweet = '$SMP - Standard Motor Products reports Q3 earnings beat; updates FY22 guidance'  # reports beat => earnings +, no tweet
    assert (account.parse_positive_earnings(tweet)[0].strip() == 'earnings beat')
    assert (not account.parse_negative_earnings(tweet))

    tweet = '$NWL - Newell Brands gains after topping some beaten-down estimates'  # topping -> earnings, uvaga: beaten-down <> beat
    assert (account.parse_positive_earnings(tweet)[0].strip() == 'topping some beaten-down estimate')
    assert (not account.parse_negative_earnings(tweet))

    tweet = '$RNGR - Ranger Energy Services reports Q3 earnings beat; reaffirms FY22 capex guidance'  # + earnings, no tweet
    assert (account.parse_positive_earnings(tweet)[0].strip() == 'earnings beat')
    assert (not account.parse_positive_guidance(tweet))
    assert (not account.parse_negative_guidance(tweet))
    assert (not account.parse_negative_earnings(tweet))

    tweet = '$ABBV - AbbVie Non-GAAP EPS of $3.66 beats by $0.10, revenue of $14.81B misses by $130M, raises dividend by 5%'
    assert (account.parse_positive_earnings(tweet)[0].strip() == 'beat')
    assert (account.parse_negative_earnings(tweet)[0].strip() == 'miss')
    assert (not account.parse_positive_guidance(tweet))
    assert (not account.parse_negative_guidance(tweet))

    tweet = '$CHD - Church &amp; Dwight tops estimates, points to strong consumption trends'  # tops => earnings +, no tweet
    assert (account.parse_positive_earnings(tweet)[0].strip() == 'tops estimate')
    assert (account.parse_positive_earnings(tweet)[1].strip() == 'strong consumption')
    assert (not account.parse_negative_earnings(tweet))

    tweet = '$SLCA - U.S. Silica Holdings reports Q3 earnings beat; updates FY22 guidance'  # earnings +, no tweet
    assert (account.parse_positive_earnings(tweet)[0].strip() == 'earnings beat')
    assert (not account.parse_positive_guidance(tweet))
    assert (not account.parse_negative_guidance(tweet))

    tweet = '$SNY $REGN - Sanofi Q3 sales boosted by Dupixent, Vaccines business; raises FY22 outlook again'  # miss this because of:
    assert (account.parse_positive_earnings(tweet)[0].strip() == 'sales boost')
    assert (account.parse_positive_guidance(tweet)[0].strip() == 'raises FY22 outlook')

    tweet = '$SNY - Sanofi reports Q3 earnings beat; raises FY22 EPS guidance'  # Q3 earnings beat
    assert (account.parse_positive_earnings(tweet)[0].strip() == 'earnings beat')
    assert (account.parse_positive_guidance(tweet)[0].strip() == 'raises FY22 EPS guidance')

    tweet = '$HIG - Hartford Financial Q3 earnings beat, helped by Commercial Lines, Group Benefits'  # earnings => repeats
    assert (account.parse_positive_earnings(tweet)[0].strip() == 'earnings beat')
    assert (len(account.parse_positive_earnings(tweet)) == 1)
    assert (not account.parse_positive_guidance(tweet))

    tweet = '$JAKK - JAKKS Pacific stock jumps 17% after the bell as strong demand drives earnings beat'  # repeats but 17% and reinforces
    assert (account.parse_positive_earnings(tweet)[0].strip() == 'strong demand')
    assert (account.parse_positive_earnings(tweet)[1].strip() == 'earnings beat')
    assert (len(account.parse_positive_earnings(tweet)) == 2)
    assert (not account.parse_positive_guidance(tweet))

    tweet = '$ALK $SKYW $DAL - SkyWest stock flies higher as quarterly profits surpass expectations'  # beat, no tweet, but 3 tickers ???
    assert (account.parse_positive_earnings(tweet)[0].strip() == 'profits surpass')
    assert (len(account.parse_positive_earnings(tweet)) == 1)
    assert (not account.parse_positive_guidance(tweet))

    tweet = '$CWST - Waste recycler Casella posts Q3 beat and raises forecast, shares spike'  # earnings => beat, raises, spike +3 earnings also positive
    assert (account.parse_positive_earnings(tweet)[0].strip() == 'Q3 beat')
    assert (len(account.parse_positive_earnings(tweet)) == 1)
    assert (account.parse_positive_guidance(tweet)[0].strip() == 'raises forecast')

    tweet = '$LADR - Ladder Capital stock gains after Q3 results exceed analyst expectations'  # earnings + on exceed expectations but tweet has no surprises
    assert (account.parse_positive_earnings(tweet)[0].strip() == 'results exceed')
    assert (len(account.parse_positive_earnings(tweet)) == 1)
    assert (not account.parse_positive_guidance(tweet))

    tweet = '$GILD - Gilead Sciences raises full-year 2022 outlook following Q3 beats'  # earnings, + raises but repeats earnings
    assert (account.parse_positive_earnings(tweet)[0].strip() == 'Q3 beat')
    assert (len(account.parse_positive_earnings(tweet)) == 1)
    assert (account.parse_positive_guidance(tweet)[0].strip() == 'raises full-year 2022 outlook')

    tweet = '$AAPL - Apple results top forecasts as iPhone, services lead strong quarterly sales'
    assert (account.parse_positive_earnings(tweet)[0].strip() == 'results top')
    assert (account.parse_positive_earnings(tweet)[1].strip() == 'strong')
    assert (len(account.parse_positive_earnings(tweet)) == 2)


def test_parse_negative_sentiment():
    account = Marketcurrents(Marketcurrents.account_name)
    tweet = '$USNZY $USNZ - High costs, low volumes weigh on miner Usiminas Q3 results'  # earnings -, high cost, low volumes
    assert(account.parse_negative_earnings(tweet)[0].strip().lower() == 'high cost')
    assert(account.parse_negative_earnings(tweet)[1].strip() == 'low volume')
    assert(not account.parse_positive_earnings(tweet))

    tweet = '$CRTO - Criteo slides after lower profit margins, revenue miss'  # miss=earnings, slides, lower earnings tweet mixed
    assert(account.parse_negative_earnings(tweet)[0].strip().lower() == 'lower profit')
    assert(account.parse_negative_earnings(tweet)[1].strip() == 'revenue miss')
    assert(not account.parse_positive_earnings(tweet))

    tweet = '$AWRE - Aware stock slides over 8% as macro headwinds, delayed orders weigh on results'  # results=earnings, - headwinds, weigh
    assert(account.parse_negative_earnings(tweet)[0].strip().lower() == 'headwind')
    assert(account.parse_negative_earnings(tweet)[1].strip() == 'delay')
    assert(not account.parse_positive_earnings(tweet))

    tweet = '$TECK $TECK.B:CA - Teck Resources tumbles as Q3 loss, cost overruns spark analyst downgrades'  # results = Q3 loss, - overrun
    assert(account.parse_negative_earnings(tweet)[0].strip() == 'Q3 loss')
    assert(account.parse_negative_earnings(tweet)[1].strip() == 'cost overrun')
    assert(not account.parse_positive_earnings(tweet))

    tweet = '$LMAT - LeMaitre stock slumps 16% amid Q3 miss, slashed outlook'  # earnings - Q3 miss, slashed outlook, earnings tweet mixed
    assert(account.parse_negative_earnings(tweet)[0].strip() == 'Q3 miss')
    assert(account.parse_negative_guidance(tweet)[0].strip() == 'slashed outlook')
    assert(not account.parse_positive_earnings(tweet))

    tweet = '$AB - AllianceBernstein Q3 earnings declined as asset values dropped, outflows rose'  # earnings -, no tweet
    assert(account.parse_negative_earnings(tweet)[0].strip() == 'earnings decline')
    assert(account.parse_negative_earnings(tweet)[1].strip() == 'asset values drop')
    assert(account.parse_negative_earnings(tweet)[2].strip() == 'outflows rose')
    assert(not account.parse_positive_earnings(tweet))

    tweet = '$B - Barnes Group Q3 profit matches analyst estimates while revenue slips on forex'  # Q3 = earnings, slips -, matches =
    assert(not account.parse_positive_earnings(tweet))
    assert(account.parse_negative_earnings(tweet)[0].strip() == 'revenue slip')

    tweet = '$SJW - SJW reports Q3 earnings miss; reaffirms FY22 guidance'  # # earnings, = - miss, no tweet
    assert(not account.parse_positive_guidance(tweet))
    assert(account.parse_negative_earnings(tweet)[0].strip() == 'earnings miss')

    tweet = '$EW - Edwards Lifesciences down 11% after Q3 misses, revised 2022 EPS guidance'  # earnings => miss, -, repeats earnings tweet, but 11% down may be signif
    assert (account.parse_negative_earnings(tweet)[0].strip() == 'Q3 miss')
    assert (not account.parse_positive_earnings(tweet))
    assert (not account.parse_positive_guidance(tweet))
    assert (not account.parse_negative_guidance(tweet))

    tweet = '$LHX - L3Harris plunges after Q3 miss, full-year guidance cut'  # earnings -> miss, guidance cut, repeats earnings
    assert (account.parse_negative_earnings(tweet)[0].strip() == 'Q3 miss')
    assert (account.parse_negative_guidance(tweet)[0].strip() == 'guidance cut')

    tweet = '$COF - Capital One Q3 earnings fall short of consensus as provision for credit losses jumps'  # earnings also -credit losses
    assert (account.parse_negative_earnings(tweet)[0].strip() == 'earnings fall')
    assert (account.parse_negative_earnings(tweet)[1].strip() == 'credit loss')
    assert (len(account.parse_negative_earnings(tweet)) == 2)

    tweet = '$ORC - Orchid Island Capital posts Q3 loss on widening spreads after Fed rate hikes'  # earnings, repeats tweet
    assert (account.parse_negative_earnings(tweet)[0].strip() == 'Q3 loss')
    assert (len(account.parse_negative_earnings(tweet)) == 1)


def test_mixed_or_neutral():
    account = Marketcurrents(Marketcurrents.account_name)
    tweet = '$DTM - DT Midstream reports Q3 earnings; raises FY22 and FY23 Adjusted EBITDA guidance'  # earnings + => raises
    assert (not account.parse_positive_earnings(tweet))

    tweet = '$NEXA - Nexa Resources reports Q3 mixed earnings; reaffirms FY22 capex guidance'  # earnings, = mixed, reaffirms, no tweet
    assert (not account.parse_positive_earnings(tweet))
    assert (not account.parse_negative_earnings(tweet))
    assert (not account.parse_positive_guidance(tweet))
    assert (not account.parse_negative_guidance(tweet))

    tweet = '$LTC - LTC Properties Q3 results mixed on rental income growth, higher expenses'  # mixed, repeats mixed info in tweet, +growth -expenses
    assert (account.parse_negative_earnings(tweet)[0].strip() == 'higher expenses')
    assert (account.parse_positive_earnings(tweet)[0].strip() == 'income grow')



# News Positive
tweet = '$BSTG - Regenerative therapy developer Biostage files for Nasdaq uplisting, $6M offering'  # +, uplisting
tweet = '$BFIN - BankFinancial adds 300,000 shares to existing share repurchase program'  # + repurchase
tweet = '$OTLK - FDA accepts Outlook Therapeutics biologics license application for wet AMD drug'  # +, FDA accepts
tweet = '$PHGUF $PHAR - Pharming gets EMA accelerated review of leniolisib for rare immunodeficiency disorder'  # + => accelerated review
tweet = '$STAB - Statera Biopharma granted continued listing on Nasdaq'  # + -> granted continued listing

# News negative
tweet = '$AHG - Akso Health gets Nasdaq notice for not complying with minimum bid price rule'  # -, not complying
tweet = '$YMAB - Y-mAbs fails to win FDA AdCom backing for neuroblastoma therapy'  # -, fails to win FDA
tweet = '$PME - Chinese fisher Pingtan gets Nasdaq minimum bid compliance notice'  # - compliance notice
tweet = '$WNW - Meiwu Technology regains compliance with Nasdaq minimum bid price requirement'  # + regains compliance
tweet = '$BX $KKR $APO - KKR, Apollo, Blackstone face Justice Department probe on influence over boards'  # - face probe
tweet = '$SBHMY $FSTX - F-star Therapeutics drops amid concern about CFIUS approval for Sino-Biopharma'  # - drops, can't use 'approval' on its own
tweet = '$COF - Capital One credit card delinquency, net charge-off rates climb in September'  # -, industry, delinquency climbs =>IGNORE
tweet = '$ALRM $VVNT - https://t.co/LStNLDdfU5 stock slips 3% after the bell on licensing dispute with Vivint'  # news, licensing dispute

# Dividends
tweet = '$TAIT - Taitron Components raises dividend by 11% to $0.05'  # +, raises dividend
tweet = '$ZION - Zions declares $0.41 dividend, approves up to $50M buyback'  # + buyback
tweet = 'Wells Fargo Multi-Sector Income Fund lowers dividend by 4.1%'  # -, lowers dividend
tweet = '$FTAI - Fortress Transportation dividend declines by 10% to $0.30'  # - dividend declines

# Guidance
tweet = '$LYB - LyondellBasell paints a gloomy picture for current qtr, succumbing to high energy costs'  # -, gloomy
tweet = '$AMZN $RIVN - Amazon stock dives over 20% on downbeat sales forecast'  # not earnings -> downbeat sales forecast
tweet = '$BLMN - Bloomin Brands notches narrow earnings bear, raises sales forecasts'  # beat misspelled, but raises

# False positive
tweet = '$SLNA - Hotel operator Selina stock plunges after rallying as high as 442% in prior session'  # mixed => plunge + rally, but not an earning