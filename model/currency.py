import re


class Currency:
    currencies = {
        '$': 'USD',
        'C$': 'CAD',
        'CAD': 'CAD',
        '€': 'EUR',
        'Є': 'EUR',
        'EUR': 'EUR',
        '£': 'GBP',
        'GBP': 'GBP',
        '¥': 'JPY',
        'S$': 'SGD', # Singaporean dollar
        'SGD': 'SGD',
        '₹': 'INR',  # Indian rupee
        'SEK': 'SEK',  # swedish kroner
        'DKK': 'DKK',
        'NOK': 'NOK',   # norwegian kroner
        'CHF': 'CHF', # swiss franc
        'RMB': 'CNY', # Chinese remnibi -> yuan
        'CNY': 'CNY',  # Yuan
        'Ps.': 'MXN', # mexican Peso
                }

    @staticmethod
    def format_for_regex():
        return format('|'.join(map(re.escape, sorted(Currency.currencies, key=len, reverse=True))))

