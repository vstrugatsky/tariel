from loaders.twitter_marketcurrents import Marketcurrents


def test_parse_analyst():
    account = Marketcurrents(Marketcurrents.account_name)

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
