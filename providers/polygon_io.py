from providers import sleep_if_needed, parse_query_param_value
import model
import requests
from datetime import datetime
from typing import Callable


class PolygonIo:
    polygonApiKey = 'o_wd3aO1d9Dyi9KEjxbpxJNrbkM5ssmN' # 5/min
    polygonPrefix = 'https://api.polygon.io/'

    @staticmethod
    def call_paginated_api(url_suffix: str,
                           payload: dict,
                           method: Callable[[dict, model.Session, dict], object],
                           method_params: dict,
                           commit: bool,
                           paginate: bool,
                           cursor: str) -> None:
        if cursor is None:  # first or last execution
            payload.update({'apiKey': PolygonIo.polygonApiKey})
        else:
            payload = {'apiKey': PolygonIo.polygonApiKey, 'cursor': cursor}

        last_call_time = datetime.utcnow()
        r = requests.get(url_suffix, params=payload, timeout=10)
        cursor = parse_query_param_value(r.json().get('next_url'), 'cursor')

        print(f'INFO {datetime.utcnow()} URL={r.url} \n Status={r.status_code} Count={r.json().get("count")}')
        print(f'INFO {datetime.utcnow()} Next URL={r.json().get("next_url")} cursor={cursor}')

        with model.Session() as session:
            for i in r.json()['results']:
                print(i)
                model_object = method(i, session, method_params)
                if model_object:
                    session.merge(model_object)
            if commit:
                session.commit()

        if cursor and paginate is True:
            sleep_if_needed(last_call_time, api_calls_per_minute=5)
            PolygonIo.call_paginated_api(url_suffix, {}, method, method_params, commit, paginate, cursor)
