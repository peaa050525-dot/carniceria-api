from app.models.database import get_connection
import matplotlib.pyplot as plt
from app.models.database import get_connection

class VentaModel:
    def __init__(self):
        # Aquí guardaremos temporalmente los productos antes de cobrar
        self.venta_actual = []
        self.cliente_actual = ""
        self.total_ticket = 0.0
        


    def generar_grafica_pastel_semanal(self):
        """Genera una gráfica de pastel de los cortes vendidos en la semana actual."""
        conn = get_connection()
        cursor = conn.cursor()

        query = """
            SELECT corte, SUM(kilos) as total_kg 
            FROM ventas 
            WHERE strftime('%W', fecha) = strftime('%W', 'now')
            AND strftime('%Y', fecha) = strftime('%Y', 'now')
            GROUP BY corte 
            ORDER BY total_kg DESC
        """
        
        cursor.execute(query)
        datos = cursor.fetchall()
        conn.close()

        if not datos:
            print("No hay ventas registradas en esta semana.")
            return

        cortes = [fila[0] for fila in datos]
        kilos = [fila[1] for fila in datos]
        
        plt.figure(figsize=(10, 7))
        
        # Paleta de colores 
        colores = ['#B71C1C', '#D32F2F', '#F44336', '#EF5350', '#E57373', '#FFCDD2']

        # Ajustamos autopct para que no se amontone si hay cortes pequeños
        plt.pie(
            kilos, 
            labels=cortes, 
            autopct='%1.1f%%', 
            startangle=140, 
            colors=colores,
            pctdistance=0.85, # Mueve los porcentajes un poco hacia afuera
            explode=[0.05] * len(cortes) # Separa un poquito cada rebanada
        )

      
        plt.title("Distribución de Ventas Semanales (kg)", fontsize=16, fontweight='bold', pad=25)
        
        plt.axis('equal') 
        plt.tight_layout()
        plt.show()

    def obtener_tipos_carne(self):
        """Consulta la base de datos para obtener los tipos de carne disponibles."""
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT DISTINCT tipo FROM inventario")
        tipos = [row[0] for row in cursor.fetchall()]
        conn.close()
        return tipos

    def obtener_cortes_por_tipo(self, tipo):
        """Obtiene los cortes y precios basados en el tipo de carne."""
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT corte, precio, kilos FROM inventario WHERE tipo = ?", (tipo,))
        cortes = cursor.fetchall()
        conn.close()
        return cortes

    def guardar_venta_final(self):
        """Guarda la venta en la DB y descuenta del inventario."""
        if not self.venta_actual:
            raise Exception("No hay productos en el ticket")

        conn = get_connection()
        cursor = conn.cursor()

        try:
            for v in self.venta_actual:
                tipo, corte, kilos, precio, subtotal = v

                # Descontar inventario
                cursor.execute("""
                    UPDATE inventario
                    SET kilos = kilos - ?
                    WHERE tipo = ? AND corte = ?
                """, (kilos, tipo, corte))

                # Registrar venta
                cursor.execute("""
                    INSERT INTO ventas (cliente, tipo, corte, kilos, precio, subtotal)
                    VALUES (?, ?, ?, ?, ?, ?)
                """, (self.cliente_actual, tipo, corte, kilos, precio, subtotal))

            conn.commit()
            self.limpiar_venta_actual()
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            conn.close()

    def limpiar_venta_actual(self):
        self.venta_actual.clear()
        self.cliente_actual = ""
        self.total_ticket = 0.0