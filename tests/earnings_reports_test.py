import model
from loaders.earnings_reports_from_twitter import LoadEarningsReportsFromTwitter
from loaders.twitter_livesquawk import Livesquawk
from loaders.twitter_marketcurrents import Marketcurrents
from model.earnings_reports import EarningsReport
from model.jobs import Provider
from model.symbols import Symbol
from utils.utils import Utils


def test_update_earnings_sentiment():
    assert(LoadEarningsReportsFromTwitter.update_earnings_sentiment(surprise_amount=20, current_sentiment=0) == 1)
    assert(LoadEarningsReportsFromTwitter.update_earnings_sentiment(surprise_amount=20, current_sentiment=2) == 2)
    assert(LoadEarningsReportsFromTwitter.update_earnings_sentiment(surprise_amount=0, current_sentiment=2) == 2)
    assert(LoadEarningsReportsFromTwitter.update_earnings_sentiment(surprise_amount=-5, current_sentiment=2) == 1)
    assert(LoadEarningsReportsFromTwitter.update_earnings_sentiment(surprise_amount=-5, current_sentiment=-2) == -2)


def test_update_positive_sentiment():
    assert (LoadEarningsReportsFromTwitter.update_positive_sentiment(current_sentiment=0, update=1, max_sentiment=2) == 1)
    assert (LoadEarningsReportsFromTwitter.update_positive_sentiment(current_sentiment=0, update=2, max_sentiment=2) == 2)
    assert (LoadEarningsReportsFromTwitter.update_positive_sentiment(current_sentiment=0, update=3, max_sentiment=2) == 2)
    assert (LoadEarningsReportsFromTwitter.update_positive_sentiment(current_sentiment=-2, update=4, max_sentiment=2) == 2)


def test_update_negative_sentiment():
    assert (LoadEarningsReportsFromTwitter.update_negative_sentiment(current_sentiment=0, update=1, max_sentiment=2) == -1)
    assert (LoadEarningsReportsFromTwitter.update_negative_sentiment(current_sentiment=0, update=2, max_sentiment=2) == -2)
    assert (LoadEarningsReportsFromTwitter.update_negative_sentiment(current_sentiment=0, update=3, max_sentiment=2) == -2)
    assert (LoadEarningsReportsFromTwitter.update_negative_sentiment(current_sentiment=2, update=4, max_sentiment=2) == -2)


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
        assert('PPG' in loader.associate_tweet_with_symbols(session, cashtags, tweet).keys())

        cashtags = [{'start': 0, 'end': 4, 'tag': 'SPY'},
                    {'start': 5, 'end': 9, 'tag': 'WMTZZ'},
                    {'start': 10, 'end': 15, 'tag': 'AAPLZZ'}]
        assert('SPY' in loader.associate_tweet_with_symbols(session, cashtags, tweet).keys())
        assert(len(loader.associate_tweet_with_symbols(session, cashtags, tweet).keys()) == 1)

        cashtags = [{'start': 0, 'end': 4, 'tag': 'SPY'},
                    {'start': 5, 'end': 9, 'tag': 'SPY'}]
        assert('SPY' in loader.associate_tweet_with_symbols(session, cashtags, tweet).keys())
        assert(len(loader.associate_tweet_with_symbols(session, cashtags, tweet).keys()) == 1)

        cashtags = [{'start': 0, 'end': 4, 'tag': 'SPY'},
                    {'start': 5, 'end': 9, 'tag': 'SPYZZZ'}]
        assert('SPY' in loader.associate_tweet_with_symbols(session, cashtags, tweet).keys())
        assert(len(loader.associate_tweet_with_symbols(session, cashtags, tweet).keys()) == 1)

        cashtags = [{'start': 0, 'end': 4, 'tag': 'GFELF'},
                    {'start': 5, 'end': 9, 'tag': 'ZZ'}]
        assert('GFELF' in loader.associate_tweet_with_symbols(session, cashtags, tweet).keys())
        assert(len(LoadEarningsReportsFromTwitter.associate_tweet_with_symbols(session, cashtags, tweet).keys()) == 1)

        cashtags = [{'start': 0, 'end': 4, 'tag': 'SPYZZZ'}]
        assert(not loader.associate_tweet_with_symbols(session, cashtags, tweet))

        cashtags = None
        assert(not loader.associate_tweet_with_symbols(session, cashtags, tweet))


