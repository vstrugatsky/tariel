import re

import model


class Sentiment():
    positive_words = [
        'activist', 'beat', 'boost', 'buoy', 'buyback', 'climb', 'gain', 'improve', 'jump', 'positive', 'rally',
        'repurchase', 'robust', 'savor', 'soar',
        'strength', 'strong', 'surge', 'surpass', 'topper', 'tops', 'upbeat', 'upgrade', 'raise']
    positive_phrases = [
        'above consensus', 'all-time high', 'approve', 'best quarter', 'better than expected', 'exceed estimates',
        'exceed expectations', 'FDA clear', 'FDA fast-track', 'get nod', 'lower expenses', 'price strength', 'receives OK',
        'reduce risk', 'reinstate dividend', 'revenue rise', 'seen up', 'shows promise', 'topline record']
    negative_words = [
        'bleed', 'crash', 'cut', 'decline', 'deficiency', 'delist', 'deteriorate', 'dim', 'downbeat', 'downgrade',
        'downturn', 'drop', 'failure',
        'fall', 'headwind', 'lowers', 'maul', 'miss', 'negative', 'non-compliance', 'overrun', 'plunge', 'sink', 'slump', 'weak', 'weigh', 'woes']
    negative_phrases = [
        'all-time low', 'below consensus', 'delinquency rate rise', 'FDA halts', 'higher expenses', 'hurt demand',
        'licensing dispute', 'patient death', 'seen down', 'suspended from trading']

    neutral = ['consolidation']
    earnings_words = ['results', 'beat', 'miss', 'exceed', 'Q1', 'Q2', 'Q3', 'Q4', 'FY' ]

    @staticmethod
    def parse_sentiment(tweet_text: str) -> int:
        sentiment = 0
        p = re.compile(r'''
           (?P<positive_sentiment>
           \W(earnings|results|estimates)\ (surpass|exceed|gain|beat|top)|
           \W(revenue(s?)|profit(s?))\ (soar|surpass|jump)|
           \W(guidance|forecast|outlook|dividend)\ (raise)|
           \Wraise[sd]\ .*(guidance|forecast|outlook|dividend)|
           \W(tops|topping|topped)\ .*(forecast|estimate)|
           \Wincome\ (growth)|
           \W(expenses|costs)\ (plummet|improve)|
           \W(high(er)?|strong)\ (sales|earnings|revenues|margins|demand|profit|income|volume|pricing|consumption)|
           \Wlow(er)?\ (expenses|costs)|\Wfree\ cash\ flow\ jump|
           \W(Q[1-4]\ )?beat(?!e)|\Wboost|\Wstrength|\Wstrong|\Wtailwind|\Wraise[sd])
           ''', re.VERBOSE | re.IGNORECASE | re.DOTALL)
        for i in p.finditer(tweet_text):
            print('i.groupdict()["positive_sentiment"] = ' + i.groupdict()["positive_sentiment"])
            sentiment += 1

        p = re.compile(r'''
           (?P<negative_sentiment>
           \W(earnings|revenue(s?)|profit(s?))\ (slip|fall|miss|decline|plummet)|
           \Wguidance\ (cut|lowered|slashed)|
           \Whigh(er)?\ (expenses|costs)|
           \W(low(er)?|weak)\ (sales|earnings|revenues|margins|demand|profit|income|volume|pricing|consumption)|
           \W(lowers|lowered|slashe[sd])\ .*(guidance|forecast|outlook|dividend)|
           \W((Q[1-4]|credit)\ )?(loss|miss)|
           \Wweak|\Wheadwind|\Wlowered|\Wdecline|\Wdrop|\Wdelay|\Wcost\ overrun)
           ''', re.VERBOSE | re.IGNORECASE | re.DOTALL)
        for i in p.finditer(tweet_text):
            print('i.groupdict()["negative_sentiment"] = ' + i.groupdict()["negative_sentiment"])
            sentiment -= 1

        return sentiment
