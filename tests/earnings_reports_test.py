import model
from loaders.earnings_reports_from_twitter import LoadEarningsReportsFromTwitter
from loaders.twitter_livesquawk import Livesquawk
from loaders.twitter_marketcurrents import Marketcurrents
from model.earnings_reports import EarningsReport
from model.jobs import Provider
from model.symbols import Symbol
from utils.utils import Utils


def test_should_update():
    er = EarningsReport(creator=Provider['Twitter_Livesquawk'], updater=None)
    provider = 'Twitter_Livesquawk'
    assert(LoadEarningsReportsFromTwitter.should_update(er, provider) is True)

    er = EarningsReport(creator=Provider['Twitter_Marketcurrents'], updater=None)
    provider = 'Twitter_Marketcurrents'
    assert(LoadEarningsReportsFromTwitter.should_update(er, provider) is True)

    er = EarningsReport(creator=Provider['Twitter_Livesquawk'], updater=None)
    provider = 'Twitter_Marketcurrents'
    assert(LoadEarningsReportsFromTwitter.should_update(er, provider) is True)

    er = EarningsReport(creator=Provider['Twitter_Livesquawk'], updater=Provider['Twitter_Livesquawk'])
    provider = 'Twitter_Marketcurrents'
    assert(LoadEarningsReportsFromTwitter.should_update(er, provider) is True)

    er = EarningsReport(creator=Provider['Twitter_Livesquawk'], updater=Provider['Twitter_Marketcurrents'])
    provider = 'Twitter_Livesquawk'
    assert(LoadEarningsReportsFromTwitter.should_update(er, provider) is False)


def test_determine_currency():
    assert(LoadEarningsReportsFromTwitter.determine_currency(eps_currency=None, revenue_currency=None) is None)
    assert(LoadEarningsReportsFromTwitter.determine_currency('$', None) == 'USD')
    assert(LoadEarningsReportsFromTwitter.determine_currency(None, '$') == 'USD')
    assert(LoadEarningsReportsFromTwitter.determine_currency('$', '$') == 'USD')


def test_determine_eps():
    # determine_eps(eps_sign: str | None, eps: str | None) -> float:
    assert(LoadEarningsReportsFromTwitter.determine_eps(eps_sign=None, eps=None) is None)
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

    match_dict = {'eps_surprise_direction': 'in-line', 'eps_surprise_amount': None, 'eps_surprise_uom': None}
    assert (loader.account.determine_surprise(match_dict=match_dict, metrics='eps') == 0.00)


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
    loader = LoadEarningsReportsFromTwitter(Marketcurrents(Marketcurrents.account_name))
    with model.Session() as session:
        tweet = 'something irrelevant'
        cashtags = [{'start': 0, 'end': 4, 'tag': 'PPG'}]
        returned_symbols, eliminated_symbols = loader.associate_tweet_with_symbols(session, cashtags, tweet, 'url desc')
        assert('PPG' in returned_symbols.keys())

        cashtags = [{'start': 0, 'end': 4, 'tag': 'SPY'},
                    {'start': 5, 'end': 9, 'tag': 'WMTZZ'},
                    {'start': 10, 'end': 15, 'tag': 'AAPLZZ'}]
        returned_symbols, eliminated_symbols = loader.associate_tweet_with_symbols(session, cashtags, tweet, 'url desc')
        assert('SPY' in returned_symbols.keys())
        assert(len(returned_symbols.keys()) == 1)

        cashtags = [{'start': 0, 'end': 4, 'tag': 'SPY'},
                    {'start': 5, 'end': 9, 'tag': 'SPY'}]
        returned_symbols, eliminated_symbols = loader.associate_tweet_with_symbols(session, cashtags, tweet, 'url desc')
        assert('SPY' in returned_symbols.keys())
        assert(len(returned_symbols.keys()) == 1)

        cashtags = [{'start': 0, 'end': 4, 'tag': 'SPY'},
                    {'start': 5, 'end': 9, 'tag': 'SPYZZZ'}]
        returned_symbols, eliminated_symbols = loader.associate_tweet_with_symbols(session, cashtags, tweet, 'url desc')
        assert('SPY' in returned_symbols.keys())
        assert(len(returned_symbols.keys()) == 1)

        cashtags = [{'start': 0, 'end': 4, 'tag': 'GFELF'},
                    {'start': 5, 'end': 9, 'tag': 'ZZ'}]
        returned_symbols, eliminated_symbols = loader.associate_tweet_with_symbols(session, cashtags, tweet, 'url desc')
        assert('GFELF' in returned_symbols.keys())
        assert(len(returned_symbols.keys()) == 1)

        cashtags = [{'start': 0, 'end': 4, 'tag': 'SPYZZZ'}]
        returned_symbols, eliminated_symbols = loader.associate_tweet_with_symbols(session, cashtags, tweet, 'url desc')
        assert(not returned_symbols)

        cashtags = None
        returned_symbols, eliminated_symbols = loader.associate_tweet_with_symbols(session, cashtags, tweet, 'url desc')
        assert(not returned_symbols)


