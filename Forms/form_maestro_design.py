import tkinter as tk
from tkinter import messagebox
from tkinter import font
from Forms.form_login_out import FormularioLogin 
from config import color_barra_superior,color_cuerpo_principal,color_menu_cursor_encima,color_menu_lateral
import Utilitys.util_ventana as util_ventana
import Utilitys.util_images as util_img
from Forms.form_info_design import FormularioInfoDesign
from Forms.form_construccion import FormularioSitioContruccionDesign
from Forms.form_empleados import PanelEmpleados
from Forms.form_setting import Setting, app_state
from Forms.form_products import PanelProducts
from Forms.form_store import PanelStore

class FormularioMaestroDesign(tk.Tk):

    def __init__(self):
        super().__init__()

        #Variable globales
        self.ventas_global=[]

        #Carga todos los iconos e imagenes
        #Fondos
        self.logo = util_img.leer_imagen("./Images/Logo.png",(300,300))
        self.img_construccion = util_img.leer_imagen("./Images/Construccion.png",(220,220))

        #Iconos
        self.caja = util_img.leer_imagen("./Images/Caja.png",(40,40))
        self.calculate = util_img.leer_imagen("./Images/Calculate.png",(40,40))
        self.Empleados = util_img.leer_imagen("./Images/Empleados.png",(40,40))
        self.Graph = util_img.leer_imagen("./Images/Graph.png",(40,40))
        self.Info = util_img.leer_imagen("./Images/Info.png",(40,40))
        self.Setting = util_img.leer_imagen("./Images/Setting.png",(40,40))
        self.Nube = util_img.leer_imagen("./Images/Nube.png",(40,40))
        self.Menu = util_img.leer_imagen("./Images/Menu.png",(40,40))
        self.Lista = util_img.leer_imagen("./Images/Lista.png",(40,40))

 

        #iconos para empleados
        self.add= util_img.leer_imagen("./Images/add.png",(60,60))
        self.delete=util_img.leer_imagen("./Images/Erase.png",(60,60))
        self.edit= util_img.leer_imagen("./Images/edit.png",(60,60))
        self.consulta= util_img.leer_imagen("./Images/consulta.png",(60,60))
        
        #icono admin
        self.On = util_img.leer_imagen("./Images/On.png",(20,20))
        self.Off = util_img.leer_imagen("./Images/Off.png",(20,20))  

        #Carga las ventanas
        self.config_window()
        self.paneles()
        self.controles_barra_superior()
        self.controles_menu_iconos()
        self.controles_menu_lateral()
        self.controles_cuerpo()
        
        


    def config_window(self):
        #Configuracion Inicial de la ventana
        self.title("Gestion CEI")
        self.icono = tk.PhotoImage(file="./Images/ICONO.png")  # Usa PNG para PhotoImage
        self.iconphoto(True, self.icono)
        w, h = 1024, 600
        self.geometry("%dx%d+0+0"%(w,h))
        self.state('zoomed')  # Abrir la ventana maximizada
        util_ventana.centrar_ventana(self , w , h)
    
    def paneles(self):
        #Cear paneles: Barra superior, Menu lateral y cuerpo principal
        self.barra_superior = tk.Frame(self, bg = color_barra_superior, height=50)#el height 50 es que entran 50 caracteres
        self.barra_superior.pack(side=tk.TOP,fill='both')

        #Donde estan los iconos
        self.menu_iconos = tk.Frame(self, bg=color_menu_lateral,width=50)
        self.menu_iconos.pack(side=tk.LEFT,fill='both',expand=False)

        #Donde estan los nombres
        self.menu_lateral = tk.Frame(self,bg = color_menu_lateral ,width=100)
        self.menu_lateral.pack(side=tk.LEFT,fill='both',expand=False)

        #Donde se muestran las ventanas
        self.cuerpo_principal =  tk.Frame(self, bg= color_cuerpo_principal)
        self.cuerpo_principal.pack(side=tk.RIGHT,fill='both',expand=True)

    def controles_barra_superior(self):
        self.frame_admin = tk.Frame(self.barra_superior,bg=color_barra_superior)
        self.frame_admin.pack(side=tk.RIGHT,fill='both',expand=False)
        
        self.frame_Menu = tk.Frame(self.barra_superior,bg=color_barra_superior)
        self.frame_Menu.pack(side=tk.LEFT,fill='both',expand=False)
        #Configuracion de la barra superior
        font_awesome =font.Font(family='FontAwesome',size=12)

        #boton de menu lateral
        self.MenuIcon= util_img.leer_imagen("./Images/Menu.png",(30,30))
        self.buttonMenuLateral =tk.Button(self.frame_Menu,image=self.MenuIcon,font=font_awesome,command=self.toggle_panel,bd=0, bg=color_barra_superior, fg="white",padx=10,width=60)
        self.buttonMenuLateral.pack(side=tk.LEFT)

        
        
        #etiqueta de titulo
        self.label_Menu = tk.Label(self.frame_Menu,text="Menu")
        self.label_Menu.config(fg="#fff",font=("Roboto",15),bg=color_barra_superior, pady=5,width=5)
        self.label_Menu.pack(side=tk.LEFT)
        
       
        #Etiqueta de informacion
        self.label_Mail=tk.Label(self.frame_Menu,text="impresiones_cei@fi.mdp.edu.ar")
        self.label_Mail.config(fg="#fff",font=("Roboto",10),bg=color_barra_superior,padx=10,width=25)
        self.label_Mail.pack(side=tk.RIGHT,fill='both',expand=False)
        
        #Admin on/off
        
        #boton off
        self.button_on_off =tk.Button(self.frame_admin,image=self.Off,font=font_awesome,command=self.log_in_out,bd=0, bg=color_barra_superior, fg="white",padx=10,width=60)
        self.button_on_off.pack(side=tk.RIGHT)
        
        #texto de modo:
        
        self.label_Modo=tk.Label(self.frame_admin,text="Modo: Empleados")
        self.label_Modo.config(fg="#fff",font=("Roboto",10),bg=color_barra_superior,padx=5)
        self.label_Modo.pack(side=tk.RIGHT,fill='both',expand=False)
        app_state.add_observer(self.update_admin_icon)


   
    def log_in_out(self):
        
        if app_state.is_admin:
            app_state.set_admin(False)           
            messagebox.showinfo("Sesión Cerrada", "Modo empleado activado.")
        else:
            FormularioLogin(self)
            


    def update_admin_icon(self):
        """
        Se ejecuta automáticamente cuando app_state.set_admin() es llamado
        (ya sea con True o False).
        """
        if app_state.is_admin:
             self.label_Modo.config(text="Modo: Administrador")
             self.button_on_off.config(image=self.On)
        else:
            self.label_Modo.config(text="Modo: Empleados")
            self.button_on_off.config(image=self.Off)


