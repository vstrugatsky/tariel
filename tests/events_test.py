import model
from datetime import datetime
from model.events import EarningsReport, Event, EventType
from model.symbols import Symbol
from model.jobs import Provider

test_ticker = 'NEWP'


def test_create_er():
    with model.Session() as session:
        symbol = Symbol.get_unique_by_ticker_and_country(session, test_ticker, 'US')
        event_date = datetime.strptime('2022-11-15T11:11:11.000Z', '%Y-%m-%dT%H:%M:%S.%fZ').date()
        er = EarningsReport(event_date=event_date, creator=Provider.Twitter_Marketcurrents.name)
        er.symbols.append(symbol)
        session.add(er)

        loaded_er = Event.get_unique(session, symbol, EventType.Earnings_Report, event_date)
        session.delete(loaded_er)

        session.rollback()