def test_eliminate_spurious_symbols_ALK_SKYW_DAL():
    loader = LoadEarningsReportsFromTwitter(Marketcurrents(Marketcurrents.account_name))
    with model.Session() as session:
        symbols = {}
        tweet = '$ALK $SKYW $DAL - SkyWest stock flies higher as quarterly profits surpass expectations https://t.co/vvv1gDxLk7'
        tweet_desc = 'SkyWest (SKYW) shares rose sharply in Thursday’s extended session after posting stronger than expected profits for Q3.'
        symbols['ALK'] = Symbol.get_unique_by_ticker_and_country(session, 'ALK', 'US')
        symbols['SKYW'] = Symbol.get_unique_by_ticker_and_country(session, 'SKYW', 'US')
        symbols['DAL'] = Symbol.get_unique_by_ticker_and_country(session, 'DAL', 'US')

        retained_symbols, eliminated_symbols = loader.eliminate_spurious_symbols(session, tweet, tweet_desc, symbols)
        assert('SKYW' in retained_symbols)
        assert('ALK' in eliminated_symbols)
        assert('DAL' in eliminated_symbols)


def test_eliminate_spurious_symbols_NVZMF_NVZMY():
    loader = LoadEarningsReportsFromTwitter(Marketcurrents(Marketcurrents.account_name))
    with model.Session() as session:
        symbols = {}
        tweet = '$NVZMF $NVZMY - Novozymes A/S reports Q3 results; raises its full-year organic sales growth outlook https://t.co/vvv1gDxLk7'
        tweet_url_desc = "Novozymes A/S press release (NVZMF): Q3 Revenue of DKK4.37B (+16.2% Y/Y), (6% organic, 9% currency, 1% M&A).Novozymes increases its full-year organic sales growth outlook from..."
        symbols['NVZMF'] = Symbol.get_unique_by_ticker_and_country(session, 'NVZMF', 'US')
        symbols['NVZMY'] = Symbol.get_unique_by_ticker_and_country(session, 'NVZMY', 'US')

        retained_symbols, eliminated_symbols = loader.eliminate_spurious_symbols(session, tweet, tweet_url_desc, symbols)
        assert('NVZMF' in retained_symbols)
        assert('NVZMY' in retained_symbols or 'NVZMY' in eliminated_symbols)


