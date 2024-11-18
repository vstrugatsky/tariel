from datetime import date, time, datetime
from time import sleep
import ssl
import pandas as pd
import requests
import urllib3
import pytest
import websocket
import rel

baseUrl = "https://localhost:7498/v1/api"
websocketUrl = "wss://localhost:5000/v1/api/ws"
regAcctId = "U14546299"
iraAcctId = "U14555356"
paperRegId = "DU9017794"
paperIraId = "DU9288971"
aaplConid = 265598
servConid = 689676896

@pytest.fixture(autouse=True)
def common_setup():
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def test_account_pnl(common_setup):
    request_url = f"{baseUrl}/iserver/account/pnl/partitioned"
    response = requests.get(url=request_url, verify=False)
    print(response.status_code, response.json())
    # dpl: float. Daily PnL for the specified account profile.
    # nl: float. Net Liquidity for the specified account profile.
    # upl: float. Unrealized PnL for the specified account profile.
    # el: float. Excess Liquidity for the specified account profile.
    # mv: float.Margin value for the specified account profile.

def test_account_search(common_setup): # TODO: Use /account instead
    request_url = f"{baseUrl}/iserver/account/search/{iraAcctId}"
    response = requests.get(url=request_url, verify=False)
    print(response.status_code, response.json())
    # Getting 503 because accounts with DYNACCT proprty must dynamically query then set their account number?

def test_set_dynamic_account(common_setup): # TODO: Use /account instead
    request_url = f"{baseUrl}/iserver/dynaccount"
    response = requests.post(url=request_url, verify=False, json={"acctId": iraAcctId})
    print(response.status_code, response.json())
    # Can get 500 {'error': 'Account already set'} - poor API design.
    # Can get 401 {'error': 'Acct not found from search result'}
    # Can get 401 {'error': 'not authenticated', 'statusCode': 401}
    # Can also get 400{'error': 'Bad Request: no bridge', 'statusCode': 400}

def test_switch_account(common_setup):
    request_url = f"{baseUrl}/iserver/account"
    response = requests.post(url=request_url, verify=False, json={"acctId": regAcctId})
    print(response.status_code, response.json())

def test_get_accounts(common_setup):
    request_url = f"{baseUrl}/iserver/accounts"
    response = requests.get(url=request_url, verify=False)
    print(response.status_code, response.json())
    # {'accounts': ['All', 'U14546299', 'U14555356'], 
    # 'acctProps': {'All': {'hasChildAccounts': False, 'supportsCashQty': False, 'supportsFractions': False}, 
    # 'U14555356': {'hasChildAccounts': False, 'supportsCashQty': True, 'liteUnderPro': False, 'noFXConv': False, 'isProp': False, 'supportsFractions': True, 'allowCustomerTime': False}, 
    # 'U14546299': {'hasChildAccounts': False, 'supportsCashQty': True, 'liteUnderPro': False, 'noFXConv': False, 'isProp': False, 'supportsFractions': True, 'allowCustomerTime': False}}, 
    # 'aliases': {'All': 'All', 'U14555356': 'U14555356', 'U14546299': 'U14546299'}, 
    # 'allowFeatures': {'showGFIS': True, 'showEUCostReport': False, 'allowEventContract': True, 'allowFXConv': True, 'allowFinancialLens': False, 'allowMTA': False, 'allowTypeAhead': True, 'allowEventTrading': True, 'snapshotRefreshTimeout': 30, 'liteUser': False, 'showWebNews': True, 'research': True, 'debugPnl': True, 'showTaxOpt': True, 'showImpactDashboard': True, 
    # 'allowDynAccount': False, 
    # 'allowCrypto': True, 'allowFA': False, 'allowLiteUnderPro': False, 'allowedAssetTypes': 'STK,CFD,OPT,FOP,WAR,FUT,BAG,PDC,CASH,IND,BOND,BILL,FUND,SLB,News,CMDTY,IOPT,ICU,ICS,PHYSS,CRYPTO'}, 
    # 'chartPeriods': {'STK': ['*'], 'CFD': ['*'], 'OPT': ['2h', '1d', '2d', '1w', '1m'], 'FOP': ['2h', '1d', '2d', '1w', '1m'], 'WAR': ['*'], 'IOPT': ['*'], 'FUT': ['*'], 'CASH': ['*'], 'IND': ['*'], 'BOND': ['*'], 'FUND': ['*'], 'CMDTY': ['*'], 'PHYSS': ['*'], 'CRYPTO': ['*']}, 
    # 'groups': ['All'], 'profiles': [], 'selectedAccount': 'U14546299', 
    # 'serverInfo': {'serverName': 'JifN19087', 'serverVersion': 'Build 10.30.1p, Sep 26, 2024 3:48:55 PM'}, 'sessionId': '66fe1afd.00000134', 'isFT': False, 'isPaper': False}

def test_get_secdef():
    request_url = f"{baseUrl}/trsrv/secdef?conids={aaplConid}"
    response = requests.get(url=request_url, verify=False)
    print(response.status_code, response.json())
    # {'secdef': [{'incrementRules': [{'lowerEdge': 0.0, 'increment': 0.01}], 
    # 'displayRule': {'magnification': 0, 'displayRuleStep': [{'decimalDigits': 2, 'lowerEdge': 0.0, 'wholeDigits': 4}]}, 'conid': 265598, 'currency': 'USD', 'time': 31, 'chineseName': '&#x82F9;&#x679C;&#x516C;&#x53F8;', 'allExchanges': 'AMEX,NYSE,CBOE,PHLX,CHX,ARCA,ISLAND,ISE,IDEAL,NASDAQQ,NASDAQ,DRCTEDGE,BEX,BATS,NITEECN,EDGEA,CSFBALGO,NYSENASD,PSX,BYX,ITG,PDQ,IBKRATS,CITADEL,NYSEDARK,MIAX,IBDARK,CITADELDP,NASDDARK,IEX,WEDBUSH,SUMMER,WINSLOW,FINRA,LIQITG,UBSDARK,BTIG,VIRTU,JEFF,OPCO,COWEN,DBK,JPMC,EDGX,JANE,NEEDHAM,FRACSHARE,RBCALGO,VIRTUDP,BAYCREST,FOXRIVER,MND,NITEEXST,PEARL,GSDARK,NITERTL,NYSENAT,IEXMID,HRT,FLOWTRADE,HRTDP,JANELP,PEAK6,CTDLZERO,HRTMID,JANEZERO,HRTEXST,IMCLP,LTSE,SOCGENDP,MEMX,INTELCROS,VIRTUBYIN,JUMPTRADE,NITEZERO,TPLUS1,XTXEXST,XTXDP,XTXMID,COWENLP,BARCDP,JUMPLP,OLDMCLP,RBCCMALP,WALLBETH,IBEOS,JONES,GSLP,BLUEOCEAN,USIBSILP,OVERNIGHT,JANEMID,IBATSEOS,HRTZERO,VIRTUALGO,G1XLP,VIRTUMID,GLOBALXLP,CTDLMID,TPLUS0,JUMPMID', 
    # 'listingExchange': 'NASDAQ', 'countryCode': 'US', 'name': 'APPLE INC', 'assetClass': 'STK', 'expiry': None, 
    # 'lastTradingDay': None, 'group': 'Computers', 'putOrCall': None, 'sector': 'Technology', 'sectorGroup': 'Computers', 
    # 'strike': '0', 'ticker': 'AAPL', 'undConid': 0, 'multiplier': 0.0, 'type': 'COMMON', 
    # 'hasOptions': True, 'fullName': 'AAPL', 'isUS': True, 'isEventContract': False, 'pageSize': 100}]}

def test_get_all_conids_by_exchange(common_setup):
    request_url = f"{baseUrl}/trsrv/all-conids?exchange=TSE" # "AMEX" returns same results
    response = requests.get(url=request_url, verify=False)
    print(response.status_code, response.json())
    # [{'ticker': 'BMO', 'conid': 5094, 'exchange': 'NYSE'}, {'ticker': 'BNS', 'conid': 15156975, 'exchange': 'NYSE'}
    # note that a different exchange can be returned. 10,725 results, no duplicates
    # AMEX and NYSE return very similar results - 10,725 vs 10,726. Probs does not matter which is used

def test_contract_info(common_setup):
    request_url = f"{baseUrl}/iserver/contract/{aaplConid}/info"
    response = requests.get(url=request_url, verify=False)
    print(response.status_code, response.json())
# {'cfi_code': '', 'symbol': 'AAPL', 'cusip': None, 'expiry_full': None, 'con_id': 265598, 'maturity_date': None, 'industry': 'Computers', 
# 'instrument_type': 'STK', 'trading_class': 'NMS', 'valid_exchanges': 'SMART,AMEX,NYSE,CBOE,PHLX,ISE,CHX,ARCA,NASDAQ,DRCTEDGE,BEX,BATS,EDGEA,BYX,IEX,EDGX,FOXRIVER,PEARL,NYSENAT,LTSE,MEMX,IBEOS,OVERNIGHT,TPLUS0,PSX', 'allow_sell_long': False, 'is_zero_commission_security': False, 'local_symbol': 'AAPL', 'contract_clarification_type': None, 'classifier': None, 'currency': 'USD', 'text': None, 'underlying_con_id': 0, 
# 'r_t_h': True, 'multiplier': None, 'underlying_issuer': None, 'contract_month': None, 'company_name': 'APPLE INC', 'smart_available': True, 'exchange': 'SMART', 'category': 'Computers'}

