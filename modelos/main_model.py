import json
import os

class MainModel:
    def __init__(self):
        self._es_admin = False
        self.ventas_global = [] 
        self._observadores = []
        
        # --- NUEVO: Gestión de la configuración absorbida ---
        self.config_path = "config_maquina.json"
        self.config_data = self.cargar_configuracion()

    # --- Lógica del JSON ---
    def cargar_configuracion(self):
        """Lee el JSON del disco. Si no existe, devuelve el valor por defecto."""
        if os.path.exists(self.config_path):
            with open(self.config_path, "r") as file:
                return json.load(file)
        return {"nombre_maquina": "SIN_NOMBRE"}

    def guardar_configuracion(self, nueva_config):
        """Actualiza la memoria y guarda en el disco duro."""
        self.config_data.update(nueva_config)
        with open(self.config_path, "w") as file:
            json.dump(self.config_data, file, indent=4)

    # --- Resto del código que ya teníamos (es_admin, observadores, etc.) ---
    @property
    def es_admin(self):
        return self._es_admin
    
    def set_admin(self, estado):
        self._es_admin = estado
        self.notificar_observadores()
        
    def agregar_observador(self, funcion_callback):
        if funcion_callback not in self._observadores:
            self._observadores.append(funcion_callback)

    def notificar_observadores(self):
        for callback in self._observadores:
            callback(self._es_admin)
            
    # Agrega este método en tu MainModel
    def validar_password(self, password_ingresada):
        # Aquí está la regla de negocio real
        contrasena_correcta = "1234"
        return password_ingresada == contrasena_correcta