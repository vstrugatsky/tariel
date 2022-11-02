from __future__ import annotations
import requests
from typing import Callable, Optional
from datetime import datetime

from config import config
import model


class Twitter:
    url_prefix = 'https://api.twitter.com/2'

    @staticmethod
    def get_cashtags(response: dict) -> Optional[dict]:
        entities = response.get('entities', None)
        return entities.get('cashtags', None) if entities else None

    @staticmethod
    def call_paginated_api(url: str,
                           payload: dict,
                           method: Callable[[dict, model.Session, dict], object],
                           method_params: dict,
                           paginate: bool, commit: bool, next_token: str | None):

        if next_token and paginate:  # first or last execution
            payload.update({'pagination_token': next_token})

        r = requests.get(url=url,
                         params=payload,
                         headers={'Authorization': 'Bearer ' + config.twitter['bearer_token']})

        print(f'INFO {datetime.utcnow()} {r.headers["content-type"]} {r.encoding} {r.url} \n Status={r.status_code}')
        if r.status_code != 200:
            print(f'ERROR status code {r.status_code} and response {r.json()}')
            exit(1)
        print(f'Meta={r.json()["meta"]}')
        next_token = r.json()["meta"].get("next_token", None)

        count = 0
        with model.Session() as session:
            while count < r.json()["meta"]["result_count"]:
                # print('r.json=' + str(r.json()))
                method(r.json()['data'][count], session, method_params)
                count += 1
            if commit:
                session.commit()
            else:
                session.rollback()

        if paginate and next_token:
            Twitter.call_paginated_api(
                url=url,
                payload=payload,
                method=method, method_params=method_params,
                paginate=paginate, commit=commit, next_token=next_token)
