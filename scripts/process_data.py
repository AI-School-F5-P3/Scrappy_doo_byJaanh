import pandas as pd
import os
import logging
import json

# Configurar logging
logging.basicConfig(
    filename=os.path.join(os.path.dirname(__file__), '..', 'logs', 'process_data.log'),
    filemode='a',
    format='%(asctime)s - %(levellevelname)s - %(message)s',
    level=logging.INFO
)

class DataProcessor:
    def __init__(self, quotes_input_file, quotes_output_file, authors_input_file, authors_output_file):
        self.quotes_input_file = quotes_input_file
        self.quotes_output_file = quotes_output_file
        self.authors_input_file = authors_input_file
        self.authors_output_file = authors_output_file

    def validate_json(self, file_path):
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                json.load(f)
            return True
        except json.JSONDecodeError as e:
            logging.error(f"Invalid JSON in {file_path}: {e}")
            return False

    def clean_quotes_data(self):
        try:
            data = pd.read_json(self.quotes_input_file, lines=True)
            data = data.dropna()
            data.to_json(self.quotes_output_file, orient='records', lines=True)
            logging.info(f"Quotes data cleaned and saved to {self.quotes_output_file}")
        except Exception as e:
            logging.error(f"Error processing quotes data: {e}")

    def clean_authors_data(self):
        try:
            data = pd.read_json(self.authors_input_file, lines=True)
            data = data.dropna()
            data.to_json(self.authors_output_file, orient='records', lines=True)
            logging.info(f"Authors data cleaned and saved to {self.authors_output_file}")
        except Exception as e:
            logging.error(f"Error processing authors data: {e}")

    def process_data(self):
        if self.validate_json(self.quotes_input_file):
            self.clean_quotes_data()
        else:
            logging.error("Skipping quotes data processing due to invalid JSON")

        if self.validate_json(self.authors_input_file):
            self.clean_authors_data()
        else:
            logging.error("Skipping authors data processing due to invalid JSON")

if __name__ == "__main__":
    quotes_input_file = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'data/raw/quotes.json'))
    quotes_output_file = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'data/processed/cleaned_quotes.json'))
    authors_input_file = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'data/raw/authors.json'))
    authors_output_file = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'data/processed/cleaned_authors.json'))
    
    processor = DataProcessor(quotes_input_file, quotes_output_file, authors_input_file, authors_output_file)
    processor.process_data()
