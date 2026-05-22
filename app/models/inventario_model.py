from app.models.database import get_connection

class InventarioModel:
    def obtener_inventario_db(self):
        """Obtiene todo el inventario actual para mostrarlo en la tabla."""
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT tipo, corte, kilos, precio FROM inventario")
        datos = cursor.fetchall()
        conn.close()
        return datos

    def obtener_tipos_carne(self):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT DISTINCT tipo FROM inventario")
        tipos = [row[0] for row in cursor.fetchall()]
        conn.close()
        return tipos

    def obtener_cortes_por_tipo(self, tipo):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT corte FROM inventario WHERE tipo = ?", (tipo,))
        cortes = [row[0] for row in cursor.fetchall()]
        conn.close()
        return cortes

    def obtener_proveedores(self):
        """Trae los proveedores. Ahora tipo_carne puede ser 'Res, Cerdo'."""
        conn = get_connection()
        cursor = conn.cursor()
        # Traemos nombre y la cadena de texto de los tipos que maneja
        cursor.execute("SELECT nombre, tipo_carne FROM proveedores")
        proveedores = cursor.fetchall()
        conn.close()
        return proveedores

    def registrar_abastecimiento(self, tipo, corte, kilos, proveedor):
        """Aumenta el stock y guarda el registro en el historial."""
        conn = get_connection()
        cursor = conn.cursor()

        try:
            # 1. Actualizar el stock
            cursor.execute("""
                UPDATE inventario
                SET kilos = kilos + ?
                WHERE tipo = ? AND corte = ?
            """, (kilos, tipo, corte))

            # 2. Guardar en el historial
            cursor.execute("""
                INSERT INTO abastecimientos (tipo, corte, kilos, proveedor)
                VALUES (?, ?, ?, ?)
            """, (tipo, corte, kilos, proveedor))

            conn.commit()
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            conn.close()