##logica de botones laterales 

    def controles_menu_iconos(self):
        #Configuracion de los iconos
        ancho_menu= 60
        alto_menu= 57
        #Botones
        self.buttonCaja1 = tk.Button(self.menu_iconos)
        self.buttonProductos1 = tk.Button(self.menu_iconos)
        self.buttonEmpleados1 = tk.Button(self.menu_iconos)
        self.buttonEstadisticas1 = tk.Button(self.menu_iconos)
        self.buttonInfo1 = tk.Button(self.menu_iconos)
        self.buttonSettings1 = tk.Button(self.menu_iconos)

        iconos_info =[
            (self.caja, self.buttonCaja1,self.abrir_panel_store),
            (self.Lista,self.buttonProductos1,self.abrir_panel_products),
            (self.Empleados,self.buttonEmpleados1,self.abrir_panel_empleados),
            (self.Graph,self.buttonEstadisticas1,self.abrir_panel_contruccion),
            (self.Info,self.buttonInfo1,self.abrir_panel_info),
            (self.Setting,self.buttonSettings1,self.abrir_panel_setting)
        ]
        for image, button, comando in iconos_info:
            self.configurar_boton_icono(button,image,ancho_menu,alto_menu,comando) 

    def controles_menu_lateral(self):
        #Configuracion del menu lateral
        ancho_menu= 10
        alto_menu= 2
        font_awesome=font.Font(family='FontAwesome',size=15)
        
        #Botones del menu lateral
        self.buttonCaja = tk.Button(self.menu_lateral)
        self.buttonProductos = tk.Button(self.menu_lateral)
        self.buttonEmpleados = tk.Button(self.menu_lateral)
        self.buttonEstadisticas = tk.Button(self.menu_lateral)
        self.buttonInfo = tk.Button(self.menu_lateral)
        self.buttonSettings = tk.Button(self.menu_lateral)

        buttons_info = [
            ("Caja", self.buttonCaja,self.abrir_panel_store),
            ("Productos",self.buttonProductos,self.abrir_panel_products),
            ("Empleados",self.buttonEmpleados,self.abrir_panel_empleados),
            ("Estadisticas",self.buttonEstadisticas,self.abrir_panel_contruccion),
            ("Info",self.buttonInfo,self.abrir_panel_info),
            ("Settings",self.buttonSettings,self.abrir_panel_setting)
        ]

        for text,button, comando in buttons_info:
            self.configurar_boton_menu(button,text,font_awesome,ancho_menu,alto_menu,comando)

    def controles_cuerpo(self):
        #Imagen en el cuerpo principal
        label =tk.Label(self.cuerpo_principal, image=self.logo,bg=color_cuerpo_principal)
        label.place(x=0,y=0,relwidth=1,relheight=1)

    def configurar_boton_menu(self,button,text,font_awesome,ancho_menu,alto_menu,comando):
        
        button.config(text=f"{text}",compound="left", anchor="w", font=font_awesome, bd=0, bg=color_menu_lateral, fg="white", width=ancho_menu, height=alto_menu, command = comando)
        if text == "Info":
            button.pack(side=tk.BOTTOM)
        else:
            button.pack(side=tk.TOP)
        self.bind_hover_events(button)

    def configurar_boton_icono(self,button,imagen,ancho_menu,alto_menu,comando):
        button.config(image=imagen,bd=0,bg=color_menu_lateral,fg="white",width=ancho_menu,height=alto_menu,command =comando)
        if imagen == self.Info:
            button.pack(side=tk.BOTTOM)
        else:
            button.pack(side=tk.TOP)
        self.bind_hover_events(button)

    def bind_hover_events(self,button):
        #Asociar eventos Enter y Leave con la funcion dinamica
        button.bind("<Enter>", lambda event: self.on_enter(event, button))
        button.bind("<Leave>", lambda event: self.on_leave(event, button))
    
    def on_enter(self,event,button):
        #cambiar el estilo al pasar el raton por encima
        button.config(bg=color_menu_cursor_encima, fg="black")

    def on_leave(self,event,button):
        #Restaurar estilo al salir el raton
        button.config(bg=color_menu_lateral, fg='white')

    def toggle_panel(self):
        #Alternar visibilidad del menu lateral
        if self.menu_lateral.winfo_ismapped():
            self.menu_lateral.pack_forget()
        else:
            self.menu_lateral.pack(side=tk.LEFT,fill='y')

    def abrir_panel_info(self):
        FormularioInfoDesign()

    def abrir_panel_contruccion(self):
        self.limpiar_panel(self.cuerpo_principal)
        FormularioSitioContruccionDesign(self.cuerpo_principal,self.img_construccion)

    def limpiar_panel(self,panel):
        for widget in panel.winfo_children():
            widget.destroy()

    def abrir_panel_empleados(self):
        self.limpiar_panel(self.cuerpo_principal)
        PanelEmpleados(self,self.cuerpo_principal,self.add,self.delete,self.edit,self.consulta)
                       
    def abrir_panel_setting(self):
        self.limpiar_panel(self.cuerpo_principal)
        Setting(self.cuerpo_principal)

    def abrir_panel_products(self):
        self.limpiar_panel(self.cuerpo_principal)
        PanelProducts(self.cuerpo_principal)

    def abrir_panel_store(self):
        self.limpiar_panel(self.cuerpo_principal)
        PanelStore(self.cuerpo_principal,self.ventas_global)