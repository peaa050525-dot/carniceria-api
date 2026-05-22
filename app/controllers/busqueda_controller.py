from app.models.busqueda_model import BusquedaModel
from app.views.busqueda_view import BusquedaView

class BusquedaController:
    def __init__(self, parent_notebook, entry_busqueda):
        self.notebook = parent_notebook
        self.modelo = BusquedaModel()
        self.vista = None # Se crea solo cuando se busca por primera vez
        
        # Escuchamos el Enter en la barra de búsqueda que nos pasaron
        entry_busqueda.bind("<Return>", lambda e: self.realizar_busqueda(entry_busqueda.get()))

    def realizar_busqueda(self, termino):
        if not termino.strip(): return
        
        datos = self.modelo.buscar_en_todo(termino)
        
        # Si la vista no se ha creado (es la primera búsqueda), la instanciamos
        if self.vista is None:
            from app.views.busqueda_view import BusquedaView # Importación tardía para evitar círculos
            self.vista = BusquedaView(self.notebook)
            self.notebook.add(self.vista.frame, text="🔍 Resultados")

        # --- LLENAR TABLA INVENTARIO ---
        self._llenar_tabla(self.vista.tabla_inv, 
            [(d['tipo'], d['corte'], f"{d['kilos']} kg") for d in datos['inventario']])
        
        # --- LLENAR TABLA PROVEEDORES ---
        self._llenar_tabla(self.vista.tabla_prov, 
            [(d['nombre'], d['telefono'], d['tipo_carne']) for d in datos['proveedores']])
        
        # --- LLENAR TABLA CLIENTES (CON LÓGICA DE FRECUENCIA) ---
        lista_clientes = []
        for c in datos['clientes']:
            # Lógica: Si tiene 5 o más ventas registradas, es cliente estrella
            frecuencia = "⭐ Frecuente" if c['total_compras'] >= 5 else "Ocasional"
            lista_clientes.append((c['cliente'], f"{c['total_compras']} compras", frecuencia))
        
        self._llenar_tabla(self.vista.tabla_clie, lista_clientes)
        
        # Cambiar el foco a la pestaña de resultados
        self.notebook.select(self.vista.frame)

    def _llenar_tabla(self, tabla, filas):
        tabla.delete(*tabla.get_children())
        for f in filas:
            tabla.insert("", "end", values=list(f))