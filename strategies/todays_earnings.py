from __future__ import annotations
import csv
from datetime import date, datetime
import time
import numpy as np
import pandas as pd
import urllib3
from providers.ibkr import IbkrMarketDataSnapshot, IbkrHistoricalData, IbkrCommon

all_us_contracts = {}
all_ca_contracts = {}
candidates = []
lookback_days = 6
path = '/Users/vs/dev/tariel/earnings/'
RUT_conid = '416888' # obtain from {baseUrl}/iserver/secdef/search?symbol=RUT"
memes = ['AMC', 'BB', 'BBW', 'FOSL', 'GME', 'IRBT', 'KODK', 'KOSS']
ma_period = 100
min_price = 1
min_hv21 = 40
max_hv21 = 150
min_turnover = 700000


class TodaysEarnings:
    snapshot: IbkrMarketDataSnapshot
    closeN: float
    ma: float
    ma_bars: int
    hv21: float
    rocN: float
    c2ma: float

    def __init__(self, snapshot: IbkrMarketDataSnapshot):
        self.snapshot = snapshot

    def process_historical_data(self, bars: list[IbkrHistoricalData]):       
        for index, bar in enumerate(bars):
            if index == 0 or index == len(bars) - 1 or index == len(bars) - lookback_days:
                print(f"{self.snapshot.conid} {self.snapshot.symbol} {datetime.fromtimestamp(float(bar.timestamp) / 1000).strftime('%Y-%m-%d')} close: {bar.close:.2f} v: {bar.volume}")

        if len(bars) < lookback_days: 
            print(f"*** {self.snapshot.conid} {self.snapshot.symbol} not enough data, {len(bars)} bars")
            self.closeN = self.ma = self.hv21 = None
        else:
            closing_prices = [bar.close for bar in bars]
            self.closeN = closing_prices[-lookback_days]
            self.ma = np.average(closing_prices)
            self.ma_bars = len(bars)
            if self.ma_bars < ma_period:
                print(f"*** {self.snapshot.conid} {self.snapshot.symbol} - {self.ma_bars} bars < {ma_period}")

            returns = np.diff(np.log(closing_prices))
            self.hv21 = 100 *np.std(returns[-21:]) * np.sqrt(252)
            if not self.snapshot.last or self.snapshot.last == 'N/A':
                self.snapshot.last = closing_prices[-1]
            if not self.snapshot.yest or self.snapshot.yest == 'N/A':
                self.snapshot.yest = closing_prices[-2]
            if not self.snapshot.roc1 or self.snapshot.roc1 == 'N/A':
                self.snapshot.roc1 = calc_roc(self.snapshot.last, self.snapshot.yest)


    def evaluate(self, index_rocN: float):
        snapshot = self.snapshot
        self.signal = 0
        self.messages = []
        if snapshot.earn is None or snapshot.earn == 'N/A':
            self.messages.append("no earnings info")
        if snapshot.last and float(snapshot.last) < min_price:
            self.messages.append(f"price < {min_price}")
        if snapshot.v30 and snapshot.last:
            v30 = convert_to_number(snapshot.v30)
            if v30 * float(snapshot.last) < min_turnover:
                self.messages.append(f"turnover < {min_turnover}")
        if snapshot.cat and snapshot.cat == 'Medical-Biomedical/Gene':
            self.messages.append("biotech")
        if snapshot.symbol in memes:
            self.messages.append("meme")
        if self.hv21 and float(self.hv21) < min_hv21:
            self.messages.append(f"hv21 < {min_hv21}")
        if self.hv21 and float(self.hv21) > max_hv21:
            self.messages.append(f"hv21 > {max_hv21}")
        if self.rocN and float(self.rocN) > 0 and self.ma and snapshot.last and float(snapshot.last) <= float(self.ma):
            self.signal = 1
        if self.rocN and float(self.rocN) < 0 and self.ma and snapshot.last and float(snapshot.last) >= float(self.ma) and float(self.rocN) < index_rocN:
            self.signal = -1
        if self.signal == 1 and float(self.rocN) < index_rocN:
            self.messages.append("rocN less than index")
        # if self.signal == -1 and float(self.rocN) > index_rocN:
        #     self.messages.append("rocN greater than index")


    def format_snapshot(self):
        snapshot = self.snapshot
        self.rocN = f"{self.rocN:.2f}%" if self.rocN else None
        self.ma = f"{self.ma:.2f}" if self.ma else None
        self.c2ma = f"{self.c2ma:.2f}%" if self.c2ma else None
        self.hv21 = f"{self.hv21:.2f}%" if self.hv21 else None

        print(f"{snapshot.symbol} {snapshot.name} sig:{self.signal} {snapshot.cat} {snapshot.last} 1d:{snapshot.roc1}% 6d:{self.rocN} c2ma:{self.c2ma} ma100:{self.ma}" \
              f" iv:{snapshot.iv} hv21:{self.hv21} hv30:{snapshot.hv30_ib} iv/hv:{snapshot.iv2hv_ib} p/c:{snapshot.p2c} {snapshot.shortable} fee:{snapshot.fee} c2ema:{snapshot.c2ema100}" \
              f" o:{snapshot.o} h:{snapshot.h} l:{snapshot.l} v:{snapshot.v} v30:{snapshot.v30} 52h:{snapshot.h52w} 52l:{snapshot.l52w} div:{snapshot.div} mc:{snapshot.cap} eps:{snapshot.eps} earn:{snapshot.earn} msg:{self.messages}")


