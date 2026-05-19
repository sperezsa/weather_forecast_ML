# 🌤️ Weather Forecast ML

Proyecto de Machine Learning para predecir temperaturas máximas utilizando **Python**, **DVC** para el control de versiones de datos y **Scikit-Learn**.

## 🚀 Estructura del Pipeline
El proyecto utiliza DVC para gestionar las etapas de datos:
1. **Extract**: Obtiene datos de `weather.db` y genera `raw_weather.csv`.
2. **Prepare**: Limpia textos, realiza One-Hot Encoding y genera sets de train/test.
3. **Train**: Entrena un `RandomForestRegressor` y genera métricas.

## 📊 Resultados Actuales
- **R² Score**: 0.95
- **MAE**: 1.68 °C

## 🛠️ Instalación, Configuración y Ejecución

Este proyecto utiliza **DVC (Data Version Control)** combinado con **Google Cloud Storage (GCS)** para gestionar el ciclo de vida de los datos y los modelos de Machine Learning de forma eficiente y colaborativa. 

La base de datos original (`weather.db`), los datasets intermedios y los modelos entrenados están almacenados de forma segura en la nube en un bucket, por lo que **no se suben a GitHub** ni se incluyen en el clonado inicial.

### 🚀 Guía de Inicio Rápido para Consulta

Si estás clonando el proyecto, sigue estos pasos para sincronizar tu entorno:

1. **Clona el repositorio e instala las dependencias:**
Utilizamos `uv` como gestor de entornos y paquetes para asegurar que todos usemos exactamente las mismas librerías.

   ```bash
   mkdir C:\weather_forecast_ML
   cd weather_forecast_ML
   git clone https://github.com/sperezsa/weather_forecast_ML.git .
   uv sync
   ```

2. **Clave privada para acceso al bucket**
Al hacer privado el acceso al bucket, el paso adicional a ejecutar sería disponer de la clave privada para acceder al mismo.
Coloca la clave en el proyecto y ejecuta este comando para actualizar el fichero local donde se indica dónde se encuentra la clave:

   ```bash
   uv run dvc remote modify storage-privado credentialpath ruta/fichero/clave.json --local
   ```

3. **Descarga los artefactos del Pipeline (Datos preparados y Modelos):**
El almacenamiento de Google Cloud está configurado con acceso privado, se requiere ejecutar el paso anterior para configurar claves de GCP para bajarte el modelo actual y los datos procesados:

   ```bash
   uv run dvc pull
   ```

4. **Descarga la Base de Datos original:**
Para poder ejecutar o reproducir el pipeline completo desde cero, necesitas traerte explícitamente el archivo de la base de datos meteorológica ejecutando:

   ```bash
   uv run dvc pull data/weather.db.dvc
   ```

4. **Verifica y ejecuta el Pipeline:**
Una vez descargado todo, puedes comprobar el estado del proyecto o lanzar el entrenamiento completo de Machine Learning con:

   ```bash
   # Debería indicar que todo está al día (Up to date)
   uv run dvc status

   # Ejecuta el pipeline respetando la caché de DVC
   uv run dvc repro
   ```

🛠️ ¿Quieres experimentar y guardar cambios en la nube?
El acceso por defecto vía dvc pull es público y de solo lectura, por lo que no podrás realizar cambios en el dataset original o registrar un nuevo modelo oficial en la nube (dvc push).
