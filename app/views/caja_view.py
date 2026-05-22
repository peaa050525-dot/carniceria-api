import tkinter as tk

class CajaView:
    def __init__(self, parent_notebook):
        self.frame = tk.Frame(parent_notebook, bg="#F5F5F5")
        parent_notebook.add(self.frame, text="💵 Corte de Caja")

        tk.Label(self.frame, text="💵 CONTROL DE CAJA", font=("Segoe UI", 22, "bold"), 
                 bg="#F5F5F5", fg="#2E7D32").pack(pady=10)
        
        # --- ÁREA DE TICKET ---
        frame_ticket = tk.Frame(self.frame, bg="white", bd=2, relief="sunken")
        frame_ticket.pack(pady=10, padx=50, fill="both", expand=True)

        self.txt_vista_previa = tk.Text(frame_ticket, font=("Consolas", 12), 
                                       bg="#FFFDE7", bd=0, padx=20, pady=20)
        self.txt_vista_previa.pack(fill="both", expand=True)
        self.txt_vista_previa.insert("1.0", "\n\n   Presione 'Generar Corte' para ver las ventas.")
        self.txt_vista_previa.config(state="disabled")

        # --- PANEL DE BOTONES ---
        frame_btns = tk.Frame(self.frame, bg="#F5F5F5")
        frame_btns.pack(pady=20)

        # 1. BOTÓN GENERAR (El nuevo)
        self.btn_generar = tk.Button(frame_btns, text="🔍 GENERAR VISTA PREVIA", 
                                    bg="#FB8C00", fg="white", font=("Segoe UI", 11, "bold"),
                                    padx=15, pady=8, relief="flat", cursor="hand2")
        self.btn_generar.pack(side="left", padx=5)

        # 2. BOTÓN GUARDAR
        self.btn_guardar_db = tk.Button(frame_btns, text="💾 GUARDAR EN HISTORIAL", 
                                       bg="#1976D2", fg="white", font=("Segoe UI", 11, "bold"),
                                       padx=15, pady=8, relief="flat", cursor="hand2")
        self.btn_guardar_db.pack(side="left", padx=5)

        # 3. BOTÓN IMPRIMIR
        self.btn_imprimir = tk.Button(frame_btns, text="🖨️ IMPRIMIR (.txt)", 
                                     bg="#2E7D32", fg="white", font=("Segoe UI", 11, "bold"),
                                     padx=15, pady=8, relief="flat", cursor="hand2")
        self.btn_imprimir.pack(side="left", padx=5)
        
        #4 HISTORIAL DE CORTES
        self.btn_ver_historial = tk.Button(frame_btns, text="📜 VER HISTORIAL", 
                                          bg="#455A64", fg="white", font=("Segoe UI", 11, "bold"),
                                          padx=15, pady=8, relief="flat", cursor="hand2")
        self.btn_ver_historial.pack(side="left", padx=5)

    def actualizar_vista_previa(self, texto):
        self.txt_vista_previa.config(state="normal")
        self.txt_vista_previa.delete("1.0", tk.END)
        self.txt_vista_previa.insert(tk.END, texto)
        self.txt_vista_previa.config(state="disabled")