from loaders.twitter_marketcurrents import Marketcurrents

# \W(Morgan\ Stanley | BofA | Citigroup | Moody(\Ws)? | Wedbush)(\W | $))


def test_parse_analyst():
    account = Marketcurrents(Marketcurrents.account_name)

    tweet = "$TSN - Tyson Foods margin guidance raises analyst suspicion"
    assert(not account.parse_analyst(tweet))
    assert (not account.parse_positive_guidance(tweet))
    assert (not account.parse_simple_earnings_indicator(tweet))

    tweet = "$SI - Silvergate Capital stock slides as Morgan Stanley slashes 2023 EPS estimate by 51%"
    assert(account.parse_analyst(tweet) == 'Morgan Stanley')

    tweet = "$DE - Moody's affirms Deere's A2 rating, raises outlook to positive"
    assert(not account.parse_false_positive(tweet))
    assert(account.parse_analyst(tweet) == "Moody's")
    assert (not account.parse_simple_earnings_indicator(tweet))

    tweet = '$UCO $USO $DBO - Oil reverses gain as OPEC again cuts oil demand forecast'
    assert (not account.parse_false_positive(tweet))
    assert(not account.parse_analyst(tweet))
