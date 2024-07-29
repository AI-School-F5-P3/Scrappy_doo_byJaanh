import schedule
import time
import logging
from run_spider import run_quotes_spider, run_authors_spider
import os

# Configurar logging
logging.basicConfig(
    filename=os.path.join(os.path.dirname(__file__), '..', 'logs', 'schedule.log'),
    filemode='a',
    format='%(asctime)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

def job():
    logging.info("Starting scheduled job...")
    run_quotes_spider()
    run_authors_spider()
    logging.info("Scheduled job finished.")

# Configurar la tarea para que se ejecute cada 12 horas
schedule.every(12).hours.do(job)

logging.info("Scheduler started, will run every 12 hours.")

while True:
    schedule.run_pending()
    time.sleep(1)
