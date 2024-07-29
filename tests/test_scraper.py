import os
import sys
import pytest
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import yaml
from scripts.run_spider import Base, Quote  

load_dotenv(os.path.join(os.path.dirname(__file__), '..', '.env'))

# Añadir la ruta src al path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

# Cargar la configuración de la base de datos
with open(os.path.join(os.path.dirname(__file__), '../config/config.yaml'), 'r') as file:
    config = yaml.safe_load(file)

db_config = config['database']
db_port = int(db_config.get('port', 3306))
DATABASE_URL = f"mysql+pymysql://{db_config['user']}:{db_config['password']}@{db_config['host']}:{db_port}/{db_config['dbname']}"

# Configurar SQLAlchemy
engine = create_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope='module')
def setup_database():
    # Crear las tablas
    Base.metadata.create_all(bind=engine)
    yield
    # Eliminar las tablas después de la prueba
    Base.metadata.drop_all(bind=engine)

def test_database_connection(setup_database):
    session = SessionLocal()
    result = session.execute(text("SELECT 1"))
    assert result.scalar() == 1
    session.close()

def test_insert_quote(setup_database):
    session = SessionLocal()
    new_quote = Quote(text="This is a test quote", author="Test Author", tags="test,pytest")
    session.add(new_quote)
    session.commit()

    # Verificar que la cita fue insertada
    inserted_quote = session.query(Quote).filter_by(author="Test Author").first()
    assert inserted_quote is not None
    assert inserted_quote.text == "This is a test quote"
    assert inserted_quote.author == "Test Author"
    assert inserted_quote.tags == "test,pytest"

    session.close()
