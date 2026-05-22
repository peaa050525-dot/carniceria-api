import os
import json
import random
from datetime import datetime
from app.models.pedido_model import Pedido
from app.services.email_service import enviar_codigo

# ESTA ES LA PARTE CLAVE:
# Detectamos dónde está este archivo y construimos la ruta hacia la carpeta data
DIR_DEL_SERVICIO = os.path.dirname(os.path.abspath(__file__))
# Subimos dos niveles (fuera de services, fuera de app) para llegar a carniceria_mvc
RAIZ_PROYECTO = os.path.abspath(os.path.join(DIR_DEL_SERVICIO, "..", ".."))
RUTA = os.path.join(RAIZ_PROYECTO, "data", "pedidos.json")

class PedidoService:

    @staticmethod
    def cargar():
        # Crear la carpeta data si no existe
        folder = os.path.dirname(RUTA)
        if not os.path.exists(folder):
            os.makedirs(folder)

        if not os.path.exists(RUTA):
            with open(RUTA, "w") as f:
                json.dump([], f)
        
        with open(RUTA, "r") as f:
            try:
                return json.load(f)
            except:
                return []

    @staticmethod
    def guardar(pedidos):
        with open(RUTA, "w") as f:
            json.dump(pedidos, f, indent=4)

    @staticmethod
    def generar_codigo():
        return str(random.randint(100000, 999999))

    @staticmethod
    def crear(cliente, correo, tipo, corte, kilos):
        pedidos = PedidoService.cargar()
        nuevo_id = len(pedidos) + 1
        codigo = PedidoService.generar_codigo()

        pedido = Pedido(
            id=nuevo_id,
            cliente=cliente,
            correo=correo,
            tipo=tipo,
            corte=corte,
            kilos=float(kilos),
            codigo_verificacion=codigo,
            fecha=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        )

        if enviar_codigo(correo, codigo):
            pedidos.append(pedido.to_dict())
            PedidoService.guardar(pedidos)
            return True, "Pedido creado y código enviado"
        else:
            return False, "No se pudo enviar el correo"

    @staticmethod
    def verificar(pedido_id, codigo_ingresado):
        pedidos = PedidoService.cargar()

        for pedido in pedidos:
            if pedido["id"] == pedido_id:
                if pedido["estado"] != "PENDIENTE_VERIFICACION":
                    return False, "El pedido no está pendiente"

                pedido["intentos"] = pedido.get("intentos", 0) + 1

                if codigo_ingresado == pedido["codigo_verificacion"]:
                    pedido["estado"] = "CONFIRMADO"
                    pedido["codigo_verificacion"] = None
                    pedido["intentos"] = 0
                    PedidoService.guardar(pedidos)
                    return True, "Pedido confirmado"
                else:
                    if pedido["intentos"] >= 3:
                        pedido["estado"] = "CANCELADO"
                        pedido["codigo_verificacion"] = None
                        PedidoService.guardar(pedidos)
                        return False, "Pedido cancelado por intentos"
                    else:
                        PedidoService.guardar(pedidos)
                        return False, f"Intento {pedido['intentos']} de 3"
        return False, "Pedido no encontrado"

    @staticmethod
    def reenviar(pedido_id):
        pedidos = PedidoService.cargar()

        for pedido in pedidos:
            if pedido["id"] == pedido_id:
                if pedido.get("reenvios", 0) >= 3:
                    return False, "Máximo de 3 reenvíos alcanzado"

                nuevo_codigo = PedidoService.generar_codigo()
                pedido["codigo_verificacion"] = nuevo_codigo
                pedido["intentos"] = 0
                pedido["reenvios"] = pedido.get("reenvios", 0) + 1

                if enviar_codigo(pedido["correo"], nuevo_codigo):
                    PedidoService.guardar(pedidos)
                    return True, "Código reenviado"
                else:
                    return False, "No se pudo enviar el correo"
        return False, "Pedido no encontrado"