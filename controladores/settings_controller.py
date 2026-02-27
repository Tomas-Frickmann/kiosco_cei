
from modelos.main_model import MainModel
from vistas.setting_view import SettingsView

class SettingsController:
    def __init__(self, parent, main_modelo: MainModel):
        self.main_modelo = main_modelo
        
        # Leemos el nombre actual directamente de nuestro MainModel
        nombre_actual = self.main_modelo.config_data.get("nombre_maquina", "SIN_NOMBRE")
        
        # Instanciamos la vista pasándole el contenedor, a sí mismo, y el dato inicial
        self.vista = SettingsView(parent, self, nombre_actual)

   
        
    def validar_credenciales(self):
        
        contrasena = self.vista.get_password()
       
        
        if self.main_modelo.validar_password(contrasena):
           
            self.main_modelo.set_admin(True)
            
            self.vista.mostrar_mensaje("info","Acceso permitido", "¡Bienvenido al panel de administración!")
        else:
            self.main_modelo.set_admin(False)
            self.vista.mostrar_mensaje("error","Acceso denegado", "Usuario o contraseña incorrectos.")
        
        
        self.vista.limpiar_password()
        
    def guardar_nombre(self):
        nombre = self.vista.get_nombre_maquina()
        
        if not nombre:
            self.vista.mostrar_mensaje("error","Error", "Debe ingresar un nombre para la máquina.")
            return
        
        # 1. Le decimos al modelo que guarde físicamente el cambio en el JSON
        nueva_config = {"nombre_maquina": nombre}
        self.main_modelo.guardar_configuracion(nueva_config)
        
        # 2. Le decimos a la vista que refresque la etiqueta visual
        self.vista.actualizar_label_nombre(nombre)
        self.vista.mostrar_mensaje("info","Guardado", f"Nombre de máquina guardado: {nombre}")