import re
import model
from loaders.earnings_reports_from_twitter import LoadEarningsReportsFromTwitter
from loaders.twitter_livesquawk import Livesquawk
from loaders.twitter_marketcurrents import Marketcurrents
from model.earnings_reports import EarningsReport
from model.jobs import Provider
from utils.utils import Utils


def test_should_update():
    er = EarningsReport(creator=Provider['Twitter_Livesquawk'], updater=None)
    provider = 'Twitter_Livesquawk'
    assert(LoadEarningsReportsFromTwitter.should_update(er, provider) is True)

    er = EarningsReport(creator=Provider['Twitter_Livesquawk'], updater=None)
    provider = 'Twitter_Livesquawk'
    assert(LoadEarningsReportsFromTwitter.should_update(er, provider) is True)

    er = EarningsReport(creator=Provider['Twitter_Livesquawk'], updater=None)
    provider = 'Twitter_Marketcurrents'
    assert(LoadEarningsReportsFromTwitter.should_update(er, provider) is False)

    er = EarningsReport(creator=Provider['Twitter_Livesquawk'], updater=Provider['Twitter_Livesquawk'])
    provider = 'Twitter_Marketcurrents'
    assert(LoadEarningsReportsFromTwitter.should_update(er, provider) is False)

    er = EarningsReport(creator=Provider['Twitter_Livesquawk'], updater=Provider['Twitter_Marketcurrents'])
    provider = 'Twitter_Livesquawk'
    assert(LoadEarningsReportsFromTwitter.should_update(er, provider) is True)


def test_determine_currency():
    assert(LoadEarningsReportsFromTwitter.determine_currency(eps_currency=None, revenue_currency=None) is None)
    assert(LoadEarningsReportsFromTwitter.determine_currency('$', None) == 'USD')
    assert(LoadEarningsReportsFromTwitter.determine_currency(None, '$') == 'USD')
    assert(LoadEarningsReportsFromTwitter.determine_currency('$', '$') == 'USD')


def test_determine_eps():
    # determine_eps(eps_sign: str | None, eps: str | None) -> float:
    assert(LoadEarningsReportsFromTwitter.determine_eps(eps_sign=None, eps=None) == 0)
    assert(LoadEarningsReportsFromTwitter.determine_eps(None, eps='0.67') == 0.67)
    assert(LoadEarningsReportsFromTwitter.determine_eps('-', eps='0.67') == -0.67)
    assert(LoadEarningsReportsFromTwitter.determine_eps('-', eps='1') == -1)


def test_determine_surprise_marketcurrents():
    loader = LoadEarningsReportsFromTwitter(Marketcurrents(Marketcurrents.account_name))

    match_dict = {'eps_surprise_direction': None, 'eps_surprise_amount': None, 'eps_surprise_uom': None}
    assert(loader.account.determine_surprise(match_dict=match_dict, metrics='eps') is None)

    match_dict = {'eps_surprise_direction': 'BAD', 'eps_surprise_amount': 0.01, 'eps_surprise_uom': None}
    assert (loader.account.determine_surprise(match_dict=match_dict, metrics='eps') is None)

    match_dict = {'eps_surprise_direction': 'beats', 'eps_surprise_amount': 0.01, 'eps_surprise_uom': None}
    assert (loader.account.determine_surprise(match_dict=match_dict, metrics='eps') == 0.01)

    match_dict = {'revenue_surprise_direction': 'MISSES', 'revenue_surprise_amount': 0.01, 'revenue_surprise_uom': 'm'}
    assert (loader.account.determine_surprise(match_dict=match_dict, metrics='revenue') == -10000)

    match_dict = {'revenue_surprise_direction': 'misses', 'revenue_surprise_amount': 64.24, 'revenue_surprise_uom': 'M'}
    assert (loader.account.determine_surprise(match_dict=match_dict, metrics='revenue') == -64240000)


def test_determine_surprise_livesquawk():
    loader = LoadEarningsReportsFromTwitter(Livesquawk(Livesquawk.account_name))
    match_dict = {'eps': '1.51', 'eps_estimate_amount': '1.54'}
    assert (loader.account.determine_surprise(match_dict=match_dict, metrics='eps') == -0.03)

    match_dict = {'revenue': '12.84', 'revenue_uom': 'b', 'revenue_estimate_amount': '12.83', 'revenue_estimate_uom': 'B'}
    assert (loader.account.determine_surprise(match_dict=match_dict, metrics='revenue') == 10000000)

    match_dict = {'revenue': '12.84', 'revenue_uom': None, 'revenue_estimate_amount': '12.83', 'revenue_estimate_uom': None}
    assert (loader.account.determine_surprise(match_dict=match_dict, metrics='revenue') == 10000000)