def test_contract_info_and_rules(common_setup):
    request_url = f"{baseUrl}/iserver/contract/{aaplConid}/info-and-rules?isBuy=true"
    response = requests.get(url=request_url, verify=False)
    print(response.status_code, response.json())
    # 'cfi_code': '', 'symbol': 'AAPL', 'cusip': None, 'expiry_full': None, 'con_id': 265598, 'maturity_date': None, 'industry': 'Computers', 'instrument_type': 'STK', 'trading_class': 'NMS', 'valid_exchanges': 'SMART,AMEX,NYSE,CBOE,PHLX,ISE,CHX,ARCA,NASDAQ,DRCTEDGE,BEX,BATS,EDGEA,BYX,IEX,EDGX,FOXRIVER,PEARL,NYSENAT,LTSE,MEMX,IBEOS,OVERNIGHT,TPLUS0,PSX', 'allow_sell_long': False, 'is_zero_commission_security': False, 
    # 'local_symbol': 'AAPL', 'contract_clarification_type': None, 'classifier': None, 'currency': 'USD', 'text': None, 'underlying_con_id': 0, 
    # 'r_t_h': True, 'multiplier': None, 'underlying_issuer': None, 'contract_month': None, 'company_name': 'APPLE INC', 'smart_available': True, 'exchange': 'SMART', 'category': 'Computers', 
    # 'rules': {'algoEligible': True, 'allOrNoneEligible': True, 'overnightEligible': True, 'displayMessage': {'url': 'https://api.ibkr.com/tws.widgets/ios1/ios.html#/messages?contentId=overnight'}, 'costReport': False, 
    # 'canTradeAcctIds': ['U14546299', 'U14555356'], 'error': None, 
    # 'orderTypes': ['limit', 'midprice', 'market', 'stop', 'stop_limit', 'mit', 'lit', 'trailing_stop', 'trailing_stop_limit', 'relative', 'marketonclose', 'limitonclose'], 
    # 'ibAlgoTypes': ['limit', 'stop_limit', 'lit', 'trailing_stop_limit', 'relative', 'marketonclose', 'limitonclose'], 
    # 'fraqTypes': ['limit', 'market', 'stop', 'stop_limit', 'mit', 'lit', 'trailing_stop', 'trailing_stop_limit'], 'forceOrderPreview': False, 
    # 'cqtTypes': ['limit', 'market', 'stop', 'stop_limit', 'mit', 'lit', 'trailing_stop', 'trailing_stop_limit'], 
    # 'orderDefaults': {'LMT': {'LP': '226.47'}}, 'orderTypesOutside': ['limit', 'stop_limit', 'lit', 'trailing_stop_limit', 'relative'], 
    # 'defaultSize': 100, 'cashSize': 0.0, 'sizeIncrement': 100, 'tifTypes': ['IOC/MARKET,LIMIT,RELATIVE,MARKETONCLOSE,MIDPRICE,LIMITONCLOSE,MKT_PROTECT,STPPRT,a', 'GTC/o,a', 'OPG/LIMIT,MARKET,a', 'GTD/o,a', 'DAY/o,a'], 'tifDefaults': {'TIF': 'DAY', 'SIZE': '100.00', 'PMALGO': True}, 
    # 'limitPrice': 226.47, 'stopprice': 226.47, 'orderOrigination': None, 'preview': True, 'displaySize': None, 'fraqInt': 4, 'cashCcy': 'USD', 'cashQtyIncr': 500, 'priceMagnifier': None, 'negativeCapable': False

def test_search_contract_by_symbol(common_setup): # probs unnecesary - can return multiple contracts 
    request_url = f"{baseUrl}/iserver/secdef/search?symbol=RUT"
    response = requests.get(url=request_url, verify=False)
    print(response.status_code, response.json())

def test_contract_rules_by_conid_and_side(common_setup):
    request_url = f"{baseUrl}/iserver/contract/rules"
    json_content = {
    "conid": 265598,
    "exchange": "SMART",
    "isBuy": True,
    # only for modify order -> "modifyOrder": True, "orderId": 1234567890
    }
    response = requests.post(url=request_url, json=json_content, verify=False)
    print(response.status_code, response.json())
    # {'algoEligible': True, 'allOrNoneEligible': True, 'overnightEligible': True, 'displayMessage': {'url': 'https://api.ibkr.com/tws.widgets/ios1/ios.html#/messages?contentId=overnight'}, 'costReport': False, 'canTradeAcctIds': ['U14546299', 'U14555356'], 'error': None, 
    # 'orderTypes': ['limit', 'midprice', 'market', 'stop', 'stop_limit', 'mit', 'lit', 'trailing_stop', 'trailing_stop_limit', 'relative', 'marketonclose', 'limitonclose'], 
    # 'ibAlgoTypes': ['limit', 'stop_limit', 'lit', 'trailing_stop_limit', 'relative', 'marketonclose', 'limitonclose'], 
    # 'fraqTypes': ['limit', 'market', 'stop', 'stop_limit', 'mit', 'lit', 'trailing_stop', 'trailing_stop_limit'], 
    # 'forceOrderPreview': False, 'cqtTypes': ['limit', 'market', 'stop', 'stop_limit', 'mit', 'lit', 'trailing_stop', 'trailing_stop_limit'], 
    # 'orderDefaults': {'LMT': {'LP': '226.71'}}, 'orderTypesOutside': ['limit', 'stop_limit', 'lit', 'trailing_stop_limit', 'relative'], 'defaultSize': 100, 'cashSize': 0.0, 'sizeIncrement': 100, 
    # 'tifTypes': ['IOC/MARKET,LIMIT,RELATIVE,MARKETONCLOSE,MIDPRICE,LIMITONCLOSE,MKT_PROTECT,STPPRT,a', 'GTC/o,a', 'OPG/LIMIT,MARKET,a', 'GTD/o,a', 'DAY/o,a'], 
    # 'tifDefaults': {'TIF': 'DAY', 'SIZE': '100.00', 'PMALGO': True}, 
    # 'limitPrice': 226.71, 'stopprice': 226.71, 'orderOrigination': None, 'preview': True, 'displaySize': None, 'fraqInt': 4, 'cashCcy': 'USD', 'cashQtyIncr': 500, 'priceMagnifier': None, 'negativeCapable': False, 'incrementType': 1, 'incrementRules': [{'lowerEdge': 0.0, 'increment': 0.01}], 'hasSecondary': True, 'increment': 0.01, 'incrementDigits': 2}

