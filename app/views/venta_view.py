import tkinter as tk
from tkinter import ttk

class VentaView:
    def __init__(self, parent_notebook):
        # Color de fondo consistente
        self.frame = tk.Frame(parent_notebook, bg="#F5F5F5")
        parent_notebook.add(self.frame, text="🥩 Ventas")

        contenedor = tk.Frame(self.frame, bg="#F5F5F5")
        contenedor.pack(fill="both", expand=True, padx=20, pady=20)

        # Formulario (Izquierda)
        self.frame_form = tk.Frame(contenedor, bg="#F5F5F5", padx=10)
        self.frame_form.grid(row=0, column=0, sticky="nsew")

        # Ticket (Derecha con sombra/borde)
        self.frame_ticket = tk.Frame(contenedor, bg="white", padx=2, pady=2, bd=0, highlightbackground="#CCCCCC", highlightthickness=1)
        self.frame_ticket.grid(row=0, column=1, sticky="nsew", padx=(20, 0))

        self.btn_grafica = tk.Button(self.frame, 
                            text="📊 VER REPORTE VISUAL", 
                            bg="#2E7D32", # Un verde para diferenciarlo del cobrar
                            fg="white", 
                            font=("Segoe UI", 12, "bold"), 
                            padx=20, 
                            pady=10, 
                            relief="flat",
                            cursor="hand2")
        self.btn_grafica.pack(side="left", padx=20)
        
        contenedor.grid_columnconfigure(0, weight=1)
        contenedor.grid_columnconfigure(1, weight=1)

        self._crear_formulario()
        self._crear_ticket()

    def _crear_formulario(self):
        # Estilo común para etiquetas
        lbl_opt = {'bg': "#F5F5F5", 'font': ("Segoe UI", 20, "bold"), 'fg': "#333333"}
        
        tk.Label(self.frame_form, text="👤 CLIENTE", **lbl_opt).pack(anchor="w")
        self.entry_cliente = tk.Entry(self.frame_form, font=("Segoe UI", 16), bd=1, relief="solid")
        self.entry_cliente.pack(fill="x", pady=(5, 15), ipady=5)

        self.btn_iniciar = tk.Button(self.frame_form, text="▶ INICIAR VENTA", bg="#B71C1C", fg="white", 
                                    font=("Segoe UI", 16, "bold"), relief="flat", cursor="hand2", pady=5)
        self.btn_iniciar.pack(fill="x", pady=(0, 20))

        tk.Label(self.frame_form, text="🥩 TIPO DE CARNE", **lbl_opt).pack(anchor="w")
        self.cb_tipo = ttk.Combobox(self.frame_form, state="readonly", font=("Segoe UI", 16))
        self.cb_tipo.pack(fill="x", pady=(5, 15))

        tk.Label(self.frame_form, text="🔪 CORTE", **lbl_opt).pack(anchor="w")
        self.cb_corte = ttk.Combobox(self.frame_form, state="readonly", font=("Segoe UI", 16))
        self.cb_corte.pack(fill="x", pady=(5, 15))

        self.lbl_precio = tk.Label(self.frame_form, text="Precio por kilo: $0.00", font=("Segoe UI", 20, "bold"), 
                                  fg="#B71C1C", bg="#F5F5F5", pady=10)
        self.lbl_precio.pack(fill="x")

        tk.Label(self.frame_form, text="⚖️ KILOS", **lbl_opt).pack(anchor="w")
        self.entry_kilos = tk.Entry(self.frame_form, font=("Segoe UI", 16), bd=1, relief="solid")
        self.entry_kilos.pack(fill="x", pady=(5, 20), ipady=5)

        # Botones de Acción
        self.btn_agregar = tk.Button(self.frame_form, text="🛒 AGREGAR A LISTA", bg="#424242", fg="white", 
                                    font=("Segoe UI", 16, "bold"), relief="flat", cursor="hand2", pady=8)
        self.btn_agregar.pack(fill="x", pady=5)

        self.btn_guardar = tk.Button(self.frame_form, text="✅ FINALIZAR Y GUARDAR", bg="#2E7D32", fg="white", 
                                    font=("Segoe UI", 16, "bold"), relief="flat", cursor="hand2", pady=10)
        self.btn_guardar.pack(fill="x", pady=5)

    def _crear_ticket(self):
        # Encabezado del Ticket
        tk.Label(self.frame_ticket, text="🧾 TICKET DE COMPRA", font=("Segoe UI", 22, "bold"), 
                 fg="white", bg="#B71C1C", pady=10).pack(fill="x")
        
        self.txt_ticket = tk.Text(self.frame_ticket, font=("Consolas", 15), bg="#FFFFFF", 
                                 bd=0, state="disabled", padx=10, pady=10)
        self.txt_ticket.pack(fill="both", expand=True)

    def actualizar_ticket_ui(self, texto_completo):
        self.txt_ticket.config(state="normal")
        self.txt_ticket.delete("1.0", tk.END)
        self.txt_ticket.insert(tk.END, texto_completo)
        self.txt_ticket.config(state="disabled")
