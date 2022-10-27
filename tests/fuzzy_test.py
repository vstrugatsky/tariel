from fuzzywuzzy import fuzz


def test_ratios():
    name = 'SPDR ICE Preferred Securities ETF'
    tweet = '$PREKF $PSK:CA - PrairieSky Royalty FFO of C$0.52, revenue of C$154.7M'
    print(f'\nPSK rаtio= {fuzz.WRatio(tweet, name)}')

    name = 'PRAIRIESKY ROYALTY LTD'
    print(f'PREKF rаtio= {fuzz.WRatio(tweet, name)}')

# fuzz ratio=16 name=PRAIRIESKY ROYALTY LTD tweet=$PREKF $PSK:CA - PrairieSky Royalty FFO of C$0.52, revenue of C$154.7M