import tkinter as tk
from tkinter import messagebox
from tkinter import font

from Utilitys.util_config import color_barra_superior,color_cuerpo_principal,color_menu_cursor_encima,color_menu_lateral
import Utilitys.util_ventana as util_ventana
import Utilitys.util_images as util_img
from Utilitys.util_gestorimagenes import GestorImagenes as gi



# class MainView(tk.Tk):

#     def __init__(self):
#         super().__init__()

       
#         self.logo = util_img.leer_imagen("./Images/Logo.png",(300,300))
#         self.img_construccion = util_img.leer_imagen("./Images/Construccion.png",(220,220))

#         #Iconos
#         self.caja = util_img.leer_imagen("./Images/Caja.png",(40,40))
#         self.calculate = util_img.leer_imagen("./Images/Calculate.png",(40,40))
#         self.Empleados = util_img.leer_imagen("./Images/Empleados.png",(40,40))
#         self.Graph = util_img.leer_imagen("./Images/Graph.png",(40,40))
#         self.Info = util_img.leer_imagen("./Images/Info.png",(40,40))
#         self.Setting = util_img.leer_imagen("./Images/Setting.png",(40,40))
#         self.Nube = util_img.leer_imagen("./Images/Nube.png",(40,40))
#         self.Menu = util_img.leer_imagen("./Images/Menu.png",(40,40))
#         self.Lista = util_img.leer_imagen("./Images/Lista.png",(40,40))

 

#         #iconos para empleados
#         self.add= util_img.leer_imagen("./Images/add.png",(60,60))
#         self.delete=util_img.leer_imagen("./Images/Erase.png",(60,60))
#         self.edit= util_img.leer_imagen("./Images/edit.png",(60,60))
#         self.consulta= util_img.leer_imagen("./Images/consulta.png",(60,60))
        
#         #icono admin
#         self.On = util_img.leer_imagen("./Images/On.png",(20,20))
#         self.Off = util_img.leer_imagen("./Images/Off.png",(20,20))  

