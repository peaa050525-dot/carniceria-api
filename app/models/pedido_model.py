from app.models.database import get_connection
import random
import string

class PedidoModel:
    def generar_codigo(self):
        return ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))

    def registrar_pedido_db(self, cliente, correo, tipo, corte, kilos):
        codigo = self.generar_codigo()
        conn = get_connection()
        cursor = conn.cursor()
        # Usamos los nombres exactos de tu tabla: pedidos_online
        cursor.execute("""
            INSERT INTO pedidos_online (cliente, correo, tipo, corte, kilos, codigo_verificacion, estado)
            VALUES (?, ?, ?, ?, ?, ?, 'Pendiente')
        """, (cliente, correo, tipo, corte, kilos, codigo))
        pedido_id = cursor.lastrowid
        conn.commit()
        conn.close()
        return pedido_id, codigo

    def obtener_pedidos(self):
        conn = get_connection()
        cursor = conn.cursor()
        # Seleccionamos las columnas que definiste
        cursor.execute("SELECT id, cliente, correo, tipo, corte, kilos, estado FROM pedidos_online")
        datos = cursor.fetchall()
        conn.close()
        return datos

    def verificar_codigo_db(self, pedido_id, codigo_usuario):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT codigo_verificacion FROM pedidos_online WHERE id = ?", (pedido_id,))
        resultado = cursor.fetchone()
        
        if resultado and resultado[0] == codigo_usuario:
            cursor.execute("UPDATE pedidos_online SET estado = 'Verificado' WHERE id = ?", (pedido_id,))
            conn.commit()
            conn.close()
            return True
        conn.close()
        return False