import tkinter as tk
from tkinter import ttk, messagebox, simpledialog

class VentanaAviso(tk.Toplevel):
    def __init__(self, parent, titulo, mensaje, tipo):
        super().__init__(parent)
        self.title(titulo)
        self.geometry("400x200")
        self.resizable(False, False)
        self.configure(bg="white")
        
        # Colores según el tipo
        color_tema = "#B71C1C" if tipo == "error" else "#2E7D32"
        icono = "⚠️" if tipo == "error" else "✅"

        # Hacer modal
        self.transient(parent)
        self.grab_set()
        
        # Centrar
        self.update_idletasks()
        x = parent.winfo_screenwidth() // 2 - 200
        y = parent.winfo_screenheight() // 2 - 100
        self.geometry(f"+{x}+{y}")

        # Barra de título personalizada
        header = tk.Frame(self, bg=color_tema, height=40)
        header.pack(fill="x")
        tk.Label(header, text=f"{icono} {titulo.upper()}", fg="white", bg=color_tema, 
                 font=("Segoe UI", 10, "bold")).pack(pady=8)

        # Contenido
        body = tk.Frame(self, bg="white", padx=20, pady=20)
        body.pack(fill="both", expand=True)

        tk.Label(body, text=mensaje, bg="white", font=("Segoe UI", 10), 
                 wraplength=350, justify="center").pack(expand=True)

        # Botón de cierre
        btn_cerrar = tk.Button(body, text="ENTENDIDO", bg=color_tema, fg="white", 
                               font=("Segoe UI", 9, "bold"), relief="flat", 
                               padx=20, pady=5, command=self.destroy, cursor="hand2")
        btn_cerrar.pack(pady=10)