def test_get_settings(common_setup):
    request_url = f"{baseUrl}/fyi/settings"
    response = requests.get(url=request_url, verify=False)
    print(response.status_code, response.json())
    # A=1: subscription can be modified, H=1: notification was read
    # [{'FC': 'M8', 'H': 0, 'A': 1, 'FD': 'Notify me when I establish position subject to US dividend tax withholding 871(m) rules.', 'FN': '871(m) Trades'}, 
    # {'FC': 'AA', 'H': 1, 'A': 1, 'FD': 'Notifications related to account activity such as funding, application, trading and market data permission status', 'FN': 'Account Activity'}, 
    # {'FC': 'T2', 'H': 0, 'A': 1, 'FD': 'Notify me if an option assignment or exercise results in delivery of US stock with long-term gains.', 'FN': 'Assignment or Exercise Realizing Long-Term Gains'}, 
    # {'FC': 'BA', 'H': 0, 'A': 1, 'FD': 'Notify me when shares have been located on stocks that had previously been rejected for short sale orders created within the last three trading days.', 'FN': 'Borrow Availability'}, {'FC': 'BR', 'H': 0, 'A': 1, 'FD': 'Notify me if there is a risk of an expensive stock borrow due to potential call assignments.', 'FN': 'Borrow Risk from Call Assignment FYI'}, 
    # {'FC': 'CA', 'H': 0, 'A': 1, 'FD': 'Notify me if there is a comparable Algo or Order Type with lower fees', 'FN': 'Comparable Algo'}, 
    # {'FC': 'EH', 'H': 1, 'A': 1, 'FD': 'Notify me of upcoming exchange holidays', 'FN': 'Exchange Holidays'}, 
    # {'FC': 'NS', 'H': 1}, 
    # {'FC': 'TD', 'H': 0, 'A': 1, 'FD': 'Notify me if the value of open position(s) in my account(s) depreciate by 10% or more.', 'FN': 'MiFID II 10% Depreciation Notice'}, 
    # {'FC': 'CB', 'H': 0, 'A': 1, 'FD': 'Notify me if cost basis information is missing for my position transfers.', 'FN': 'Missing Cost Basis'}, 
    # {'FC': 'MF', 'H': 0, 'A': 1, 'FD': 'Notify me if there is an ETF comparable to my Mutual Fund/ETF holdings.', 'FN': 'Mutual Fund/ETF Advisory'}, 
    # {'FC': 'NP', 'H': 0, 'A': 1, 'FD': 'Send me information about new products that may be relevant to me.', 'FN': 'New Products'}, 
    # {'FC': 'DL', 'H': 0, 'FD': 'Notify me if I lose money by failing to early exercise options or by exercising too early.', 'FN': 'Option Exercise Loss Prevention Reminder'}, 
    # {'FC': 'OE', 'H': 1, 'A': 1, 'FD': 'Notify me three days before my options or futures expire.', 'FN': 'Option or Future expiration'}, 
    # {'FC': 'PS', 'H': 1, 'A': 1, 'FD': 'Send me suggestions to better utilize the trading platform.', 'FN': 'Platform Use Suggestions'}, 
    # {'FC': 'PF', 'H': 1, 'A': 1, 'FD': 'Notify me of recent activity affecting my portfolio holdings.', 'FN': 'Portfolio FYIs'}, 
    # {'FC': 'PT', 'H': 0, 'A': 1, 'FD': 'Notify me of potential account configuration changes needed and useful features based on my position transfers.', 'FN': 'Position Transfer'}, 
    # {'FC': 'PC', 'H': 0, 'A': 1, 'FD': 'Notify me when my orders are price capped or may be potentially price capped.', 'FN': 'Price Cap FYI'}, 
    # {'FC': 'SP', 'H': 0, 'A': 1, 'FD': 'Notify me when SPACs (Special Purpose Acquisition Companies) are traded in my account.', 'FN': 'SPAC FYI'}, 
    # {'FC': 'SG', 'H': 0, 'A': 1, 'FD': 'Notify me when the U.S. capital gains tax holding period on my profitable positions is about to change from short term to long term.', 'FN': 'Short Term Gain turning Long Term'}, {'FC': 'SL', 'H': 0, 'A': 1, 'FD': 'Notify me when the U.S. capital gains tax holding period on my positions with unrealized losses is about to change from short term to long term.', 'FN': 'Short Term Loss Becoming Long Term Loss'}, 
    # {'FC': 'MS', 'H': 0, 'A': 1, 'FD': 'Notify me on special milestones and occasions.', 'FN': 'Special Occasions'}, 
    # {'FC': 'TO', 'H': 0, 'A': 1, 'FD': 'Notify me when a company in which I hold positions is part of a merger or takeover.', 'FN': 'Takeover'}, 
    # {'FC': 'EA', 'H': 1, 'A': 1, 'FD': 'Notify me of upcoming earnings announcements from any of my holdings.', 'FN': 'Upcoming Earnings'}, 
    # {'FC': 'DA', 'H': 0, 'SS': 'TA_FYI', 'FD': 'Notify me if my account holds call options whose underlying stock is scheduled to trade ex-dividend within the next two trading days.', 'FN': 'Dividend-Triggered Option Exercise Advisory'}, 
    # {'FC': 'SE', 'H': 0, 'SS': 'TA_FYI', 'FD': 'Upcoming events and times during which your orders will be suspended as specified by you.', 'FN': 'Suspend Orders On Economic Event'}, 
    # {'FC': 'SM', 'H': 1, 'FD': 'System generated messages for your account(s)', 'FN': 'System Messages'}, 
    # {'FC': 'UA', 'H': 0, 'FD': 'Notifications that you activated using the Mobile Trading Assistant', 'FN': 'User Defined Alerts'}]

def test_set_setting(common_setup):
    typecode = "SP" # PACs (Special Purpose Acquisition Companies) are traded in my account
    request_url = f"{baseUrl}/fyi/settings/{typecode}"
    response = requests.post(url=request_url, json={"enabled": True}, verify=False)
    print(response.status_code, response.json())
    # { "V": 1,"T": 10} v:1 = acknowledged

def test_marketdata_snapshot(common_setup):
    request_url = f"{baseUrl}/iserver/accounts" # preflight method required
    response = requests.get(url=request_url, verify=False)
    print(response.status_code, request_url)
    # fields parameter seems to be largely ignored for my subscription type. Maybe it remembers my previous requests. But should be able to get IV, EMA calculations, prev. close, etc.
    fields = "31,55,70,71,83,84,85,86,87,88,7059,7084,7085,7086,7087,7281,7282,7283,7287,7288,7291,7293,7294,7295,7607,7636,7637,7644,7675,7679,7682,7718,7741,7686"
    # returns the following anyway:
    # 31, 55,70, 71, 83, 87, 6509: DPB, 7051, 7059, 7084, 7085, 7087, 7088, 7281, 7282, 7283, 7289, 7293, 7294, 7295, 7636, 7637, 7644, 7675, 7679, 7682, 7718, 7741

    conid = 178634687 # WBA
    request_url = f"{baseUrl}/iserver/marketdata/snapshot?conids={conid}&fields={fields}"
    response = requests.get(url=request_url, verify=False)
    print(response.status_code, request_url, response.json())
    # [{'6509': 'DPB', 1: D=Delayed,R=RealTime,Z=Frozen(market close real-time),Y=Frozen Delayed(market close delayed),N=not subscribed
    # '31': '224.57' -> Last Price	The last price at which the contract traded. May contain one of the following prefixes: C – Previous day’s closing price. H – Trading has halted
    # '55': Symbol, '7051': Company name		
    # '70': High, '71': Low	=> H /L , '83': Change % The difference between the last price and the close on the previous trading day in percentage.
    # '84': Bid Price, '85': Ask Size, '86': Ask Price, '88': Bid Size
    # '87': Volume	Volume for the day, formatted with ‘K’ for thousands or ‘M’ for millions. For higher precision volume refer to field 7762.
    # '7059': Last Size	The number of unites traded at the last price
    # '7084': Implied Vol./Hist. Vol %	The ratio of the implied volatility over the historical volatility, expressed as a percentage.
    # '7085': Put/Call Interest	Put option open interest/call option open interest for the trading day.
    # '7086': Put/Call Volume	Put option volume/call option volume for the trading day.
    # '7087': Hist. Vol. %	30-day real-time historical volatility.
    # '7088': Hist. Vol. Close %	Shows the historical volatility based on previous close price.
    # '7280': Industry	Displays the type of industry under which the underlying company can be categorized.
    # '7281': Category	Displays a more detailed level of description within the industry under which the underlying company can be categorized.
    # '7282': Average Volume	The average daily trading volume over 90 days.
    # '7283': Option Implied Vol. %	A prediction of how volatile an underlying will be in the future. At the market volatility estimated for a maturity 30 calendar days forward of the current trading day, and based on option prices from two consecutive expiration months. To query the Implied Vol. % of a specific strike refer to field 7633.
    # '7285': Put/Call Ratio
    # '7287': Dividend Yield %	This value is the toal of the expected dividend payments over the next twelve months per share divided by the Current Price and is expressed as a percentage. For derivatives, this displays the total of the expected dividend payments over the expiry date
    # '7288': Ex-date of the dividend	
    # '7289': Market Cap
    # '7291': EPS (7290 PE n/a)
    # '7293', '7294': 52 Week High / Low	
    # '7295', '7296': Today’s opening / closing price.
    # '7636': Shortable Shares	Number of shares available for shorting.
    # '7637': Fee Rate	Interest rate charged on borrowed shares.
    # '7644': Shortable	Describes the level of difficulty with which the security can be sold short.
    # '7674', '7675', '7676', '7677', '7679', '7724', '7681': EMA(200), EMA(100), EMA(50), EMA(20), Price/EMA(100), Price/EMA(50), Price/EMA(20)
    # '7682': Change Since Open	The difference between the last price and the open price.
    # '7686': Upcoming Earnings	The date and time of the next scheduled earnings/earnings call event. Requires Wall Street Horizon subscription.
    # '7718': beta against standard index
    # '7741': Prior Close - yesterday
    # 'conidEx': '265598', 'conid': 265598, '_updated': 1728057088284, 
    # '6119': 'q0', 'server_id': 'q0',
    # '6508': '&serviceID1=122&serviceID2=123&serviceID3=203&serviceID4=775&serviceID5=204&serviceID6=206&serviceID7=108&serviceID8=109'}]

