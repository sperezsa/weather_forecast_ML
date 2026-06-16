# 1. Usamos una imagen oficial y ligera de Python que ya viene con 'uv' instalado
FROM ghcr.io/astral-sh/uv:python3.12-alpine

# 2. Establecemos el directorio de trabajo dentro del contenedor
WORKDIR /app

# 3. Copiamos solo los archivos de configuración primero (para aprovechar la caché de Docker)
COPY pyproject.toml uv.lock ./

# 4. AHORA copiamos todo el código fuente antes de intentar instalar
COPY src/ ./src
COPY data/ ./data

# 5. Instalamos las dependencias
RUN uv pip install --system .

# 6. Comando por defecto
CMD ["python", "src/train.py"]
