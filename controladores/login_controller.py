from tkinter import messagebox
from vistas.login_view import LoginView

class LoginController:
    # Recibe el root (para dibujar la ventana emergente ahí) y el main_modelo
    def __init__(self, root, main_modelo):
        self.main_modelo = main_modelo
        self.vista = LoginView(root, self)

    def verificar_login(self):
        # 1. Le pedimos los datos a la vista
        usuario = self.vista.get_usuario()
        password = self.vista.get_password()
        
        # 2. Lógica de verificación
        if usuario == "admin" and password == "1234":
            self.main_modelo.set_admin(True) 
            self.vista.cerrar()
            messagebox.showinfo("Login Exitoso", "Modo administrador activado.")
        else:
            # Falló el login
            messagebox.showerror("Error de Login", "Usuario o contraseña incorrectos.")
            self.vista.limpiar_password()