def test_historical_marketdata_snapshot(common_setup):
    # it appears no data for today is returned, use beta below if today's data is needed
    # works backwards from the current time
    conid = '277300040' # PENG
    request_url = f"{baseUrl}/iserver/marketdata/history?conid={conid}&exchange=SMART&period=6d&bar=1d&outsideRth=false" # &startTime=20241015-13:30:00
    response = requests.get(url=request_url, verify=False)
    print(response.status_code, response.json())
    bars = response.json()['data']
    for index, bar in enumerate(bars):
        timestamp = bar['t'] / 1000
        print(f"{response.json()['symbol']} {datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')} close: {bar['c']:.2f} v: {bar['v']}")
    # 'symbol': 'AAPL', 'text': 'APPLE INC', 'priceFactor': 100, 'startTime': '20241003-13:30:00', 
    # 'high': '22681/38038.14/30', 'low': '22332/18714.11/210', 'timePeriod': '1d', 'barLength': 3600, 
    # 'mdAvailability': 'S', 'mktDataDelay': 0, 
    # 'outsideRth': False, 'tradingDayDuration': 390, 'volumeFactor': 100, 'priceDisplayRule': 1, 'priceDisplayValue': '2', 
    # 'chartPanStartTime': '20241004-06:30:00', 'direction': -1, 'negativeCapable': False, 'messageVersion': 2, 
    # 'data': [{'o': 225.14, 'c': 226.31, 'h': 226.7, 'l': 224.89, 'v': 25662.56, 't': 1727962200000}, 
    # {'o': 223.62, 'c': 225.67, 'h': 225.84, 'l': 223.5, 'v': 57700.31, 't': 1727982000000}],  'points': 6, 'travelTime': 118}

def test_historical_marketdata_beta(common_setup):
    # barType parameter is required. - Timestamp in GMT! - Returns today's data up to the last minute!
    period = "1d"
    bar = "1mins"
    startTime = "20241004-19:00:00"
    request_url = f"{baseUrl}/hmds/history?conid={aaplConid}&period={period}&bar={bar}&startTime={startTime}&outsideRth=false&barType=Last"
    response = requests.get(url=request_url, verify=False)
    print(response.status_code, response.json())
    # {'startTime': '20241004-09:30:00', 'startTimeVal': 1728048600000, 'endTime': '20241004-15:07:07', 'endTimeVal': 1728068827000, 
    # 'data': [{'t': 1728048600000, 'o': 227.9, 'c': 225.15, 'h': 228.0, 'l': 225.07, 'v': 415531.0}, {'t': 1728050400000, 'o': 225.16, 'c': 225.09, 'h': 225.62, 'l': 224.13, 'v': 503147.0}, 
    # {'t': 1728054000000, 'o': 225.11, 'c': 225.53, 'h': 225.53, 'l': 224.31, 'v': 326683.0}, {'t': 1728057600000, 'o': 225.54, 'c': 225.16, 'h': 225.57, 'l': 224.7, 'v': 203920.0}, 
    # {'t': 1728068400000, 'o': 225.53, 'c': 225.46, 'h': 225.53, 'l': 225.29, 'v': 34430.0}], 'points': 7, 'mktDataDelay': 0}

def test_live_orders(common_setup):
    request_url = f"{baseUrl}/iserver/accounts" # preflight method required
    response = requests.get(url=request_url, verify=False)
    print(response.status_code, request_url)

    request_url = f"{baseUrl}/iserver/account/orders" # ?filter=filled?force=true" # filter seems to be ignored, returns today's orders no matter what
    response = requests.get(url=request_url, verify=False)
    print(response.status_code, response.json())
# {'orders': [{'acct': 'U14546299', 'conidex': '266285', 'conid': 266285, 'account': 'U14546299', 'orderId': 553617933, 'cashCcy': 'USD', 'sizeAndFills': '0/45', 'orderDesc': 'Buy 45 APOG MKT CLS, Day', 
# 'description1': 'APOG', 'ticker': 'APOG', 'secType': 'STK', 'listingExchange': 'NASDAQ.NMS', 'remainingQuantity': 45.0, 'filledQuantity': 0.0, 'totalSize': 45.0, 
# 'companyName': 'APOGEE ENTERPRISES INC', 'status': 'Submitted', 'order_ccp_status': 'Submitted', 'origOrderType': 'MARKETONCLOSE', 'supportsTaxOpt': '1', 
# 'lastExecutionTime': '241004152400', 'orderType': 'MARKETONCLOSE', 
# 'bgColor': '#000000', 'fgColor': '#00F000', 'isEventTrading': '0', 'price': '', 'timeInForce': 'CLOSE', 'lastExecutionTime_r': 1728055440000, 'side': 'BUY'}], 'snapshot': True}

def test_order_status(common_setup):
    request_url = f"{baseUrl}/iserver/account"
    response = requests.post(url=request_url, verify=False, json={"acctId": paperRegId})
    print(response.status_code, response.json())

    orderId = '1171486718'
    request_url = f"{baseUrl}/iserver/account/order/status/{orderId}"
    response = requests.get(url=request_url, verify=False)
    print(response.status_code, response.json())
    # 503 {'error': 'Order 553617933 is not found', 'statusCode': 503}
    # it seems that orders are only active for a couple of days.
    # 200 {'sub_type': None, 'request_id': '379967', 'server_id': '1461', 'order_id': 1405318862, 'conidex': '268060148', 'conid': 268060148, 
    # 'symbol': 'SNAP', 'side': 'S', 'contract_description_1': 'SNAP', 'listing_exchange': 'NYSE', 'option_acct': 'c', 'company_name': 'SNAP INC - A', 'size': '250.0', 'total_size': '250.0', 'currency': 'USD', 
    # 'account': 'U14546299', 'order_type': 'LIMIT', 'limit_price': '10.65', 'cum_fill': '0.0', 
    # 'order_status': 'Submitted', 'order_ccp_status': '0', 'order_status_description': 'Order Submitted', 'tif': 'DAY', 'order_not_editable': False, 'editable_fields': '\x1e', 
    # 'cannot_cancel_order': False, 'outside_rth': False, 'deactivate_order': False, 'use_price_mgmt_algo': False, 'sec_type': 'STK', 'available_chart_periods': '#R|1', 'order_description': 'Sell 250 Limit 10.65, Day', 'order_description_with_contract': 'Sell 250 SNAP Limit 10.65, Day', 'clearing_id': 'IB', 'clearing_name': 'IB', 'alert_active': 1, 'child_order_type': '3', 'order_clearing_account': 'U14546299', 'size_and_fills': '0/250', 'exit_strategy_display_price': '10.65', 'exit_strategy_chart_description': 'Sell 250 Limit 10.65, Day', 'exit_strategy_tool_availability': '1', 
    # 'allowed_duplicate_opposite': True, 'order_time': '241007161814'}

def test_trades(common_setup):
    # It is advised to call this endpoint once per session?
    request_url = f"{baseUrl}/iserver/account"
    response = requests.post(url=request_url, verify=False, json={"acctId": regAcctId})
    print(response.status_code, response.json())

    request_url = f"{baseUrl}/iserver/account/trades?days=7"
    response = requests.get(url=request_url, verify=False)
    print(response.status_code, response.json())
    # 503 {'error': 'Order 553617933 is not found', 'statusCode': 503}
    # Not working

def test_place_order(common_setup):
    request_url = f"{baseUrl}/iserver/account/{paperRegId}/orders"
    # MOC works with DAY
    json_content = {
        "orders": [
        {
        "acctId": paperRegId,
        "conid": servConid,
        # "conidex": "265598@SMART",      # optional, can be used instead of conid
        "secType": f"{servConid}@STK",
        "cOID": "SERV-BUY-2",         # An arbitrary string that can be used to identify the order. The value must be unique for a 24h span. Do not set this value for child orders when placing a bracket order.
        # "parentId": None,               # Only specify for child orders when placing bracket orders. The parentId for the child order(s) must be equal to the cOId (customer order id) of the parent.
        "orderType": "MOC",             # Required: LMT | MKT | STP | STOP_LIMIT | MIDPRICE | TRAIL | TRAILLMT. MOC also works
        # "listingExchange": "NASDAQ",    # Primary routing exchange for the order. By default we use “SMART” routing. Possible values via the endpoint: /iserver/contract/{conid}/info
        # "isSingleGroup": False,         # Set to true if you want to place a single group orders(OCA)
        # "outsideRTH": True,             # Set to true if the order can be executed outside regular trading hours.
        #  "price": 185.50,                # Required for LMT, STOP_LIMIT. This is typically the limit price. For STP | TRAIL this is the stop price. For MIDPRICE this is the option price.
        #  "auxPrice": 183,                # Required for STOP_LIMIT and TRAILLMT orders. Stop price for STOP_LIMIT and TRAILLMT orders. Must specify both price and auxPrice for STOP_LIMIT|TRAILLMT orders.
        "side": "BUY",                  # Required. Valid Values: SELL or BUY
        "ticker": "SERV",               # 
        "tif": "DAY",                   # Required. The Time-In-Force determines how long the order remains active on the market. Valid Values: GTC, OPG (opening), DAY, IOC (immediate or cancel), PAX (CRYPTO ONLY).
        # "trailingAmt": 1.00,            # Required if order is TRAIL, or TRAILLMT. When trailingType is amt, this is the trailing amount. When trailingType is %, it means percentage.
        # "trailingType": "amt",          # Required for TRAIL and TRAILLMT order. This is the trailing type for trailing amount. You must specify both trailingType and trailingAmt. Valid Values: “amt” or “%”
        "referrer": "paper acct test",   # Custom order reference
        "quantity": 2,                # Required. Used to designate the total number of shares traded for the order. Only whole share values are supported.
        # Can not be used in tandem with quantity value.
        # "cashQty": {{ cashQty }},      Only supported for Crypto and Forex
        # "fxQty": {{ fxQty }},          
        # "useAdaptive": False,           # If true, the system will use the Price Management Algo to submit the order.
        # "isCcyConv": False,             # set to true if the order is a FX conversion order
        # "allocationMethod":           # For FA (Financial Advisor) only
        # "strategy": "Vwap",             # Specify which IB Algo algorithm to use for this order.
        #     "strategyParameters": {
        #     "MaxPctVol":"0.1",
        #     "StartTime":"14:00:00 EST",
        #     "EndTime":"15:00:00 EST",
        #     "AllowPastEndTime":True
        #     }
        }
        ]
    }
    response = requests.post(url=request_url, json=json_content, verify=False)
    print(response.status_code, response.json())
    # 200 [{'order_id': '1171486718', 'local_order_id': 'AAPL-BUY-100', 'order_status': 'PreSubmitted', 'encrypt_message': '1'}]
    # 200 {'error': '"BUY 100 SERV NASDAQ.SCM"\nInvalid time-in-force for at-the-closing order.'} - when type = MOC but tif = GTC
    # 400 {'error': 'java.lang.String cannot be cast to java.lang.Number'}

