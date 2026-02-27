import tkinter as tk
from tkinter import messagebox
from Utilitys.util_config import color_cuerpo_principal, color_barra_superior, color_menu_lateral


class SettingsView:
    def __init__(self, parent, controlador, nombre_actual):
        self.controlador = controlador
        
        self.subcuerpo = tk.Frame(parent, bg=color_barra_superior)
        self.subcuerpo.pack(side=tk.TOP, fill='both', expand=True)

        self._construir_ui(nombre_actual)

    def _construir_ui(self, nombre_actual):
        panelAdmin = tk.Frame(self.subcuerpo, bg=color_menu_lateral)
        panelAdmin.pack(side=tk.TOP, fill='both', expand=True)
        
        borde_superior = tk.Frame(panelAdmin, bg=color_barra_superior)
        borde_superior.pack(side=tk.TOP, fill='both', expand=False)
        labelAdmin = tk.Label(borde_superior, text="Panel de Administracion", font=("Roboto", 15), bg=color_barra_superior, fg="white")
        labelAdmin.pack(side=tk.LEFT, fill='both', expand=False)

        # --- Frame Contraseña ---
        frame_contrasena = tk.Frame(panelAdmin, bg=color_cuerpo_principal)
        frame_contrasena.pack(side=tk.TOP, fill='both', expand=True, pady=20)

        label_password = tk.Label(frame_contrasena, text="Contraseña:", font=('Calibri', 12), bg=color_barra_superior, fg="white", width=20)
        label_password.pack(side=tk.TOP, fill='both', expand=False, padx=5, pady=5)
        
        self.entry_password = tk.Entry(frame_contrasena, font=('Calibri', 12), bg=color_cuerpo_principal, fg="black", show="*")
        self.entry_password.pack(side=tk.TOP, fill='both', expand=False, padx=5, pady=5)
        self.entry_password.bind("<Return>", lambda event: self.controlador.validar_credenciales())


        self.btn_login = tk.Button(frame_contrasena, text="Ingresar", font=('Calibri', 12), command=self.controlador.validar_credenciales)
        self.btn_login.pack(side=tk.TOP, fill='both', expand=False, padx=5, pady=5)

        # --- Frame Nombre Máquina ---
        frame_nombre_maquina = tk.Frame(panelAdmin, bg=color_cuerpo_principal)
        frame_nombre_maquina.pack(side=tk.TOP, fill='both', expand=True, pady=10)

        label_nombre = tk.Label(frame_nombre_maquina, text="Nombre de esta máquina:", font=('Calibri', 12), bg=color_barra_superior, fg="white", width=20)
        label_nombre.pack(side=tk.TOP, fill='both', expand=False, padx=5, pady=5)
        
        self.entry_nombre_maquina = tk.Entry(frame_nombre_maquina, font=('Calibri', 12), bg=color_cuerpo_principal, fg="black")
        self.entry_nombre_maquina.pack(side=tk.TOP, fill='both', expand=False, padx=5, pady=5)

        # Cargar nombre inicial en el input
        if nombre_actual:
            self.entry_nombre_maquina.insert(0, nombre_actual)

        self.label_nombre_actual = tk.Label(frame_nombre_maquina, text=f"Nombre actual: {nombre_actual}", font=('Calibri', 11, 'italic'), bg=color_cuerpo_principal, fg="gray")
        self.label_nombre_actual.pack(side=tk.TOP, fill='both', expand=False, padx=5, pady=2)

        self.btn_guardar_nombre = tk.Button(frame_nombre_maquina, text="Guardar nombre", font=('Calibri', 12), command=self.controlador.guardar_nombre)
        self.btn_guardar_nombre.pack(side=tk.TOP, fill='both', expand=False, padx=5, pady=5)

    # --- Métodos de acceso para el Controlador ---
    def get_password(self):
        return self.entry_password.get()

    def limpiar_password(self):
        self.entry_password.delete(0, tk.END)

    def get_nombre_maquina(self):
        return self.entry_nombre_maquina.get().strip()

    def actualizar_label_nombre(self, nuevo_nombre):
        self.label_nombre_actual.config(text=f"Nombre actual: {nuevo_nombre}")
    
    def mostrar_mensaje(self, tipo, titulo, mensaje):
        """Muestra un cuadro de diálogo general según el tipo solicitado."""
        if tipo == "info":
            messagebox.showinfo(titulo, mensaje)
        elif tipo == "error":
            messagebox.showerror(titulo, mensaje)
        elif tipo == "warning":
            messagebox.showwarning(titulo, mensaje)
        
        else:
            messagebox.showinfo(titulo, mensaje)