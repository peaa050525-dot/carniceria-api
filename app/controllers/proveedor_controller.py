from app.models.proveedor_model import ProveedorModel
from app.views.proveedor_view import ProveedorView
from app.views.main_view import MainView

class ProveedorController:
    def __init__(self, parent_notebook):
        self.modelo = ProveedorModel()
        self.vista = ProveedorView(parent_notebook)
        
        # Conectar eventos de los botones
        self.vista.btn_registrar.config(command=self.abrir_registro)
        self.vista.btn_eliminar.config(command=self.eliminar_proveedor)
        
        # Cargar los datos iniciales
        self.cargar_datos_tabla()

    def cargar_datos_tabla(self):
        """Obtiene los datos del modelo y los pasa a la vista."""
        datos = self.modelo.obtener_proveedores()
        self.vista.actualizar_tabla(datos)

    def abrir_registro(self):
        """Obtiene los tipos de carne y abre la ventana de registro."""
        tipos_carne = self.modelo.obtener_tipos_carne()
        self.vista.abrir_ventana_registro(tipos_carne, self.procesar_registro)

    def procesar_registro(self, nombre, telefono, lista_cortes):
        """
        Valida y guarda el nuevo proveedor.
        lista_cortes ahora es una LISTA de Python enviada por la vista.
        """
        nombre = nombre.strip()
        telefono = telefono.strip()

        # Validación: ahora verificamos que la lista no esté vacía
        if not nombre or not telefono or not lista_cortes:
            # Mandamos el error a la ventana Toplevel (self.vista.win) si existe
            MainView.notify(self.vista.win, "Error", "Complete todos los campos y seleccione al menos un corte", "error")
            return

        try:
            # Pasamos la lista al modelo. 
            # El modelo hará el ", ".join(lista_cortes) antes de guardar en la DB.
            self.modelo.registrar_proveedor(nombre, telefono, lista_cortes)
            
            self.cargar_datos_tabla()
            MainView.notify(self.vista.frame, "Éxito", f"Proveedor '{nombre}' registrado correctamente")
            self.vista.cerrar_ventana_registro()
        except Exception as e:
            MainView.notify(self.vista.win, "Error al registrar", str(e), "error")

    def eliminar_proveedor(self):
        """Obtiene el seleccionado y lo elimina."""
        nombre = self.vista.obtener_seleccionado()
        
        if not nombre:
            MainView.notify(self.frame, "Error", "Seleccione un proveedor de la lista", "error")
            return
            
        try:
            self.modelo.eliminar_proveedor(nombre)
            self.cargar_datos_tabla()
            MainView.notify(self.vista.frame, "Éxito", f"Proveedor '{nombre}' eliminado")
        except Exception as e:
            MainView.notify(self.vista.frame, "Error al eliminar", str(e), "error")