def test_cancel_order(common_setup):
    orderId = "1171486724"
    request_url = f"{baseUrl}/iserver/account/{paperRegId}/order/{orderId}"
    response = requests.delete(url=request_url, verify=False)
    print(response.status_code, response.json())
    # 200 {'msg': 'Request was submitted', 'order_id': 1171486724, 'conid': -1, 'account': None}
    # 400 {'error': "OrderID 1171486718 doesn't exist"}

def test_modify_order(common_setup):
    request_url = f"{baseUrl}/iserver/accounts" # Must call /iserver/accounts endpoint prior to modifying an order. Use /iservers/account/orders endpoint to review open-order(s).
    response = requests.get(url=request_url, verify=False)
    print(response.status_code, request_url)

    orderId = "1171486728"
    json_content = {
        "orderType": "MOC",
        "tif": "DAY",
        "side": "BUY",
        "conid": servConid,
        "quantity": 3 # changed qty to 3
    }
    request_url = f"{baseUrl}/iserver/account/{paperRegId}/order/{orderId}"
    response = requests.post(url=request_url, json=json_content, verify=False)
    print(response.status_code, response.json())
    # 200 {'msg': 'Request was submitted', 'order_id': 1171486724, 'conid': -1, 'account': None}
    # 400 {'error': "OrderID 1171486718 doesn't exist"}

def test_suppress_message(common_setup):
    json_content = {
        "messageIds": ["o10288"] # Full list at https://www.interactivebrokers.com/campus/ibkr-api-page/cpapi-v1/#suppressible-id
    }
    request_url = f"{baseUrl}/iserver/questions/suppress"
    response = requests.post(url=request_url, json=json_content, verify=False)
    print(response.status_code, response.json())
    # 200 {'status': 'submitted'}

def test_portfolio_accounts(common_setup):
    request_url = f"{baseUrl}/portfolio/accounts"
    response = requests.get(url=request_url, verify=False)
    print(response.status_code, response.json())
    # 200 {'status': 'submitted'}

def test_portfolio_positions(common_setup):
    request_url = f"{baseUrl}/portfolio2/{paperRegId}/positions?direction=a&sort=description"
    response = requests.get(url=request_url, verify=False)
    print(response.status_code, response.json())
    # 200 [{'position': 1283.0, 'conid': '16699274', 'avgCost': 4.995, 'avgPrice': 4.995, 'currency': 'USD', 'description': 'ACTG', 'isLastToLoq': False, 'marketPrice': 4.48, 'marketValue': 5747.840024471283, 
    # 'realizedPnl': 0.0, 'secType': 'STK', 'timestamp': 1728341792, 'unrealizedPnl': -660.7449755287171, 'assetClass': 'STK', 'sector': 'Consumer, Non-cyclical', 'group': 'Commercial Services', 'model': ''}, 
    # {'position': 753.0, 'conid': '640318253', 'avgCost': 8.405, 'avgPrice': 8.405, 'currency': 'USD', 'description': 'BGC', 'isLastToLoq': False, 'marketPrice': 9.687338829040527, 'marketValue': 7294.566138267517, 
    # 'realizedPnl': 0.0, 'secType': 'STK', 'timestamp': 1728341792, 'unrealizedPnl': 965.601138267517, 'assetClass': 'STK', 'sector': 'Financial', 'group': 'Diversified Finan Serv', 'model': ''}, {'position': -943.0, 'conid': '506665692', 'avgCost': 7.864771049840933, 'avgPrice': 7.864771049840933, 'currency': 'USD', 'description': 'CLYM', 'isLastToLoq': False, 'marketPrice': 5.259932041168213, 'marketValue': -4960.115914821625, 'realizedPnl': 0.0, 'secType': 'STK', 'timestamp': 1728341792, 'unrealizedPnl': 2456.363185178375, 'assetClass': 'STK', 'sector': 'Consumer, Non-cyclical', 'group': 'Biotechnology', 'model': ''}

def test_portfolio_positions_by_conid(common_setup):
    request_url = f"{baseUrl}/portfolio2/{paperRegId}/position/16699274"
    response = requests.get(url=request_url, verify=False)
    print(response.status_code, response.json())
    # 200 [{'position': 1283.0, 'conid': '16699274', 'avgCost': 4.995, 'avgPrice': 4.995, 'currency': 'USD', 'description': 'ACTG', 'isLastToLoq': False, 'marketPrice': 4.480000019073486, 'marketValue': 5747.840024471283, 'realizedPnl': 0.0, 'secType': 'STK', 'timestamp': 1728341967, 'unrealizedPnl': -660.7449755287171, 'assetClass': 'STK', 'sector': 'Consumer, Non-cyclical', 'group': 'Commercial Services', 'model': ''}]

def test_invalidate_backend_portfolio_cache(common_setup):
    json_content = {}
    request_url = f"{baseUrl}/portfolio/{paperRegId}/positions/invalidate"
    response = requests.post(url=request_url, json=json_content, verify=False)
    print(response.status_code, response.json())
    # 200 {'message': 'success'} although documentation claims to "and calls the /portfolio/{accountId}/positions/0 endpoint automatically."

def test_portfolio_summary(common_setup): # use ledger below instead
    request_url = f"{baseUrl}/portfolio/{paperRegId}/summary"
    response = requests.get(url=request_url, verify=False)
    print(response.status_code, response.json())

def test_portfolio_ledger(common_setup):
    request_url = f"{baseUrl}/iserver/accounts" 
    response = requests.get(url=request_url, verify=False)
    print(response.status_code, request_url)

    request_url = f"{baseUrl}/portfolio/{paperRegId}/ledger"
    response = requests.get(url=request_url, verify=False)
    print(response.status_code, response.json())
    # 200 {'USD': {'commoditymarketvalue': 0.0, 'futuremarketvalue': 0.0, 'corporatebondsmarketvalue': 0.0, 'warrantsmarketvalue': 0.0, 
    # 'settledcash': 1007302.4, 'exchangerate': 1, 'sessionid': 1, 'cashbalance': 1007302.4, 'netliquidationvalue': 1026037.75, 'interest': 356.21, 'unrealizedpnl': 856.24, 'stockmarketvalue': 18379.17, 
    #  'moneyfunds': 0.0, 'currency': 'USD', 'realizedpnl': 0.0, 'funds': 0.0, 'acctcode': 'DU9017794', 'issueroptionsmarketvalue': 0.0, 'key': 'LedgerList', 'timestamp': 1728342602, 'severity': 0, 
    # 'stockoptionmarketvalue': 0.0, 'futuresonlypnl': 0.0, 'tbondsmarketvalue': 0.0, 'futureoptionmarketvalue': 0.0, 'cashbalancefxsegment': 0.0, 'secondkey': 'USD', 
    # 'tbillsmarketvalue': 0.0, 'endofbundle': 1, 'dividends': 0.0, 'cryptocurrencyvalue': 0.0}, 
    # 'BASE': {'commoditymarketvalue': 0.0, 'futuremarketvalue': 0.0, 'settledcash': 1007302.4, 'exchangerate': 1, 'sessionid': 1, 'cashbalance': 1007302.4, '
    # corporatebondsmarketvalue': 0.0, 'warrantsmarketvalue': 0.0, 'netliquidationvalue': 1026037.75, 'interest': 356.21, 'unrealizedpnl': 856.24, 'stockmarketvalue': 18379.17, 'moneyfunds': 0.0, 
    # 'currency': 'BASE', 'realizedpnl': 0.0, 'funds': 0.0, 'acctcode': 'DU9017794', 'issueroptionsmarketvalue': 0.0, 'key': 'LedgerList', 'timestamp': 1728342602, 'severity': 0, 'stockoptionmarketvalue': 0.0, 
    # 'futuresonlypnl': 0.0, 'tbondsmarketvalue': 0.0, 'futureoptionmarketvalue': 0.0, 'cashbalancefxsegment': 0.0, 'secondkey': 'BASE', 'tbillsmarketvalue': 0.0, 'dividends': 0.0, 'cryptocurrencyvalue': 0.0}}

