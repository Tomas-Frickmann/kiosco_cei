from datetime import datetime
import json
import os

from Utilitys.util_config import *
import Datos.Connect as db




"""No entiendo la utilidad del JSON
    Qué son los extra?
"""
class MainModel:
    def __init__(self):
        self._es_admin = False
        self.ventas_global = [] 
        self._observadores = []
        
        self.dnis_activos = []
        self.dnis_activos_extra = []
        self.tiempo_activo = []
        self.tiempo_activo_extra = []
        self.hora_entrada = []
        self.hora_entrada_extra = []
        self.motivo_extra = []
        
        # --- NUEVO: Gestión de la configuración absorbida ---
        self.config_path = "config_maquina.json"
        self.config_data = self.cargar_configuracion()
        db.crear_tabla()

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
            
    def validar_password(self, password_ingresada):
        contrasena_correcta = "1234"
        return password_ingresada == contrasena_correcta
    
    # En tu Modelo:
    def esta_activo(self, dni):
        return dni in self.dnis_activos
    
    
    def actualiza_lista_activos(self,dni,accion,extra=False):
        
        index = self.dnis_activos.index(dni) 
       
        if accion == DELETE and extra==False:
            self.dnis_activos.pop(index)
            self.tiempo_activo.pop(index)  # Eliminar el tiempo correspondiente
            self.hora_entrada.pop(index)  # Eliminar la hora de entrada correspondiente
            
        elif accion == DELETE and extra==True:
            
            self.dnis_activos_extra.pop(index)
            self.tiempo_activo_extra.pop(index)  # Eliminar el tiempo correspondiente
            self.hora_entrada_extra.pop(index)  # Eliminar la hora de entrada correspondiente
            self.motivo_extra.pop(index)  # Eliminar el motivo correspondiente
            
        elif accion == ADD and extra==False:
            
            self.dnis_activos.append(dni)
            self.tiempo_activo.append("00:00")  # Inicializar el tiempo activo
            self.hora_entrada.append(datetime.now().strftime("%H:%M:%S"))  # Guardar la hora de entrada
            self.actualizar_tiempo_activo()
            
    def registro_permitido(self):
        return len(self.dnis_activos) < 2