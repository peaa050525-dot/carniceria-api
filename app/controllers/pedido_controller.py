from app.models.pedido_model import PedidoModel
from app.models.inventario_model import InventarioModel # <--- Usamos este también
from app.views.pedido_view import PedidoView
from app.services.email_service import EmailService
from app.utils.thread_handler import ejecutar_en_hilo
from app.views.main_view import MainView

class PedidoController:
    def __init__(self, parent_notebook):
        self.modelo = PedidoModel()
        self.modelo_inv = InventarioModel() # Para sacar los tipos de carne
        self.vista = PedidoView(parent_notebook)
        self.email_service = EmailService()

        # Configurar eventos
        self.vista.btn_generar.config(command=self.manejar_nuevo_pedido)
        self.vista.btn_verificar.config(command=self.manejar_verificacion)
        
        # Evento para cuando el usuario cambia el Tipo de Carne
        self.vista.cb_tipo.bind("<<ComboboxSelected>>", self.actualizar_cortes)

        # Cargar datos iniciales
        self.cargar_datos_iniciales()

    def cargar_datos_iniciales(self):
        # 1. Llenar la tabla de pedidos
        self.cargar_pedidos_tabla()
        # 2. Llenar el combo de tipos de carne desde la DB
        tipos = self.modelo_inv.obtener_tipos_carne()
        self.vista.cb_tipo.config(values=tipos)

    def actualizar_cortes(self, event):
        tipo_sel = self.vista.cb_tipo.get()
        cortes = self.modelo_inv.obtener_cortes_por_tipo(tipo_sel)
        self.vista.cb_corte.config(values=cortes)
        self.vista.cb_corte.set('') # Limpiar selección anterior

    def cargar_pedidos_tabla(self):
        pedidos = self.modelo.obtener_pedidos()
        self.vista.actualizar_tabla(pedidos)

    def manejar_nuevo_pedido(self):
        cliente, correo, tipo, corte, kilos_str = self.vista.obtener_datos()
        
        if not all([cliente, correo, tipo, corte, kilos_str]):
            return MainView.notify(self.vista.frame, "Atención", "Complete todos los campos")

        try:
            kilos = float(kilos_str)
            ejecutar_en_hilo(
                tarea_target=self.proceso_envio_correo,
                args=(cliente, correo, tipo, corte, kilos),
                on_success=self.finalizar_pedido
            )
        except ValueError:
            MainView.notify(self.vista.frame, "Error", "Los kilos deben ser un número")

    def proceso_envio_correo(self, cliente, correo, tipo, corte, kilos):
        # 1. Guardar en pedidos_online
        id_p, codigo = self.modelo.registrar_pedido_db(cliente, correo, tipo, corte, kilos)
        # 2. Enviar correo
        exito = self.email_service.enviar_codigo_verificacion(correo, codigo)
        return exito

    def finalizar_pedido(self, exito):
        if exito:
            MainView.notify(self.vista.frame, "Éxito", "Pedido generado. Revisa tu correo para el código.")
            self.cargar_pedidos_tabla()
        else:
            MainView.notify(self.vista.frame, "Error", "El pedido se guardó pero falló el envío del correo.")

    def manejar_verificacion(self):
        seleccion = self.vista.tree.selection()
        if not seleccion:
            return MainView.notify(self.vista.frame, "Atención", "Seleccione un pedido de la tabla")
        
        item = self.vista.tree.item(seleccion)['values']
        id_pedido = item[0]
        estado_actual = item[6]

        if estado_actual == "Verificado":
            return MainView.notify(self.vista.frame, "Aviso", "Este pedido ya ha sido verificado.")

        codigo_usuario = self.vista.pedir_codigo()
        
        if codigo_usuario:
            if self.modelo.verificar_codigo_db(id_pedido, codigo_usuario):
                MainView.notify(self.vista.frame, "Genial", "Código correcto. Pedido Verificado.")
                self.cargar_pedidos_tabla()
            else:
                MainView.notify(self.vista.frame, "Error", "Código de verificación incorrecto.")