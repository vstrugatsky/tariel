from providers import sleep_if_needed, parse_query_param_value
import model
import requests
from datetime import datetime


class Fmp:
    fmpApiKey = 'd9d9541d1eaa345ec8ec35fadb381229'
    fmpPrefix = 'https://financialmodelingprep.com/api'

    # historical / earning_calendar / AAPL
# {
#   "date" : "2022-07-28",
#   "symbol" : "AAPL",
#   "eps" : 1.2, - correct
#   "epsEstimated" : 1.16, - correct and differs from incorrect /analyst-estimates
#   "time" : "amc",
#   "revenue" : 8.2959E+10, - correct
#   "revenueEstimated" : 80098344827, - incorrect and matches incorrect /analyst-estimates
#   "updatedFromDate" : "2022-07-25",
#   "fiscalDateEnding" : "2022-06-25"
# }