def test_apply_uom():
    assert(Utils.apply_uom(amount=0.07, uom=None) == 0.07)
    assert(Utils.apply_uom(0.07, 'Z') == 0.07)
    assert(Utils.apply_uom(0.07, 'k') == 70)
    assert(Utils.apply_uom(0.07, 'M') == 70000)
    assert(Utils.apply_uom(1.1, 'b') == 1100000000)
    assert(Utils.apply_uom(64.24, 'M') == 64240000)


def test_associate_tweet_with_symbol():
    with model.Session() as session:
        cashtags = [{'start': 0, 'end': 4, 'tag': 'PPG'}]
        assert('PPG' in LoadEarningsReportsFromTwitter.associate_tweet_with_symbols(session, cashtags).keys())

        cashtags = [{'start': 0, 'end': 4, 'tag': 'SPY'},
                    {'start': 5, 'end': 9, 'tag': 'WMT'},
                    {'start': 10, 'end': 15, 'tag': 'AAPL'}]
        assert('SPY' in LoadEarningsReportsFromTwitter.associate_tweet_with_symbols(session, cashtags).keys())
        assert('WMT' in LoadEarningsReportsFromTwitter.associate_tweet_with_symbols(session, cashtags).keys())
        assert('AAPL' in LoadEarningsReportsFromTwitter.associate_tweet_with_symbols(session, cashtags).keys())
        assert(len(LoadEarningsReportsFromTwitter.associate_tweet_with_symbols(session, cashtags).keys()) == 3)

        cashtags = [{'start': 0, 'end': 4, 'tag': 'SPY'},
                    {'start': 5, 'end': 9, 'tag': 'SPY'}]
        assert('SPY' in LoadEarningsReportsFromTwitter.associate_tweet_with_symbols(session, cashtags).keys())
        assert(len(LoadEarningsReportsFromTwitter.associate_tweet_with_symbols(session, cashtags).keys()) == 1)

        cashtags = [{'start': 0, 'end': 4, 'tag': 'SPY'},
                    {'start': 5, 'end': 9, 'tag': 'SPYZZZ'}]
        assert('SPY' in LoadEarningsReportsFromTwitter.associate_tweet_with_symbols(session, cashtags).keys())
        assert(len(LoadEarningsReportsFromTwitter.associate_tweet_with_symbols(session, cashtags).keys()) == 1)

        cashtags = [{'start': 0, 'end': 4, 'tag': 'GFELF'},
                    {'start': 5, 'end': 9, 'tag': 'GLD'}]
        assert('GFELF' in LoadEarningsReportsFromTwitter.associate_tweet_with_symbols(session, cashtags).keys())
        assert('GLD' in LoadEarningsReportsFromTwitter.associate_tweet_with_symbols(session, cashtags).keys())
        assert(len(LoadEarningsReportsFromTwitter.associate_tweet_with_symbols(session, cashtags).keys()) == 2)

        cashtags = [{'start': 0, 'end': 4, 'tag': 'SPYZZZ'}]
        assert(not LoadEarningsReportsFromTwitter.associate_tweet_with_symbols(session, cashtags))

        cashtags = None
        assert(not LoadEarningsReportsFromTwitter.associate_tweet_with_symbols(session, cashtags))


def test_parse_tweet_nii():
    tweet = '$SAR - Saratoga Investment Non-GAAP NII of $0.58 beats by $0.07, total Investment Income of $21.85M beats by $1.95M'
    account = Marketcurrents(Marketcurrents.account_name)
    dict = LoadEarningsReportsFromTwitter.parse_tweet(account, tweet)
    assert(dict.get('eps_sign') is None)
    assert(dict.get('eps_currency') == '$')
    assert(dict.get('eps') == '0.58')
    assert(dict.get('eps_surprise_direction') == 'beats')
    assert(dict.get('eps_surprise_currency') == '$')
    assert(dict.get('eps_surprise_amount') == '0.07')
    assert(dict.get('revenue_currency') == '$')
    assert(dict.get('revenue') == '21.85')
    assert(dict.get('revenue_uom') == 'M')
    assert(dict.get('revenue_surprise_direction') == 'beats')
    assert(dict.get('revenue_surprise_currency') == '$')
    assert(dict.get('revenue_surprise_amount') == '1.95')
    assert(dict.get('revenue_surprise_uom') == 'M')


