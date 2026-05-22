from app.models.caja_model import CajaModel
from app.views.caja_view import CajaView
from datetime import datetime
from app.views.main_view import MainView

import tkinter as tk
from tkinter import Toplevel, ttk, messagebox
from app.models.caja_model import CajaModel
from app.views.caja_view import CajaView
from datetime import datetime
from app.views.main_view import MainView

class CajaController:
    def __init__(self, parent_notebook):
        self.modelo = CajaModel()
        self.vista = CajaView(parent_notebook)
        
        self.total_actual_dinero = 0.0
        self.total_actual_kg = 0.0
        self.texto_reporte_actual = ""
        self.fue_guardado_en_db = False 

        # Conectar botones principales
        self.vista.btn_generar.config(command=self.procesar_generar_vista)
        self.vista.btn_guardar_db.config(command=self.guardar_corte_en_base_datos)
        self.vista.btn_imprimir.config(command=self.imprimir_ticket_txt)
        self.vista.btn_ver_historial.config(command=self.abrir_ventana_historial)

    def procesar_generar_vista(self):
        """Paso 1: Muestra ventas acumuladas."""
        ventas = self.modelo.obtener_ventas_pendientes()
        if not ventas:
            MainView.notify(self.vista.frame, "Aviso", "No hay ventas nuevas.")
            return

        self.fue_guardado_en_db = False 
        self.total_actual_dinero = 0.0
        self.total_actual_kg = 0.0
        ahora = datetime.now()
        
        texto =  "========================================\n"
        texto += "       REPORTE DE CORTE DE CAJA         \n"
        texto += "========================================\n"
        texto += f"Fecha: {ahora.strftime('%d/%m/%Y %H:%M:%S')}\n"
        texto += "----------------------------------------\n"
        
        for cliente, tipo, corte, kilos, subtotal in ventas:
            texto += f"{cliente[:10]:<10} | {corte[:10]:<10} | {kilos}kg | ${subtotal:.2f}\n"
            self.total_actual_dinero += subtotal
            self.total_actual_kg += kilos
        
        texto += "----------------------------------------\n"
        texto += f"TOTAL KILOS: {self.total_actual_kg:.2f} kg\n"
        texto += f"TOTAL CAJA:  ${self.total_actual_dinero:.2f}\n"
        texto += "========================================\n"
        
        self.texto_reporte_actual = texto
        self.vista.actualizar_vista_previa(texto)
        MainView.notify(self.vista.frame, "Vista Generada", "Paso 1 completado.")

    def guardar_corte_en_base_datos(self):
        """Paso 2: Guarda en DB."""
        if self.total_actual_dinero <= 0:
            MainView.notify(self.vista.frame, "Error", "Genere la vista previa primero.", "error")
            return
        try:
            self.modelo.registrar_corte_db(self.total_actual_kg, self.total_actual_dinero, self.texto_reporte_actual)
            self.fue_guardado_en_db = True
            MainView.notify(self.vista.frame, "Éxito", "Corte guardado. Ya puede imprimir.")
        except Exception as e:
            MainView.notify(self.vista.frame, "Error", str(e), "error")

    def imprimir_ticket_txt(self):
        """Paso 3: Imprime .txt y limpia."""
        if not self.fue_guardado_en_db:
            MainView.notify(self.vista.frame, "Acción Bloqueada", "Primero debe GUARDAR en la DB.", "error")
            return
        try:
            nombre = self.modelo.guardar_corte_txt(self.texto_reporte_actual)
            MainView.notify(self.vista.frame, "Impreso", f"Ticket: {nombre}")
            self.texto_reporte_actual = ""
            self.total_actual_dinero = 0
            self.fue_guardado_en_db = False
            self.vista.actualizar_vista_previa("\n\n   CORTE FINALIZADO E IMPRESO")
        except Exception as e:
            MainView.notify(self.vista.frame, "Error", str(e), "error")

    # --- NUEVAS FUNCIONES DEL HISTORIAL ---

    def abrir_ventana_historial(self):
        ventana = Toplevel(self.vista.frame)
        ventana.title("Historial de Cortes")
        ventana.geometry("700x500")
        ventana.grab_set() # Bloquea la ventana principal hasta cerrar esta

        tk.Label(ventana, text="📜 HISTORIAL DE CORTES", font=("Segoe UI", 14, "bold")).pack(pady=10)

        # Tabla
        columnas = ("ID", "Fecha", "KG", "Total")
        tabla = ttk.Treeview(ventana, columns=columnas, show="headings")
        for col in columnas:
            tabla.heading(col, text=col)
            tabla.column(col, width=100, anchor="center")
        tabla.pack(fill="both", expand=True, padx=20)

        cortes = self.modelo.obtener_historial_completo()
        for c in cortes:
            tabla.insert("", "end", values=(c[0], c[1], c[2], f"${c[3]:.2f}"))

        frame_h_btns = tk.Frame(ventana)
        frame_h_btns.pack(pady=20)

        tk.Button(frame_h_btns, text="🖨️ IMPRIMIR TODO", bg="#2E7D32", fg="white",
                  command=lambda: self.imprimir_todo_historial(cortes)).pack(side="left", padx=10)

        tk.Button(frame_h_btns, text="🗑️ VACIAR HISTORIAL", bg="#C62828", fg="white",
                  command=lambda: self.vaciar_historial_confirmado(ventana)).pack(side="left", padx=10)

    def imprimir_todo_historial(self, cortes):
        if not cortes:
            messagebox.showwarning("Aviso", "No hay cortes en el historial.")
            return
        
        total_d = sum(c[3] for c in cortes)
        total_k = sum(c[2] for c in cortes)
        
        texto = "=== REPORTE HISTÓRICO GLOBAL ===\n"
        for c in cortes:
            texto += f"ID: {c[0]} | {c[1]} | {c[2]}kg | ${c[3]:.2f}\n"
        texto += "================================\n"
        texto += f"TOTAL GLOBAL: {total_k:.2f}kg | ${total_d:.2f}\n"

        nombre = self.modelo.guardar_corte_txt(texto)
        messagebox.showinfo("Éxito", f"Reporte global guardado: {nombre}")

    def vaciar_historial_confirmado(self, ventana):
        if messagebox.askyesno("Confirmar", "¿Borrar TODO el historial permanentemente?"):
            self.modelo.eliminar_todo_el_historial()
            ventana.destroy()
            MainView.notify(self.vista.frame, "Éxito", "Historial eliminado.")