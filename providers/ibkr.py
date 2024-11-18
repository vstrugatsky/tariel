from __future__ import annotations
from datetime import datetime
import requests
import time

import urllib3

baseUrl = "https://localhost:7498/v1/api"
websocketUrl = "wss://localhost:5000/v1/api/ws"
regAcctId = "U14546299"
iraAcctId = "U14555356"
paperRegId = "DU9017794"
paperIraId = "DU9288971"

class IbkrCommon:
    @staticmethod
    def disable_warnings():
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

    @staticmethod
    def request_retry(url, max_retries=4, backoff_factor=0.3, status_forcelist=[404, 500, 502, 503, 504]):
        for i in range(max_retries):
            try:
                response = requests.get(url, verify=False)
                if response.status_code not in status_forcelist:
                    return response
            except requests.exceptions.RequestException:
                print(f"*** In Retry Request Exception {url} failed")
                pass
            
            print(f"In retry will sleep a little {backoff_factor * (2 ** i)}")
            time.sleep(backoff_factor * (2 ** i))
        
        return None
    
    @staticmethod
    def load_contracts(exchange: str) -> dict[str, str]:
        IbkrCommon.disable_warnings()
        contracts = {}
        request_url = f"{baseUrl}/trsrv/all-conids?exchange={exchange}"
        response = requests.get(url=request_url, verify=False)
        print(response.status_code, request_url)

        for entry in response.json():
            contracts[entry['ticker']] = entry['conid']
        print(f"loaded {len(contracts)} {exchange} contracts")
        return contracts
    
class IbkrHistoricalData:    
    timestamp: int
    open: float
    close: float
    high: float
    low: float
    volume: float

    @staticmethod
    def get_historical_data(conid: str, lookback_days: int) -> list[IbkrHistoricalData] | None:
        IbkrCommon.disable_warnings()
        request_url = f"{baseUrl}/hmds/history?conid={conid}&period={lookback_days}d&bar=1d&direction=-1&outsideRth=false" # direction old to new
        response = IbkrCommon.request_retry(request_url)
        print(response.status_code, request_url)

        if not response.json().get('data'):
            print(f"*** {request_url} returned no data {response.json()}")
            return None
        
        bars = []      
        for index, bar in enumerate(response.json().get('data')):
            ibhd = IbkrHistoricalData()
            ibhd.timestamp = bar['t']
            ibhd.open = bar['o']
            ibhd.close = bar['c']
            ibhd.high = bar['h']
            ibhd.low = bar['l']
            ibhd.volume = bar['v']
            bars.append(ibhd)

        return bars

class IbkrMarketDataSnapshot:
    def __init__(self, conid: str):
        self.conid = conid

    conid: str
    last: str
    yest: str
    roc1: str
    iv: str
    hv21: str
    hv30_ib: str
    iv2hv_ib: str
    p2c: str
    v: str
    v30: str
    cap: str
    earn: str
    o: str
    h: str
    l: str
    h52w: str
    l52w: str
    div: str
    eps: str
    c2ema100: str
    shortable: str
    fee: str

    @staticmethod
    def get_market_snapshot(conids: str) -> dict[str, IbkrMarketDataSnapshot] | None:
        IbkrCommon.disable_warnings()
        market_data_snapshots = {}

        request_url = f"{baseUrl}/iserver/accounts" # preflight required
        response = requests.get(url=request_url, verify=False)
        print(response.status_code, request_url)
        if response.status_code != 200:
            print(f"*** {request_url} failed"); exit(1)

        fields = "31,55,70,71,83,87,88,7051,7059,7084,7085,7087,7088,7281,7282,7283,7287,7288,7289,7291,7293,7294,7295,7607,7636,7637,7644,7675,7679,7682,7686,7718,7741"
        request_url = f"{baseUrl}/iserver/marketdata/snapshot?conids={conids}&fields={fields}"
        response = requests.get(url=request_url, verify=False)
        print(response.status_code, request_url)
        print(response.json())
        contracts = response.json()
        
        for c in contracts:
            imds = IbkrMarketDataSnapshot(c['conid'])
            assert(str(imds.conid) == str(c['conid']))
            imds.symbol = c.get('55')
            imds.name = c.get('7051')
            imds.signal = 0
            imds.messages = []
            imds.cat = c.get('7281')

            imds.last = c.get('31')
            if imds.last and (imds.last.startswith('C') or imds.last.startswith('H')): # Closing price or Halted
                imds.last = imds.last[1:]

            imds.yest = c.get('7741')
            if imds.yest and imds.last and imds.last != 'N/A' and imds.yest != 'N/A' and float(imds.yest) != 0.0:
                imds.roc1 = f"{((float(imds.last) - float(imds.yest)) / float(imds.yest)) * 100:.2f}%"
            else:
                imds.roc1 = 'N/A'
            # imds.roc1 = c.get('83') # commented out because it calculates based on after-hours price
            # if imds.roc1 != 'N/A':
            #     imds.roc1 = f"{imds.roc1}%"
            imds.closeN = None
            imds.rocN = None
            imds.c2ma = None
            imds.ma = None
            imds.ma_bars = None

            imds.iv = c.get('7283')
            imds.hv21 = None
            imds.hv30_ib = c.get('7088') # maybe more accurate than 7087
            imds.iv2hv_ib = c.get('7084')
            imds.p2c = c.get('7085') 
            imds.v = c.get('87')
            imds.v30 = c.get('7282')
            imds.cap = c.get('7289')
            imds.earn = c.get('7686') 
            imds.o = c.get('7295')
            imds.h = c.get('70')
            imds.l = c.get('71')
            imds.h52w = c.get('7293')
            imds.l52w = c.get('7294')
            imds.div = c.get('7287')
            imds.eps = c.get('7291')
            imds.c2ema100 = c.get('7679')
            imds.shortable = c.get('7644') 
            imds.fee = c.get('7637')
            market_data_snapshots[str(imds.conid)] = imds

        return market_data_snapshots
