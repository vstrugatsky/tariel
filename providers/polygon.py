from __future__ import annotations
from providers import sleep_if_needed, parse_query_param_value
import model
import requests
from datetime import datetime
from typing import Callable, Optional


class Polygon:
    polygonApiKey = 'o_wd3aO1d9Dyi9KEjxbpxJNrbkM5ssmN'  # 5/min
    polygonPrefix = 'https://api.polygon.io/'

    @staticmethod
    def convert_polygon_symbol_to_eod(symbol: str) -> str | None:
        # Polygon format for preferred stock:
        # replace lowercase p e.g. AAICpB -> AAIC-PB
        # replace dot e.g. AKO.A -> AKO-A
        index: int = symbol.find('p')
        if index > 0:
            return symbol[:index] + '-P' + symbol[index+1:]
        else:
            index = symbol.find('.')
            if index > 0:
                return symbol[:index] + '-' + symbol[index+1:]
            else:
                return None

    @staticmethod
    def call_paginated_api(url: str,
                           payload: dict,
                           method: Callable[[dict, model.Session, dict], object],
                           method_params: dict,
                           commit: bool,
                           paginate: bool,
                           cursor: Optional[str]) -> None:
        if cursor is None:  # first or last execution
            payload.update({'apiKey': Polygon.polygonApiKey})
        else:
            payload = {'apiKey': Polygon.polygonApiKey, 'cursor': cursor}

        last_call_time = datetime.utcnow()
        r = requests.get(url, params=payload, timeout=10)
        cursor = parse_query_param_value(r.json().get('next_url'), 'cursor')

        print(f'INFO {datetime.utcnow()} URL={r.url} \n Status={r.status_code} Count={r.json().get("count")}')
        print(f'INFO {datetime.utcnow()} Next URL={r.json().get("next_url")} cursor={cursor}')

        with model.Session() as session:
            for i in r.json()['results']:
                print(i)
                method(i, session, method_params)
            if commit:
                session.commit()

        if cursor and paginate is True:
            sleep_if_needed(last_call_time, api_calls_per_minute=5)
            Polygon.call_paginated_api(url, {}, method, method_params, commit, paginate, cursor)