def test_eliminate_spurious_symbols_ASM_TMXFF_INCAF():
    loader = LoadEarningsReportsFromTwitter(Marketcurrents(Marketcurrents.account_name))
    with model.Session() as session:
        symbols = {}
        tweet = '$ASM $TMXXF $INCAF - Inca One Gold Q3 sales fall 1% https://t.co/vvv1gDxLk7'
        tweet_url_desc = "Inca One Gold (INCAF) reports blah-blah Q3"
        symbols['ASM'] = Symbol.get_unique_by_ticker_and_country(session, 'ASM', 'US')
        symbols['TMXXF'] = Symbol.get_unique_by_ticker_and_country(session, 'TMXXF', 'US')
        symbols['INCAF'] = Symbol.get_unique_by_ticker_and_country(session, 'INCAF', 'US')

        retained_symbols, eliminated_symbols = loader.eliminate_spurious_symbols(session, tweet, tweet_url_desc, symbols)
        assert('INCAF' in retained_symbols)
        assert('ASM' in eliminated_symbols)
        assert('TMXXF' in eliminated_symbols)


def test_eliminate_spurious_symbols_VEON_VNLTF():
    loader = LoadEarningsReportsFromTwitter(Marketcurrents(Marketcurrents.account_name))
    with model.Session() as session:
        symbols = {}
        tweet = '$VEON $VNLTF - VEON reports strong Q3 revenue performance gaining market share as countries execute digital operator strategy https://t.co/vvv1gDxLk7'
        tweet_url_desc = "Amsterdam-listed mobile operator VEON (VEON) reported third-quarter revenues rising 3.4% in local currency terms and up 3.6% in dollars, the currency it reports in, to $2.08..."
        symbols['VEON'] = Symbol.get_unique_by_ticker_and_country(session, 'VEON', 'US')
        symbols['VNLTF'] = Symbol.get_unique_by_ticker_and_country(session, 'VNLTF', 'US')

        retained_symbols, eliminated_symbols = loader.eliminate_spurious_symbols(session, tweet, tweet_url_desc, symbols)
        assert('VEON' in retained_symbols)
        assert('VNLTF' in retained_symbols)


def test_associate_tweet_with_symbols_canadian():
    loader = LoadEarningsReportsFromTwitter(Marketcurrents(Marketcurrents.account_name))
    tweet = '$CPG $CPG:CA - Crescent Point Energy GAAP EPS of C$0.82, revenue of C$1.1B https://t.co/vvv1gDxLk7'
    cashtags = [{'start': 0, 'end': 4, 'tag': 'CPG'}, {'start': 5, 'end': 9, 'tag': 'CPG'}]
    with model.Session() as session:
        retained_symbols, eliminated_symbols = loader.associate_tweet_with_symbols(session, cashtags, tweet, 'url desc')
        assert(len(retained_symbols.keys()) == 1)


def test_evaluate_data_quality():
    er = EarningsReport(revenue_surprise=-100, revenue=50)
    assert('-100 too large' in LoadEarningsReportsFromTwitter.evaluate_data_quality(er))

    er = EarningsReport(revenue_surprise=None, revenue=50)
    assert(None is LoadEarningsReportsFromTwitter.evaluate_data_quality(er))

    er = EarningsReport(revenue_surprise=74, revenue=100)
    assert(None is LoadEarningsReportsFromTwitter.evaluate_data_quality(er))

    er = EarningsReport(revenue_surprise=75, revenue=100)
    assert('75 too large' in LoadEarningsReportsFromTwitter.evaluate_data_quality(er))


def test_parse_symbol_from_url_desc():
    loader = LoadEarningsReportsFromTwitter(Marketcurrents(Marketcurrents.account_name))
    tweet_url_desc = "Toyota Motor press release (TM): Q2 net income ¥434.2B, -18.2% Y/YBasic EPS of ¥31.73Revenue of ¥9218.2B (+22.2% Y/Y).Operating income ¥562.79B.FY 2023 Forecast: Sales revenues ¥36T..."
    assert(loader.account.parse_symbol_from_url_desc(tweet_url_desc) == 'TM')


def test_update_sentiment_fields_noop():
    loader = LoadEarningsReportsFromTwitter(Marketcurrents(Marketcurrents.account_name))
    er = EarningsReport()
    loader.update_sentiment_fields(er)
    assert(er.earnings_sentiment == 0)


