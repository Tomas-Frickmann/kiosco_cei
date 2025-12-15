import tkinter as tk
from Utilitys.util_ventana import centrar_ventana
from tkinter import messagebox
from Forms.form_setting import app_state # Necesario para cambiar el estado de administrador
from config import color_barra_superior, color_cuerpo_principal, color_menu_lateral

class FormularioLogin(tk.Toplevel):
    def __init__(self, master=None):
        # 1. Llamar al constructor de Toplevel, pasándole la ventana maestra
        super().__init__(master)
        self.master = master
        self.transient(master)  # Hace que la ventana de Login dependa de la ventana principal
        self.grab_set()        # Captura todos los eventos: obliga al usuario a interactuar con el login

        # Configuración visual de la ventana de login
        self.title("Login de Administrador")
        self.geometry("300x150")
        self.resizable(False, False)
        self.config(bg=color_cuerpo_principal)

        centrar_ventana(self,300, 150) # Si importas la función

        self.create_widgets()
        
    def create_widgets(self):
        # Frame principal para contener los campos (opcional, pero buena práctica)
        frame = tk.Frame(self, bg=color_cuerpo_principal, padx=10, pady=10)
        frame.pack(expand=True)

        # Etiqueta y campo de Usuario
        lbl_user = tk.Label(frame, text="Usuario:", bg=color_cuerpo_principal, fg="black")
        lbl_user.grid(row=0, column=0, pady=5, sticky="w")
        self.entry_user = tk.Entry(frame)
        self.entry_user.grid(row=0, column=1, pady=5)

        # Etiqueta y campo de Contraseña
        lbl_pass = tk.Label(frame, text="Contraseña:", bg=color_cuerpo_principal, fg="black")
        lbl_pass.grid(row=1, column=0, pady=5, sticky="w")
        self.entry_pass = tk.Entry(frame, show="*") 
        self.entry_pass.grid(row=1, column=1, pady=5)

        # Botón de Login
        btn_login = tk.Button(
            frame, text="Iniciar Sesión", command=self.check_login,
            bg=color_menu_lateral, fg="white", bd=0, padx=10
        )
        btn_login.grid(row=2, column=0, columnspan=2, pady=10)

    def check_login(self):
        # Lógica de verificación de usuario y contraseña
        usuario = self.entry_user.get()
        password = self.entry_pass.get()
        
        # Simulamos la verificación con credenciales fijas
        # NOTA: En un proyecto real, esto debería ir contra tu base de datos!
        if usuario == "admin" and password == "1234":
            # 1. Actualiza el estado global de la app
            app_state.set_admin(True) 
            
            # 2. Cierra la ventana emergente
            self.destroy()
            messagebox.showinfo("Login Exitoso", "Modo administrador activado.")
        else:
            messagebox.showerror("Error de Login", "Usuario o contraseña incorrectos.")
            self.entry_pass.delete(0, tk.END) # Limpia el campo de contraseña

