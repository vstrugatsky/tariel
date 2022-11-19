from __future__ import annotations
from jsonpath_ng import parse


class Utils:
    @staticmethod
    def find_first_match(jsonpath, json):
        jsonpath_expr = parse(jsonpath)
        matches = jsonpath_expr.find(json)
        if len(matches) > 0:
            return matches[0].value
        else:
            return None

    @staticmethod
    def apply_uom(amount: float, uom: str | None) -> float:
        scale = {'K': 1000, 'M': 1000000, 'B': 1000000000, 'T': 1000000000000}
        if not uom or uom.upper() not in scale.keys():
            return float(amount)
        else:
            return round(float(amount) * scale.get(uom.upper()))

    @staticmethod
    def update_list_without_dups(existing_list: [], new_list: []) -> []:
        if not existing_list:
            return new_list
        elif new_list:
            return list(set(existing_list + new_list))
        else:
            return existing_list
