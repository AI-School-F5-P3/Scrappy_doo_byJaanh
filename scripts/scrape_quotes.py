import os
import sys
from scrapy.crawler import CrawlerProcess
import logging

# Configurar logging
logging.basicConfig(
    filename=os.path.join(os.path.dirname(__file__), '..', 'logs', 'scrape_quotes.log'),
    filemode='a',
    format='%(asctime)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# Añadir la ruta src al path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

try:
    from scraping.quotes_scraper import QuotesSpider
    from scraping.authors_scraper import AuthorsSpider
except ModuleNotFoundError as e:
    logging.error(f"Error importing scrapers: {e}")
    sys.exit(1)

def run_quotes_spider():
    try:
        process = CrawlerProcess(settings={
            "FEEDS": {
                os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'data/raw/quotes.json')): {"format": "json", "overwrite": True},
            },
            "LOG_FILE": os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'logs/quotes_scraper.log')),
        })
        process.crawl(QuotesSpider)
        process.start()
        logging.info("Quotes spider finished successfully.")
    except Exception as e:
        logging.error(f"Error running quotes spider: {e}")

def run_authors_spider():
    try:
        process = CrawlerProcess(settings={
            "FEEDS": {
                os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'data/raw/authors.json')): {"format": "json", "overwrite": True},
            },
            "LOG_FILE": os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'logs/authors_scraper.log')),
        })
        process.crawl(AuthorsSpider)
        process.start()
        logging.info("Authors spider finished successfully.")
    except Exception as e:
        logging.error(f"Error running authors spider: {e}")

def run_spiders():
    run_quotes_spider()
    run_authors_spider()

if __name__ == "__main__":
    run_spiders()
