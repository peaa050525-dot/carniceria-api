import tkinter as tk
from tkinter import ttk
from app.views.main_view import MainView

class InventarioView:
    def __init__(self, parent_notebook):
        self.frame = tk.Frame(parent_notebook, bg="#F5F5F5")
        parent_notebook.add(self.frame, text="📦 Inventario")

        # --- ESTILOS ---
        style = ttk.Style()
        style.theme_use("clam")
        
        style.configure("Custom.Treeview.Heading", 
                        background="#B71C1C", 
                        foreground="white", 
                        font=("Segoe UI", 14, "bold"),
                        padding=10)
        
        style.configure("Custom.Treeview", 
                        rowheight=45, 
                        font=("Segoe UI", 13),
                        background="white",
                        fieldbackground="white")

        style.map("Custom.Treeview", 
                  background=[('selected', '#43A047')], 
                  foreground=[('selected', 'white')])

        # --- TÍTULO ---
        self.lbl_titulo = tk.Label(self.frame, 
                                 text="📦 INVENTARIO DE CARNES", 
                                 fg="#B71C1C", 
                                 bg="#F5F5F5", 
                                 font=("Segoe UI", 22, "bold"), 
                                 pady=30)
        self.lbl_titulo.pack()

        # --- TABLA ---
        columnas = ("Tipo", "Corte", "Kilos", "Precio", "Total")
        self.tree = ttk.Treeview(self.frame, columns=columnas, show="headings", style="Custom.Treeview")

        for col in columnas:
            self.tree.heading(col, text=col) 
            self.tree.column(col, width=150, anchor="center")
        
        self.tree.tag_configure('even', background='#FFFFFF')
        self.tree.tag_configure('odd', background='#F9F9F9')
        self.tree.pack(fill="both", expand=True, padx=40)

        # --- BOTÓN ---
        self.btn_abastecer = tk.Button(self.frame, 
                                    text="➕ ABASTECER INVENTARIO", 
                                    bg="#B71C1C", 
                                    fg="white", 
                                    font=("Segoe UI", 14, "bold"), 
                                    padx=30, 
                                    pady=15, 
                                    relief="flat",
                                    cursor="hand2")
        self.btn_abastecer.pack(pady=30)

    def actualizar_tabla(self, registros_procesados):
        self.tree.delete(*self.tree.get_children())
        for i, reg in enumerate(registros_procesados):
            tag = 'even' if i % 2 == 0 else 'odd'
            self.tree.insert("", "end", values=reg, tags=(tag,))

    # --- VENTANA EMERGENTE ACTUALIZADA ---
    def abrir_ventana_abastecer(self, tipos_carne, nombres_proveedores, callback_cambio_tipo, callback_guardar):
        """
        nombres_proveedores ahora recibe una lista de tuplas: [(nombre, tipo_carne), ...]
        """
        self.win = tk.Toplevel(self.frame)
        self.win.title("Abastecimiento")
        self.win.geometry("500x600") # Aumentamos un poco el ancho por los nombres largos
        self.win.configure(bg="white")
        self.win.resizable(False, False)
        self.win.transient(self.frame)
        self.win.grab_set()

        header = tk.Frame(self.win, bg="#B71C1C", height=60)
        header.pack(fill="x")
        tk.Label(header, text="📥 NUEVO ABASTECIMIENTO", fg="white", bg="#B71C1C", 
                 font=("Segoe UI", 14, "bold")).pack(pady=15)

        form = tk.Frame(self.win, bg="white", padx=40, pady=20)
        form.pack(fill="both", expand=True)

        lbl_style = {"bg": "white", "font": ("Segoe UI", 11, "bold"), "fg": "#333333"}

        # Tipo de Carne
        tk.Label(form, text="TIPO DE CARNE", **lbl_style).pack(anchor="w", pady=(10,0))
        self.cb_tipo = ttk.Combobox(form, values=tipos_carne, state="readonly", font=("Segoe UI", 12))
        self.cb_tipo.pack(fill="x", pady=5)

        # Corte
        tk.Label(form, text="CORTE", **lbl_style).pack(anchor="w", pady=(10,0))
        self.cb_corte = ttk.Combobox(form, state="readonly", font=("Segoe UI", 12))
        self.cb_corte.pack(fill="x", pady=5)

        # Kilos
        tk.Label(form, text="KILOS A AGREGAR", **lbl_style).pack(anchor="w", pady=(10,0))
        self.entry_kilos = tk.Entry(form, font=("Segoe UI", 14), bd=1, relief="solid")
        self.entry_kilos.pack(fill="x", pady=5)

        # Proveedor con Información Adicional
        tk.Label(form, text="PROVEEDOR (Distribuye)", **lbl_style).pack(anchor="w", pady=(10,0))
        
        # FORMATEO: Convertimos la lista de tuplas en texto: "Don Juan (Res, Cerdo)"
        # Esto es lo que verá el usuario en el desplegable
        lista_con_info = [f"{p[0]} ({p[1]})" for p in nombres_proveedores]
        
        self.cb_proveedor = ttk.Combobox(form, values=lista_con_info, state="readonly", font=("Segoe UI", 12))
        self.cb_proveedor.pack(fill="x", pady=5)

        # Evento cambio de tipo
        self.cb_tipo.bind("<<ComboboxSelected>>", lambda e: callback_cambio_tipo(self.cb_tipo.get(), self.cb_corte))

        # Botón Confirmar
        tk.Button(form, text="CONFIRMAR INGRESO", bg="#2E7D32", fg="white", 
                  font=("Segoe UI", 12, "bold"), relief="flat", cursor="hand2", pady=12,
                  command=lambda: callback_guardar(
                      self.cb_tipo.get(), 
                      self.cb_corte.get(), 
                      self.entry_kilos.get(), 
                      self.cb_proveedor.get() # Pasamos el string completo "Nombre (Tipos)"
                  )).pack(fill="x", pady=30)

    def cerrar_ventana_abastecer(self):
        if hasattr(self, 'win') and self.win.winfo_exists():
            self.win.destroy()