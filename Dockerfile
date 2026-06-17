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
# Copiamos la carpeta .dvc para que el contenedor sepa dónde ir a buscar los datos
COPY .dvc/ ./.dvc/
COPY .dvcignore .dvcignore
COPY .git/ ./.git/

# 7. PASO PENDIENTE DE VALIDAR 
# Instalamos DVC y descargamos los datos REALES desde el S3/Remoto
# Necesitarás pasar las credenciales como ARG si usas S3 privado
# RUN uv pip install --system dvc[s3]
RUN dvc pull /app/data/prepared/train_X.csv.dvc

# 8. Comando por defecto
CMD ["python", "src/train.py"]