def test_parse_tweet_basic():
    tweet = '$BABB GAAP EPS of $0.02, revenue of $0.88M'
    account = Marketcurrents(Marketcurrents.account_name)
    dict = LoadEarningsReportsFromTwitter.parse_tweet(account, tweet)
    assert(dict.get('eps_sign') is None)
    assert(dict.get('eps_currency') == '$')
    assert(dict.get('eps') == '0.02')
    assert(dict.get('eps_surprise_direction') is None)
    assert(dict.get('eps_surprise_currency') is None)
    assert(dict.get('eps_surprise_amount') is None)
    assert(dict.get('revenue_currency') == '$')
    assert(dict.get('revenue') == '0.88')
    assert(dict.get('revenue_uom') == 'M')
    assert(dict.get('revenue_surprise_direction') is None)
    assert(dict.get('revenue_surprise_currency') is None)
    assert(dict.get('revenue_surprise_amount') is None)
    assert(dict.get('revenue_surprise_uom') is None)


def test_parse_tweet_with_surprises():
    tweet = '$TLRY $TLRY:CA - Tilray Non - GAAP EPS of -$0.08 misses by $0.01, revenue of $153M misses by $3.6M'
    account = Marketcurrents(Marketcurrents.account_name)
    dict = LoadEarningsReportsFromTwitter.parse_tweet(account, tweet)
    assert(dict.get('eps_sign') == '-')
    assert(dict.get('eps_currency') == '$')
    assert(dict.get('eps') == '0.08')
    assert(dict.get('eps_surprise_direction') == 'misses')
    assert(dict.get('eps_surprise_currency') == '$')
    assert(dict.get('eps_surprise_amount') == '0.01')
    assert(dict.get('revenue_currency') == '$')
    assert(dict.get('revenue') == '153')
    assert(dict.get('revenue_uom') == 'M')
    assert(dict.get('revenue_surprise_direction') == 'misses')
    assert(dict.get('revenue_surprise_currency') == '$')
    assert(dict.get('revenue_surprise_amount') == '3.6')
    assert(dict.get('revenue_surprise_uom') == 'M')


def test_parse_tweet_canadian():
    tweet = '$ATZAF $ATZ:CA - Aritzia&amp;nbsp; GAAP EPS of C$0.44, revenue of C$525.5M'
    account = Marketcurrents(Marketcurrents.account_name)
    dict = LoadEarningsReportsFromTwitter.parse_tweet(account, tweet)
    assert(dict.get('eps_sign') is None)
    assert(dict.get('eps_currency') == 'C$')
    assert(dict.get('eps') == '0.44')
    assert(dict.get('eps_surprise_direction') is None)
    assert(dict.get('eps_surprise_currency') is None)
    assert(dict.get('eps_surprise_amount') is None)
    assert(dict.get('revenue_currency') == 'C$')
    assert(dict.get('revenue') == '525.5')
    assert(dict.get('revenue_uom') == 'M')
    assert(dict.get('revenue_surprise_direction') is None)
    assert(dict.get('revenue_surprise_currency') is None)
    assert(dict.get('revenue_surprise_amount') is None)
    assert(dict.get('revenue_surprise_uom') is None)


def test_parse_tweet_with_guidance_1():
    tweet = 'AngioDynamics Non-GAAP EPS of -$0.06 misses by $0.04, revenue of $81.5M misses by $1.93M, reaffirms FY guidance'
    account = Marketcurrents(Marketcurrents.account_name)
    dict = LoadEarningsReportsFromTwitter.parse_tweet(account, tweet)
    assert (dict.get('eps_sign') == '-')
    assert(dict.get('eps_currency') == '$')
    assert(dict.get('eps') == '0.06')
    assert(dict.get('eps_surprise_direction') == 'misses')
    assert(dict.get('eps_surprise_currency') == '$')
    assert(dict.get('eps_surprise_amount') == '0.04')
    assert(dict.get('revenue_currency') == '$')
    assert(dict.get('revenue') == '81.5')
    assert(dict.get('revenue_uom') == 'M')
    assert(dict.get('revenue_surprise_direction') == 'misses')
    assert(dict.get('revenue_surprise_currency') == '$')
    assert(dict.get('revenue_surprise_amount') == '1.93')
    assert(dict.get('revenue_surprise_uom') == 'M')
    assert(dict.get('guidance_1') == 'reaffirms')


