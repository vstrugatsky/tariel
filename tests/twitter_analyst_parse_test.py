from loaders.twitter_marketcurrents import Marketcurrents


def challenges():  # 19 out of 88 incorrect
    # recorded as Guidance for both
    t = "$CAR $HTZ - Avis and Hertz draw cautious view from Susquehanna in initial ratings"
    t = "$EL - Estee Lauder gains after Deutsche Bank turns bullish on China outlook"
    t = "$LI - Li Auto is recommended by BofA ahead of earnings because guidance may be strong"
    t = "$CHRW $XPO $RXO - RXO rated at Buy as Jefferies sees ‘compelling opportunity’ ahead"
    t = "$AAPL - Apple slips as UBS cuts iPhone build estimates, citing China disruptions"
    t = "$AAPL $HNHPF - Apple slips as Morgan Stanley cuts iPhone estimates for second time in less than a month"
    t = "$JACK - Jack in the Box draws cautious views from Wall Street after earnings"
    t = "$AMAT $LRCX - Lam Research, Applied Materials estimates tweaked as Bernstein cuts spending forecast"
    t = "$BKNG $EXPE $TRIP - Expedia, Tripadvisor cut to Sell as Wolfe Research takes bearish view on travel stocks https://t.co/zxzMVjgV2r"
    # recorded as earnings
    t = "$SPY $GS $WFC - Goldman Sachs' David Kostin predicts S&amp;P 500 will be flat in 2023 with no earnings growth"
    t = "$RGA - Reinsurance Group of America upped to Outperform at RBC on earnings growth potential"

    # recorded as both positive and negative earnings AND negative guidance
    # {disappointing earnings growth outlook} + {earnings grow} + {disappointing earnings growth}
    t = "$SR - Spire sinks after JPM downgrades on disappointing earnings growth outlook"

    # XLI recorded (fund)
    t = "$GE $XLI $BA - Deere leads weekly gains in industrial stocks after upbeat outlook"
    # recorded with both positive and negative guidance
    # {guides FY 2023 adj. EPS below consensus ahead}", "{guides FY 2023 adj. EPS below}"
    t = "$UNH - UnitedHealth guides FY 2023 adj. EPS below consensus ahead of investor conference"
    # wrongly associated with both DIS and TCEHY - Tencent (BILI not in cashtags)
    t = "$DIS $BIDU $TCEHY - Bilibili surges as Q3 tops expectations; Chinese tech rises on refined COVID-19 measures"


