## Dockerfile
FROM python:3.12.4-slim

WORKDIR /usr/src/app

# Copiar el archivo pyproject.toml y requirements.txt
COPY pyproject.toml .
COPY requirements.txt .

# Actualizar pip, setuptools y wheel a las últimas versiones antes de instalar las dependencias
RUN pip install --upgrade pip setuptools wheel

# Instalar las dependencias del proyecto
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el resto de los archivos del proyecto
COPY . .

# Definir el comando por defecto para ejecutar el scheduler
CMD ["python", "scripts/scheduler.py"]
