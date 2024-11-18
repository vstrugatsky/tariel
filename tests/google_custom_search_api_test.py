from urllib.parse import urlparse
import requests
import urllib
from config import config

def test_google_custom_search_api():
    prefix = 'https://customsearch.googleapis.com/customsearch/v1'
    key = config.google['custom_search_api_key']
    engine_id = config.google['custom_search_engine_id']
    website = 'dicks.com'
    company = "DICK'S Sporting Goods"
    ticker = 'HPE'
    text = 'quarter earnings'
    query =  'intitle:' + company + ' ' + text
    # daysToSearch = 45

    url = f'{prefix}?key={key}&cx={engine_id}&q={query}&sort=date&siteSearch={website}' # &linkSite={website}' # &dateRestrict=d{daysToSearch}'
    print(url)
    r = requests.get(url)
    print(r.status_code)
    print(r.json()['url'])
    print(r.json()['queries'])

    if r.json()['items']:
        for item in r.json()['items']:
            domain = urlparse(item['link']).netloc
            print(item['title'] + ' ' + domain + ' ' + item['snippet'])

def test_google_search():
    prefix = 'https://google.com/search' # Scraping results against Google Terms of service
    website = 'hellogroup.com'
    sites = 'site:' + website + '+OR+site:prnewswire.com+OR+site:globenewswire.com+OR+site:businesswire.com+OR+site:accesswire.com'
    company = 'Hello+Group'
    ticker = 'MOMO'
    text = 'quarter'
    verbatim = 'li:1'
    query = company + '+' + text + '+' + sites

    url = f'{prefix}?&q={query}&tbs={verbatim}'
    print(url)
    r = requests.get(url)
    print(r.status_code)
    print(r.text)


def test_403_requests():
    url = 'https://www.globenewswire.com/news-release/2024/08/09/2927920/0/en/Zscaler-to-Host-Fourth-Quarter-and-Fiscal-Year-2024-Earnings-Conference-Call.html'
    headers = {
        # 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:106.0) Gecko/20100101 Firefox/106.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
        # 'Accept-Language': 'en-US,en;q=0.5',
        # # 'Accept-Encoding': 'gzip, deflate, br',
        # 'DNT': '1',
        # 'Connection': 'keep-alive',
        # 'Upgrade-Insecure-Requests': '1',
        # 'Sec-Fetch-Dest': 'document',
        # 'Sec-Fetch-Mode': 'navigate',
        # 'Sec-Fetch-Site': 'none',
        # 'Sec-Fetch-User': '?1',
    }
    r = requests.get(url, headers=headers)
    print(r.status_code)
    print(r.text)


def test_403_urllib():
    req = urllib.request.Request('https://investorsmedia.mesoblast.com/')
    req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:106.0) Gecko/20100101 Firefox/106.0')
    req.add_header('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8')
    req.add_header('Accept-Language', 'en-US,en;q=0.5')

    r = urllib.request.urlopen(req).read().decode('utf-8')
    print(r)

   