def test_position_info(common_setup):
    request_url = f"{baseUrl}/portfolio/positions/16699274"
    response = requests.get(url=request_url, verify=False)
    print(response.status_code, response.json())
    # {'DU9017794C': 
    # [{'acctId': 'DU9017794C', 'conid': 16699274, 'contractDesc': 'ACTG', 'position': 1283.0, 'mktPrice': 4.48, 'mktValue': 5747.84, 'currency': 'USD', 'avgCost': 4.995, 'avgPrice': 4.995, 'realizedPnl': 0.0, 
    # 'unrealizedPnl': -660.74, 'exchs': None, 'expiry': None, 'putOrCall': None, 'multiplier': 0.0, 'strike': '0', 'exerciseStyle': None, 'conExchMap': [], 'assetClass': 'STK', 'undConid': 0, 'model': '', 
    # 'incrementRules': [{'lowerEdge': 0.0, 'increment': 0.0001}, {'lowerEdge': 1.0, 'increment': 0.01}], 
    # 'displayRule': {'magnification': 0, 'displayRuleStep': [{'decimalDigits': 4, 'lowerEdge': 0.0, 'wholeDigits': 1}, {'decimalDigits': 2, 'lowerEdge': 1.0, 'wholeDigits': 4}]}, 'time': 31, 'chineseName': 'Acacia&#x7814;&#x7A76;&#x516C;&#x53F8;', 
    # 'allExchanges': 'AMEX,NYSE,CBOE,PHLX,CHX,ARCA,ISLAND,ISE,IDEAL,NASDAQQ,NASDAQ,DRCTEDGE,BEX,BATS,NITEECN,EDGEA,CSFBALGO,NYSENASD,PSX,BYX,ITG,PDQ,IBKRATS,CITADEL,NYSEDARK,MIAX,IBDARK,CITADELDP,NASDDARK,IEX,WEDBUSH,SUMMER,WINSLOW,FINRA,LIQITG,UBSDARK,BTIG,VIRTU,JEFF,OPCO,COWEN,DBK,JPMC,EDGX,JANE,NEEDHAM,FRACSHARE,RBCALGO,VIRTUDP,BAYCREST,FOXRIVER,MND,NITEEXST,PEARL,NITERTL,NYSENAT,IEXMID,HRT,FLOWTRADE,HRTDP,JANELP,PEAK6,CTDLZERO,HRTMID,JANEZERO,HRTEXST,IMCLP,LTSE,SOCGENDP,MEMX,INTELCROS,VIRTUBYIN,JUMPTRADE,NITEZERO,TPLUS1,XTXEXST,XTXDP,XTXMID,COWENLP,BARCDP,JUMPLP,OLDMCLP,RBCCMALP,WALLBETH,IBEOS,JONES,GSLP,BLUEOCEAN,OVERNIGHT,JANEMID,IBATSEOS,HRTZERO,VIRTUALGO,G1XLP,VIRTUMID,GLOBALXLP,CTDLMID,TPLUS0,JUMPMID', 
    # 'listingExchange': 'NASDAQ', 'countryCode': 'US', 'name': 'ACACIA RESEARCH CORP', 'lastTradingDay': None, 'group': 'Commercial Services', 'sector': 'Consumer, Non-cyclical', 'sectorGroup': 'Consulting Services', 
    # 'ticker': 'ACTG', 'type': 'COMMON', 'hasOptions': True, 'fullName': 'ACTG', 'isUS': True, 'isEventContract': False, 'pageSize': 100}], 
    # 'DU9017794': [{'acctId': 'DU9017794', 'conid': 16699274, 'contractDesc': 'ACTG', 'position': 1283.0, 'mktPrice': 4.48, 'mktValue': 5747.84, 'currency': 'USD', 'avgCost': 4.995, 'avgPrice': 4.995, 'realizedPnl': 0.0, 'unrealizedPnl': -660.74, 'exchs': None, 'expiry': None, 'putOrCall': None, 'multiplier': 0.0, 'strike': '0', 'exerciseStyle': None, 'conExchMap': [], 'assetClass': 'STK', 'undConid': 0, 'model': '', 
    # 'incrementRules': [{'lowerEdge': 0.0, 'increment': 0.0001}, {'lowerEdge': 1.0, 'increment': 0.01}], 'displayRule': {'magnification': 0, 'displayRuleStep': [{'decimalDigits': 4, 'lowerEdge': 0.0, 'wholeDigits': 1}, {'decimalDigits': 2, 'lowerEdge': 1.0, 'wholeDigits': 4}]}, 'time': 31, 'chineseName': 'Acacia&#x7814;&#x7A76;&#x516C;&#x53F8;', 
    # 'allExchanges': 'AMEX,NYSE,CBOE,PHLX,CHX,ARCA,ISLAND,ISE,IDEAL,NASDAQQ,NASDAQ,DRCTEDGE,BEX,BATS,NITEECN,EDGEA,CSFBALGO,NYSENASD,PSX,BYX,ITG,PDQ,IBKRATS,CITADEL,NYSEDARK,MIAX,IBDARK,CITADELDP,NASDDARK,IEX,WEDBUSH,SUMMER,WINSLOW,FINRA,LIQITG,UBSDARK,BTIG,VIRTU,JEFF,OPCO,COWEN,DBK,JPMC,EDGX,JANE,NEEDHAM,FRACSHARE,RBCALGO,VIRTUDP,BAYCREST,FOXRIVER,MND,NITEEXST,PEARL,NITERTL,NYSENAT,IEXMID,HRT,FLOWTRADE,HRTDP,JANELP,PEAK6,CTDLZERO,HRTMID,JANEZERO,HRTEXST,IMCLP,LTSE,SOCGENDP,MEMX,INTELCROS,VIRTUBYIN,JUMPTRADE,NITEZERO,TPLUS1,XTXEXST,XTXDP,XTXMID,COWENLP,BARCDP,JUMPLP,OLDMCLP,RBCCMALP,WALLBETH,IBEOS,JONES,GSLP,BLUEOCEAN,OVERNIGHT,JANEMID,IBATSEOS,HRTZERO,VIRTUALGO,G1XLP,VIRTUMID,GLOBALXLP,CTDLMID,TPLUS0,JUMPMID', 
    # 'listingExchange': 'NASDAQ', 'countryCode': 'US', 'name': 'ACACIA RESEARCH CORP', 'lastTradingDay': None, 'group': 'Commercial Services', 'sector': 'Consumer, Non-cyclical', 'sectorGroup': 'Consulting Services', 'ticker': 'ACTG', 'type': 'COMMON', 'hasOptions': True, 'fullName': 'ACTG', 'isUS': True, 'isEventContract': False, 'pageSize': 100}]}

