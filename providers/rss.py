import feedparser

d = feedparser.parse("https://seekingalpha.com/market_currents.xml", modified='Fri, 19 Aug 2012 23:00:34 GMT')
# feedparser.parse()
feed = d['feed']
print(d.etag, d.encoding, d.bozo)
print(f'Headers={d.headers}', d.href, d.status, d.namespaces, d.version, feed)
print(f'{feed.title} base={feed.title_detail.base} link={feed.link}')
for key in d.entries:
    print(key)