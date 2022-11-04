from fuzzywuzzy import fuzz


def test_ratios():
    tweet = '$PREKF $PSK:CA - PrairieSky Royalty FFO of C$0.52, revenue of C$154.7M'
    name = 'SPDR ICE Preferred Securities ETF'
    print(f'\nPSK rаtio= {fuzz.WRatio(tweet, name)}')
    name = 'PRAIRIESKY ROYALTY LTD'
    print(f'PREKF rаtio= {fuzz.WRatio(tweet, name)}')

    tweet = '$ALK $SKYW $DAL - SkyWest stock flies higher as quarterly profits surpass expectations'
    tweet_url_desc = "SkyWest (SKYW) shares rose sharply in Thursday’s extended session after posting stronger than expected profits for Q3."
    name = 'Alaska Air Group, Inc'
    print(f'ALK rаtio= {fuzz.WRatio(tweet, name)}')
    name = 'DELTA AIR LINES INC DEL'
    print(f'DAL rаtio= {fuzz.WRatio(tweet, name)}')
    name = 'Skywest Inc'
    print(f'SKYW rаtio= {fuzz.WRatio(tweet, name)}')

    tweet = '$NVZMF $NVZMY - Novozymes A/S reports Q3 results; raises its full-year organic sales growth outlook'
    tweet_url_desc = '"Novozymes A/S press release (NVZMF): Q3 Revenue of DKK4.37B (+16.2% Y/Y), (6% organic, 9% currency, 1% M&A).Novozymes increases its full-year organic sales growth outlook from...'
    name = "NOVOZYMES A/S"
    print(f'$NVZMF rаtio= {fuzz.WRatio(tweet, name)}')
    name = "NOVOZYMES A/S UNSP/ADR"
    print(f'$NVZMY rаtio= {fuzz.WRatio(tweet, name)}')

    tweet = '$ASM $TMXXF $INCAF - Inca One Gold Q3 sales fall 1%'
    tweet_url_desc = "Inca One Gold (INCAF) reports Q3 sales of $9.6M (-1% Y/Y) as lower selling prices offset gains from higher gold production during the quarter"
    name = 'Avino Silver & Gold Mines Ltd. (Canada)'
    print(f'ASM rаtio= {fuzz.WRatio(tweet, name)}')
    name = 'INCA ONE GOLD CORP NEW'
    print(f'INCAF rаtio= {fuzz.WRatio(tweet, name)}')
    name = 'TMX GROUP LTD'
    print(f'TMXXF rаtio= {fuzz.WRatio(tweet, name)}')

    tweet = '$VEON $VNLTF - VEON reports strong Q3 revenue performance gaining market share as countries execute digital operator strategy'
    tweet_url_desc = 'Amsterdam-listed mobile operator VEON (VEON) reported third-quarter revenues rising 3.4% in local currency terms and up 3.6% in dollars, the currency it reports in, to $2.08...'
    name = 'VEON Ltd. ADS'
    print(f'VEON rаtio= {fuzz.WRatio(tweet, name)}')
    name = 'VEON LTD'
    print(f'VNLTF rаtio= {fuzz.WRatio(tweet, name)}')

# fuzz ratio=16 name=PRAIRIESKY ROYALTY LTD tweet=$PREKF $PSK:CA - PrairieSky Royalty FFO of C$0.52, revenue of C$154.7M