def test_parse_tweet_not_earnings():
    tweet = '$AZZ declares $0.17 dividend'
    account = Marketcurrents(Marketcurrents.account_name)
    dict = LoadEarningsReportsFromTwitter.parse_tweet(account, tweet)
    assert(dict is None)


def test_parse_tweet_livesquawk():
    tweet = '''
    $DAL Delta Airlines Q3 22 Earnings: \
      - Adj EPS $1.51 (est $1.54) \
      - Adj Revenue $12.84B (est $12.83B) \
      - Sees Q4 Adj EPS $1 To $1.25 (est $0.80) \
      - Raises Q4 EPS to $1.00
      '''
    account = Livesquawk(Livesquawk.account_name)
    dict = LoadEarningsReportsFromTwitter.parse_tweet(account, tweet)
    assert(dict.get('eps_sign') is None)
    assert(dict.get('eps_currency') == '$')
    assert(dict.get('eps') == '1.51')
    assert(dict.get('eps_estimate_currency') == '$')
    assert(dict.get('eps_estimate_amount') == '1.54')
    assert(dict.get('revenue_currency') == '$')
    assert(dict.get('revenue') == '12.84')
    assert(dict.get('revenue_uom') == 'B')
    assert(dict.get('revenue_estimate_currency') == '$')
    assert(dict.get('revenue_estimate_amount') == '12.83')
    assert(dict.get('revenue_estimate_uom') == 'B')
    assert(dict.get('guidance_1').lower() == 'raises')


def test_parse_tweet_livesquawk_without_uom():
    tweet = '''
    $UNH UnitedHealth Q3 22 Earnings: 
- EPS $5.55 (est $5.20) 
- Revenue $46.56 (exp $45.54) 
- Sees FY EPS $ 20.85 To $21.05 (prev $20.45 To $20.95
'''
    account = Livesquawk(Livesquawk.account_name)
    dict = LoadEarningsReportsFromTwitter.parse_tweet(account, tweet)
    assert(dict.get('eps_sign') is None)
    assert(dict.get('eps_currency') == '$')
    assert(dict.get('eps') == '5.55')
    assert(dict.get('eps_estimate_currency') == '$')
    assert(dict.get('eps_estimate_amount') == '5.20')
    assert(dict.get('revenue_currency') == '$')
    assert(dict.get('revenue') == '46.56')
    assert(dict.get('revenue_uom') is None)
    assert(dict.get('revenue_estimate_currency') == '$')
    assert(dict.get('revenue_estimate_amount') == '45.54')
    assert(dict.get('revenue_estimate_uom') is None)


def test_parse_tweet_livesquawk_revenue_first():
    tweet = '''
    $SCHW Charles Schwab Q3 22 Earnings:  
    - Revenue: $5.5B (exp $5.41B)  
    - Adj EPS: $1.10 (exp $1.05)'''
    account = Livesquawk(Livesquawk.account_name)
    dict = LoadEarningsReportsFromTwitter.parse_tweet(account, tweet)
    assert (dict.get('eps_sign') is None)
    assert (dict.get('eps_currency') == '$')
    assert (dict.get('eps') == '1.10')
    assert (dict.get('eps_estimate_currency') == '$')
    assert (dict.get('eps_estimate_amount') == '1.05')
    assert (dict.get('revenue_currency') == '$')
    assert (dict.get('revenue') == '5.5')
    assert (dict.get('revenue_uom') == 'B')
    assert (dict.get('revenue_estimate_currency') == '$')
    assert (dict.get('revenue_estimate_amount') == '5.41')
    assert (dict.get('revenue_estimate_uom') == 'B')


def test_parse_tweet_livesquawk_worded_estimated():
    tweet = '''
$UAL United Airlines Q3 22 Earnings: 
- Adj EPS: $2.81 (Estimate: $2.29) 
- Passenger Revenue: $11.65B (Estimate: $11.39B) 
- Sees Q4 Adj. Op Margin To Exceed 2019'''
    account = Livesquawk(Livesquawk.account_name)
    dict = LoadEarningsReportsFromTwitter.parse_tweet(account, tweet)
    assert (dict.get('eps_sign') is None)
    assert (dict.get('eps_currency') == '$')
    assert (dict.get('eps') == '2.81')
    assert (dict.get('eps_estimate_currency') == '$')
    assert (dict.get('eps_estimate_amount') == '2.29')
    assert (dict.get('revenue_currency') == '$')
    assert (dict.get('revenue') == '11.65')
    assert (dict.get('revenue_uom') == 'B')
    assert (dict.get('revenue_estimate_currency') == '$')
    assert (dict.get('revenue_estimate_amount') == '11.39')
    assert (dict.get('revenue_estimate_uom') == 'B')


