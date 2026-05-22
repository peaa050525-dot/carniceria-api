import sqlite3

class AbastecimientoModel:
    def __init__(self):
        self.db_path = "carniceria.db" # Asegúrate que coincida con tu archivo

    def obtener_historial_db(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        # Traemos los datos ordenados por la fecha más reciente primero
        cursor.execute("SELECT fecha, tipo, corte, kilos, proveedor FROM abastecimientos ORDER BY fecha DESC")
        datos = cursor.fetchall()
        conn.close()
        return datos