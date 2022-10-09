import re


def test_symbol_in_parens_regex():
    desc = '''
    Russia's Gazprom (OGZPY) said on Tuesday it earned a record net profit of 2.5T rubles ($41.75B) in H1 2022, 
    "despite sanctions pressure and an unfavorable"
    '''
    m = re.search(r'\([A-Z]+\)', desc)
    assert(m.group(0) == '(OGZPY)')