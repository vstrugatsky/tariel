import re


class Currency:
    currencies = {
        '$': 'USD',
        'C$': 'CAD',
        'CAD': 'CAD',
        '€': 'EUR',
        'EUR': 'EUR',
        '£': 'GBP',
        'GBP': 'GBP',
        '¥': 'JPY',
        '₹': 'INR',  # Indian rupee
        'SEK': 'SEK',  # swedish kroner
        'DKK': 'DKK',
        'NOK': 'NOK',   # norwegian kroner
        'CHF': 'CHF'  # swiss franc
                }

    @staticmethod
    def format_for_regex():
        return format('|'.join(map(re.escape, sorted(Currency.currencies, key=len, reverse=True))))

