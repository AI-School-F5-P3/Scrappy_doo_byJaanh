# Actualiza la base de datos con los datos procesados.
from sqlalchemy import create_engine
import pandas as pd

class DatabaseUpdater:
    def __init__(self, input_file, db_url):
        self.input_file = input_file
        self.db_url = db_url

    def update_database(self):
        # Leer los datos limpios desde un archivo JSON
        data = pd.read_json(self.input_file, lines=True)

        # Crear una conexión a la base de datos
        engine = create_engine(self.db_url)

        # Guardar los datos en la base de datos
        data.to_sql('quotes', engine, if_exists='replace', index=False)

if __name__ == "__main__":
    input_file = 'data/processed/cleaned_quotes.json'
    db_url = 'sqlite:///data/quotes.db'
    updater = DatabaseUpdater(input_file, db_url)
    updater.update_database()