tweet = '$BLK BlackRock Q3 22 Earnings: \
    - Adj EPS $9.55 (est $7.03) \
    - Revenue $4.31B (est $4.33B) \
    - AUM $7.96T (est $8.27T)'

# Corp actions
event = '$FUBO - FuboTV jumps 14% on upbeat early Q3 results, closing Fubo Gaming'  # No earnings accompanying
event = '$XPO - XPO Logistics comes in lighter than expected on preliminary results'  # No earnings accompanying
event = '$MATX - Matson dips 2% on prelim Q3 figures'
event = '$SYY - Trucker strike disrupts Sysco facility in Massachusetts'
event = '$RARE $MREO - Mereo BioPharma to shed 40% of workforce as part of cost-cutting plan'
event = '$NFLX $MSFT $TWTR - Microsoft laid off around 1,000 employees across various division citing global slowdown'

# Industry
event = '$MGM $PENN $CZR - DraftKings and Penn Entertainment rally after sports betting data comes in strong'  #  'sports betting'
event = '$CCJ $UUUU $DNN - Uranium shares surge as Germany extends life of three nuclear plants'  # 'uranium'
event = '$SWK $TREX $CSL - Building-product stocks slump as mortgage applications hit 25-year low'  # building products
event = '$AAPL $AMD $INTC - Chips mostly lower as yields rise; ASML guidance buoys semiconductor equipment stocks'  # semiconductors

# Buybacks, repurchases
event = '$BCBP - BCB Bancorp increases stock buyback program'
event = '$GNUS - Genius Brands announces buyback of common shares'
event = '$TOTZF $TOT:CA - Total Energy Services plans buyback'
event = '$NVGS - Navigator launches $50M stock repurchase plan'


# Pharma
event = '$RYAAY $DLAKY $EJTTF - Strong forecasts from IAG, easyJet send European airline stocks soaring'
event = "$GILD - Gilead's CAR-T therapy Yescarta gets European approval for second-line treatment of lymphoma"
event = '$INO - Inovio reports positive phase 1/2 results for recurrent respiratory papillomatosis drug'
event = '$DARE - Daré rises on positive data from early-to-mid-stage trial of intravaginal ring to treat menopause symptoms'
event = "$ATHA - Athira Alzheimer's drug trial gets monitoring panel nod to continue after efficacy analysis"
event = '$REGN $DBTX - Decibel stock surges 18% as FDA clears hearing loss gene therapy to enter trial'
event = '$ENOB - Enochian stock climbs on US patent for oncology platform'
event = '$MREO - Mereo stock rises 12% on FDA fast-track status for lung disease drug alvelestat'
event = "$GSK - GSK's single-vial presentation of meningococcal vaccine Menveo gets FDA approval"
event = '$CLVS - Clovis radiotherapy for tumors shows promise in early-stage study'
event = '$SLRX - Salarius drops 27% after patient death in cancer trial for lead asset'
event = '$TOMZ - TOMI Environmental rises as SteraMist to be used in influenza vaccine facility in Australia'
event = '$CRL - Charles River rises on collaboration to make gene therapies for vision disorders'
event = '$CMRA - Comera Life Sciences rises on positive preclinical data from Sequrus study'
event = '$AVRO - Avrobio rises as gene therapy for Gaucher disease gets ILAP designation in UK'
event = "$BMY - Bristol-Myers' Opdivo cancer drug reduces risk of death in resected stage II melanoma"

# link parsing?
earn = '$PVSP - Pervasip reports Q3 results https://t.co/C8qj3mitG9'  # several more
earn = '$SBNY - Signature Bank bottom line tops consensus on higher rates, loan growth'
event = '$GRPRF - Grupo Rotoplas S.A.B. de C.V. reports Q3 results'