def load_candidates_from_csv() -> list[str]:
    conids: list[str] = []
    # read csv with tickers (more data such as CII or PS possible later)and lookup conids
    filename = f"earn_cands_{date.today().strftime('%Y%m%d')}.csv"

    with open(path + filename, 'r') as file:
        csv_reader = csv.reader(file)
        for row in csv_reader:
            ticker = row[0]
            country_code = row[1]
            conid = all_ca_contracts.get(ticker) if country_code == 'CA' else all_us_contracts.get(ticker)
            if not conid:
                print(f"*** CONID NOT FOUND for {ticker} and {country_code}")
            else:
                conids.append(str(conid))
    print(f"loaded {len(conids)} conids out of {csv_reader.line_num} candidates")
    return conids

def convert_to_number(string):
    suffixes = {'K': 1000, 'M': 1000000, 'B': 1000000000}
    if string[-1].isalpha():
        number = float(string[:-1]) * suffixes[string[-1].upper()]
        return int(number)
    return int(string)

def calc_roc(last: float, closeN: float) -> float | None:
    if last and closeN:
        return round(100 * (float(last) / float(closeN) - 1), 2)
    else:
        return None

def calc_RUT_rocN(conid: str, lookback_days: int) -> float | None:
    RUT_snapshot: IbkrMarketDataSnapshot = IbkrMarketDataSnapshot.get_market_snapshot(conid)[str(conid)]
    bars: list[IbkrHistoricalData] = IbkrHistoricalData.get_historical_data(RUT_snapshot.conid, lookback_days)
    RUT_rocN = calc_roc(RUT_snapshot.last, bars[-lookback_days].close)
    if RUT_rocN:
        print(f"RUT rocN: {RUT_rocN:.2f}%")
    return RUT_rocN


if __name__ == '__main__':
    RUT_rocN = calc_RUT_rocN(RUT_conid, lookback_days) # prime IBKR server

    RUT_rocN = calc_RUT_rocN(RUT_conid, lookback_days) # now for realz

    all_us_contracts = IbkrCommon.load_contracts('AMEX')
    all_ca_contracts = IbkrCommon.load_contracts('TSE')
    conids = load_candidates_from_csv()

    batch_size = 50
    market_data_snapshots: dict[str, IbkrMarketDataSnapshot] = {}
    for i in range(0, len(conids), batch_size):
        batch = conids[i:i+batch_size]
        time.sleep(1)
        market_data_snapshots.update(IbkrMarketDataSnapshot.get_market_snapshot(','.join(batch)))  

    for snapshot in market_data_snapshots.values():
        te: TodaysEarnings = TodaysEarnings(snapshot)

        bars: list[IbkrHistoricalData] = IbkrHistoricalData.get_historical_data(snapshot.conid, ma_period)
        if bars:
            te.process_historical_data(bars)

            if te.closeN:
                te.rocN = calc_roc(snapshot.last, te.closeN)
                te.c2ma = calc_roc(snapshot.last, te.ma)

                te.evaluate(RUT_rocN)
                te.format_snapshot()
                candidates.append((snapshot.conid, snapshot.symbol, snapshot.name, snapshot.cat, snapshot.earn, te.signal, te.messages, snapshot.last, snapshot.roc1, te.closeN, te.rocN, te.c2ma, te.ma, te.ma_bars, te.hv21, snapshot.iv, 
                                snapshot.p2c, snapshot.v, snapshot.v30, snapshot.cap, snapshot.h52w, snapshot.l52w, snapshot.o, snapshot.h, snapshot.l, snapshot.div, snapshot.eps, snapshot.c2ema100, snapshot.shortable, snapshot.fee))
        else:
            print(f"*** {snapshot.conid} {snapshot.symbol} no historical data")


    df = pd.DataFrame(candidates)
    columns = ['conid', 'symbol', 'name', 'cat', 'earn', 'signal', 'messages', 'last', 'roc1', 'closeN', 'rocN', 'c2ma', 'ma', 'ma_bars', 'hv21', 'iv', 'p2c', 'v', 'v30', 'cap', 'h52w', 'l52w', 'o', 'h', 'l', 'div', 'eps', 'c2ema100', 'shortable', 'fee']
    df.to_csv(f"{path}earn_out_{date.today().strftime('%Y%m%d')}.csv", index=False, header=columns)
