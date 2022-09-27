from providers import parse_query_param_value
import unittest


class TestParseQueryParamValue(unittest.TestCase):
    def runTest(self):
        value = parse_query_param_value('https://api.polygon.io/v3/tickers?cursor=xyz', 'cursor')
        self.assertEqual(value, 'xyz')

        value = parse_query_param_value('https://api.polygon.io/v3/tickers?cursor=', 'cursor')
        self.assertIsNone(value)

        value = parse_query_param_value('https://api.polygon.io/v3/tickers?different=xyz', 'cursor')
        self.assertIsNone(value)

        value = parse_query_param_value('https://api.polygon.io/v3/tickers?cursor', 'cursor')
        self.assertIsNone(value)

        value = parse_query_param_value('https://api.polygon.io/v3/tickers?', 'cursor')
        self.assertIsNone(value)

        value = parse_query_param_value('https://api.polygon.io/v3/tickers', 'cursor')
        self.assertIsNone(value)
