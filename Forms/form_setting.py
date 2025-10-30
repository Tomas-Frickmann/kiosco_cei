import tkinter as tk
import json
import os
from tkinter import messagebox
from config import color_cuerpo_principal,color_barra_superior,color_menu_lateral

CONFIG_PATH = "config_maquina.json"
DEFAULT_CONFIG = {
    "nombre_maquina": "SIN_NOMBRE"
}

# Clase para manejar el estado global
class AppState:
    def __init__(self):
        self.is_admin = False  # Estado inicial
        self._observers = []  # Lista de observadores

    def add_observer(self, callback):
        """Registra una función que será llamada cuando cambie el estado."""
        self._observers.append(callback)

    def notify_observers(self):
        """Notifica a todas las funciones registradas."""
        for callback in self._observers:
            callback()

    def set_admin(self, value):
        """Cambia el estado de admin y notifica a los observadores."""
        self.is_admin = value
        self.notify_observers()


# Crear una instancia global del estado
app_state = AppState()


class Setting():

    def __init__(self,panel_principal):
        self.subcuerpo = tk.Frame(panel_principal,bg=color_barra_superior)
        self.subcuerpo.pack(side=tk.TOP, fill='both',expand=True)

        self.config = cargar_configuracion()
        self.PanelAdmin()
        


    def PanelAdmin(self):
        panelAdmin = tk.Frame(self.subcuerpo,bg=color_menu_lateral)
        panelAdmin.pack(side=tk.TOP, fill='both',expand=True)
        borde_superior = tk.Frame(panelAdmin,bg=color_barra_superior)
        borde_superior.pack(side=tk.TOP, fill='both',expand=False)
        labelAdmin=tk.Label(borde_superior,text="Panel de Administracion",font=("Roboto",15),bg=color_barra_superior,fg="white")
        labelAdmin.pack(side=tk.LEFT,fill='both',expand=False)

    
        # Frame para intruducir contraseña
        frame_contraseña = tk.Frame(panelAdmin, bg=color_cuerpo_principal)
        frame_contraseña.pack(side=tk.TOP, fill='both', expand=True, pady=20)

        # Campo de entrada para contraseña
        label_password = tk.Label(frame_contraseña, text="Contraseña:", font=('Calibri', 12), bg=color_barra_superior,fg="white", width=20)
        label_password.pack(side=tk.TOP,fill='both',expand=False,padx=5,pady=5)
        self.entry_password = tk.Entry(frame_contraseña, font=('Calibri', 12),bg=color_cuerpo_principal,fg="black", show="*")
        self.entry_password.pack(side=tk.TOP,fill='both',expand=False,padx=5,pady=5)

        # Botón para validar credenciales
        self.btn_login = tk.Button(frame_contraseña, text="Ingresar", font=('Calibri', 12), command=self.validar_credenciales)
        self.btn_login.pack(side=tk.TOP,fill='both',expand=False,padx=5,pady=5)

        # Frame para nombre de máquina
        frame_nombre_maquina = tk.Frame(panelAdmin, bg=color_cuerpo_principal)
        frame_nombre_maquina.pack(side=tk.TOP, fill='both', expand=True, pady=10)

        label_nombre = tk.Label(frame_nombre_maquina, text="Nombre de esta máquina:", font=('Calibri', 12), bg=color_barra_superior, fg="white", width=20)
        label_nombre.pack(side=tk.TOP, fill='both', expand=False, padx=5, pady=5)
        self.entry_nombre_maquina = tk.Entry(frame_nombre_maquina, font=('Calibri', 12), bg=color_cuerpo_principal, fg="black")
        self.entry_nombre_maquina.pack(side=tk.TOP, fill='both', expand=False, padx=5, pady=5)

        # Cargar nombre guardado si existe
        nombre_guardado = self.config.get("nombre_maquina", "")
        if nombre_guardado:
            self.entry_nombre_maquina.insert(0, nombre_guardado)

        # Label para mostrar el nombre actual de la máquina
        self.label_nombre_actual = tk.Label(
            frame_nombre_maquina,
            text=f"Nombre actual: {nombre_guardado}",
            font=('Calibri', 11, 'italic'),
            bg=color_cuerpo_principal,
            fg="gray"
        )
        self.label_nombre_actual.pack(side=tk.TOP, fill='both', expand=False, padx=5, pady=2)

        # Botón para guardar nombre
        self.btn_guardar_nombre = tk.Button(
            frame_nombre_maquina,
            text="Guardar nombre",
            font=('Calibri', 12),
            command=self.guardar_nombre_maquina
        )
        self.btn_guardar_nombre.pack(side=tk.TOP, fill='both', expand=False, padx=5, pady=5)


    def validar_credenciales(self):
        # Credenciales fijas
        contrasena_correcta = "1234"

        # Obtener valores ingresados
        contrasena = self.entry_password.get()

        # Validar credenciales
        if  contrasena == contrasena_correcta:
            app_state.set_admin(True)
            tk.messagebox.showinfo("Acceso permitido", "¡Bienvenido al panel de administración!")
        else:
            app_state.set_admin(False)
            tk.messagebox.showerror("Acceso denegado", "Usuario o contraseña incorrectos.")

    def guardar_nombre_maquina(self):
        nombre = self.entry_nombre_maquina.get().strip()
        if not nombre:
            tk.messagebox.showerror("Error", "Debe ingresar un nombre para la máquina.")
            return
        self.config["nombre_maquina"] = nombre
        # Actualiza el label con el nuevo nombre
        self.label_nombre_actual.config(text=f"Nombre actual: {nombre}")
        tk.messagebox.showinfo("Guardado", f"Nombre de máquina guardado: {nombre}")

def guardar_configuracion(config):
    with open(CONFIG_PATH, "w", encoding="utf-8") as f:
        json.dump(config, f, indent=4)

def cargar_configuracion():
    if not os.path.exists(CONFIG_PATH):
        guardar_configuracion(DEFAULT_CONFIG)
        return DEFAULT_CONFIG.copy()
    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        return json.load(f)
    
