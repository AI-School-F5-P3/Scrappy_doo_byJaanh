import os
import logging

BOT_NAME = 'project_scrappy_doo'
SPIDER_MODULES = ['src.scraping']
NEWSPIDER_MODULE = 'src.scraping'
REQUEST_FINGERPRINTER_IMPLEMENTATION = "2.7"

ITEM_PIPELINES = {
    'src.pipelines.jsonwriter_pipeline.JsonWriterPipeline': 300,
}

LOG_LEVEL = 'INFO'

# Añadir middlewares necesarios
DOWNLOADER_MIDDLEWARES = {
    'scrapy.downloadermiddlewares.retry.RetryMiddleware': 543,
    'scrapy.downloadermiddlewares.httperror.HttpErrorMiddleware': 50,
}

# Configuración de logs
LOG_FILE = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'logs/scraping.log'))

logging.basicConfig(
    filename=LOG_FILE,
    filemode='a',
    format='%(asctime)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# Configuración de codificación
FEED_EXPORT_ENCODING = 'utf-8'

# Configuración de FEEDS
FEEDS = {
    'data/raw/authors.json': {
        'format': 'json',
        'encoding': 'utf-8',
        'indent': 4,
        'ensure_ascii': False,
        'overwrite': True,
    },
    'data/raw/quotes.json': {
        'format': 'json',
        'encoding': 'utf-8',
        'indent': 4,
        'ensure_ascii': False,
        'overwrite': True,
    },
}
