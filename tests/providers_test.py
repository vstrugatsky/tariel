from providers import parse_query_param_value


def test_parse_Query_Param_Value():
    value = parse_query_param_value('https://api.polygon.io/v3/tickers?cursor=xyz', 'cursor')
    assert(value == 'xyz')

    value = parse_query_param_value('https://api.polygon.io/v3/tickers?cursor=', 'cursor')
    assert(value is None)

    value = parse_query_param_value('https://api.polygon.io/v3/tickers?different=xyz', 'cursor')
    assert(value is None)

    value = parse_query_param_value('https://api.polygon.io/v3/tickers?cursor', 'cursor')
    assert(value is None)

    value = parse_query_param_value('https://api.polygon.io/v3/tickers?', 'cursor')
    assert(value is None)

    value = parse_query_param_value('https://api.polygon.io/v3/tickers', 'cursor')
    assert(value is None)
