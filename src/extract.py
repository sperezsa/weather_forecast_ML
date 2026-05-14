import sqlite3
import pandas as pd
import os

def extract_from_db():
    # Conexión a tu base de datos
    conn = sqlite3.connect('data/weather.db')
    
    # Leemos la tabla (asumiendo que se llama 'clima')
    query = "SELECT * FROM clima"
    df = pd.read_sql_query(query, conn)
    
    # Guardamos en la carpeta data para que DVC lo vea
    os.makedirs('data', exist_ok=True)
    df.to_csv('data/raw_weather.csv', 
    index=False, encoding='utf-8-sig')
    
    conn.close()
    print(f"Extracción completada: {df.shape[0]} filas exportadas.")

if __name__ == "__main__":
    extract_from_db()