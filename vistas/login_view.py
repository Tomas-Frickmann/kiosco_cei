import tkinter as tk
from Utilitys.util_ventana import centrar_ventana
from Utilitys.util_config import color_cuerpo_principal, color_menu_lateral

class LoginView:
    def __init__(self, master, controlador):
        self.controlador = controlador
        
        # 1. Creamos la ventana emergente
        self.window = tk.Toplevel(master)
        self.window.transient(master)  
        self.window.grab_set()         

        # 2. Configuración visual
        self.window.title("Login de Administrador")
        self.window.geometry("300x150")
        self.window.resizable(False, False)
        self.window.config(bg=color_cuerpo_principal)

        centrar_ventana(self.window, 300, 150)

        self.create_widgets()

    def create_widgets(self):
        frame = tk.Frame(self.window, bg=color_cuerpo_principal, padx=10, pady=10)
        frame.pack(expand=True)

        # Usuario
        lbl_user = tk.Label(frame, text="Usuario:", bg=color_cuerpo_principal, fg="black")
        lbl_user.grid(row=0, column=0, pady=5, sticky="w")
        self.entry_user = tk.Entry(frame)
        self.entry_user.grid(row=0, column=1, pady=5)

        # Contraseña
        lbl_pass = tk.Label(frame, text="Contraseña:", bg=color_cuerpo_principal, fg="black")
        lbl_pass.grid(row=1, column=0, pady=5, sticky="w")
        self.entry_pass = tk.Entry(frame, show="*") 
        self.entry_pass.grid(row=1, column=1, pady=5)
        
        # Conectar Enter al controlador
        self.entry_pass.bind("<Return>", lambda event: self.controlador.verificar_login())
        
        # Botón Login conectado al controlador
        btn_login = tk.Button(
            frame, text="Iniciar Sesión", command=self.controlador.verificar_login,
            bg=color_menu_lateral, fg="white", bd=0, padx=10
        )
        btn_login.grid(row=2, column=0, columnspan=2, pady=10)

    # --- MÉTODOS DE AYUDA PARA EL CONTROLADOR ---
    def get_usuario(self):
        return self.entry_user.get()

    def get_password(self):
        return self.entry_pass.get()

    def limpiar_password(self):
        self.entry_pass.delete(0, tk.END)

    def cerrar(self):
        self.window.destroy()