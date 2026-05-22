from app.models.database import get_connection
import sqlite3

class BusquedaModel:
    def buscar_en_todo(self, termino):
        conn = get_connection()
        # Usamos sqlite3.Row para acceder a los datos por nombre de columna
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        t = f"%{termino}%"

        # 1. BUSCAR EN INVENTARIO
        # Busca por tipo (Res/Pollo) o por nombre del corte
        cursor.execute("""
            SELECT tipo, corte, kilos, precio 
            FROM inventario 
            WHERE tipo LIKE ? OR corte LIKE ?
        """, (t, t))
        inventario = cursor.fetchall()

        # 2. BUSCAR EN PROVEEDORES
        # Aquí atacamos tu columna 'tipo_carne' para que si buscas "Res", 
        # aparezcan los proveedores que la surten.
        cursor.execute("""
            SELECT nombre, telefono, tipo_carne 
            FROM proveedores 
            WHERE nombre LIKE ? OR tipo_carne LIKE ?
        """, (t, t))
        proveedores = cursor.fetchall()

        # 3. BUSCAR CLIENTES Y FRECUENCIA (Desde la tabla ventas)
        # Agrupamos por el nombre del cliente para contar sus visitas
        cursor.execute("""
            SELECT cliente, COUNT(*) as total_compras, SUM(subtotal) as inversion_total
            FROM ventas 
            WHERE cliente LIKE ? 
            GROUP BY cliente
            ORDER BY total_compras DESC
        """, (t,))
        clientes = cursor.fetchall()

        conn.close()
        return {
            "inventario": inventario,
            "proveedores": proveedores,
            "clientes": clientes
        }