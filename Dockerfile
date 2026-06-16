# 1. Usamos una imagen oficial y ligera de Python que ya viene con 'uv' instalado
#FROM ghcr.io/astral-sh/uv:python3.12-alpine
FROM python:3.12-slim

# 2. Instalamos 'uv' de la forma oficial
COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/uv

# 3. Establecemos el directorio de trabajo dentro del contenedor
WORKDIR /app

# 4. Copiamos solo los archivos de configuración primero (para aprovechar la caché de Docker)
COPY pyproject.toml uv.lock ./

# 5. Instalamos las dependencias
# 'slim' ya incluye los binarios necesarios, así que 'uv' descargará 
# las versiones pre-compiladas (wheels) y no intentará compilarlas.
RUN uv pip install --system .


# 6. Copiamos todo el código fuente antes de intentar instalar
COPY src/ ./src
COPY data/ ./data

# 7. Comando por defecto
CMD ["python", "src/train.py"]
