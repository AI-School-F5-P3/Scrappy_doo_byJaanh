import scrapy
import logging
from scrapy.exceptions import CloseSpider
from scrapy.spidermiddlewares.httperror import HttpError
from twisted.internet.error import DNSLookupError, TimeoutError, TCPTimedOutError
import os

# Configurar logging
logging.basicConfig(
    filename=os.path.join(os.path.dirname(__file__), '..', 'logs', 'authors_scraper.log'),
    filemode='a',
    format='%(asctime)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

class AuthorsSpider(scrapy.Spider):
    name = "authors"
    start_urls = ['http://quotes.toscrape.com']

    def parse(self, response):
        author_links = response.css('div.quote span a::attr(href)').getall()
        logging.info(f"Found {len(author_links)} author links")
        for link in author_links:
            yield response.follow(link, self.parse_author, errback=self.errback)

        next_page = response.css('li.next a::attr(href)').get()
        if next_page is not None:
            logging.info(f"Following next page: {next_page}")
            yield response.follow(next_page, self.parse, errback=self.errback)

    def parse_author(self, response):
        name = response.css('h3.author-title::text').get().strip()
        about = response.css('div.author-description::text').get().strip()

        if name and about:
            author_data = {
                "name": name,
                "about": about
            }

            logging.info(f"Author data found: {author_data}")
            yield author_data

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