class LoginGerente(tk.Toplevel):
    def __init__(self, parent, password_correcta, on_success):
        super().__init__(parent)
        self.password_correcta = password_correcta
        self.on_success = on_success
        
        self.title("Seguridad - Acceso Restringido")
        self.geometry("350x250")
        self.configure(bg="#F5F5F5")
        self.resizable(False, False)
        
        # Hacer que la ventana sea modal
        self.transient(parent)
        self.grab_set()

        # Centrar respecto a la app principal
        self.update_idletasks()
        x = parent.winfo_x() + (parent.winfo_width() // 2) - (175)
        y = parent.winfo_y() + (parent.winfo_height() // 2) - (125)
        self.geometry(f"+{x}+{y}")

        # Encabezado Rojo
        self.header = tk.Frame(self, bg="#B71C1C", height=50)
        self.header.pack(fill="x")
        tk.Label(self.header, text="🔐 ACCESO GERENTE", fg="white", bg="#B71C1C", 
                 font=("Segoe UI", 12, "bold")).pack(pady=10)

        # Contenido
        self.content = tk.Frame(self, bg="#F5F5F5", padx=30, pady=20)
        self.content.pack(fill="both", expand=True)

        tk.Label(self.content, text="Esta sección requiere autorización.\nIngrese la clave de seguridad:", 
                 bg="#F5F5F5", font=("Segoe UI", 10), justify="center").pack(pady=(0, 15))

        self.ent_pass = tk.Entry(self.content, show="●", font=("Segoe UI", 14), 
                                 justify="center", bd=2, relief="groove")
        self.ent_pass.pack(fill="x")
        self.ent_pass.focus_set()

        # Botón Verificar
        self.btn_entrar = tk.Button(self.content, text="VERIFICAR ACCESO", bg="#B71C1C", fg="white", 
                                    font=("Segoe UI", 10, "bold"), relief="flat", cursor="hand2",
                                    command=self.verificar, pady=8)
        self.btn_entrar.pack(fill="x", pady=20)

        self.bind('<Return>', lambda e: self.verificar())

    def verificar(self):
        if self.ent_pass.get() == self.password_correcta:
            self.on_success() # Llama a la función de éxito en MainView
            self.destroy()
        else:
            messagebox.showerror("Seguridad", "Contraseña incorrecta", parent=self)
            self.ent_pass.delete(0, tk.END)

class MainView:
    def __init__(self, root, password_admin, indices_protegidos):
        self.root = root
        self.password_admin = password_admin
        self.indices_protegidos = indices_protegidos
        self.autenticado = False
        
        self.configurar_ventana()
        self.configurar_estilos()
        
        # --- AGREGAR ESTO: BARRA DE BÚSQUEDA GLOBAL ---
        self.frame_superior = tk.Frame(self.root, bg="#B71C1C", pady=10)
        self.frame_superior.pack(fill="x")

        tk.Label(self.frame_superior, text="🔎 BUSCADOR GLOBAL:", 
                 fg="white", bg="#B71C1C", font=("Segoe UI", 10, "bold")).pack(side="left", padx=(20, 10))

        self.ent_global = tk.Entry(self.frame_superior, font=("Segoe UI", 12), width=40)
        self.ent_global.pack(side="left", padx=10)
        
        tk.Label(self.frame_superior, text="(Presiona Enter para buscar)", 
                 fg="#FFCDD2", bg="#B71C1C", font=("Segoe UI", 8, "italic")).pack(side="left")
        # ----------------------------------------------
        
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Escuchar cambios de pestaña
        self.notebook.bind("<<NotebookTabChanged>>", self._gestionar_seguridad)

    def configurar_ventana(self):
        self.root.title("Sistema de Gestión - Carnicería")
        self.root.geometry("1300x800")
        self.root.update_idletasks()
        x = (self.root.winfo_screenwidth() // 2) - (650)
        y = (self.root.winfo_screenheight() // 2) - (400)
        self.root.geometry(f'+{x}+{y}')

    def configurar_estilos(self):
        self.style = ttk.Style()
        self.style.theme_use("clam")
        #
        self.root.option_add('*TCombobox*Listbox.font', ("Segoe UI", 16))
        self.root.option_add('*TCombobox*Listbox.selectBackground', "#B71C1C") # Rojo al seleccionar
        self.root.option_add('*TCombobox*Listbox.selectForeground', "white")
        self.style.configure("TCombobox", padding=10) # Esto le da altura al cuadro
        self.style.map("TCombobox", fieldbackground=[("readonly", "white")])
        
        # --- DEFINICIÓN DE FUENTES ---
        self.FUENTE_BLOQUEADO = ("Segoe UI", 15, "italic")   # Cursiva y pequeña para bloqueo
        self.FUENTE_DESBLOQUEADO = ("Segoe UI", 15, "bold") # Negrita y clara para acceso total
        
        # Colores de Texto (Foreground)
        self.TEXTO_BLOQUEADO = "#FFFFFF"    # Gris oscuro (menos legible)
        self.TEXTO_DESBLOQUEADO = "#000000" # Negro total (bien legible)
        self.TEXTO_SELECCIONADO = "#FFFFFF" # Blanco (para que resalte sobre azul/verde)
        
        # Colores definidos
        self.COLOR_BLOQUEADO = "#499B1C"    # Gris (Estado protegido)
        self.COLOR_DESBLOQUEADO = "#067913" # Gris claro (Estado libre)
        self.COLOR_SELECCION_NORMAL = "#005B1E" # Azul (Ventas/Pedidos)
        self.COLOR_SELECCION_ADMIN = "#43A047"  # Verde (Modo Administrador)

        # Configuración inicial del estilo
        self.style.configure("TNotebook.Tab", 
                            padding=[20, 10], 
                            background=self.COLOR_BLOQUEADO,
                            foreground=self.TEXTO_BLOQUEADO,
                            font=self.FUENTE_BLOQUEADO)

    def actualizar_estetica_global(self):
        """Cambia el color de todas las pestañas según el estado de autenticación."""
        if not self.autenticado:
            # ESTADO BLOQUEADO
            self.style.configure("TNotebook.Tab", background=self.COLOR_BLOQUEADO, foreground=self.TEXTO_BLOQUEADO, font=self.FUENTE_BLOQUEADO)
            
            self.style.map("TNotebook.Tab",
                            background=[("selected", self.COLOR_SELECCION_NORMAL)],
                            foreground=[("selected", self.TEXTO_BLOQUEADO)],
                            font=[("selected", self.FUENTE_DESBLOQUEADO)])
        else:
            # ESTADO DESBLOQUEADO
            self.style.configure("TNotebook.Tab", background=self.COLOR_DESBLOQUEADO, foreground=self.TEXTO_BLOQUEADO, font=self.FUENTE_DESBLOQUEADO)
            
            self.style.map("TNotebook.Tab",
                            background=[("selected", self.COLOR_SELECCION_ADMIN)],
                            foreground=[("selected", self.TEXTO_BLOQUEADO)],
                            font=[("selected", self.FUENTE_DESBLOQUEADO)])

    def _gestionar_seguridad(self, event):
        indice_actual = self.notebook.index("current")

        # Al volver a Ventas (índice 0), cerramos sesión y regresamos a colores de bloqueo
        if indice_actual == 0:
            if self.autenticado:
                self.autenticado = False
                self.actualizar_estetica_global()
            return

        # Si intenta entrar a una bloqueada y no está autenticado
        if indice_actual in self.indices_protegidos and not self.autenticado:
            self.notebook.select(0) # Rebotar inmediatamente
            
            # Lanzar nuestra nueva ventana de Login
            def login_exitoso():
                self.autenticado = True
                self.actualizar_estetica_global()
                self.notebook.select(indice_actual) # Ahora sí, lo pasamos a la pestaña que quería
            
            LoginGerente(self.root, self.password_admin, login_exitoso)
            
    @staticmethod
    def notify(parent, titulo, mensaje, tipo="info"):
        """
        Este es el método universal. 
        Lo llamamos 'notify' para que sea corto de escribir.
        """
        VentanaAviso(parent, titulo, mensaje, tipo)