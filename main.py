# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.
import model as model
from model.api_request import ApiRequest
import requests
import feedparser


def time_series_daily(symbol, outputsize='full'):
    payload = {'function': 'TIME_SERIES_DAILY',
               'apikey': model.alphavantageApiKey, 'symbol': symbol, 'outputsize': outputsize}
    r = requests.get(model.alphavantagePrefix, params=payload)
    print(r.url)
    print(r.json())
    print(r.status_code)
    session = model.Session()
    api_request = ApiRequest(url=r.url, status_code=r.status_code)
    session.add(api_request)
    session.commit()


# Press the green button in the gutter to run the script.
# if __name__ == '__main__':
    # time_series_daily('IBM', outputsize=None)
    # eod_update_exchanges()
    # eod_update_symbols('US')
    # polygon_update_symbols('stocks', 10, False)
    # polygon_update_symbols('otc', 10, False)
    # load_countries()