def test_update_sentiment_fields_based_on_earnings():
    loader = LoadEarningsReportsFromTwitter(Marketcurrents(Marketcurrents.account_name))
    er = EarningsReport(eps_surprise=20, revenue_surprise=200)
    loader.update_sentiment_fields(er)
    assert(er.earnings_sentiment == 2)

    er = EarningsReport(eps_surprise=0, revenue_surprise=200)
    loader.update_sentiment_fields(er)
    assert(er.earnings_sentiment == 1)

    er = EarningsReport(eps_surprise=20, revenue_surprise=0)
    loader.update_sentiment_fields(er)
    assert(er.earnings_sentiment == 1)

    er = EarningsReport(eps_surprise=20, revenue_surprise=-200)
    loader.update_sentiment_fields(er)
    assert(er.earnings_sentiment == 0)

    er = EarningsReport(eps_surprise=-20, revenue_surprise=200)
    loader.update_sentiment_fields(er)
    assert(er.earnings_sentiment == 0)

    er = EarningsReport(eps_surprise=-20, revenue_surprise=0)
    loader.update_sentiment_fields(er)
    assert(er.earnings_sentiment == -1)

    er = EarningsReport(eps_surprise=0, revenue_surprise=-200)
    loader.update_sentiment_fields(er)
    assert(er.earnings_sentiment == -1)


def test_update_sentiment_fields_pos_neg():
    loader = LoadEarningsReportsFromTwitter(Marketcurrents(Marketcurrents.account_name))
    er = EarningsReport(positive_earnings=['earnings beat'], negative_earnings=['weak'])
    loader.update_sentiment_fields(er)
    assert(er.earnings_sentiment == 0)


def test_update_sentiment_fields_triple_pos_neg():
    loader = LoadEarningsReportsFromTwitter(Marketcurrents(Marketcurrents.account_name))
    er = EarningsReport(eps_surprise=0.14, revenue_surprise=200000, positive_earnings=['earnings beat'], negative_earnings=['weak'])
    loader.update_sentiment_fields(er)
    assert(er.earnings_sentiment == 2)



    def test_update_earnings_sentiment():
        loader = LoadEarningsReportsFromTwitter(Marketcurrents(Marketcurrents.account_name))
        assert (loader.update_earnings_sentiment(surprise_amount=20, current_sentiment=0) == 1)
        assert (loader.update_earnings_sentiment(surprise_amount=20, current_sentiment=2) == 2)
        assert (loader.update_earnings_sentiment(surprise_amount=0, current_sentiment=2) == 2)
        assert (loader.update_earnings_sentiment(surprise_amount=-5, current_sentiment=2) == 1)
        assert (loader.update_earnings_sentiment(surprise_amount=-5, current_sentiment=-2) == -2)

    def test_update_positive_sentiment():
        loader = LoadEarningsReportsFromTwitter(Marketcurrents(Marketcurrents.account_name))
        assert (loader.update_positive_sentiment(current_sentiment=0, update=1, max_sentiment=2) == 1)
        assert (loader.update_positive_sentiment(current_sentiment=0, update=2, max_sentiment=2) == 2)
        assert (loader.update_positive_sentiment(current_sentiment=0, update=3, max_sentiment=2) == 2)
        assert (loader.update_positive_sentiment(current_sentiment=-2, update=4, max_sentiment=2) == 2)

    def test_update_negative_sentiment():
        loader = LoadEarningsReportsFromTwitter(Marketcurrents(Marketcurrents.account_name))
        assert (loader.update_negative_sentiment(current_sentiment=0, update=1, max_sentiment=2) == -1)
        assert (loader.update_negative_sentiment(current_sentiment=0, update=2, max_sentiment=2) == -2)
        assert (loader.update_negative_sentiment(current_sentiment=0, update=3, max_sentiment=2) == -2)
        assert (loader.update_negative_sentiment(current_sentiment=2, update=4, max_sentiment=2) == -2)



