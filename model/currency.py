import re


class Currency:
    currencies = {
        'C$': 'CAD',
        'CAD': 'CAD',
        '$R': 'BRL',
        'R$': 'BRL',  # Brazilian real
        '€': 'EUR',
        'Є': 'EUR',
        'EUR': 'EUR',
        '£': 'GBP',
        'GBP': 'GBP',
        '¥': 'JPY',
        'HUF': 'HUF',  # Hungarian florins
        'S$': 'SGD', # Singaporean dollar
        'SGD': 'SGD',
        'NT': 'TWD',
        'NT$': 'TWD', # New Taiwan Dollar
        '₹': 'INR',  # Indian rupee
        'SEK': 'SEK',  # swedish kroner
        'DKK': 'DKK',
        'NOK': 'NOK',   # norwegian kroner
        'CHF': 'CHF', # swiss franc
        'Rp': 'IDR',  # Indonesian Rupee
        'RMB': 'CNY', # Chinese remnibi -> yuan
        'CNY': 'CNY',  # Yuan
        'Ps.': 'MXN', # mexican Peso
        '$': 'USD',
                }

    @staticmethod
    def format_for_regex():
        return format('|'.join(map(re.escape, sorted(Currency.currencies, key=len, reverse=True))))

