import model
from loaders.events_from_twitter import LoadEventsFromTwitter
from loaders.ers_from_twitter import LoadERFromTwitter
from loaders.twitter_livesquawk import Livesquawk  # noqa
from loaders.twitter_marketcurrents import Marketcurrents
from model.events import ER

test_symbol = 'NEWP'  # should not have ER records with surprises or sentiments


def test_load_basic_tweet():
    tweet = {'text': '$' + test_symbol + ' Q3 earnings beat',
             'id': 123456789,
             'twitter_account': 'marketcurrents',
             'author_id': '987654321',
             'created_at': '2022-11-03T00:12:43.000Z',
             'entities': {'cashtags': [{'start': 0, 'end': 4, 'tag': test_symbol}]}}
    driver = LoadEventsFromTwitter(Marketcurrents('Marketcurrents'))
    with model.Session() as session:
        er: ER = LoadERFromTwitter(driver.account).load(session, tweet, driver)
        assert er
        assert (er.parsed_positive == ['Q3 earnings beat'])
        session.rollback()


def test_dup_prevention():
    tweet_1 = {'text': '$' + test_symbol + ' - IDACORP GAAP EPS of $2.10 beats by $0.05',
               'created_at': '2022-11-03T15:45:11.000Z',
               'id': 123456789,
               'twitter_account': 'marketcurrents',
               'author_id': '987654321',
               'entities': {'cashtags': [{'start': 0, 'end': 4, 'tag': test_symbol}]}}
    tweet_2 = {
        'text': '$' + test_symbol + ' - IDACORP GAAP EPS of $2.10 beats by $0.05',
        'id': 123456788,
        'created_at': '2022-11-03T15:23:14.000Z',
        'twitter_account': 'marketcurrents',
        'author_id': '987654321',
        'entities': {'cashtags': [{'start': 0, 'end': 4, 'tag': test_symbol}]}}
    driver = LoadEventsFromTwitter(Marketcurrents('Marketcurrents'))
    with model.Session() as session:
        er: ER = LoadERFromTwitter(driver.account).load(session, tweet_1, driver)
        assert er
        assert (str(round(er.eps_surprise, 2)) == '0.05')
        assert (er.sentiment == 1)
        er_id = er.id

        er: ER = LoadERFromTwitter(driver.account).load(session, tweet_2, driver)
        assert (er.id == er_id)
        assert (str(round(er.eps_surprise, 2)) == '0.05')
        assert (er.sentiment == 1)


def test_wipeout_prevention():
    tweet_1 = {
        'text': '$' + test_symbol + ' - Geron posts wider-than- expected Q3 loss, cuts outlook https://t.co/Zxr1WWoIDU',
        'created_at': '2022-11-03T15:45:11.000Z',
        'id': 123456789,
        'twitter_account': 'marketcurrents',
        'author_id': '987654321',
        'entities': {'cashtags': [{'start': 0, 'end': 4, 'tag': test_symbol}]}}
    tweet_2 = {
        'text': '$' + test_symbol + ' - Geron GAAP EPS of -$0.10 misses by $0.01, revenue of $0.3M beats by $0.21M, guides EPS lower',
        'id': 123456788,
        'created_at': '2022-11-03T15:23:14.000Z',
        'twitter_account': 'marketcurrents',
        'author_id': '987654321',
        'entities': {'cashtags': [{'start': 0, 'end': 4, 'tag': test_symbol}]}}
    tweet_3 = {
        'text': '$' + test_symbol + ' GERN slides on Q3 miss, Q3 loss, cost overruns, lowered FY23 guidance',
        'id': 123456787,
        'created_at': '2022-11-03T15:22:14.000Z',
        'twitter_account': 'marketcurrents',
        'author_id': '987654321',
        'entities': {'cashtags': [{'start': 0, 'end': 4, 'tag': test_symbol}]}}
    driver = LoadEventsFromTwitter(Marketcurrents('Marketcurrents'))
    with model.Session() as session:
        er: ER = LoadERFromTwitter(driver.account).load(session, tweet_1, driver)
        assert er
        assert (er.parsed_negative == ['Q3 loss'])
        assert (er.sentiment == -1)
        er_id = er.id

        er: ER = LoadERFromTwitter(driver.account).load(session, tweet_2, driver)
        assert (er.id == er_id)
        assert (str(round(er.eps_surprise, 2)) == '-0.01')
        assert (er.revenue_surprise == 210000)
        assert (er.parsed_negative == ['Q3 loss'])
        assert (er.sentiment == -1)

        er: ER = LoadERFromTwitter(driver.account).load(session, tweet_3, driver)
        assert (er.id == er_id)
        assert (str(round(er.eps_surprise, 2)) == '-0.01')
        assert (er.revenue_surprise == 210000)
        assert (er.sentiment == -2)
        assert (sorted(er.parsed_negative) == ['Q3 loss', 'Q3 miss', 'cost overrun'])

        session.rollback()


def test_two_positive_numbers_mixed_sentiment():
    tweet_1 = {
        'text': '$' + test_symbol + ' - Universal Display stock soars 15% on earnings beat despite weak near-term OLED demand https://t.co/c64GGWUQKm',
        'id': 123456789,
        'created_at': '2022-11-04T14:11:35.000Z',
        'twitter_account': 'marketcurrents',
        'author_id': '987654321',
        'entities': {'cashtags': [{'start': 0, 'end': 4, 'tag': test_symbol}]}}
    tweet_2 = {
        'text': '$' + test_symbol + ' - Universal Display GAAP EPS of $1.12 beats by $0.14, revenue of $160.56M beats by $13.61M https://t.co/OPgOktdzFZ',
        'created_at': '2022-11-03T20:15:27.000Z',
        'id': 123456788,
        'twitter_account': 'marketcurrents',
        'author_id': '987654321',
        'entities': {'cashtags': [{'start': 0, 'end': 4, 'tag': test_symbol}]}}

    driver = LoadEventsFromTwitter(Marketcurrents('Marketcurrents'))
    with model.Session() as session:
        er: ER = LoadERFromTwitter(driver.account).load(session, tweet_1, driver)
        assert er
        assert (er.parsed_positive == ['earnings beat'])
        assert (er.parsed_negative == ['weak near-term OLED demand'])
        assert (er.eps_surprise is None)
        assert (er.revenue_surprise is None)
        assert (er.sentiment == 0)
        er_id = er.id

        er: ER = LoadERFromTwitter(driver.account).load(session, tweet_2, driver)
        assert (er.id == er_id)
        assert (str(round(er.eps_surprise, 2)) == '0.14')
        assert (str(er.revenue_surprise) == '13610000')
        assert (er.parsed_positive == ['earnings beat'])
        assert (er.parsed_negative == ['weak near-term OLED demand'])
        assert (er.sentiment == 2)
