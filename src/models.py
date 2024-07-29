from sqlalchemy import create_engine, Column, Integer, String, Text
from sqlalchemy.orm import declarative_base, sessionmaker
from dotenv import load_dotenv
import logging
import os

# Configurar logging
logging.basicConfig(
    filename=os.path.join(os.path.dirname(__file__), '..', 'logs', 'models.log'),
    filemode='a',
    format='%(asctime)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# Cargar variables de entorno
load_dotenv(os.path.join(os.path.dirname(__file__), '..', '.env'))

Base = declarative_base()

class Quote(Base):
    __tablename__ = "quotes"
    id = Column(Integer, primary_key=True, index=True)
    text = Column(Text, nullable=False)
    author = Column(String(1000), nullable=False)
    tags = Column(String(1000), nullable=True)

class Author(Base):
    __tablename__ = "authors"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(1000), nullable=False)
    about = Column(Text, nullable=True)  # Aquí se utiliza Text para manejar descripciones largas

# Configurar la base de datos
try:
    db_config = {
        'user': os.getenv("DB_USER"),
        'password': os.getenv("DB_PASSWORD"),
        'host': os.getenv("DB_HOST"),
        'port': os.getenv("DB_PORT"),
        'dbname': os.getenv("DB_NAME")
    }

    DATABASE_URL = f"mysql+pymysql://{db_config['user']}:{db_config['password']}@{db_config['host']}:{db_config['port']}/{db_config['dbname']}"

    engine = create_engine(DATABASE_URL, echo=True)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

    # Crear las tablas en la base de datos
    logging.info("Creating tables in the database if they don't exist.")
    Base.metadata.create_all(bind=engine)
    logging.info("Tables created successfully.")
except Exception as e:
    logging.error(f"Error setting up database: {e}")
    raise
