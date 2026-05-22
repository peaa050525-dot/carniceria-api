# app/models/caja_model.py
from app.models.database import get_connection
import os
from datetime import datetime

class CajaModel:
    def obtener_ventas_pendientes(self):
        """Obtiene solo las ventas que NO han sido cortadas."""
        conn = get_connection()
        cursor = conn.cursor()
        # Solo traemos las que dicen 'PENDIENTE'
        cursor.execute("SELECT cliente, tipo, corte, kilos, subtotal FROM ventas WHERE estado = 'PENDIENTE'")
        ventas = cursor.fetchall()
        conn.close()
        return ventas

    def registrar_corte_db(self, total_kg, total_dinero, texto_reporte):
        """Guarda el corte en la base de datos y marca las ventas como cortadas."""
        conn = get_connection()
        cursor = conn.cursor()
        try:
            # 1. Insertar en el historial de la DB
            cursor.execute("""
                INSERT INTO cortes_caja (total_kilos, total_dinero, detalles_txt)
                VALUES (?, ?, ?)
            """, (total_kg, total_dinero, texto_reporte))

            # 2. Marcar las ventas actuales como 'CORTADO'
            cursor.execute("UPDATE ventas SET estado = 'CORTADO' WHERE estado = 'PENDIENTE'")
            
            conn.commit()
            return True
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            conn.close()

    def obtener_historial_cortes(self):
        """Obtiene todos los cortes realizados anteriormente."""
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id, fecha, total_kilos, total_dinero FROM cortes_caja ORDER BY fecha DESC")
        historial = cursor.fetchall()
        conn.close()
        return historial

    def guardar_corte_txt(self, contenido_texto):
        """Genera el archivo físico .txt"""
        if not os.path.exists("historial_cortes"):
            os.makedirs("historial_cortes")
        
        fecha_str = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        nombre_archivo = f"historial_cortes/corte_{fecha_str}.txt"
        
        with open(nombre_archivo, "w", encoding="utf-8") as archivo:
            archivo.write(contenido_texto)
        return nombre_archivo
    
    def obtener_historial_completo(self):
        """Trae todos los registros de la tabla cortes_caja."""
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id, fecha, total_kilos, total_dinero, detalles_txt FROM cortes_caja ORDER BY fecha DESC")
        historial = cursor.fetchall()
        conn.close()
        return historial

    def eliminar_todo_el_historial(self):
        """Borra todos los registros de cortes de caja."""
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM cortes_caja")
        conn.commit()
        conn.close()