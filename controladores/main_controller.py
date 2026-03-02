from tkinter import messagebox
from controladores.employee_controller import EmployeeController
from controladores.store_contrller import StoreController
from vistas.main_view import MainView 
from controladores.login_controller import LoginController
from vistas.info_view import InfoView



from modelos.main_model import MainModel
from controladores.settings_controller import SettingsController
from controladores.statistics_controller import StatisticsController
from vistas.form_store_view import StoreView

# from Forms.form_construccion import FormularioSitioContruccionDesign
from vistas.employee_view import EmployeeView
# from Forms.form_products import PanelProducts
# from Forms.form_store import PanelStore

class MainController:
    def __init__(self, root):
        
        self.root = root
        self.ventas_global=[] 
        self.modelo = MainModel()
        self.vista = MainView(self.root, self)
        self.MainBody = self.vista.cuerpo_principal
        self.ventana_info = None
        self.modelo.agregar_observador(self.vista.actualizar_ui_admin)
        self.controlador_actual=None
        
        
    
        

    def abrir_panel_info(self):
       
        if self.ventana_info is None or not self.ventana_info.winfo_exists():
           
            self.ventana_info = InfoView()
        else:
           
            self.ventana_info.lift()
            
    def open_statistics_panel(self):
        self.limpiar_panel(self.vista.cuerpo_principal)
        self.controlador_actual=StatisticsController(self.vista.cuerpo_principal, self.modelo)

    def limpiar_panel(self,panel):
        for widget in panel.winfo_children():
            widget.destroy()

    def abrir_panel_empleados(self):
        self.limpiar_panel(self.vista.cuerpo_principal)
        self.controlador_actual=EmployeeController(self.root, self.vista.cuerpo_principal, self.modelo)
                       


    # def abrir_panel_products(self):
    #     self.limpiar_panel(self.vista.cuerpo_principal)
    #     PanelProducts(self.vista.cuerpo_principal)

    def abrir_panel_store(self):
        self.limpiar_panel(self.vista.cuerpo_principal)     
        self.controlador_actual=StoreController(self.root, self.vista.cuerpo_principal, self.modelo)
        
    def log_in_out(self):
        
        if self.modelo.es_admin:
            self.modelo.set_admin(False)
            messagebox.showinfo("Sesión Cerrada", "Modo empleado activado.")
        else:
            self.controlador_actual=LoginController(self.MainBody, self.modelo)
            
    def abrir_panel_setting(self):
        self.limpiar_panel(self.MainBody)
        # En lugar de instanciar el formulario viejo, levantamos el controlador nuevo
        # Le inyectamos el espacio de trabajo (MainBody) y nuestra base de datos en memoria (modelo)
        self.controlador_actual=SettingsController(self.MainBody, self.modelo)
    