def test_iserver_scanner_params(common_setup): # real-time, use /hmds/scanner/params for historical
    request_url = f"{baseUrl}/iserver/scanner/params"
    response = requests.get(url=request_url, verify=False)
    print(response.status_code, response.json()) 
    #     output structure: { 
    #  "scan_type_list":[{
    #       "display_name": "Top Option Imp Vol % Gainers",
    #       "code": "TOP_OPT_IMP_VOLAT_GAIN",
    #       "instruments": ['STK', 'ETF.EQ.US', 'ETF.FI.US', 'IND.US', 'STOCK.NA', 'STOCK.EU']
    #   }],
    #  "instrument_list":[{
    #       "display_name": "US Stocks",
    #       "type": "STK",
    #       "filters": ['avgVolume', 'avgUsdVolume', 'volume', 'volumeRate', 'usdVolume', 'stVolume3min', 'stVolume5min', 'stVolume10min','tradeCount', 'tradeRate', 'imbalance', 'displayImbalanceAdvRatio', 'regulatoryImbalance', 'displayRegulatoryImbAdvRatio',
    #                   'afterHoursChange', 'afterHoursChangePerc', 'changeOpenPerc', 'changePerc', 'openGapPerc', 'price', 'priceRange', 'usdPrice', 
    #                   'marketCap', 'firstTradeDate', 'issuerCountryIs', 'stkTypes', 'haltedIs', 
    #                   'avgPriceTarget', 'avgRating', 'avgAnalystTarget2PriceRatio', 'numPriceTargets', 'numRatings', 
    #                   'curEMA20', 'curEMA50', 'curEMA100', 'curEMA200', 'lastVsEMAChangeRatio20', 'lastVsEMAChangeRatio50', 'lastVsEMAChangeRatio100', 'lastVsEMAChangeRatio200', 'curMACD', 'curMACDSignal', 'curMACDDist', 
    #                   'dividendFrd', 'dividendYieldFrd', 'dividendNextAmount', 'histDividendFrd', 'histDividendFrdYield', 'dividendNextDate', 
    #                   'feeRate', 'unshortableIs', 'shortSaleRestrictionIs', 'sharesAvailableMany', 
    #                   'hasOptionsIs', 'avgOptVolume', 'optOpenInterest', 'optVolume', 'optVolumePCRatio',
    #                   'impVolat', 'impVolatChangePerc', 'impVolatOverHist', 'ivRank13w', 'ivRank26w', 'ivRank52w', 'ivPercntl13w', 'ivPercntl26w', 'ivPercntl52w', 'hvRank13w', 'HVRank26w', 'HVRank52w', 'HVPercntl13w', 'HVPercntl26w', 'HVPercntl52w', 
    #                   'ihInsiderOfFloatPerc', 'iiInstitutionalOfFloatPerc', 'ihNumSharesInsider', 'iiNumSharesInstitutional', 'peaEligibleStkIs', 
    #                   'minGrowthRate', 'maxGrowthRate', 'minPeRatio', 'maxPeRatio', 'curPPO', 'curPPOSignal', 'curPPODist', 'minPrice2Bk', 'maxPrice2Bk', 'minPrice2TanBk', 'maxPrice2TanBk', 'minQuickRatio', 'maxQuickRatio',  'minRetnOnEq', 'maxRetnOnEq',  
    #                   'rcgLongTermClassIs', 'rcgLongTermTechnicalDate', 'rcgLongTermEventScore', 'rcgLongTermTradeIs', 'rcgIntermediateTermClassIs', 'rcgIntermediateTermTechnicalDate', 'rcgIntermediateTermEventScore', 'rcgIntermediateTermTradeIs', 'rcgShortTermClassIs', 'rcgShortTermTechnicalDate', 'rcgShortTermEventScore', 'rcgShortTermTradeIs', 
    #                   'esgScore', 'esgCombinedScore', 'esgControversiesScore', 'esgResourceUseScore', 'esgEmissionsScore', 'esgEnvInvScore', 'esgWorkforceScore', 'esgHrScore', 'esgCommunityScore', 'esgProdRespScore', 'esgManagementScore', 'esgShareholdersScore', 'esgStrategyScore', 'esgEnvPillarScore', 'esgSocialPillarScore', 'esgCorpGovPillarScore', 
    #                   'utilization', 'socialSentimentScore', 'socialSentimentScoreChange', 'tweetVolumeScore', 'tweetVolumeScoreChange', 'epsChangeTTM', 'revChange', 'revGrowthRate5Y', 'payoutRatioTTM', 'price2CashTTM', 'operatingMarginTTM', 'netProfitMarginTTM', 'returnOnInvestmentTTM']}, 
    #   }],
    #  "filter_list":[{
    #       "group": "afterHoursChangeAbove",
    #       "display_name": "After-Hours Change Above",
    #       "code": "afterHoursChangeAbove",
    #       "type": "non-range"
    #     }],
    #  "location_tree":[{
    #       "display_name": "US Stocks",
    #       "type": "STK",
    #       "locations": [{
    #           "display_name": "Listed/NASDAQ",
    #           "type": "STK.US.MAJOR",
    #           "locations": []
    #         }]
    #     }]
    # }
    
def test_iserver_scanner_run(common_setup): # real-time, use /hdms/scanner/run for historical
    json_content = {
        "instrument": "STK",
        "location": "STK.US.MAJOR",
        "type": "WSH_PREV_EARNINGS", # "TOP_TRADE_COUNT",
        "filter": []
        # filter:
        #     { "code": "priceAbove", "value": 5}, { "code": "impVolatBelow", "value": 50},
        # ]
    }
    request_url = f"{baseUrl}/iserver/scanner/run"
    response = requests.post(url=request_url, json=json_content, verify=False)
    print(response.status_code, response.json()) 
#  up to 50 'contracts': [
# {'server_id': '0', 'column_name': 'Trades', 'symbol': 'TSLA', 'conidex': '76792991', 'con_id': 76792991, 'available_chart_periods': '#R|1', 'company_name': 'TESLA INC', 'scan_data': '431.677K', 'contract_description_1': 'TSLA', 'listing_exchange': 'NASDAQ.NMS', 'sec_type': 'STK'}, 
# {'server_id': '1', 'symbol': 'NVDA', 'conidex': '4815747', 'con_id': 4815747, 'available_chart_periods': '#R|1', 'company_name': 'NVIDIA CORP', 'scan_data': '420.629K', 'contract_description_1': 'NVDA', 'listing_exchange': 'NASDAQ.NMS', 'sec_type': 'STK'},

# TODO: test next day, 404 and 503 (service unavailable) on Sat
def test_hmds_scanner_params(common_setup):
    request_url = f"{baseUrl}/hmds/scanner/params"
    response = requests.get(url=request_url, verify=False)
    print(response.status_code, response.json()) 
    
def test_hmds_scanner_run(common_setup):
    json_content= {
    "instrument":"BOND",
    "locations": "BOND.US",
    "scanCode": "HIGH_BOND_ASK_YIELD_ALL",
    "secType": "BOND",
    "delayedLocations":"SMART",
    "maxItems":25,
    "filters":[{
        "bondAskYieldBelow": 15.819 }]
    }
    request_url = f"{baseUrl}/hmds/scanner/run"
    response = requests.post(url=request_url, json=json_content, verify=False)
    print(response.status_code, response.json())


def test_auth_status(common_setup):
    request_url = f"{baseUrl}/iserver/auth/status"
    response = requests.get(url=request_url, verify=False)
    print(response.status_code, response.json())
    # 200 {'authenticated': True, 'competing': False, 'connected': True, 'message': '', 'MAC': '98:F2:B3:23:BF:A0', 'serverInfo': {'serverName': 'JifN13001', 'serverVersion': 'Build 10.30.1q, Oct 3, 2024 6:30:36 PM'}, 'hardware_info': '2f6bedbc|98:F2:B3:23:BF:A0', 'fail': ''}
    #200 {'authenticated': False, 'competing': False, 'connected': False, 'MAC': '98:F2:B3:23:BF:A0'}

def test_init_brokerage_session(common_setup):
    request_url = f"{baseUrl}/iserver/auth/ssodh/init"
    json_content= {"publish": True, "compete": True}
    response = requests.post(url=request_url, json=json_content, verify=False)
    print(response.status_code, response.json())
    # 200 {'authenticated': True, 'competing': False, 'connected': True, 'message': '', 'MAC': '98:F2:B3:23:BF:A0', 'serverInfo': {'serverName': 'JifN13001', 'serverVersion': 'Build 10.30.1q, Oct 3, 2024 6:30:36 PM'}, 'hardware_info': '2f6bedbc|98:F2:B3:23:BF:A0'}
    # 200 {'passed': True, 'authenticated': True, 'connected': True, 'competing': False, 'hardware_info': '28f68bd9|98:F2:B3:23:BF:A0'}

def test_logout(common_setup):
    request_url = f"{baseUrl}/logout"
    json_content= {}
    response = requests.post(url=request_url, json=json_content, verify=False)
    print(response.status_code, response.json())
    # 200 {'status': True}

def test_validate_sso(common_setup):
    request_url = f"{baseUrl}/sso/validate"
    response = requests.get(url=request_url, verify=False)
    print(response.status_code, response.json())
    # 200 {'USER_ID': 122103533, 'USER_NAME': 'wgwtky012', 'RESULT': True, 'AUTH_TIME': 1728751902917, 'SF_ENABLED': True, 'IS_FREE_TRIAL': False, 'CREDENTIAL': 'smugstrug', 'IP': '75.164.78.20', 'EXPIRES': 16181, 
    # 'QUALIFIED_FOR_MOBILE_AUTH': None, 'LANDING_APP': 'PORTAL-US', 'IS_MASTER': False, 'lastAccessed': 1728757042356, 
    # 'features': {'env': 'PROD', 'wlms': True, 'realtime': True, 'bond': True, 'optionChains': True, 'calendar': True, 'newMf': True}, 'region': 'NJ'}

def test_create_watchlist(common_setup): #
    request_url = f"{baseUrl}/iserver/watchlist"
    json_content= {"id": "1234", # Supply a unique identifier to track a given watchlist. Must supply a number.
        "name": "Test Watchlist", # the human readable name of a given watchlist. Displayed in TWS and Client Portal.
        "rows":[
            {"C": aaplConid}, # C: int.Provide the conid, or contract identifier, of the conid to add.
            {"H": ""}, # H: Empty String. Can be used to add a blank row between contracts in the watchlist.
            {"C": servConid}
        ]
    }
    response = requests.post(url=request_url, json=json_content, verify=False)
    print(response.status_code, response.json())
    # 400 {'error': 'Bad Request: no bridge', 'statusCode': 400}
    # 200 {'id': '1234', 'hash': '1728855653701', 'name': 'Test Watchlist', 'readOnly': False, 'instruments': [] - always returns an empty array, don't freak out}

