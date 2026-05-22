import tkinter as tk
from tkinter import ttk
from app.views.main_view import MainView

class ProveedorView:
    def __init__(self, parent_notebook):
        self.frame = tk.Frame(parent_notebook, bg="#F5F5F5")
        parent_notebook.add(self.frame, text="🚚 Proveedores")

        # Título
        tk.Label(
            self.frame,
            text="🚚 GESTIÓN DE PROVEEDORES",
            font=("Segoe UI", 22, "bold"),
            fg="#B71C1C",
            bg="#F5F5F5",
            pady=25
        ).pack()

        # Tabla
        self.tree = ttk.Treeview(
            self.frame,
            columns=("Nombre", "Teléfono", "Tipo"),
            show="headings",
            style="Custom.Treeview" 
        )
        
        for col in self.tree["columns"]:
            self.tree.heading(col, text=col.upper())
            self.tree.column(col, anchor="center", width=250)
            
        self.tree.pack(fill="both", expand=True, padx=40, pady=10)

        # Contenedor de botones
        frame_botones = tk.Frame(self.frame, bg="#F5F5F5")
        frame_botones.pack(pady=30)

        self.btn_registrar = tk.Button(
            frame_botones, 
            text="➕ REGISTRAR PROVEEDOR",
            bg="#2E7D32", fg="white",
            font=("Segoe UI", 14, "bold"),
            relief="flat", cursor="hand2",
            padx=25, pady=12
        )
        self.btn_registrar.pack(side="left", padx=10)

        self.btn_eliminar = tk.Button(
            frame_botones,
            text="🗑️ ELIMINAR SELECCIONADO",
            bg="#B71C1C", fg="white",
            font=("Segoe UI", 14, "bold"),
            relief="flat", cursor="hand2",
            padx=25, pady=12
        )
        self.btn_eliminar.pack(side="left", padx=10)

    def actualizar_tabla(self, datos):
        self.tree.delete(*self.tree.get_children())
        for i, fila in enumerate(datos):
            tag = 'even' if i % 2 == 0 else 'odd'
            self.tree.insert("", "end", values=fila, tags=(tag,))

    def obtener_seleccionado(self):
        seleccionado = self.tree.selection()
        if not seleccionado: return None
        return self.tree.item(seleccionado)["values"][0]

    # --- VENTANA EMERGENTE CON MULTI-SELECCIÓN ---
    def abrir_ventana_registro(self, tipos_carne, callback_guardar):
        self.win = tk.Toplevel(self.frame)
        self.win.title("Nuevo Proveedor")
        self.win.geometry("500x650")
        self.win.configure(bg="white")
        self.win.resizable(False, False)
        self.win.transient(self.frame)
        self.win.grab_set()

        # Encabezado
        header = tk.Frame(self.win, bg="#B71C1C", height=60)
        header.pack(fill="x")
        tk.Label(header, text="📝 DATOS DEL PROVEEDOR", fg="white", bg="#B71C1C", 
                 font=("Segoe UI", 14, "bold")).pack(pady=15)

        body = tk.Frame(self.win, bg="white", padx=40, pady=10)
        body.pack(fill="both", expand=True)

        lbl_opt = {"bg": "white", "font": ("Segoe UI", 11, "bold"), "fg": "#333333"}

        tk.Label(body, text="NOMBRE COMPLETO / EMPRESA", **lbl_opt).pack(anchor="w", pady=(10, 0))
        self.entry_nombre = tk.Entry(body, font=("Segoe UI", 14), bd=1, relief="solid")
        self.entry_nombre.pack(fill="x", pady=5, ipady=5)

        tk.Label(body, text="TELÉFONO DE CONTACTO", **lbl_opt).pack(anchor="w", pady=(10, 0))
        self.entry_tel = tk.Entry(body, font=("Segoe UI", 14), bd=1, relief="solid")
        self.entry_tel.pack(fill="x", pady=5, ipady=5)

        # --- ÁREA DE SELECCIÓN MÚLTIPLE ---
        tk.Label(body, text="CORTES QUE DISTRIBUYE", **lbl_opt).pack(anchor="w", pady=(15, 5))
        
        # Frame con scroll para los Checkbuttons
        container_tipos = tk.Frame(body, bg="#F9F9F9", bd=1, relief="solid")
        container_tipos.pack(fill="both", expand=True, pady=5)
        
        canvas = tk.Canvas(container_tipos, bg="#F9F9F9", highlightthickness=0, height=150)
        scrollbar = ttk.Scrollbar(container_tipos, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg="#F9F9F9")

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        # Diccionario para guardar los estados de los checks
        self.dict_vars = {}

        for tipo in tipos_carne:
            var = tk.BooleanVar()
            cb = tk.Checkbutton(
                scrollable_frame, 
                text=tipo, 
                variable=var, 
                bg="#F9F9F9",
                font=("Segoe UI", 11),
                activebackground="#F9F9F9"
            )
            cb.pack(anchor="w", padx=10, pady=2)
            self.dict_vars[tipo] = var

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Función puente para recolectar los seleccionados
        def recolectar_y_guardar():
            seleccionados = [tipo for tipo, var in self.dict_vars.items() if var.get()]
            if not seleccionados:
                MainView.notify(self.win, "Aviso", "Selecciona al menos un tipo de carne", "warning")
                return
            
            callback_guardar(
                self.entry_nombre.get(),
                self.entry_tel.get(),
                seleccionados # Enviamos la lista al controlador
            )

        # Botón guardar
        tk.Button(
            body,
            text="CONFIRMAR REGISTRO",
            bg="#2E7D32", fg="white",
            font=("Segoe UI", 12, "bold"),
            relief="flat", cursor="hand2",
            pady=12,
            command=recolectar_y_guardar
        ).pack(fill="x", pady=20)

    def cerrar_ventana_registro(self):
        if hasattr(self, 'win') and self.win.winfo_exists():
            self.win.destroy()