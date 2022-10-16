from providers import sleep_if_needed, parse_query_param_value
import model
import requests
from config import config


class Atom:
    apiPrefix = 'https://platform.atom.finance/api/2.0'

    # curl - -request POST \
    # --url "https://sandbox-platform.atom.finance/api/2.0/search?api_key=${YOUR_API_KEY}" \
    # --header 'Accept: application/json' \
    # --header 'Content-Type: application/json' \
    # --data '{"query":"cars"}'

# def estimates(payload, json):


if __name__ == '__main__':
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json"
    }
    payload = {
        "limit": 20,
     "asset": {
               "identifier": "ticker",
               "value": "AAPL",
               "assetType": "equity",
               "market": "USA"
          }
    }
    # r = requests.post(Atom.apiPrefix + '/price/snapshot?api_key=' + Atom.apiKey, json=payload, headers=headers)
    # r = requests.post(Atom.apiPrefix + '/equity/estimates?api_key=' + Atom.apiKey, json=payload, headers=headers)
    r = requests.post(Atom.apiPrefix + '/peers?api_key=' + config.atom['api_key'], json=payload, headers=headers)
    print(r.text)