# 1. Usamos una imagen oficial y ligera de Python que ya viene con 'uv' instalado
FROM ghcr.io/astral-sh/uv:python3.11-alpine

# 2. Establecemos el directorio de trabajo dentro del contenedor
WORKDIR /app

# 3. Copiamos los archivos que definen las dependencias
COPY pyproject.toml uv.lock ./

# 4. Instalamos las dependencias del proyecto de forma global en el contenedor
# Usamos --system porque dentro de un contenedor Docker no necesitamos un entorno virtual (.venv)
RUN uv pip install --system . --verbose

# 5. Copiamos el resto de tu código fuente al contenedor
COPY src/ ./src
COPY data/ ./data

# 6. Definimos variables de entorno por defecto (Desarrollo por defecto)
# Airflow podrá sobrescribir esta variable en producción a "PRODUCTION"
ENV ENVIRONMENT="DEVELOPMENT"

# 7. El comando que se ejecutará cuando el contenedor se encienda
CMD ["python", "src/train.py"]