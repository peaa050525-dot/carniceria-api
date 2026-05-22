from app.models.inventario_model import InventarioModel
from app.views.inventario_view import InventarioView
from app.views.main_view import MainView

class InventarioController:
    def __init__(self, parent_notebook):
        self.modelo = InventarioModel()
        self.vista = InventarioView(parent_notebook)
        
        self.vista.btn_abastecer.config(command=self.iniciar_abastecimiento)
        parent_notebook.bind_all("<<VentaRealizada>>", self.cargar_inventario)
        self.cargar_inventario()
        
    def cargar_inventario(self, event=None): 
        try:
            datos_crudos = self.modelo.obtener_inventario_db()
            self.procesar_y_mostrar_datos(datos_crudos)
        except Exception as e:
            print(f"Error al cargar inventario: {e}")
        
    def procesar_y_mostrar_datos(self, datos_crudos):
        datos_con_total = []
        for fila in datos_crudos:
            tipo, corte, kilos, precio = fila
            total = kilos * precio 
            nueva_fila = (tipo, corte, kilos, f"${precio:,.2f}", f"${total:,.2f}")
            datos_con_total.append(nueva_fila)
        
        self.vista.actualizar_tabla(datos_con_total)

    def iniciar_abastecimiento(self):
        """Prepara los datos incluyendo la info de qué vende cada proveedor."""
        tipos = self.modelo.obtener_tipos_carne()
        
        # Obtenemos la lista de proveedores [(nombre, tipo_carne), ...]
        self.proveedores_db = self.modelo.obtener_proveedores()
        
        # Pasamos toda la info de proveedores a la vista para que pueda mostrar "Nombre (Res, Cerdo)"
        self.vista.abrir_ventana_abastecer(
            tipos_carne=tipos, 
            nombres_proveedores=self.proveedores_db, # Enviamos la lista completa, no solo nombres
            callback_cambio_tipo=self.al_cambiar_tipo_carne,
            callback_guardar=self.procesar_abastecimiento
        )

    def al_cambiar_tipo_carne(self, tipo_seleccionado, combobox_corte):
        cortes = self.modelo.obtener_cortes_por_tipo(tipo_seleccionado)
        combobox_corte.config(values=cortes)
        combobox_corte.set('') 

    def procesar_abastecimiento(self, tipo, corte, kilos_str, seleccion_proveedor):
        """Valida si el tipo de carne está dentro de la lista del proveedor."""
        try:
            # 1. Limpieza de datos: Extraer el nombre real si la selección viene como "Nombre (Tipos)"
            nombre_proveedor = seleccion_proveedor.split(" (")[0] if "(" in seleccion_proveedor else seleccion_proveedor

            if not tipo or not corte or not nombre_proveedor or not kilos_str:
                raise Exception("Por favor, complete todos los campos")

            kilos = float(kilos_str)
            if kilos <= 0:
                raise Exception("La cantidad de kilos debe ser mayor a 0")

            # 2. Buscar qué tipos maneja este proveedor en la lista que cargamos
            tipos_que_vende = next((p[1] for p in self.proveedores_db if p[0] == nombre_proveedor), "")
            
            # 3. VALIDACIÓN MULTI-TIPO:
            # En lugar de usar '!=', usamos 'in' para ver si el tipo está en la cadena (ej: "Res" en "Res, Cerdo")
            if tipo not in tipos_que_vende:
                raise Exception(f"Acceso Denegado:\nEl proveedor '{nombre_proveedor}' no distribuye {tipo}.\n\nDistribuye: {tipos_que_vende}")

            # Guardar en la DB
            self.modelo.registrar_abastecimiento(tipo, corte, kilos, nombre_proveedor)
            
            # Eventos y refresco
            self.vista.frame.winfo_toplevel().event_generate("<<NuevoAbastecimiento>>")
            self.cargar_inventario()
            
            MainView.notify(self.vista.frame, "Éxito", f"Se agregaron {kilos}kg de {corte} vía {nombre_proveedor}")
            self.vista.cerrar_ventana_abastecer()

        except ValueError:
            MainView.notify(self.vista.frame, "Error", "Ingrese un número válido en kilos", "error")
        except Exception as e:
            MainView.notify(self.vista.frame, "Error", str(e), "error")