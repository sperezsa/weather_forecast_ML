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

## 🛠️ Instalación y Ejecución

1. Clonar el repo y preparar entorno:
```bash
git clone https://github.com/sperezsa/weather_forecast_ML.git
cd weather_forecast_ML
uv sync
```

2. Reproducir el pipeline

Si tienes acceso a los datos originales o al remoto de DVC:

```bash
uv run dvc repro
```

3. Ver métricas

```bash
uv run dvc metrics show
```