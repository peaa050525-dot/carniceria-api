import tkinter as tk
from tkinter import ttk, messagebox, simpledialog

class PedidoView:
    def __init__(self, parent_notebook):
        self.frame = tk.Frame(parent_notebook, bg="#F5F5F5")
        parent_notebook.add(self.frame, text="🌐 Pedidos Online")

        # --- TÍTULO ROJO ESTILO DASHBOARD ---
        self.lbl_titulo = tk.Label(self.frame, 
                                   text="✉️ GESTIÓN DE PEDIDOS Y VERIFICACIÓN", 
                                   fg="#B71C1C", bg="#F5F5F5", 
                                   font=("Segoe UI", 16, "bold"), pady=15)
        self.lbl_titulo.pack()

        # --- FORMULARIO ALINEADO ---
        self.frame_form = tk.Frame(self.frame, bg="#F5F5F5", padx=20)
        self.frame_form.pack(fill="x")

        # Estilo de etiquetas
        lb_style = {'bg': "#F5F5F5", 'font': ("Segoe UI", 16, "bold")}
        
        # Fila 1
        tk.Label(self.frame_form, text="Cliente:", **lb_style).grid(row=0, column=0, sticky="w", pady=5)
        self.ent_cliente = tk.Entry(self.frame_form, width=20)
        self.ent_cliente.grid(row=0, column=1, padx=5)

        tk.Label(self.frame_form, text="Correo:", **lb_style).grid(row=0, column=2, sticky="w")
        self.ent_correo = tk.Entry(self.frame_form, width=30)
        self.ent_correo.grid(row=0, column=3, padx=5)

        # Fila 2
        tk.Label(self.frame_form, text="Tipo:", **lb_style).grid(row=1, column=0, sticky="w", pady=5)
        self.cb_tipo = ttk.Combobox(self.frame_form, state="readonly", width=18)
        self.cb_tipo.grid(row=1, column=1, padx=5)

        tk.Label(self.frame_form, text="Corte:", **lb_style).grid(row=1, column=2, sticky="w")
        self.cb_corte = ttk.Combobox(self.frame_form, state="readonly", width=18)
        self.cb_corte.grid(row=1, column=3, padx=5, sticky="w")

        # Fila 3
        tk.Label(self.frame_form, text="Kilos:", **lb_style).grid(row=2, column=0, sticky="w", pady=5)
        self.ent_kilos = tk.Entry(self.frame_form, width=10)
        self.ent_kilos.grid(row=2, column=1, padx=5, sticky="w")

        self.btn_generar = tk.Button(self.frame_form, text="➕ Generar Pedido", 
                                    bg="#2E7D32", fg="white", font=("Segoe UI", 16, "bold"), 
                                    padx=15, relief="flat", cursor="hand2")
        self.btn_generar.grid(row=2, column=2, columnspan=2, pady=10)

        # --- TABLA (Mismas columnas que tu DB) ---
        columnas = ("ID", "Cliente", "Correo", "Tipo", "Corte", "Kilos", "Estado")
        self.tree = ttk.Treeview(self.frame, columns=columnas, show="headings", style="Custom.Treeview")
        
        for col in columnas:
            self.tree.heading(col, text=col)
            # Ajustamos anchos según contenido
            ancho = 180 if col == "Correo" else 80
            self.tree.column(col, width=ancho, anchor="center")
        
        self.tree.pack(fill="both", expand=True, padx=20, pady=10)

        # Botón de Verificación abajo
        self.btn_verificar = tk.Button(self.frame, text="🔑 Verificar Código", 
                                      bg="#B71C1C", fg="white", font=("Segoe UI", 10, "bold"),
                                      padx=20, pady=5, relief="flat", cursor="hand2")
        self.btn_verificar.pack(pady=10)

    def obtener_datos(self):
        return (self.ent_cliente.get(), self.ent_correo.get(), 
                self.cb_tipo.get(), self.cb_corte.get(), self.ent_kilos.get())

    def limpiar_campos(self):
        self.ent_cliente.delete(0, 'end')
        self.ent_correo.delete(0, 'end')
        self.ent_kilos.delete(0, 'end')
        self.cb_tipo.set('')
        self.cb_corte.set('')

    def actualizar_tabla(self, lista_pedidos):
        self.tree.delete(*self.tree.get_children())
        for i, p in enumerate(lista_pedidos):
            tag = 'even' if i % 2 == 0 else 'odd'
            self.tree.insert("", "end", values=p, tags=(tag,))

    def pedir_codigo(self):
        return simpledialog.askstring("Verificación", "Introduce el código de 6 dígitos:")