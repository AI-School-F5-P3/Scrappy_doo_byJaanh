import os
import yaml
from sqlalchemy import create_engine, Column, Integer, String, Text
from sqlalchemy.orm import sessionmaker, declarative_base

# Cargar la configuración de la base de datos desde el archivo config.yaml
config_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'config/config.yaml'))
with open(config_path, 'r') as file:
    config = yaml.safe_load(file)

db_config = config['database']

# Obtener los valores de las variables de entorno, si están definidas
db_user = os.getenv('DB_USER', db_config['user'])
db_password = os.getenv('DB_PASSWORD', db_config['password'])
db_host = os.getenv('DB_HOST', db_config['host'])
db_port = os.getenv('DB_PORT', db_config['port'])
db_name = os.getenv('DB_NAME', db_config['dbname'])

# Construir la URL de la base de datos
DATABASE_URL = f"mysql+pymysql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"

# Configurar SQLAlchemy
engine = create_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Definir el modelo
class Quote(Base):
    __tablename__ = "quotes"

    id = Column(Integer, primary_key=True, index=True)
    text = Column(Text, nullable=False)
    author = Column(String(255), nullable=False)
    tags = Column(String(255), nullable=True)

# Crear las tablas en la base de datos
Base.metadata.create_all(bind=engine)

