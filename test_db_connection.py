import pymysql
from dotenv import load_dotenv
import os

# Cargar las variables de entorno desde el archivo .env
load_dotenv()

# Obtener detalles de conexión desde variables de entorno
db_user = os.getenv('DB_USER')
db_password = os.getenv('DB_PASSWORD')
db_host = os.getenv('DB_HOST')
db_port = int(os.getenv('DB_PORT'))
db_name = os.getenv('DB_NAME')

# Intentar conectarse a la base de datos
try:
    connection = pymysql.connect(
        host=db_host,
        user=db_user,
        password=db_password,
        database=db_name,
        port=db_port
    )
    print("Conexión exitosa a la base de datos.")
    connection.close()
except Exception as e:
    print(f"Error al conectarse a la base de datos: {e}")