def test_eliminate_spurious_symbols_ALK_SKYW_DAL():
    with model.Session() as session:
        symbols = {}
        tweet = '$ALK $SKYW $DAL - SkyWest stock flies higher as quarterly profits surpass expectations'
        symbols['ALK'] = Symbol.get_unique_by_ticker_and_country(session, 'ALK', 'US')
        symbols['SKYW'] = Symbol.get_unique_by_ticker_and_country(session, 'SKYW', 'US')
        symbols['DAL'] = Symbol.get_unique_by_ticker_and_country(session, 'DAL', 'US')

        retained_symbols = LoadEarningsReportsFromTwitter.eliminate_spurious_symbols(session, tweet, symbols)
        assert('SKYW' in retained_symbols)
        assert('ALK' not in retained_symbols)
        assert('DAL' not in retained_symbols)


def test_eliminate_spurious_symbols_NVZMF_NVZMY():
    with model.Session() as session:
        symbols = {}
        tweet = '$NVZMF $NVZMY - Novozymes A/S reports Q3 results; raises its full-year organic sales growth outlook'
        symbols['NVZMF'] = Symbol.get_unique_by_ticker_and_country(session, 'NVZMF', 'US')
        symbols['NVZMY'] = Symbol.get_unique_by_ticker_and_country(session, 'NVZMY', 'US')

        retained_symbols = LoadEarningsReportsFromTwitter.eliminate_spurious_symbols(session, tweet, symbols)
        assert('NVZMF' in retained_symbols)
        assert('NVZMY' in retained_symbols)


def test_eliminate_spurious_symbols_ASM_TMXFF_INCAF():
    with model.Session() as session:
        symbols = {}
        tweet = '$ASM $TMXXF $INCAF - Inca One Gold Q3 sales fall 1%'
        symbols['ASM'] = Symbol.get_unique_by_ticker_and_country(session, 'ASM', 'US')
        symbols['TMXXF'] = Symbol.get_unique_by_ticker_and_country(session, 'TMXXF', 'US')
        symbols['INCAF'] = Symbol.get_unique_by_ticker_and_country(session, 'INCAF', 'US')

        retained_symbols = LoadEarningsReportsFromTwitter.eliminate_spurious_symbols(session, tweet, symbols)
        assert('INCAF' in retained_symbols)
        assert('ASM' not in retained_symbols)
        assert('TMXXF' not in retained_symbols)


def test_eliminate_spurious_symbols_VEON_VNLTF():
    with model.Session() as session:
        symbols = {}
        tweet = '$VEON $VNLTF - VEON reports strong Q3 revenue performance gaining market share as countries execute digital operator strategy'
        symbols['VEON'] = Symbol.get_unique_by_ticker_and_country(session, 'VEON', 'US')
        symbols['VNLTF'] = Symbol.get_unique_by_ticker_and_country(session, 'VNLTF', 'US')

        retained_symbols = LoadEarningsReportsFromTwitter.eliminate_spurious_symbols(session, tweet, symbols)
        assert('VEON' in retained_symbols)
        assert('VNLTF' in retained_symbols)


def test_associate_tweet_with_symbols_canadian():
    tweet = '$CPG $CPG:CA - Crescent Point Energy GAAP EPS of C$0.82, revenue of C$1.1B'
    cashtags = [{'start': 0, 'end': 4, 'tag': 'CPG'}, {'start': 5, 'end': 9, 'tag': 'CPG'}]
    with model.Session() as session:
        assert(len(LoadEarningsReportsFromTwitter.associate_tweet_with_symbols(session, cashtags, tweet).keys()) == 1)


def test_evaluate_data_quality():
    er = EarningsReport(revenue_surprise=-100, revenue=50)
    assert('-100 too large' in LoadEarningsReportsFromTwitter.evaluate_data_quality(er))

    er = EarningsReport(revenue_surprise=None, revenue=50)
    assert(None is LoadEarningsReportsFromTwitter.evaluate_data_quality(er))

    er = EarningsReport(revenue_surprise=74, revenue=100)
    assert(None is LoadEarningsReportsFromTwitter.evaluate_data_quality(er))

    er = EarningsReport(revenue_surprise=75, revenue=100)
    assert('75 too large' in LoadEarningsReportsFromTwitter.evaluate_data_quality(er))