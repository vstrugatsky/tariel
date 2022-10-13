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
