from fuzzywuzzy import fuzz


def test_ratios():
    function = fuzz.ratio
    print(function.__name__)
    tweet = '$PREKF $PSK:CA - PrairieSky Royalty FFO of C$0.52, revenue of C$154.7M https://t.co/vvv1gDxLk7'
    name = 'SPDR ICE Preferred Securities ETF'
    print(f'\nPSK rаtio= {function(name, tweet)}')
    name = 'PRAIRIESKY ROYALTY LTD'
    print(f'PREKF rаtio= {function(name, tweet)}')

    tweet = '$ALK $SKYW $DAL - SkyWest stock flies higher as quarterly profits surpass expectations https://t.co/vvv1gDxLk7'
    tweet_url_desc = "SkyWest (SKYW) shares rose sharply in Thursday’s extended session after posting stronger than expected profits for Q3."
    name = 'Alaska Air Group, Inc'
    print(f'ALK rаtio= {function(name, tweet)}')
    name = 'DELTA AIR LINES INC DEL'
    print(f'DAL rаtio= {function(name, tweet)}')
    name = 'Skywest Inc'
    print(f'SKYW rаtio= {function(name, tweet)}')

    tweet = '$KDDIF $KDDIY - KDDI Corporation GAAP EPS of ¥161.04, revenue of ¥2.74T https://t.co/2R9k5xOQzc'
    name = 'KDDI CORP'
    print(f'KDDIF rаtio= {function(name, tweet)}')
    name = 'KDDI CORP UNSP/ADR'
    print(f'KDDIY rаtio= {function(name, tweet)}')

    tweet = '$PARA $DTC - Paramount Global Non-GAAP EPS of $0.39 misses by $0.05, revenue of $6.92B misses by $130M https://t.co/NW4DxAZGhX'
    name = 'Solo Brands, Inc.'
    print(f'DTC rаtio= {function(name, tweet)}')
    name = 'Paramount Global Class B Common Stock'
    print(f'PARA rаtio= {function(name, tweet)}')

    tweet = '$SONY $SNEJF - Sony GAAP EPS of ¥212.29, revenue of ¥2751.88B; raises FY22 guidance https://t.co/rLxfgyuqwU'
    name = 'SONY CORP ORD'
    print(f'SNEJF rаtio= {function(name, tweet)}')
    name = 'SONY CORP ORD'
    print(f'SONY rаtio= {function(name, tweet)}')

    tweet = '$TM $TOYOF - Toyota Motor reports Q2 results; raises FY23 guidance https://t.co/GBiTDly6la'
    name = 'Toyota Motor Corporation American Depositary Shares (Each representing ten Ordinary Shares)'
    print(f'TM rаtio= {function(name, tweet)}')
    name = 'TOYOTA MOTOR CORP ORD'
    print(f'TOYOF rаtio= {function(name, tweet)}')

    tweet = '$XOM $DVN $CVX - Devon Energy Q3 preview: Another earnings beat expected https://t.co/PTHbpmxCOF'
    name = 'Chevron Corporation'
    print(f'CVX rаtio= {function(name, tweet)}')
    name = 'Devon Energy Corporation'
    print(f'DVN rаtio= {function(name, tweet)}')
    name = 'Exxon Mobil Corporation'
    print(f'XOM rаtio= {function(name, tweet)}')

    tweet = '$NVZMF $NVZMY - Novozymes A/S reports Q3 results; raises its full-year organic sales growth outlook https://t.co/vvv1gDxLk7'
    tweet_url_desc = '"Novozymes A/S press release (NVZMF): Q3 Revenue of DKK4.37B (+16.2% Y/Y), (6% organic, 9% currency, 1% M&A).Novozymes increases its full-year organic sales growth outlook from...'
    name = "NOVOZYMES A/S"
    print(f'NVZMF rаtio= {function(name, tweet)}')
    name = "NOVOZYMES A/S UNSP/ADR"
    print(f'NVZMY rаtio= {function(name, tweet)}')

    tweet = '$SRE $EPS - Sempra Non-GAAP EPS of $1.97 beats by $0.19, revenue of $3.62B beats by $260M, raises FY Adj EPS guidance https://t.co/XKOOCiaBuU'
    name = "WisdomTree U.S. LargeCap Fund"
    print(f'EPS rаtio= {function(name, tweet)}')
    name = "Sempra"
    print(f'SRE rаtio= {function(name, tweet)}')

    tweet = '$ENB $DCF $ENB:CA - Enbridge Non-GAAP EPS of $0.67 beats by $0.03, revenue of $11.57B misses by $900M https://t.co/X0kRGIpR8m'
    name = 'BNY Mellon Alcentra Global Credit Income 2024 Target Term Fund, Inc.'
    print(f'DCF rаtio= {function(name, tweet)}')
    name = "Enbridge, Inc"
    print(f'ENB rаtio= {function(name, tweet)}')

    tweet = '$FLR $EPS - Fluor Non-GAAP EPS of $0.07 misses by $0.35, revenue of $3.61B beats by $70M https://t.co/4AeLc7c9vh'
    name = "WisdomTree U.S. LargeCap Fund"
    print(f'EPS rаtio= {function(name, tweet)}')
    name = "Fluor Corporation"
    print(f'FLR rаtio= {function(name, tweet)}')

    tweet = '$ES $EPS - Eversource Energy Non-GAAP EPS of $1.01 misses by $0.04, revenue of $3.22B beats by $560M https://t.co/usMcVbl5Ym'
    name = "WisdomTree U.S. LargeCap Fund"
    print(f'EPS rаtio= {function(name, tweet)}')
    name = "Eversource Energy"
    print(f'ES rаtio= {function(name, tweet)}')

    tweet = '$ASM $TMXXF $INCAF - Inca One Gold Q3 sales fall 1% https://t.co/vvv1gDxLk7'
    tweet_url_desc = "Inca One Gold (INCAF) reports Q3 sales of $9.6M (-1% Y/Y) as lower selling prices offset gains from higher gold production during the quarter"
    name = 'Avino Silver & Gold Mines Ltd. (Canada)'
    print(f'ASM rаtio= {function(name, tweet)}')
    name = 'INCA ONE GOLD CORP NEW'
    print(f'INCAF rаtio= {function(name, tweet)}')
    name = 'TMX GROUP LTD'
    print(f'TMXXF rаtio= {function(name, tweet)}')

    tweet = '$VEON $VNLTF - VEON reports strong Q3 revenue performance gaining market share as countries execute digital operator strategy https://t.co/vvv1gDxLk7'
    tweet_url_desc = 'Amsterdam-listed mobile operator VEON (VEON) reported third-quarter revenues rising 3.4% in local currency terms and up 3.6% in dollars, the currency it reports in, to $2.08... '
    name = 'VEON Ltd. ADS'
    print(f'VEON rаtio= {function(name, tweet)}')
    name = 'VEON LTD'
    print(f'VNLTF rаtio= {function(name, tweet)}')

# fuzz ratio=16 name=PRAIRIESKY ROYALTY LTD tweet=$PREKF $PSK:CA - PrairieSky Royalty FFO of C$0.52, revenue of C$154.7M