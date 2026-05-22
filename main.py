import tkinter as tk
from tkinter import ttk
# Importamos todos nuestros controladores
from app.models.database import inicializar_base
from app.views.main_view import MainView
from app.controllers.venta_controller import VentaController
from app.controllers.inventario_controller import InventarioController
from app.controllers.abastecimiento_controller import AbastecimientoController
from app.controllers.proveedor_controller import ProveedorController
from app.controllers.caja_controller import CajaController
from app.controllers.pedido_controller import PedidoController
from app.controllers.busqueda_controller import BusquedaController

class AplicacionCarniceria:
    def __init__(self, root):
        inicializar_base()

        self.main_view = MainView(root, password_admin="1234",indices_protegidos=[1,2,3,4,5])

        # INICIALIZACIÓN DE MÓDULOS
        # Al instanciar cada controlador, ellos crean su propia pestaña
        self.modulo_ventas = VentaController(self.main_view.notebook)
        self.modulo_inventario = InventarioController(self.main_view.notebook)
        self.modulo_historial = AbastecimientoController(self.main_view.notebook)
        self.modulo_proveedores = ProveedorController(self.main_view.notebook)
        self.modulo_caja = CajaController(self.main_view.notebook)
        self.modulo_pedidos = PedidoController(self.main_view.notebook)

        # --- INTEGRACIÓN DEL MÓDULO DE BÚSQUEDA ---
        # Le pasamos el notebook y el entry que creamos en MainView
        self.modulo_busqueda = BusquedaController(
            parent_notebook=self.main_view.notebook, 
            entry_busqueda=self.main_view.ent_global
        )
        # ------------------------------------------
        
        self.main_view.actualizar_estetica_global()
 
if __name__ == "__main__":
    root = tk.Tk()
    app = AplicacionCarniceria(root)
    root.mainloop()