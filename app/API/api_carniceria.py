from fastapi import FastAPI
import sqlite3

app = FastAPI(title="API Sistema Carnicería")

DB_NAME = "carniceria.db"

def get_db_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row  # Esto permite acceder por nombre de columna
    return conn

@app.get("/cortes")
def obtener_cortes():
    """Devuelve la lista de todos los cortes con sus kilos y precios."""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT tipo, corte, kilos, precio FROM inventario")
    productos = cursor.fetchall()
    conn.close()
    
    # Convertimos los resultados a una lista de diccionarios (JSON)
    return [dict(row) for row in productos]

@app.get("/cortes/{tipo}")
def obtener_cortes_por_tipo(tipo: str):
    """Filtra cortes por tipo (Res, Pollo, Cerdo)."""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT corte, kilos, precio FROM inventario WHERE tipo = ?", (tipo.capitalize(),))
    productos = cursor.fetchall()
    conn.close()
    
    return [dict(row) for row in productos]