#         #Carga las ventanas
#         self.config_window()
#         self.paneles()
#         self.controles_barra_superior()
#         self.controles_menu_iconos()
#         self.controles_menu_lateral()
#         self.controles_cuerpo()
class MainView:
    # 1. Ya no hereda de tk.Tk. Ahora recibe la ventana (root) y el cerebro (controlador)
    def __init__(self, root, controlador):
        self.root = root
        self.controlador = controlador
        self.root.minsize(1500, 900)
        
        # 2. Carga SOLO las imágenes que esta vista necesita, usando el Gestor
        self.logo = gi.obtener_imagen("logo", "./Images/Logo.png", (300,300))
        self.MenuIcon = gi.obtener_imagen("menu", "./Images/Menu.png", (30,30))
        
        # Iconos Menu
        self.caja = gi.obtener_imagen("caja", "./Images/Caja.png", (40,40))
        self.Lista = gi.obtener_imagen("lista", "./Images/Lista.png", (40,40))
        self.Empleados = gi.obtener_imagen("empleados", "./Images/Empleados.png", (40,40))
        self.Graph = gi.obtener_imagen("graph", "./Images/Graph.png", (40,40))
        self.Info = gi.obtener_imagen("info", "./Images/Info.png", (40,40))
        self.Setting = gi.obtener_imagen("setting", "./Images/Setting.png", (40,40))
        
        # Iconos Admin
        self.On = gi.obtener_imagen("on", "./Images/On.png", (20,20))
        self.Off = gi.obtener_imagen("off", "./Images/Off.png", (20,20))  

        # 3. Construye la interfaz
        self.config_window()
        self.paneles()
        self.controles_barra_superior()
        self.controles_menu_iconos()
        self.controles_menu_lateral()
        self.controles_cuerpo()

    def config_window(self):
        # Todo lo que antes era "self." para la ventana, ahora es "self.root."
        self.root.title("Gestion CEI")
        self.root.icono = tk.PhotoImage(file="./Images/ICONO.png")
        self.root.iconphoto(True, self.root.icono)
        w, h = 1024, 600
        self.root.geometry("%dx%d+0+0" % (w, h))
        self.root.state('zoomed')
        util_ventana.centrar_ventana(self.root, w, h)
    
    def paneles(self):
        # Los paneles ahora se adhieren a self.root
        self.barra_superior = tk.Frame(self.root, bg=color_barra_superior, height=50)
        self.barra_superior.pack(side=tk.TOP, fill='both')

        self.menu_iconos = tk.Frame(self.root, bg=color_menu_lateral, width=50)
        self.menu_iconos.pack(side=tk.LEFT, fill='both', expand=False)

        self.menu_lateral = tk.Frame(self.root, bg=color_menu_lateral, width=100)
        self.menu_lateral.pack(side=tk.LEFT, fill='both', expand=False)

        self.cuerpo_principal = tk.Frame(self.root, bg=color_cuerpo_principal)
        self.cuerpo_principal.pack(side=tk.RIGHT, fill='both', expand=True)

    def controles_barra_superior(self):
        self.frame_admin = tk.Frame(self.barra_superior, bg=color_barra_superior)
        self.frame_admin.pack(side=tk.RIGHT, fill='both', expand=False)
        
        self.frame_Menu = tk.Frame(self.barra_superior, bg=color_barra_superior)
        self.frame_Menu.pack(side=tk.LEFT, fill='both', expand=False)
        
        font_awesome = font.Font(family='FontAwesome', size=12)

        # Botón de menú lateral (Este se queda en la vista porque es 100% visual)
        self.buttonMenuLateral = tk.Button(self.frame_Menu, image=self.MenuIcon, font=font_awesome, command=self.toggle_panel, bd=0, bg=color_barra_superior, fg="white", padx=10, width=60)
        self.buttonMenuLateral.pack(side=tk.LEFT)
        
        self.label_Menu = tk.Label(self.frame_Menu, text="Menu", fg="#fff", font=("Roboto",15), bg=color_barra_superior, pady=5, width=5)
        self.label_Menu.pack(side=tk.LEFT)
        
        self.label_Mail = tk.Label(self.frame_Menu, text="impresiones_cei@fi.mdp.edu.ar", fg="#fff", font=("Roboto",10), bg=color_barra_superior, padx=10, width=25)
        self.label_Mail.pack(side=tk.RIGHT, fill='both', expand=False)
        
        # Botón off (Este delega la lógica al controlador)
        self.button_on_off = tk.Button(self.frame_admin, image=self.Off, font=font_awesome, command=self.controlador.log_in_out, bd=0, bg=color_barra_superior, fg="white", padx=10, width=60)
        self.button_on_off.pack(side=tk.RIGHT)
        
        self.label_Modo = tk.Label(self.frame_admin, text="Modo: Empleados", fg="#fff", font=("Roboto",10), bg=color_barra_superior, padx=5)
        self.label_Modo.pack(side=tk.RIGHT, fill='both', expand=False)

    def controles_menu_iconos(self):
        ancho_menu, alto_menu = 60, 57
        
        # self.buttonCaja1 = tk.Button(self.menu_iconos)
        # self.buttonProductos1 = tk.Button(self.menu_iconos)
        self.buttonEmpleados1 = tk.Button(self.menu_iconos)
        self.buttonEstadisticas1 = tk.Button(self.menu_iconos)
        self.buttonInfo1 = tk.Button(self.menu_iconos)
        self.buttonSettings1 = tk.Button(self.menu_iconos)

        # 4. Los comandos ahora apuntan a self.controlador
        iconos_info = [
            # (self.caja, self.buttonCaja1, self.controlador.abrir_panel_store),
            # (self.Lista, self.buttonProductos1, self.controlador.abrir_panel_products),
            (self.Empleados, self.buttonEmpleados1, self.controlador.abrir_panel_empleados),
            (self.Graph, self.buttonEstadisticas1, self.controlador.open_statistics_panel),
            (self.Info, self.buttonInfo1, self.controlador.abrir_panel_info),
            (self.Setting, self.buttonSettings1, self.controlador.abrir_panel_setting)
        ]
        for image, button, comando in iconos_info:
            self.configurar_boton_icono(button, image, ancho_menu, alto_menu, comando) 

    def controles_menu_lateral(self):
        ancho_menu, alto_menu = 10, 2
        font_awesome = font.Font(family='FontAwesome', size=15)
        
        # self.buttonCaja = tk.Button(self.menu_lateral)
        # self.buttonProductos = tk.Button(self.menu_lateral)
        self.buttonEmpleados = tk.Button(self.menu_lateral)
        self.buttonEstadisticas = tk.Button(self.menu_lateral)
        self.buttonInfo = tk.Button(self.menu_lateral)
        self.buttonSettings = tk.Button(self.menu_lateral)

        buttons_info = [
        #     ("Caja", self.buttonCaja, self.controlador.abrir_panel_store),
        #     ("Productos", self.buttonProductos, self.controlador.abrir_panel_products),
            ("Empleados", self.buttonEmpleados, self.controlador.abrir_panel_empleados),
            ("Estadisticas", self.buttonEstadisticas, self.controlador.open_statistics_panel),
            ("Info", self.buttonInfo, self.controlador.abrir_panel_info),
            ("Settings", self.buttonSettings, self.controlador.abrir_panel_setting)
        ]

        for text, button, comando in buttons_info:
            self.configurar_boton_menu(button, text, font_awesome, ancho_menu, alto_menu, comando)

    def controles_cuerpo(self):
        label = tk.Label(self.cuerpo_principal, image=self.logo, bg=color_cuerpo_principal)
        label.place(x=0, y=0, relwidth=1, relheight=1)

    # --- MÉTODOS VISUALES (Se quedan en la Vista) ---
    def configurar_boton_menu(self, button, text, font_awesome, ancho_menu, alto_menu, comando):
        button.config(text=f"{text}", compound="left", anchor="w", font=font_awesome, bd=0, bg=color_menu_lateral, fg="white", width=ancho_menu, height=alto_menu, command=comando)
        if text == "Info":
            button.pack(side=tk.BOTTOM)
        else:
            button.pack(side=tk.TOP)
        self.bind_hover_events(button)

    def configurar_boton_icono(self, button, imagen, ancho_menu, alto_menu, comando):
        button.config(image=imagen, bd=0, bg=color_menu_lateral, fg="white", width=ancho_menu, height=alto_menu, command=comando)
        if imagen == self.Info:
            button.pack(side=tk.BOTTOM)
        else:
            button.pack(side=tk.TOP)
        self.bind_hover_events(button)

    def bind_hover_events(self, button):
        button.bind("<Enter>", lambda event: self.on_enter(event, button))
        button.bind("<Leave>", lambda event: self.on_leave(event, button))
    
    def on_enter(self, event, button):
        button.config(bg=color_menu_cursor_encima, fg="black")

    def on_leave(self, event, button):
        button.config(bg=color_menu_lateral, fg='white')

    def toggle_panel(self):
        if self.menu_lateral.winfo_ismapped():
            self.menu_lateral.pack_forget()
        else:
            self.menu_lateral.pack(side=tk.LEFT, fill='y')

    # --- MÉTODO PARA QUE EL CONTROLADOR ACTUALICE LA UI ---
    def actualizar_ui_admin(self, es_admin):
        """
        Se ejecuta automáticamente cuando app_state.set_admin() es llamado
        (ya sea con True o False).
        """
        if es_admin:
             self.label_Modo.config(text="Modo: Administrador")
             self.button_on_off.config(image=self.On)
        else:
            self.label_Modo.config(text="Modo: Empleados")
            self.button_on_off.config(image=self.Off)
    