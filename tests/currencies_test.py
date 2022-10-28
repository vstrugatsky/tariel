from model.currency import Currency


def test_format_for_regex():
    # currencies should be sorted by longest first (3 letters as in USD) so that the first separator | is in position 4
    assert(Currency.format_for_regex().index('|') == 3)