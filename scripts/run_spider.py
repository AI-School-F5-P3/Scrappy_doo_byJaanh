import os
import sys
import logging
from scrapy.crawler import CrawlerProcess
from sqlalchemy import create_engine, Column, Integer, String, Text
from sqlalchemy.orm import declarative_base, sessionmaker
from dotenv import load_dotenv
import yaml
import json

# Configurar logging
logging.basicConfig(
    filename=os.path.join(os.path.dirname(__file__), '..', 'logs', 'run_spider.log'),
    filemode='a',
    format='%(asctime)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# Cargar variables de entorno
load_dotenv(os.path.join(os.path.dirname(__file__), '..', '.env'))

# Añadir la ruta src al path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

try:
    from scraping.quotes_scraper import QuotesSpider
    from scraping.authors_scraper import AuthorsSpider
    from models import Quote, Author, SessionLocal
except ModuleNotFoundError as e:
    logging.error(f"Error importing modules: {e}")
    sys.exit(1)

# Determinar si estamos en un entorno Docker
IS_DOCKER = os.getenv('IS_DOCKER', 'False').lower() in ('true', '1', 't')

# Cargar la configuración de la base de datos
try:
    with open(os.path.join(os.path.dirname(__file__), '../config/config.yaml'), 'r') as file:
        config = yaml.safe_load(file)
    db_config = config['database']

    # Si estamos en Docker, usamos 'db' como host
    db_host = 'db' if IS_DOCKER else db_config['host']

    # Asegurarse de que el puerto es un número entero
    db_port = int(db_config.get('port', 3306))
    DATABASE_URL = f"mysql+pymysql://{db_config['user']}:{db_config['password']}@{db_host}:{db_port}/{db_config['dbname']}"
except Exception as e:
    logging.error(f"Error loading database configuration: {e}")
    sys.exit(1)

# Configurar SQLAlchemy
engine = create_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Crear las tablas en la base de datos
logging.info("Creating tables in the database if they don't exist.")
Base.metadata.create_all(bind=engine)

def save_to_json(items, filename):
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(items, f, ensure_ascii=False, indent=2)
        logging.info(f"Data successfully saved to {filename}")
    except Exception as e:
        logging.error(f"Error saving data to {filename}: {e}")

# Función para guardar datos en la base de datos
def save_to_db(items, model):
    logging.info(f"Saving {model.__tablename__} to database.")
    session = SessionLocal()
    try:
        for item in items:
            logging.info(f"Saving {model.__tablename__}: {item}")
            db_item = model(**item)
            session.add(db_item)
        session.commit()
        logging.info(f"{model.__tablename__} saved successfully.")
    except Exception as e:
        logging.error(f"Error saving {model.__tablename__} to database: {e}")
    finally:
        session.close()

# Clase personalizada de QuotesSpider para guardar en la base de datos
class CustomQuotesSpider(QuotesSpider):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.quotes = []

    def parse(self, response):
        for quote in super().parse(response):
            self.quotes.append(quote)
            yield quote

    def closed(self, reason):
        super().closed(reason)
        logging.info("QuotesSpider closed, starting to save quotes.")
        if self.quotes:
            filename = os.path.join(os.path.dirname(__file__), '..', 'data/raw/quotes.json')
            save_to_json(self.quotes, filename)
            save_to_db(self.quotes, Quote)

class CustomAuthorsSpider(AuthorsSpider):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.authors = []

    def parse_author(self, response):
        author_data = super().parse_author(response)
        self.authors.append(author_data)
        return author_data

    def closed(self, reason):
        super().closed(reason)
        logging.info("AuthorsSpider closed, starting to save authors.")
        if self.authors:
            filename = os.path.join(os.path.dirname(__file__), '..', 'data/raw/authors.json')
            save_to_json(self.authors, filename)
            save_to_db(self.authors, Author)

def run_spiders():
    logging.info("Starting spiders...")
    process = CrawlerProcess(settings={
        "FEEDS": {
            os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'data/raw/quotes.json')): {"format": "json", "overwrite": True},
            os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'data/raw/authors.json')): {"format": "json", "overwrite": True},
        },
        "LOG_FILE": os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'logs/scraping.log')),
    })
    logging.info("Crawler process initialized...")
    process.crawl(CustomQuotesSpider)
    process.crawl(CustomAuthorsSpider)
    logging.info("Crawling started...")
    process.start()
    logging.info("Crawling finished.")

if __name__ == "__main__":
    os.environ['SCRAPY_SETTINGS_MODULE'] = 'src.settings'
    run_spiders()