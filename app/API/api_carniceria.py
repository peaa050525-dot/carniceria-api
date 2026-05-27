from fastapi import FastAPI
import sqlite3
from pydantic import BaseModel
from typing import List

app = FastAPI(title="API Sistema Carnicería")

DB_NAME = "carniceria.db"

def get_db_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn

# --- RUTA PARA LOS CORTES (Lo que ya tienes) ---
@app.get("/cortes")
def obtener_cortes():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT tipo, corte, kilos, precio FROM inventario")
    productos = cursor.fetchall()
    conn.close()
    return [dict(row) for row in productos]

# --- NUEVO: ESTRUCTURA PARA PEDIDOS ---
class Pedido(BaseModel):
    cliente: str
    tipo: str
    corte: str
    kilos: float

@app.post("/pedidos")
def recibir_pedido(pedido: Pedido):
    """Recibe un pedido desde la app y lo guarda en la base de datos."""
    conn = get_db_connection()
    cursor = conn.cursor()
    # Usamos la tabla pedidos_online que ya tienes en tu sistema de ventas
    cursor.execute("""
        INSERT INTO pedidos_online (cliente, correo, tipo, corte, kilos, estado) 
        VALUES (?, ?, ?, ?, ?, 'Pendiente')
    """, (pedido.cliente, "sin_correo", pedido.tipo, pedido.corte, pedido.kilos))
    conn.commit()
    conn.close()
    return {"mensaje": "Pedido recibido"}

@app.get("/pedidos/nuevos")
def obtener_pedidos_nuevos():
    """Para que tu sistema de ventas de escritorio consulte si hay pedidos."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM pedidos_online WHERE estado = 'Pendiente'")
    pedidos = cursor.fetchall()
    conn.close()
    return [dict(row) for row in pedidos]