## 1. Usamos una imagen oficial y ligera de Python que ya viene con 'uv' instalado
FROM python:3.12-slim

# Instalamos git, ya que DVC lo requiere para identificar el root del repo
RUN apt-get update && apt-get install -y git && rm -rf /var/lib/apt/lists/*

# Instalamos uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/uv

WORKDIR /app

COPY data/weather.db.dvc ./data/weather.db.dvc

# Copiamos los archivos de configuración y la definición del pipeline
COPY src/ ./src/
COPY dvc.yaml dvc.lock ./
COPY pyproject.toml uv.lock ./
COPY .dvc/ ./.dvc/
COPY .git/ ./.git/
COPY params.yaml ./

# Instalamos las dependencias del proyecto y DVC con todos sus drivers
RUN uv pip install --system . "dvc[all]"

RUN mkdir -p reports data/prepared models

# VARIABLES DE ENTORNO PARA ACCESO PÚBLICO A GCS
# GCS_READ_ONLY=true y el resto deshabilitan la búsqueda de credenciales
ENV GCS_ANONYMOUS=true
ENV GOOGLE_APPLICATION_CREDENTIALS=""


# 1. Recuperamos únicamente la BBDD base desde el almacenamiento remoto
#RUN dvc pull /app/data/weather.db.dvc
RUN dvc pull -r storage-publico data/weather.db.dvc

# 2. Ejecutamos el pipeline completo de DVC (extract -> prepare -> train)
# DVC leerá dvc.yaml y ejecutará los pasos en orden
#RUN dvc checkout 
#RUN dvc repro

# Comando final que mantiene el contenedor activo o realiza una acción adicional
#CMD ["python", "src/train.py"]
#CMD ["dvc", "repro", "--force"]
CMD ["dvc", "repro", "--downstream", "extract"]
#CMD ["sh", "-c", "dvc checkout && dvc repro"]
