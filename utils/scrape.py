from scrapy.crawler import CrawlerProcess
import scrapy

class IRSpider(scrapy.Spider):
    name = 'ir'
    start_urls = ["https://investorsmedia.mesoblast.com/asx-announcements"]

    def parse(self, response):
        print('url = ' + response.url)
        print('title = ' + response.css("title::text").getall())
        # print('body = ' + response.css("body::text").getall())

process = CrawlerProcess(
    settings={
        # 'DOWNLOADER_MIDDLEWARES': {'scrapy.spidermiddlewares.UrlPreprocessMiddleware': 543},
        'ROBOTSTXT_OBEY': False,
        'COOKIES_ENABLED': False,
        'DEFAULT_REQUEST_HEADERS': {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'Accept-Language': 'en-US,en;q=0.9,ru;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br, zstd',
            'Referer': 'https://www.google.com/',
            'Sec-Ch-Ua': '"Not/A)Brand";v="8", "Chromium";v="126", "Google Chrome";v="126"',
            'Sec-Ch-Ua-Mobile': "?0",
            'Sec-Ch-Ua-Platform': "macOS",
            'Sec-Fetch-Dest': "document",
            'Sec-Fetch-Mode': "navigate",
            'Sec-Fetch-Site': "same-origin",
            'Sec-Fetch-User': "?1",
            'Upgrade-Insecure-Requests': "1",
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36',
        }
    }
)

process.crawl(IRSpider)
process.start() 