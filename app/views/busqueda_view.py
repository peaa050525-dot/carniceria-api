import tkinter as tk
from tkinter import ttk

class BusquedaView:
    def __init__(self, parent_notebook):
        # El frame principal de la pestaña
        self.frame = tk.Frame(parent_notebook, bg="#F5F5F5")
        
        # Título de la pestaña
        tk.Label(self.frame, text="🔍 RESULTADOS DE BÚSQUEDA GLOBAL", font=("Segoe UI", 18, "bold"), 
                 fg="#B71C1C", bg="#F5F5F5").pack(pady=10)

        # Creamos un Canvas con Scrollbar porque si hay muchos resultados necesitaremos bajar
        self.canvas = tk.Canvas(self.frame, bg="#F5F5F5", highlightthickness=0)
        self.scrollbar = ttk.Scrollbar(self.frame, orient="vertical", command=self.canvas.yview)
        self.scroll_frame = tk.Frame(self.canvas, bg="#F5F5F5")

        self.scroll_frame.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        self.canvas.create_window((0, 0), window=self.scroll_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.canvas.pack(side="left", fill="both", expand=True, padx=20)
        self.scrollbar.pack(side="right", fill="y")

        # --- SECCIÓN 1: INVENTARIO ---
        # Ajustado a: Tipo, Corte, Existencia (Kilos)
        self.tabla_inv = self._crear_tabla("📦 PRODUCTOS Y CORTES", ("Tipo", "Corte", "Disponible"))

        # --- SECCIÓN 2: PROVEEDORES ---
        # Ajustado a: Nombre, Teléfono, Especialidad (tipo_carne)
        self.tabla_prov = self._crear_tabla("🚚 PROVEEDORES QUE SURTEN", ("Nombre", "Teléfono", "Especialidad"))

        # --- SECCIÓN 3: CLIENTES ---
        # Ajustado a: Nombre, Cantidad de compras, Estatus (Frecuencia)
        self.tabla_clie = self._crear_tabla("👥 CLIENTES Y FRECUENCIA", ("Nombre", "Compras Realizadas", "Estatus"))

    def _crear_tabla(self, titulo, columnas):
        """Función auxiliar para no repetir código de creación de tablas"""
        tk.Label(self.scroll_frame, text=titulo, font=("Segoe UI", 12, "bold"), 
                 bg="#F5F5F5", fg="#333333").pack(anchor="w", pady=(15, 5))
        
        # Estilo para las tablas de resultados
        tabla = ttk.Treeview(self.scroll_frame, columns=columnas, show="headings", height=6)
        
        for col in columnas:
            tabla.heading(col, text=col)
            tabla.column(col, width=250, anchor="center") # Columnas anchas para que se lea bien
            
        tabla.pack(fill="x", expand=True, padx=5)
        return tabla