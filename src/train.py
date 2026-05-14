import pandas as pd
import joblib
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, r2_score
import os
import json
import yaml

def train_model():
    # 1. Cargar los datos preparados
    X_train = pd.read_csv('data/prepared/train_X.csv')
    y_train = pd.read_csv('data/prepared/train_y.csv').values.ravel() # Convertir a array 1D
    X_test = pd.read_csv('data/prepared/test_X.csv')
    y_test = pd.read_csv('data/prepared/test_y.csv').values.ravel()

    # 2. Configurar el modelo
    with open("params.yaml", "r") as f:
        params = yaml.safe_load(f)

    n_estimators = params["train"]["n_estimators"]
    max_depth    = params["train"]["max_depth"]

    print(f"Entrenando RandomForest con n_estimators={n_estimators}...")
    rf = RandomForestRegressor(
        n_estimators=n_estimators, 
        max_depth=max_depth, 
        random_state=42
    )

    # 3. Entrenar
    rf.fit(X_train, y_train)

    # 4. Evaluar (Métricas básicas)
    predictions = rf.predict(X_test)
    mae = mean_absolute_error(y_test, predictions)
    r2 = r2_score(y_test, predictions)
    
    print(f"Entrenamiento completado.")
    print(f"Error Medio Absoluto (MAE): {mae:.2f} grados")
    print(f"Puntuación R2: {r2:.2f}")

    # 5. Analizar importancia de las características
    importancia = pd.DataFrame({
        'feature': X_train.columns,
        'importance': rf.feature_importances_
    }).sort_values(by='importance', ascending=False)

    print("\nRanking de importancia de variables:")
    print(importancia)

    # Guardar importancia en un CSV para consultas futuras
    importancia.to_csv('reports/feature_importance.csv', index=False)

    # 6. Guardar el modelo y las métricas
    os.makedirs('models', exist_ok=True)
    os.makedirs('reports', exist_ok=True)
    
    # Guardamos el modelo
    joblib.dump(rf, 'models/weather_model.pkl')
    
    # Guardamos las métricas en un JSON para que DVC pueda compararlas
    metrics = {
        "mae": mae,
        "r2": r2
    }
    with open('reports/metrics.json', 'w') as f:
        json.dump(metrics, f, indent=4)

if __name__ == "__main__":
    train_model()