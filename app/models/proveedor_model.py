from app.models.database import get_connection

class ProveedorModel:
    def obtener_proveedores(self):
        """Consulta todos los proveedores para mostrarlos en la tabla."""
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT nombre, telefono, tipo_carne FROM proveedores")
        proveedores = cursor.fetchall()
        conn.close()
        return proveedores

    def obtener_tipos_carne(self):
        """Obtiene los tipos de carne disponibles directamente del inventario."""
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT DISTINCT tipo FROM inventario")
        tipos = [row[0] for row in cursor.fetchall()]
        conn.close()
        return tipos

    def registrar_proveedor(self, nombre, telefono, lista_tipos):
        """
        Inserta un nuevo proveedor. 
        Recibe una lista ['Res', 'Cerdo'] y la guarda como 'Res, Cerdo'.
        """
        # Convertimos la lista de la interfaz a un solo texto para la DB
        tipos_texto = ", ".join(lista_tipos) if isinstance(lista_tipos, list) else lista_tipos
        
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("""
                INSERT INTO proveedores (nombre, telefono, tipo_carne)
                VALUES (?, ?, ?)
            """, (nombre, telefono, tipos_texto))
            conn.commit()
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            conn.close()

    def eliminar_proveedor(self, nombre):
        """Elimina un proveedor de la base de datos usando su nombre."""
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("DELETE FROM proveedores WHERE nombre = ?", (nombre,))
            conn.commit()
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            conn.close()