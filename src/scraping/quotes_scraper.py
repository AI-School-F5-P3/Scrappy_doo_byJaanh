import scrapy
import logging
from scrapy.exceptions import CloseSpider
from scrapy.spidermiddlewares.httperror import HttpError
from twisted.internet.error import DNSLookupError, TimeoutError, TCPTimedOutError
import os
import json

# Configurar logging
logging.basicConfig(
    filename=os.path.join(os.path.dirname(__file__), '..', 'logs', 'quotes_scraper.log'),
    filemode='a',
    format='%(asctime)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

class QuotesSpider(scrapy.Spider):
    name = "quotes"
    start_urls = ['http://quotes.toscrape.com']

    def parse(self, response):
        for quote in response.css('div.quote'):
            text = quote.css('span.text::text').get().strip()
            author = quote.css('small.author::text').get().strip()
            tags = quote.css('div.tags a.tag::text').getall()

            if text and author:
                quote_data = {
                    'text': text,
                    'author': author,
                    'tags': tags
                }

                logging.info(f"Quote data found: {quote_data}")
                yield quote_data

        next_page = response.css('li.next a::attr(href)').get()
        if next_page is not None:
            logging.info(f"Following next page: {next_page}")
            yield response.follow(next_page, self.parse, errback=self.errback)

    def errback(self, failure):
        logging.error(repr(failure))
        if failure.check(HttpError):
            response = failure.value.response
            logging.error('HttpError on %s', response.url)
        elif failure.check(DNSLookupError):
            request = failure.request
            logging.error('DNSLookupError on %s', request.url)
        elif failure.check(TimeoutError, TCPTimedOutError):
            request = failure.request
            logging.error('TimeoutError on %s', request.url)