def test_parse_analyst():
    account = Marketcurrents(Marketcurrents.account_name)

    tweet = "$OGS - ONE Gas cut to Sell at Guggenheim after disappointing guidance"
    assert (account.parse_analyst(tweet) == 'Guggenheim')
    assert(account.parse_analyst_negative(tweet)[0] == 'cut to Sell')

    tweet = "$AMAT $LRCX - Lam Research, Applied Materials estimates tweaked as Bernstein cuts spending forecast"
    assert (account.parse_analyst(tweet) == 'Bernstein')
    assert(account.parse_analyst_negative(tweet)[0] == 'cuts spending')

    tweet = "$WSM - Williams-Sonoma cut to Sell at Morgan Stanley on margin concern, slowing sales"
    assert (account.parse_analyst(tweet) == 'Morgan Stanley')
    assert(account.parse_analyst_negative(tweet)[0] == 'cut to Sell')

    tweet = "$BUD - Anheuser-Busch InBev rallies after JPMorgan flips from bear to bull"

    tweet = "$APTV - Aptiv slips after losing bull rating at Morgan Stanley"
    assert (account.parse_analyst(tweet) == 'Morgan Stanley')
    # assert(account.parse_analyst_negative(tweet)[0] == 'after losing bull rating')

    tweet = "$LYV - Live Nation rises on Citi upgrade, firm gives it 80% chance it stays intact"
    assert (account.parse_analyst(tweet) == 'Citi')
    assert(account.parse_analyst_positive(tweet)[0] == 'upgrade,')

    tweet = "$CRM - Salesforce Q3 results likely to be 'generally positive' but some weakness abounds: Wedbush"
    assert (account.parse_analyst(tweet) == 'Wedbush')
    assert(not account.parse_analyst_positive(tweet))
    assert(not account.parse_analyst_negative(tweet))

    tweet = "$TDG - TransDigm downgraded to Equal Weight at Wells Fargo"
    assert (account.parse_analyst(tweet) == 'Wells Fargo')
    assert(account.parse_analyst_negative(tweet)[0] == 'downgraded to Equal')

    tweet = "$FSLR $TAN - First Solar downgraded at J.P. Morgan as 'easy money seems likely made'"
    assert (account.parse_analyst(tweet) == 'J.P. Morgan')
    assert(account.parse_analyst_negative(tweet)[0] == 'downgraded at')

    tweet = "$TWLO - Twilio dips as Jefferies cuts, citing low conviction, 'sustained headwinds' to growth"
    assert (account.parse_analyst(tweet) == 'Jefferies')
    assert(account.parse_analyst_negative(tweet)[0] == 'cuts,')

    tweet = "$AMG - Affiliated Managers Group upgraded to Buy at Jefferies on 2023 growth outlook"
    assert (account.parse_analyst(tweet) == 'Jefferies')
    assert(account.parse_analyst_positive(tweet)[0] == 'upgraded to Buy')

    tweet = "$COHR - Coherent slips even as Deutsche Bank upgrades, saying bear case 'not as bad as feared'"
    assert (account.parse_analyst(tweet) == 'Deutsche Bank')
    assert(account.parse_analyst_positive(tweet)[0] == 'upgrades,')

    tweet = "$XENE - Xenon initiated Overweight at Wells Fargo on prospects in depression"
    assert (account.parse_analyst(tweet) == 'Wells Fargo')
    assert(account.parse_analyst_negative(tweet)[0] == 'initiated Overweight')

    tweet = "$VLKAF $POAHY $VWAGY - Porsche is overvalued, Bernstein says in 'Sell' initiation"
    assert (account.parse_analyst(tweet) == 'Bernstein')
    assert(account.parse_analyst_negative(tweet)[0] == 'overvalued')

    tweet = "$ZBH - Zimmer Biomet upgraded at Wells Fargo on ortho trends and realistic outlook"
    assert (account.parse_analyst(tweet) == 'Wells Fargo')
    assert(account.parse_analyst_positive(tweet)[0] == 'upgraded at')

    tweet = "$LVLU - Lulu’s Fashion Lounge Holdings downgraded at Cowen on margin concerns"
    assert (account.parse_analyst(tweet) == 'Cowen')
    assert(account.parse_analyst_negative(tweet)[0] == 'downgraded at')

    tweet = "$ADSK - Autodesk plunges as Mizuho downgrades after weak billings, free cash flow guidance"
    assert (account.parse_analyst(tweet) == 'Mizuho')
    assert(account.parse_analyst_negative(tweet)[0] == 'downgrades after')

    tweet = "$YUM - Yum Brands lands Buy rating from Argus with growth on the menu"
    assert (account.parse_analyst(tweet) == 'Argus')
    assert(account.parse_analyst_positive(tweet)[0] == 'lands Buy')

    tweet = "$BYND - Beyond Meat cut to Sell at Goldman amid diminishing demand"
    assert (account.parse_analyst(tweet) == 'Goldman')
    assert(account.parse_analyst_negative(tweet)[0] == 'cut to Sell')

    tweet = "$CNTG - Centogene spikes as H.C. Wainwright initiates Buy with over 200% upside"
    assert (account.parse_analyst(tweet) == 'H.C. Wainwright')
    assert(account.parse_analyst_positive(tweet)[0] == 'initiates Buy')

    tweet = "$SCCO $SBSW - Sibanye Stillwater, Southern Copper cut at Deutsche Bank"
    assert (account.parse_analyst(tweet) == 'Deutsche Bank')
    assert(account.parse_analyst_negative(tweet)[0] == 'cut at')

    tweet = "$ARES $VCTR $OWL - Victory Capital cut to Underweight at Piper on revenue pressure from market vol, outflows"
    assert (account.parse_analyst(tweet) == 'Piper')
    assert(account.parse_analyst_negative(tweet)[0] == 'cut to Underweight')

    tweet = "$MDT - Medtronic cut to Neutral at Citi on Q2 revenue miss"
    assert (account.parse_analyst(tweet) == 'Citi')
    assert(account.parse_analyst_negative(tweet)[0] == 'cut to Neutral')

    tweet = "$JACK - Jack in the Box draws cautious views from Wall Street after earnings"
    assert(account.parse_analyst(tweet) == 'Wall Street')  # misclassified as Guidance

    tweet = "$LVS $DKNG $RRR - DraftKings, Las Vegas Sands and Red Rock Resorts are called gaming sector standouts by Morgan Stanley"
    assert(account.parse_analyst(tweet) == 'Morgan Stanley')
    assert(not account.parse_analyst_positive(tweet))
    assert(not account.parse_analyst_negative(tweet))

    tweet = "$TEAM - Atlassian plunges as Piper Sandler downgrades following guidance cut, slowing user growth"
    assert(account.parse_analyst(tweet) == 'Piper Sandler')
    assert(account.parse_analyst_negative(tweet)[0] == 'downgrades following')

    tweet = "$PANW - Palo Alto Networks pops after Loop Capital upgrade"
    assert(account.parse_analyst(tweet) == 'Loop Capital')
    assert(account.parse_analyst_positive(tweet)[0] == 'upgrade')

    tweet = "$OMER - Omeros downgraded at Bank of America after FDA snub for narsoplimab appeal"
    assert(account.parse_analyst(tweet) == 'Bank of America')
    assert(account.parse_analyst_negative(tweet)[0] == 'downgraded at')

    tweet = "$SHLS - Shoals sizzles after raising low end of revenue guidance; Northland upgrades"
    assert(account.parse_analyst(tweet) == 'Northland')
    assert(account.parse_analyst_positive(tweet)[0] == 'upgrades')

    tweet = "$TSN - Tyson Foods margin guidance raises analyst suspicion"
    assert(not account.parse_analyst(tweet))
    assert (not account.parse_positive_guidance(tweet))
    assert (not account.parse_simple_earnings_indicator(tweet))

    tweet = "$SI - Silvergate Capital stock slides as Morgan Stanley slashes 2023 EPS estimate by 51%"
    assert(account.parse_analyst(tweet) == 'Morgan Stanley')
    assert(not account.parse_negative_earnings(tweet))
    assert(account.parse_analyst_negative(tweet)[0] == 'slashes 2023')

    tweet = "$DE - Moody's affirms Deere's A2 rating, raises outlook to positive"
    assert(not account.parse_false_positive(tweet))
    assert(account.parse_analyst(tweet) == "Moody's")
    assert(not account.parse_positive_guidance(tweet))
    assert(account.parse_analyst_positive(tweet)[0] == 'raises outlook to positive')

    tweet = "$COF - Capital One stock falls as credit losses rise; BofA downgrades to Neutral"
    assert(account.parse_analyst(tweet) == "BofA")
    assert(account.parse_simple_earnings_indicator(tweet))
    assert(account.parse_negative_earnings(tweet))
    assert(account.parse_analyst_negative(tweet)[0] == 'downgrades to Neutral')

    tweet = '$UCO $USO $DBO - Oil reverses gain as OPEC again cuts oil demand forecast'
    assert (not account.parse_false_positive(tweet))
    assert(not account.parse_analyst(tweet))


def mixes():
    t = "$APTV - Aptiv slips after losing bull rating at Morgan Stanley"
    t = "$WMT - Walmart is called a Black Friday winner by Bank of America"
    t = "$BUD - Anheuser-Busch InBev rallies after JPMorgan flips from bear to bull"
    t = "$LU - Lufax stock retreats after JPMorgan cuts to Underperform on Q3 miss, weakened guidance"
    t = "$AMAT $LRCX - Lam Research, Applied Materials estimates tweaked as Bernstein cuts spending forecast"