event = '$Y $AR - Antero Resources jumps 5% on addition to MidCap 400'
event = '$AGFY - Agrify dips on plan to execute 1-for-10 reverse stock split'
event = '$RLMD - Relmada spikes as Steve Cohen’s Point72 discloses 7% stake'
event = '$UP - Wheels up Experience stock soars on new financing agreement'
event = '$CI - Cigna faces government lawsuit over fraudulent Medicare Advantage payments'
event = "$NLST $SSNLF $GOOGL - Netlist plunges after Samsung '912 IPR patent trial institute"
event = '$CZR - Caesars Entertainment pops with casino traffic said to be still strong' # industry = casino. study: entities
event = "$BHP $VALE $RIO - Iron ore drops near lowest in a year as China's Xi reiterates COVID restrictions" # industry = iron ore
event = '$PTRA - Proterra rallies after BTIG calls out 50% upside off commercial EV upside' # industry = commercial EV?
event = '$AMSC $FAN $TPIC - TPI Composites jumps as U.S. plans sale of wind rights off California coast' # industry - wind energy
event = '$GOEV - Canoo stock surges on order for 9,300 EVs'


# Earnings summary
event = '$BAC - Bank of America Q3 earnings top consensus on higher interest, strong consumer'
event = '$UNH - UnitedHealth stock trades higher as revenue soars 12%, FY22 outlook raised again'
event = '$SI - Silvergate Capital stock slides after Q3 earnings hurt buy lower network usage'
event = '$STT - State Street stock climbs after Q3 earnings bolstered by NII growth, $1B buyback plan'
event = '$LBRT - Liberty Energy beats Q3 estimates on "record operational performance'
event = '$STLD - Steel Dynamics tops Q3 estimates, as steel shipments hit quarterly record'
event = '$IBM - IBM heads for higher ground on upbeat outlook and earnings results'
event = '$MKTX - MarketAxess trades down after Q3 revenue miss, updated guidance'

# Mergers, acquisitions
event = '$BP $LFG - BP to buy Archaea Energy for $26/share'
event = '$CVS $CANO - Cano Health plunges 21% on report CVS has walked away from pursuit' # challenge - 2 tickers, one walks away
event = '$SPLK - Splunk jumps 10% on reports activist Starboard has taken stake'
event = '$CRM - Salesforce jumps on report activist Starboard has taken stake'
event = '$LLY $REGN $AKUS - Decibel Therapeutics hears it may be an takeout target after Lilly acquisition of Akouos'
event = '$AVEO $LGCLF - AVEO Oncology shares jumped on acqusition by LG Chem for $15.00 per share in cash'

# Guidance-driven
event = 'NEWS: $INMD InMode Expects Record Third Quarter 2022 Revenue of $120.5M-$120.9M, Raising Full-Year 2022 Revenue Guidance to $445M-450M'
event = '$SM - SM Energy sinks after lower than expected Q3 production'
event = '$MAIN - Main Street Capital sees quarterly record for NII in Q3, higher NAV'
event = '$INMD - InMode gains after setting strong-than-anticipated Q3 pre-results, guidance'
event = '$TPB - Turning Point Brands guides Q3 sales above consensus, revises full-year outlook'
event = 'Will Intuitive Surgical Q3 earnings bring positive surprise amid COVID woes, pressure on stock?' # ignore question mark at the end
event = '$RWT - Redwood Trust stock gains 5% after hours on preliminary Q3 results'
event = '$QDEL - QuidelOrtho forecasts strong Q3 revenue above estimates, shares rise ~6% after hours'
event = '$PLUG - Plug Power plunges as full-year revenues seen missing guidance'
event = '$THTX $TH:CA - Theratechnologies reports Q3 results, FY22 guidance is on track'
event = '$PCRX - Pacira BioSciences guides Q3 revenue below consensus'
event = '$VSH - Vishay Intertechnology climbs higher on raising Q3 revenue guidance'
event = '$RHHBY $RHHBF - Roche Q3 sales falls as COVID products slump; confirms FY22 outlook'
event = '$SILK - Silk Road Medical sees Q3 revenue $37.4M, consensus $33.5M'
event = '$PPG - PPG dips after guiding for below-consensus Q4 earnings'
event = '$SMCI - Super Micro Computer raises FQ1 2023 guidance, stock soars ~18% after hours'
event = '$ALL - Allstate estimates Q3 net loss on high catastrophe losses; stock drops'
event = '$EFX - Equifax cuts EPS guidance as housing cooldown hits Mortgage Solutions revenue'
event = '$AA - Alcoa swings to Q3 loss; cuts alumina, bauxite shipment guidance'
event = '$WU - Western Union guides Q3 earnings above estimates, maintains FY outlook'

# reject due to error
earn = '$PPG - PPG Non-GAAP EPS of $1.66 beats by $0.01, revenue of $4.47M misses by $4.45B'
