import tkinter as tk
from tkinter import ttk

class AbastecimientoView:
    def __init__(self, parent_notebook):
        self.frame = tk.Frame(parent_notebook, bg="#F5F5F5")
        parent_notebook.add(self.frame, text="📋 Historial")

        # Título
        self.lbl_titulo = tk.Label(self.frame, 
                                   text="📋 HISTORIAL DE ABASTECIMIENTOS", 
                                   fg="#B71C1C", bg="#F5F5F5", 
                                   font=("Segoe UI", 16, "bold"), pady=20)
        self.lbl_titulo.pack()

        # Configuración de tabla
        columnas = ("Fecha", "Tipo", "Corte", "Kilos", "Proveedor")
        self.tree = ttk.Treeview(self.frame, columns=columnas, show="headings", style="Custom.Treeview")
        
        for col in columnas:
            self.tree.heading(col, text=col)
            self.tree.column(col, anchor="center", width=150)
        
        self.tree.pack(fill="both", expand=True, padx=20, pady=10)

    def actualizar_tabla(self, registros):
        self.tree.delete(*self.tree.get_children())
        for i, reg in enumerate(registros):
            tag = 'even' if i % 2 == 0 else 'odd'
            self.tree.insert("", "end", values=reg, tags=(tag,))