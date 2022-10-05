from urllib import parse
from datetime import datetime
import time


def parse_query_param_value(url, param_name):
    query = parse.urlparse(url).query
    if query:
        param_value = parse.parse_qs(query).get(param_name, None)
    else:
        return None
    if param_value:
        return param_value[0]
    else:
        return None


def sleep_if_needed(last_call_time, api_calls_per_minute):
    call_every_n_seconds = 60 / api_calls_per_minute + 1
    now = datetime.utcnow()
    if (now - last_call_time).seconds < call_every_n_seconds:
        print(f'Sleeping for {call_every_n_seconds - (now - last_call_time).seconds} seconds')
        time.sleep(call_every_n_seconds - (now - last_call_time).seconds)
