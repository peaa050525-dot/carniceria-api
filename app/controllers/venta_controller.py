from app.models.venta_model import VentaModel
from app.views.venta_view import VentaView
from app.views.main_view import MainView  # <--- IMPORTANTE: Importamos MainView
from datetime import datetime

class VentaController:
    def __init__(self, parent_notebook):
        self.modelo = VentaModel()
        self.vista = VentaView(parent_notebook)
        
        self.vista.btn_grafica.config(command=self.modelo.generar_grafica_pastel_semanal)
        
        self._conectar_eventos()
        self._cargar_datos_iniciales()
        self.datos_cortes_actuales = {}
        
    # Creamos la función para grafica
    def mostrar_grafica_ventas(self):
        """Llama al modelo para generar la visualización."""
        try:
            # Llamamos a la funciónen VentaModel
            self.modelo.generar_grafica_mas_vendidos()
        except Exception as e:
            MainView.notify(self.vista.frame, "Error", f"No se pudo generar la gráfica: {e}", "error")

    def _conectar_eventos(self):
        self.vista.btn_iniciar.config(command=self.iniciar_cliente)
        self.vista.btn_agregar.config(command=self.agregar_compra)
        self.vista.btn_guardar.config(command=self.guardar_venta_final)
        self.vista.cb_tipo.bind("<<ComboboxSelected>>", self.al_seleccionar_tipo)
        self.vista.cb_corte.bind("<<ComboboxSelected>>", self.al_seleccionar_corte)

    def _cargar_datos_iniciales(self):
        tipos = self.modelo.obtener_tipos_carne()
        self.vista.cb_tipo.config(values=tipos)

    def al_seleccionar_tipo(self, event):
        tipo_seleccionado = self.vista.cb_tipo.get()
        cortes_data = self.modelo.obtener_cortes_por_tipo(tipo_seleccionado)
        self.datos_cortes_actuales = {row[0]: {"precio": row[1], "stock": row[2]} for row in cortes_data}
        
        cortes_nombres = list(self.datos_cortes_actuales.keys())
        self.vista.cb_corte.config(values=cortes_nombres)
        self.vista.cb_corte.set('')
        self.vista.lbl_precio.config(text="Precio por kilo: $0.00")

    def al_seleccionar_corte(self, event):
        corte = self.vista.cb_corte.get()
        if corte in self.datos_cortes_actuales:
            precio = self.datos_cortes_actuales[corte]["precio"]
            self.vista.lbl_precio.config(text=f"Precio por kilo: ${precio:.2f}")

    def iniciar_cliente(self):
        cliente = self.vista.entry_cliente.get().strip()
        if not cliente:
            # Usamos el nuevo sistema de avisos
            MainView.notify(self.vista.frame, "Atención", "Ingrese el nombre del cliente para iniciar", "error")
            return

        self.modelo.limpiar_venta_actual()
        self.modelo.cliente_actual = cliente
        self.actualizar_ticket()

    def agregar_compra(self):
        try:
            if not self.modelo.cliente_actual:
                raise Exception("Debe iniciar un cliente primero")

            tipo = self.vista.cb_tipo.get()    
            corte = self.vista.cb_corte.get()
            kilos_str = self.vista.entry_kilos.get()

            if not tipo or not corte:
                raise Exception("Seleccione tipo y corte de carne")

            kilos = float(kilos_str)
            if kilos <= 0:
                raise Exception("La cantidad de kilos debe ser mayor a 0")

            stock_disponible = self.datos_cortes_actuales[corte]["stock"]
            if stock_disponible < kilos:
                raise Exception(f"Stock insuficiente. Disponible: {stock_disponible} kg")

            precio = self.datos_cortes_actuales[corte]["precio"]
            subtotal = kilos * precio

            self.modelo.venta_actual.append((tipo, corte, kilos, precio, subtotal))
            self.modelo.total_ticket += subtotal

            self.actualizar_ticket()
            self.vista.entry_kilos.delete(0, 'end')

        except ValueError:
            MainView.notify(self.vista.frame, "Error de Formato", "Ingrese una cantidad numérica válida", "error")
        except Exception as e:
            MainView.notify(self.vista.frame, "Error", str(e), "error")

    def guardar_venta_final(self):
        try:
            if not self.modelo.venta_actual:
                raise Exception("No hay productos en el ticket")

            self.modelo.guardar_venta_final()
            
            # Generar evento para actualizar otros módulos (como Inventario o Caja)
            self.vista.frame.winfo_toplevel().event_generate("<<VentaRealizada>>")
            
            # Mensaje de éxito con estilo verde
            MainView.notify(self.vista.frame, "Venta Exitosa", "La venta ha sido registrada y el stock actualizado", "success")
            
            self.actualizar_ticket()
            self.vista.entry_cliente.delete(0, 'end')
            
        except Exception as e:
            MainView.notify(self.vista.frame, "Error al Guardar", str(e), "error")

    def actualizar_ticket(self):
        texto = "       🥩 CARNICERÍA 🥩\n"
        texto += "===============================\n"
        texto += f"Cliente: {self.modelo.cliente_actual}\n"
        texto += f"Fecha: {datetime.now().strftime('%d/%m/%Y %H:%M')}\n"
        texto += "-------------------------------\n"
        texto += f"{'PRODUCTO':<15} {'KG':>5} {'SUBT':>8}\n"
        texto += "-------------------------------\n"

        for v in self.modelo.venta_actual:
            corte, kilos, subtotal = v[1], v[2], v[4]
            texto += f"{corte[:15]:<15} {kilos:>5.2f} ${subtotal:>7.2f}\n"

        texto += "-------------------------------\n"
        texto += f"TOTAL A PAGAR:      ${self.modelo.total_ticket:>8.2f}\n"
        texto += "===============================\n"
        texto += "\n   ¡Gracias por su compra!"
        
        self.vista.actualizar_ticket_ui(texto)