def test_get_watchlists(common_setup):
    request_url = f"{baseUrl}/iserver/watchlists?SC=USER_WATCHLIST"
    response = requests.get(url=request_url, verify=False)
    print(response.status_code, response.json())
    # 200 {'data': {'scanners_only': False, 'show_scanners': False, 'bulk_delete': False, 'user_lists': 
    # [{'is_open': False, 'read_only': False, 'name': 'Test Watchlist', 'modified': 1728855653701, 'id': '1234', 'type': 'watchlist'}, 
    # {'is_open': False, 'read_only': False, 'name': 'SMMT Jun 21', 'modified': 1716997395884, 'id': '100', 'type': 'watchlist'}, 
    # {'is_open': False, 'read_only': False, 'name': 'Favorites', 'modified': 1714976678718, 'id': '1', 'type': 'watchlist'}, 
    # {'is_open': False, 'read_only': False, 'name': 'Watchlist', 'modified': 1714976655984, 'id': '2', 'type': 'watchlist'}]}, 'action': 'content', 'MID': '2'}

def test_get_watchlist(common_setup):
    request_url = f"{baseUrl}/iserver/watchlist?id=2"
    response = requests.get(url=request_url, verify=False)
    print(response.status_code, response.json())
    # 200 {'id': '1234', 'hash': '1728855653701', 'name': 'Test Watchlist', 'readOnly': False, 
    # 'instruments': [{'ST': 'STK', 'C': '265598', 'conid': 265598, 'name': 'APPLE INC', 'fullName': 'AAPL', 'assetClass': 'STK', 'ticker': 'AAPL', 'chineseName': '&#x82F9;&#x679C;&#x516C;&#x53F8;'}, {'H': ''},
    #  {'ST': 'STK', 'C': '689676896', 'conid': 689676896}]}

def test_delete_watchlist(common_setup):
    request_url = f"{baseUrl}/iserver/watchlist?id=2"
    response = requests.delete(url=request_url, verify=False)
    print(response.status_code, response.json())
    # 200 {'data': {'deleted': '100'}, 'action': 'context', 'MID': '3'}

def test_ping(common_setup): # Expected every 60 seconds?
    request_url = f"{baseUrl}/tickle"
    json_content = {}
    response = requests.post(url=request_url, json=json_content, verify=False)
    print(response.status_code, response.json())

# WEBSOCKETS
# Websocket topics requiring a brokerage session: 
# smd (live market data), smh (historical market data), sbd (live price ladder data), sor (order updates), str (trades), act (unsolicited account property info), 
# sts (unsolicited brokerage session authentication status), blt (unsolicited bulletins), ntf (unsolicited notifications)
#
# Websocket topics that do not require a brokerage session: 
# spl (profit & loss updates), ssd (account summary updates), sld (account ledger updates), system (unsolicited connection-related messages).
#
# The url for websockets is: wss://localhost:5000/v1/api/ws
#
# If you require brokerage functionality, you will need to establish a brokerage session prior to opening a websocket, just as is required before making requests to /iserver endpoints.
#
# First make request the /tickle endpoint and save the returned session value.

# NOT quite working - something is running on port 5000?
 
def on_open(ws):
    print("Opened Connection")
    time.sleep(3)
    ws.send('smd+265598+{"fields":["31","84","86"]}')

def on_message(ws, message):
    print("Received message" + message)
    sleep(3)

def on_error(ws, error):
    print("Received error" + str(error))

def on_close(ws):
    print("### closed ###")

def on_cont(ws):
    print("on_cont")

def test_ws_connect(common_setup): # Can't get to work reliably, short-lived method below is ok. Instructions say port 5000, but it is used by the AirPlay server on MacOS
    # request_url = f"{baseUrl}/tickle"
    # json_content = {}
    # response = requests.post(url=request_url, json=json_content, verify=False)
    # print(response.status_code, response.json())
    # sessionToken = response.json()['session']
    sessionToken = "2ea1b33c17f14279ea27c6b235c3725f"

    ws = websocket.WebSocketApp(
        url="wss://localhost:7498/v1/api/ws",
        on_open=on_open,
        on_message=on_message,
        on_error=on_error,
        on_close=on_close,
        cookie=f"api={sessionToken}"
    )
    ws.run_forever(sslopt={"cert_reqs": ssl.CERT_NONE}, dispatcher=rel, reconnect=5)  # Set dispatcher to automatic reconnection, 5 second reconnect delay if connection closed unexpectedly
    rel.signal(2, rel.abort)  # Keyboard Interrupt
    rel.dispatch()

def test_ws_connect_shortlived(common_setup):
    ws = websocket.create_connection("wss://localhost:7498/v1/api/ws", sslopt={"cert_reqs": ssl.CERT_NONE})
    print(ws.recv())
    print("Sending 'Hello, World'...")
    ws.send("Hello, World")
    print("Sent")
    print("Receiving...")
    result = ws.recv()
    print("Received '%s'" % result)
    ws.close()

def test_earn_entry(common_setup):
    # conid = '178634687' # WBA
    conids = ['8428', '69195736', '5811', '764657', '173962302', '302202060', '6478095'] # IIIN, IRDM, CMC, BMI, ELV, LBRT, STLD
    conid_6d = {}
    for conid in conids:
        lookback_days = 6
        period = f"{lookback_days}d"
        bar = "1d"
        direction = "-1" # backwards - only needed for hmds
        request_url = f"{baseUrl}/hmds/history?conid={conid}&period={period}&bar={bar}&direction={direction}&outsideRth=false"
#       request_url = f"{baseUrl}/iserver/marketdata/history?conid={conid}&exchange=SMART&period={period}&bar={bar}&outsideRth=false"
        print(request_url)
        response = requests.get(url=request_url, verify=False)
        print(response.status_code, response.json())
        bars = response.json()['data']
        close_lookback = bars[0]['c']
        close_today = bars[len(bars) - 1]['c']
        if len(bars) == lookback_days:
            conid_6d[conid] = close_lookback
            print(f"{conid} lookback: {close_lookback}, today: {close_today}")
        else:
            conid_6d[conid] = "N/A"
        for index, bar in enumerate(bars):
            timestamp = bar['t'] / 1000
            print(f"{conid} {datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')} close: {bar['c']:.2f} v: {bar['v']}")

    print(conid_6d)

    request_url = f"{baseUrl}/iserver/accounts" # preflight method required
    response = requests.get(url=request_url, verify=False)
    print(response.status_code, request_url)

    fields = "31,55,70,71,83,87,88,7051,7059,7084,7085,7087,7281,7282,7283,7287,7288,7289,7291,7293,7294,7295,7607,7636,7637,7644,7675,7679,7682,7686,7718,7741"
    request_url = f"{baseUrl}/iserver/marketdata/snapshot?conids={','.join(conids)}&fields={fields}"
    response = requests.get(url=request_url, verify=False)
    print(response.status_code, request_url, response.json())
    contracts = response.json()
    data = []
    for c in contracts:
        conid: str = c['conid']
        s = c['55']
        name = c['7051']
        cat = c['7281']
        last = c['31']
        roc = f"{c['83']}%"
        print("CONID 6D", conid_6d)
        sixd = conid_6d[str(conid)]
        roc6 = f"{100 * (float(last) / float(sixd) - 1):.2f}%"
        c2ema100 = c['7679']
        iv = c['7283']
        hv30 = c['7087']
        iv2hv = c['7084']
        p2c = c.get('7085', 'N/A') # put/call interest
        v = c['87']
        v30 = c['7282']
        cap = c['7289']
        earn = c['7686'] 
        o = c['7295']
        h = c['70']
        l = c['71']
        h52w = c['7293']
        l52w = c['7294']
        div = c['7287']
        eps = c['7291']
        shortable = c['7644'] 
        fee = c['7637']

        my_dict = {k: v for k, v in locals().items() if k in ['s', 'name', 'cat', 'last', 'roc', 'sixd', 'roc6', 'c2ema100', 'iv', 'hv30', 'iv2hv', 'p2c', 'v', 'v30', 'earn', 'o', 'h', 'l', 'h52w', 'l52w', 'div', 'cap', 'eps', 'shortable', 'fee']}
        data.append(my_dict)
        print(f"{s} {name} {cat} {last} 1d:{roc} 6d:{roc6} c/ema100:{c2ema100} o:{o} h:{h} l:{l} v:{v} v30:{v30} 52h:{h52w} 52l:{l52w} div:{div} mc:{cap} eps:{eps} iv:{iv} hv30:{hv30} iv/hv:{iv2hv} p/c:{p2c} {shortable} fee:{fee} earn:{earn}")

    df = pd.DataFrame(data)
    df.to_csv(f"earn_{date.today().strftime('%Y%m%d')}.csv", index=False)


def test_dict_create():
        shortable = 'shortable' 
        fee = '0.25%'
        earn = '20.17'
        my_dict = {k: v for k, v in locals().items() if k not in ['my_dict', 'k', 'v']}
        print(my_dict)

def test_convert_to_number(common_setup):
    suffixes = {'K': 1000, 'M': 1000000, 'B': 1000000000}
    string = '90.4K'
    if string[-1].isalpha():
        number = float(string[:-1]) * suffixes[string[-1].upper()]
        assert(number == 90400)