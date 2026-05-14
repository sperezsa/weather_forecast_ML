import pandas as pd
from sklearn.model_selection import train_test_split
import os
import unicodedata

def normalize_text(text):
    """
    Elimina acentos, eñes y caracteres especiales, convirtiendo a minúsculas.
    """
    if not isinstance(text, str):
        return text
    # Normalizar para separar caracteres base de sus acentos
    text = unicodedata.normalize('NFD', text)
    # Filtrar solo los caracteres que no sean marcas de acentuación
    text = "".join([c for c in text if unicodedata.category(c) != 'Mn'])
    # Convertir a minúsculas y quitar espacios extra
    return text.lower().replace("ñ", "n").strip()

def prepare_data():
    # 1. Cargar datos (usando utf-8-sig por seguridad para visualizar los acentos y eñes correctamente)
    if not os.path.exists('data/raw_weather.csv'):
        print("Error: No se encuentra data/raw_weather.csv")
        return

    df = pd.read_csv('data/raw_weather.csv', encoding='utf-8-sig')
    
    # 2. Normalización de texto
    # Limpiar nombres de columnas (ej: 'precipitación_mm' -> 'precipitacion_mm')
    df.columns = [normalize_text(col) for col in df.columns]
    
    # Limpiar contenido de columnas tipo texto (ciudad, estado, etc.)
    text_cols = df.select_dtypes(include=['object', 'string']).columns
    for col in text_cols:
        df[col] = df[col].apply(normalize_text)

    # 3. Feature Engineering
    # Convertir fecha a datetime y extraer mes
    df['fecha'] = pd.to_datetime(df['fecha'])
    df['mes'] = df['fecha'].dt.month
    
    # Convertir la ciudad a columnas numéricas (One-Hot Encoding)
    df = pd.get_dummies(df, columns=['ciudad'])
    
    # 4. Definir Objetivo y Características
    # Ajusta esta lista según las columnas reales que quieres ignorar
    cols_to_drop = ['temp_max_c', 'fecha', 'estado', 'amanecer', 'atardecer', 'fecha_carga', 'dia_semana', 'uv_index_max', 'nivel_uv']
    # Solo borramos si existen (para evitar errores si cambiaste nombres)
    cols_to_drop = [c for c in cols_to_drop if c in df.columns]
    
    X = df.drop(cols_to_drop, axis=1)
    y = df['temp_max_c']
    
    # 5. Dividir en entrenamiento y test
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # 6. Guardar los sets procesados
    os.makedirs('data/prepared', exist_ok=True)
    # Usamos utf-8-sig para que los CSVs intermedios sean legibles en Windows
    X_train.to_csv('data/prepared/train_X.csv', index=False, encoding='utf-8-sig')
    X_test.to_csv('data/prepared/test_X.csv', index=False, encoding='utf-8-sig')
    y_train.to_csv('data/prepared/train_y.csv', index=False, encoding='utf-8-sig')
    y_test.to_csv('data/prepared/test_y.csv', index=False, encoding='utf-8-sig')
    
    print(f"Preparación completada. Columnas finales: {list(X.columns)}")

if __name__ == "__main__":
    prepare_data()