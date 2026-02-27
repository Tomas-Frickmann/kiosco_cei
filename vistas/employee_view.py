

import tkinter as tk
from tkcalendar import Calendar
from tkinter import filedialog
from fpdf import FPDF
import time
from datetime import datetime,timedelta
from tkinter import messagebox
import Datos.Connect as db
from Utilitys.util_config import color_barra_superior,color_cuerpo_principal,color_menu_cursor_encima,color_menu_lateral,color_iconos2
# from vistas.setting_view import  app_state
from Utilitys.util_gestorimagenes import GestorImagenes as gi
from controladores.employee_controller import EmployeeController

class PanelEmpleados():

    def __init__(self,panel_principal,controlador: EmployeeController):
        
        #Variables iniciales
        self.empleados_activos = []
        self.empleados_activos_extra = []
        self.tiempo_activo = []
        self.tiempo_activo_extra = []
        self.hora_entrada = []
        self.hora_entrada_extra = []
        self.motivo_extra = []
        self.controlador = controlador
       
        #Iconos para panel empleados
        self.agregar= gi.obtener_imagen("add","./Images/add.png",(60,60))
        self.delete=gi.obtener_imagen("delete","./Images/Erase.png",(60,60))
        self.edit=gi.obtener_imagen("edit","./Images/edit.png",(60,60))
        self.consulta=gi.obtener_imagen("consulta","./Images/consulta.png",(60,60))
        
        """El orden importa ya que estamos utilizando tkinker"""
        self.PanelDerecho(panel_principal)
        self.PanelFichaje(panel_principal)
        self.PanelExtra(panel_principal)
        self.PanelEmpleados(panel_principal)

        # Cargar empleados activos desde la base de datos
        self.controlador.cargar_empleados_activos()
       

    def crear_boton_empleado(self, parent, text, image, command):
        frame = tk.Frame(parent, bg=color_barra_superior)
        frame.pack(side=tk.LEFT, fill='both', expand=False) 
        
        button = tk.Button(frame, text=text, font=('Calibri', 12), bg=color_barra_superior, fg="white", command=command)
        button.pack(side=tk.BOTTOM, fill='both', expand=False, padx=5, pady=5)
        label = tk.Label(frame, image=image, bg=color_barra_superior)
        label.pack(side=tk.TOP, fill='both', expand=False, padx=5, pady=5)
        separador =tk.Frame(parent,bg=color_menu_lateral,width=20)
        separador.pack(side=tk.LEFT,fill='both',expand=False)
        return frame   

#Panel y empleados
    def PanelDerecho(self,panel_principal):
        #Modulo para el panel izquierdo
        panel_derecho = tk.Frame(panel_principal,bg=color_menu_lateral)
        panel_derecho.pack(side=tk.RIGHT, fill='both',expand=False)

        borde_sup_sup=tk.Frame(panel_derecho,background=color_barra_superior)
        borde_sup_sup.pack(side=tk.TOP,fill='both',expand=False)
        
        label_sup_sup=tk.Label(borde_sup_sup,text="Empleados",font=("Roboto",15),bg=color_barra_superior,fg="white")
        label_sup_sup.pack(side=tk.TOP,fill='both',expand=False)
        
        #Bordes del panel izquierdo
        borde_der_sup=tk.Frame(panel_derecho,bg=color_menu_lateral,height=20)
        borde_der_sup.pack(side=tk.TOP,fill='both',expand=False)
        
        borde_der_inf=tk.Frame(panel_derecho,bg=color_menu_lateral,height=20)
        borde_der_inf.pack(side=tk.BOTTOM,fill='both',expand=False)
        
        borde_der_der=tk.Frame(panel_derecho,bg=color_menu_lateral,width=20)
        borde_der_der.pack(side=tk.RIGHT,fill='both',expand=False)
        
        borde_der_izq=tk.Frame(panel_derecho,bg=color_menu_lateral,width=20)
        borde_der_izq.pack(side=tk.LEFT,fill='both',expand=True)
        
        #Nueva tabla de empleados
        Frame_empleados = tk.Frame(panel_derecho,bg=color_menu_lateral)
        Frame_empleados.pack(side=tk.TOP,fill='both',expand=False)

        self.frame_nombre=tk.Frame(Frame_empleados,bg=color_menu_lateral,padx=5,pady=2)
        self.frame_nombre.pack(side=tk.LEFT)
        self.frame_dni=tk.Frame(Frame_empleados,bg=color_menu_lateral,padx=5,pady=2)
        self.frame_dni.pack(side=tk.LEFT)

        #Lista de Empleados
        label_empleados=tk.Label(self.frame_dni,text="Empleado",font=('Calibri', 12),bg=color_barra_superior,fg="white",width=20)
        label_empleados.grid(row=0,padx=5,pady=5,sticky="nsew")

        #Lista de los Dni
        label_dni=tk.Label(self.frame_nombre,text="DNI",font=('Calibri', 12),bg=color_barra_superior,fg="white",width=20)
        label_dni.grid(row=0,padx=5,pady=5,sticky="nsew")

        self.TablaEmpleados(self.frame_nombre, self.frame_dni,"nombre")

    def TablaEmpleados(self,frame1,frame2,orden,edicion=False,frame3=None,frame4=None):
        empleados= self.controlador.getEmpleados()
        if orden == "dni":
            empleados.sort(key=lambda x: x[0]) # Ordenar por DNI (segundo elemento de la tupla)
        elif orden == "nombre":
            empleados.sort(key=lambda x: x[1])  # Ordenar por nombre (segundo elemento de la tupla)

        #limpiar listas
        for widget in frame1.winfo_children()[1:]: 
            widget.destroy()
        for widget in frame2.winfo_children()[1:]: 
            widget.destroy()
        if frame3:
            for widget in frame3.winfo_children()[1:]:
                widget.destroy()
            for widget in frame4.winfo_children()[1:]:
                widget.destroy()

        # Configurar el peso de las filas para que todas tengan el mismo alto
        for i in range(len(empleados) + 1):  # +1 para incluir la fila de encabezados
            frame1.grid_rowconfigure(i, weight=1)
            frame2.grid_rowconfigure(i, weight=1)
            if frame3:
                frame3.grid_rowconfigure(i, weight=1)
                frame4.grid_rowconfigure(i, weight=1)

        # Crear filas de empleados y Dni
        for i, (dni, nombre) in enumerate(empleados):
            label_dni = tk.Label(frame1, text=dni, font=('Calibri', 12), anchor="center", background=color_cuerpo_principal)
            label_dni.grid(row=i+1, column=0, sticky="nsew", padx=5, pady=2)
            label_nombre = tk.Label(frame2, text=nombre, font=('Calibri', 12),  anchor="center", background=color_cuerpo_principal)
            label_nombre.grid(row=i+1, column=0, sticky="nsew", padx=5, pady=2)
            if edicion:
                label_nombre.bind("<Button-1>", lambda e, n=nombre, d=dni: self.controlador.editar_empleado(n, d))

            if frame3:
                boton_editar = tk.Button(frame3, text="Editar", font=('Calibri', 12), bg='#6D8299', fg='white',
                                        command=lambda n=nombre, d=dni: self.controlador.editar_empleado(n, d))
                boton_editar.grid(row=i+1, column=0, sticky="nsew",padx=5, pady=2)
                boton_eliminar = tk.Button(frame4, text="Eliminar", font=('Calibri', 12), bg='#FF6B6B', fg='white',
                                        command=lambda d=dni,n=nombre: self.controlador.eliminar_empleado(n, d))
                boton_eliminar.grid(row=i+1, column=0, sticky="nsew",padx=5, pady=2)

#Paneles de fichaje
    def PanelFichaje(self, panel_principal):
        # --- 1. TITULO (Se mantiene igual) ---
        borde_sup_sup = tk.Frame(panel_principal, background=color_barra_superior)
        borde_sup_sup.pack(side=tk.TOP, fill='x', expand=False)
        label_sup_sup = tk.Label(borde_sup_sup, text="Panel Fichajes", font=("Roboto", 15), bg=color_barra_superior, fg="white")
        label_sup_sup.pack(side=tk.LEFT, fill='both', expand=False)

        # --- 2. EL "ENVOLTORIO" DEL SCROLL ---
        contenedor_canvas = tk.Frame(panel_principal, bg=color_menu_lateral)
        contenedor_canvas.pack(side=tk.TOP, fill='both', expand=True)

        canvas = tk.Canvas(contenedor_canvas, bg=color_menu_lateral, highlightthickness=0)
        # Cambiamos a horizontal como querías
        scrollbar = tk.Scrollbar(contenedor_canvas, orient="horizontal", command=canvas.xview)
        canvas.configure(xscrollcommand=scrollbar.set)

        scrollbar.pack(side=tk.BOTTOM, fill='x')
        canvas.pack(side=tk.LEFT, fill='both', expand=True)

        # Este es el frame que contendrá todo tu código original
        fichaje_interno = tk.Frame(canvas, background=color_menu_lateral)
        canvas.create_window((0, 0), window=fichaje_interno, anchor="nw")

      
        
        # Bordes
        tk.Frame(fichaje_interno, bg=color_menu_lateral, height=20).pack(side=tk.TOP, fill='both', expand=False)
        tk.Frame(fichaje_interno, bg=color_menu_lateral, height=20).pack(side=tk.BOTTOM, fill='both', expand=False)
        tk.Frame(fichaje_interno, bg=color_menu_lateral, width=20).pack(side=tk.LEFT, fill='both', expand=False)
        tk.Frame(fichaje_interno, bg=color_menu_lateral, width=20).pack(side=tk.RIGHT, fill='both', expand=False)

        # Modulo DNI
        frame_Dni = tk.Frame(fichaje_interno, bg=color_menu_lateral)
        frame_Dni.pack(side=tk.LEFT, fill='both', expand=False)

        label_Dni = tk.Label(frame_Dni, text="Ingrese DNI", font=('Calibri', 12), bg=color_barra_superior, fg="white", width=20)
        label_Dni.pack(side=tk.TOP, fill='both', expand=False, padx=5, pady=5)
        entry_Dni = tk.Entry(frame_Dni, font=('Calibri', 12), bg=color_cuerpo_principal, fg="black")
        entry_Dni.pack(side=tk.TOP, fill='both', expand=False, padx=5, pady=5)
        entry_Dni.bind("<Return>", lambda event: self.controlador.manejar_dni(entry_Dni))

        # Modulo Activos
        self.frame_fichados = tk.Frame(fichaje_interno, bg=color_menu_lateral)
        self.frame_fichados.pack(side=tk.LEFT, fill='both', expand=False, padx=10)
        self.frame_horas_fichados = tk.Frame(fichaje_interno, bg=color_menu_lateral)
        self.frame_horas_fichados.pack(side=tk.LEFT, fill='both', expand=False, padx=10)

        tk.Label(self.frame_fichados, text="Empleados activos", font=('Calibri', 12), bg=color_barra_superior, fg="white", width=20).grid(row=0, padx=5, pady=5)
        tk.Label(self.frame_horas_fichados, text="Tiempo en Actividad", font=('Calibri', 12), bg=color_barra_superior, fg="white", width=20).grid(row=0, padx=5, pady=5)

        tk.Button(frame_Dni, text="Ingreso", font=('Calibri', 12), command=lambda: self.controlador.manejar_dni(entry_Dni), bg='#6D8299', fg='white').pack(side=tk.TOP, fill='both', expand=False, padx=5, pady=5)
        
        tk.Frame(fichaje_interno, bg=color_menu_lateral, width=20).pack(side=tk.LEFT, fill='both', expand=False)
        self.actualizar_lista_activos()
        # --- 4. CIERRE DEL SCROLL (Para que sepa cuánto medir) ---
        fichaje_interno.update_idletasks()
        canvas.config(scrollregion=canvas.bbox("all"))

    def PanelExtra(self,panel_principal):
        
        
       
        #Titulo para fichaje
        borde_sup_sup=tk.Frame(panel_principal,background=color_barra_superior)
        borde_sup_sup.pack(side=tk.TOP,fill='both',expand=False)
        label_sup_sup=tk.Label(borde_sup_sup,text="Panel Extra",font=("Roboto",15),bg=color_barra_superior,fg="white")
        label_sup_sup.pack(side=tk.LEFT,fill='both',expand=False)

        contenedor_canvas = tk.Frame(panel_principal, bg=color_menu_lateral)
        contenedor_canvas.pack(side=tk.TOP, fill='both', expand=True)

        canvas = tk.Canvas(contenedor_canvas, bg=color_menu_lateral, highlightthickness=0)
        scrollbar = tk.Scrollbar(contenedor_canvas, orient="horizontal", command=canvas.xview)
        canvas.configure(xscrollcommand=scrollbar.set)
        scrollbar.pack(side=tk.BOTTOM, fill='x')
        canvas.pack(side=tk.LEFT, fill='both', expand=True)
       
        fichaje_interno_extra = tk.Frame(canvas, background=color_menu_lateral)
        canvas.create_window((0, 0), window=fichaje_interno_extra, anchor="nw")
        
       
        #Bordes para fichaje
        borde_fichaje_sup=tk.Frame(fichaje_interno_extra,bg=color_menu_lateral,height=20)
        borde_fichaje_sup.pack(side=tk.TOP,fill='both',expand=False)
        borde_fichaje_inf=tk.Frame(fichaje_interno_extra,bg=color_menu_lateral,height=20)
        borde_fichaje_inf.pack(side=tk.BOTTOM,fill='both',expand=False)
        borde_fichaje_izq=tk.Frame(fichaje_interno_extra,bg=color_menu_lateral,width=20)
        borde_fichaje_izq.pack(side=tk.LEFT,fill='both',expand=False)
        borde_fichaje_der=tk.Frame(fichaje_interno_extra,bg=color_menu_lateral,width=20)
        borde_fichaje_der.pack(side=tk.RIGHT,fill='both',expand=False)

        #Modulo para entrar Dni
        frame_Dni=tk.Frame(fichaje_interno_extra,bg=color_menu_lateral)
        frame_Dni.pack(side=tk.LEFT, fill='both',expand=False)

        #Entrada de Dni
        label_Dni = tk.Label(frame_Dni, text="Ingrese DNI",font=('Calibri', 12), bg=color_barra_superior,fg="white", width=20)
        label_Dni.pack(side=tk.TOP,fill='both',expand=False,padx=5,pady=5)
        entry_Dni_extra = tk.Entry(frame_Dni,font=('Calibri', 12),bg=color_cuerpo_principal,fg="black")
        entry_Dni_extra.pack(side=tk.TOP,fill='both',expand=False,padx=5,pady=5)
        entry_Dni_extra.bind("<Return>", lambda event: self.controlador.manejar_dni(entry_Dni_extra,1))
        label_motivo = tk.Label(frame_Dni, text="Motivo:",font=('Calibri', 12), bg=color_barra_superior,fg="white", width=20)
        label_motivo.pack(side=tk.TOP,fill='both',expand=False,padx=5,pady=5)
        entry_motivo = tk.Entry(frame_Dni,font=('Calibri', 12),bg=color_cuerpo_principal,fg="black")
        entry_motivo.pack(side=tk.TOP,fill='both',expand=False,padx=5,pady=5)
        entry_motivo.bind("<Return>", lambda event: [self.controlador.manejar_dni(entry_Dni_extra, 1, entry_motivo.get()), entry_motivo.delete(0, tk.END)])

        #Modulo para ver los activos
        self.frame_fichados_extra=tk.Frame(fichaje_interno_extra,bg=color_menu_lateral)
        self.frame_fichados_extra.pack(side=tk.LEFT, fill='both',expand=False,padx=10)
        self.frame_motivos=tk.Frame(fichaje_interno_extra,bg=color_menu_lateral)
        self.frame_motivos.pack(side=tk.LEFT, fill='both',expand=False,padx=10)
        self.frame_horas_fichados_extra=tk.Frame(fichaje_interno_extra,bg=color_menu_lateral)
        self.frame_horas_fichados_extra.pack(side=tk.LEFT, fill='both',expand=False,padx=10)


        #Lista de empleados activos
        label_empleados_activos=tk.Label(self.frame_fichados_extra,text="Empleados activos",font=('Calibri', 12),bg=color_barra_superior,fg="white",width=20)
        label_empleados_activos.grid(row=0,padx=5,pady=5)
        label_motivo= tk.Label(self.frame_motivos, text="Motivo", font=('Calibri', 12), bg=color_barra_superior, fg="white", width=20)
        label_motivo.grid(row=0, column=1, padx=5, pady=5)
        

        #Lista de las horas de los empleados activos
        label_horas_activas=tk.Label(self.frame_horas_fichados_extra,text="Tiempo en Actividad",font=('Calibri', 12),bg=color_barra_superior,fg="white",width=20)
        label_horas_activas.grid(row=0,padx=5,pady=5)

        boton_fichar = tk.Button(frame_Dni, text="Ingreso", font=('Calibri', 12), command=lambda: self.manejar_dni(entry_Dni_extra,1,entry_motivo.get()), bg='#D77F09', fg='white')
        boton_fichar.pack(side=tk.TOP, fill='both', expand=False, padx=5, pady=5)
        separador1=tk.Frame(fichaje_interno_extra,bg=color_menu_lateral,width=20)
        separador1.pack(side=tk.LEFT,fill='both',expand=False)

        self.actualizar_lista_activos()
        # --- 4. CIERRE DEL SCROLL (Para que sepa cuánto medir) ---
        fichaje_interno_extra.update_idletasks()
        canvas.config(scrollregion=canvas.bbox("all"))

    
    def actualizar_lista_activos(self):
        # Verificar si los frames aún existen
        if not self.frame_fichados.winfo_exists() or not self.frame_horas_fichados.winfo_exists():
            return  # Salir si los frames ya no existen
        if not self.frame_fichados_extra.winfo_exists() or not self.frame_horas_fichados_extra.winfo_exists():
            return  # Salir si los frames ya no existen
        # Limpiar las listas actuales
        for widget in self.frame_fichados.winfo_children()[1:]:
            widget.destroy()
        for widget in self.frame_horas_fichados.winfo_children()[1:]:
            widget.destroy()
        for widget in self.frame_fichados_extra.winfo_children()[1:]:
            widget.destroy()
        for widget in self.frame_motivos.winfo_children()[1:]:
            widget.destroy()
        for widget in self.frame_horas_fichados_extra.winfo_children()[1:]:
            widget.destroy()

        # Actualizar la lista de empleados activos
        for i, empleado in enumerate(self.empleados_activos):
            label = tk.Label(self.frame_fichados, text=empleado, font=('Calibri', 12), width=20, anchor="center", background=color_cuerpo_principal)
            label.grid(row=i+1, column=0, sticky="nsew", padx=5, pady=5)

        # Actualizar la lista de tiempos activos
        for i, tiempo in enumerate(self.tiempo_activo):
            label = tk.Label(self.frame_horas_fichados, text=tiempo, font=('Calibri', 12), width=20, anchor="center", background=color_cuerpo_principal)
            label.grid(row=i+1, column=0, sticky="nsew", padx=5, pady=5)    

        # Actualizar la lista de empleados activos extra
        for i, empleado in enumerate(self.empleados_activos_extra):
            label = tk.Label(self.frame_fichados_extra, text=empleado, font=('Calibri', 12), width=20, anchor="center", background=color_cuerpo_principal)
            label.grid(row=i+1, column=0, sticky="nsew", padx=5, pady=5)

        # Actualizar la lista de motivos extra
        for i, motivo in enumerate(self.motivo_extra):
            label_motivo = tk.Label(self.frame_motivos, text=motivo, font=('Calibri', 12), width=20, anchor="center", background=color_cuerpo_principal)
            label_motivo.grid(row=i+1, column=1, sticky="nsew", padx=5, pady=5)

        # Actualizar la lista de tiempos activos extra
        for i, tiempo in enumerate(self.tiempo_activo_extra):
            label = tk.Label(self.frame_horas_fichados_extra, text=tiempo, font=('Calibri', 12), width=20, anchor="center", background=color_cuerpo_principal)
            label.grid(row=i+1, column=0, sticky="nsew", padx=5, pady=5)

    
    def PanelEmpleados(self,panel_principal):
        #Modulo para empleados
        Frame_empleados = tk.Frame(panel_principal,bg=color_menu_lateral)
        Frame_empleados.pack(side=tk.BOTTOM,fill='both',expand=False)

        #Titulo para panel de empleados
        barra_sup_sup=tk.Frame(Frame_empleados,bg=color_barra_superior)
        barra_sup_sup.pack(side=tk.TOP,fill='both',expand=False)
        label_barra_sup_sup = tk.Label(barra_sup_sup,text="Panel de control",font=("Roboto",15),bg=color_barra_superior,fg="white")
        label_barra_sup_sup.pack(side=tk.LEFT,fill='both',expand=False)

        #BORDES DE LA TABLA
        barra_sup = tk.Frame(Frame_empleados, bg = color_menu_lateral, height=20)
        barra_sup.pack(side=tk.TOP,fill='both',expand=False)
        barra_inf = tk.Frame(Frame_empleados, bg = color_menu_lateral, height=20)
        barra_inf.pack(side=tk.BOTTOM,fill='both',expand=True)
        barra_der = tk.Frame(Frame_empleados, bg = color_menu_lateral, width=20)
        barra_der.pack(side=tk.RIGHT,fill='both',expand=True)
        barra_izq = tk.Frame(Frame_empleados, bg = color_menu_lateral, width=20)
        barra_izq.pack(side=tk.LEFT,fill='both',expand=False)

        #Panel de botones
        botones=tk.Frame(Frame_empleados,bg=color_menu_lateral)
        botones.pack(side=tk.LEFT,fill='both',expand=False)
        relleno_inf=tk.Frame(botones,bg=color_menu_lateral)
        relleno_inf.pack(side=tk.BOTTOM,fill='both',expand=True)

        #boton add empleado
        self.crear_boton_empleado(botones, "Agregar\nEmpleado", self.agregar, lambda: self.add_employee()) 
        #boton EDITAR empleado
        self.crear_boton_empleado(botones, "Editar\nEmpleado", self.edit, lambda: self.abrir_ventana("Empleados"))
        #boton Borrar empleado
        self.crear_boton_empleado(botones, "Eliminar\nEmpleado", self.delete, lambda: self.abrir_ventana("Empleados"))
        #boton Consultar empleado
        self.crear_boton_empleado(botones, "Consultar\nHoras", self.consulta, lambda: self.consultar_empleados())

    """
        #Modulo del reloj
        frame_reloj=tk.Frame(Frame_empleados,bg=color_menu_lateral)
        frame_reloj.pack(side=tk.LEFT,fill='both',expand=True,padx=10)

        def tiempo_string():
            return time.strftime('%H:%M:%S')
        def update():
            label_reloj.configure(text=tiempo_string())
            label_reloj.after(1000, update)

        label_reloj = tk.Label(frame_reloj,text=tiempo_string(),font=("Digital-7", 40),bg=color_barra_superior,fg="red",anchor="center",padx=10,pady=10)
        label_reloj.columnconfigure(0)
        label_reloj.pack(expand=True)
        label_reloj.after(1000, update())
    """
    

    def abrir_ventana(self,title):

        if app_state.is_admin:
            nueva_ventana = tk.Toplevel(self.root,bg=color_menu_lateral)  # Crea una nueva ventana secundaria
            nueva_ventana.title(title)
            nueva_ventana.geometry("600x600")
            nueva_ventana.resizable(True,True)

            frame_boton = tk.Frame(nueva_ventana, bg=color_menu_lateral)
            frame_boton.pack(side=tk.BOTTOM, fill='both')
            # Configurar el frame para usar grid
            frame_boton.grid_columnconfigure(0, weight=1)  # Columna para el botón "Actualizar"
            frame_boton.grid_columnconfigure(1, weight=1)  # Columna para el botón "Cerrar"

            # Botón para actualizar la tabla
            boton_actualizar = tk.Button(frame_boton, text="Actualizar", font=('Calibri', 12), bg='#6D8299', fg='white',
                                        command=lambda: self.TablaEmpleados(frame_tabla1, frame_tabla2, "dni", edicion=True, frame3=frame_tabla3, frame4=frame_tabla4))
            boton_actualizar.grid(row=0, column=0, sticky="nsew", padx=10, pady=5)

            # Botón para cerrar la ventana
            boton_exit = tk.Button(frame_boton, text="Cerrar", font=('Calibri', 12), bg='#FF6B6B', fg='white', command=nueva_ventana.destroy)
            boton_exit.grid(row=0, column=1, sticky="nsew", padx=10, pady=5)

            frame_tabla1 = tk.Frame(nueva_ventana, bg=color_menu_lateral, padx=5, pady=10)
            frame_tabla1.pack(side=tk.LEFT, fill='both', expand=True)
            frame_tabla2 = tk.Frame(nueva_ventana, bg=color_menu_lateral, padx=5, pady=10)
            frame_tabla2.pack(side=tk.LEFT, fill='both', expand=True)
            frame_tabla3 = tk.Frame(nueva_ventana, bg=color_menu_lateral, padx=5, pady=10)
            frame_tabla3.pack(side=tk.LEFT, fill='both', expand=True)
            frame_tabla4 = tk.Frame(nueva_ventana, bg=color_menu_lateral, padx=5, pady=10)
            frame_tabla4.pack(side=tk.LEFT, fill='both', expand=True)

            # Configurar las columnas para que se distribuyan uniformemente
            frame_tabla1.grid_columnconfigure(0, weight=1)  # Columna de DNI
            frame_tabla2.grid_columnconfigure(0, weight=1)  # Columna de Empleados
            frame_tabla3.grid_columnconfigure(0, weight=1)  # Columna de Editar
            frame_tabla4.grid_columnconfigure(0, weight=1)  # Columna de Eliminar
            # Crear encabezados
            label_dni = tk.Label(frame_tabla1, text="Dni", font=('Calibri', 11), bg=color_barra_superior, fg="white", anchor="center",height=1)
            label_dni.grid(row=0, column=0, sticky="nsew", padx=5, pady=8)
            label_nombre = tk.Label(frame_tabla2, text="Empleados", font=('Calibri', 11), bg=color_barra_superior, fg="white", anchor="center",height=1)
            label_nombre.grid(row=0, column=0, sticky="nsew", padx=5, pady=8)
            label_editar = tk.Label(frame_tabla3, text="Editar", font=('Calibri', 11), bg=color_barra_superior, fg="white", anchor="center",height=1)
            label_editar.grid(row=0, column=0, sticky="nsew", padx=5, pady=8)
            label_eliminar = tk.Label(frame_tabla4, text="Eliminar", font=('Calibri', 11), bg=color_barra_superior, fg="white", anchor="center",height=1)
            label_eliminar.grid(row=0, column=0, sticky="nsew", padx=5, pady=8)

            self.TablaEmpleados(frame_tabla1, frame_tabla2, "dni",edicion=True,frame3=frame_tabla3,frame4=frame_tabla4)
        else :
            messagebox.showerror("Error", "No tienes permiso para acceder a esta función.")

#ENTRADA Y EDICION DE EMPLEADOS
    def view_add_employee(self):
        if app_state.is_admin:
            # Crear una nueva ventana para agregar empleado
            nueva_ventana = tk.Toplevel(self.root, bg=color_menu_lateral)
            nueva_ventana.title("Agregar Empleado")
            nueva_ventana.geometry("400x300")

            # Etiqueta y campo de entrada para el nombre
            label_nombre = tk.Label(nueva_ventana, text="Nombre:", font=('Calibri', 12))
            label_nombre.pack(pady=10)
            entry_nombre = tk.Entry(nueva_ventana, font=('Calibri', 12))
            entry_nombre.pack(pady=10)

            # Etiqueta y campo de entrada para el DNI
            label_dni = tk.Label(nueva_ventana, text="DNI:", font=('Calibri', 12))
            label_dni.pack(pady=10)
            entry_dni = tk.Entry(nueva_ventana, font=('Calibri', 12))
            entry_dni.pack(pady=10)

            # Botón para guardar el nuevo empleado
            boton_guardar = tk.Button(
                nueva_ventana,
                text="Guardar",
                command=lambda: self.guardar_nuevo_empleado(entry_nombre.get(), entry_dni.get(), nueva_ventana),
                font=('Calibri', 12),
                bg='#6D8299',
                fg='white')
            boton_guardar.pack(pady=10)

            # Botón para cancelar y cerrar la ventana
            boton_cancelar = tk.Button(
                nueva_ventana,
                text="Cancelar",
                command=nueva_ventana.destroy,
                font=('Calibri', 12),
                bg='#FF6B6B',
                fg='white')
            boton_cancelar.pack(pady=10)
        else:
            messagebox.showerror("Error", "No tienes permiso para acceder a esta función.")

    def editar_empleado(self, nombre, dni):
        nueva_ventana = tk.Toplevel(self.root,bg=color_menu_lateral)
        nueva_ventana.title(f"Editar Empleado: {nombre}")
        nueva_ventana.geometry("400x300")

        label_nombre = tk.Label(nueva_ventana, text="Nombre:", font=('Calibri', 12))
        label_nombre.pack(pady=10)
        entry_nombre = tk.Entry(nueva_ventana, font=('Calibri', 12))
        entry_nombre.pack(pady=10)
        entry_nombre.insert(0, nombre)

        label_dni = tk.Label(nueva_ventana, text="DNI:", font=('Calibri', 12))
        label_dni.pack(pady=10)
        entry_dni = tk.Entry(nueva_ventana, font=('Calibri', 12))
        entry_dni.pack(pady=10)
        entry_dni.insert(0, dni)

        boton_guardar = tk.Button(
            nueva_ventana, 
            text="Guardar", 
            command=lambda: self.guardar_cambios(entry_nombre.get(), entry_dni.get(), nombre, dni, nueva_ventana),
            font=('Calibri', 12),
            bg='#6D8299',
            fg='white')
        boton_guardar.pack(pady=10)
        boton_cancelar = tk.Button(
            nueva_ventana,
            text="Cancelar",
            command=nueva_ventana.destroy,
            font=('Calibri', 12),
            bg='#FF6B6B',
            fg='white')
        boton_cancelar.pack(pady=10)

    def eliminar_empleado(self, nombre, dni):
        print(f"Intentando eliminar: {nombre} con DNI {dni}")
        respuesta = messagebox.askyesno("Confirmación", f"¿Estás seguro de que deseas eliminar al empleado {nombre} con DNI {dni}?")
        print(f"Respuesta del usuario: {respuesta}")
        if not respuesta:
            return
        
        # Eliminar al empleado de la tabla empleados
        query_empleado = "DELETE FROM empleados WHERE dni = ?"
        db.execute_query("Datos/datos.db", query_empleado, (dni,))
        print(f"Ejecutando consulta: {query_empleado} con DNI {dni}")

        # Eliminar los registros asociados en la tabla registros
        query_registros = "DELETE FROM registros WHERE dni = ?"
        db.execute_query("Datos/datos.db", query_registros, (dni,))
        print(f"se borro: {query_empleado} con DNI {dni}")

        # Actualizar la tabla de empleados en la interfaz
        self.TablaEmpleados(self.frame_nombre, self.frame_dni, "dni")
        print("Tabla actualizada después de la eliminación")
        
        # Mostrar mensaje de éxito
        messagebox.showinfo("Éxito", f"Empleado {nombre} y sus registros han sido eliminados correctamente.")

    def guardar_nuevo_empleado(self, nombre, dni, ventana):
        # Validar que los campos no estén vacíos
        if not nombre.strip() or not dni.strip():
            messagebox.showerror("Error", "Todos los campos son obligatorios.")
            return

        # Validar que el DNI sea un número
        if not dni.isdigit():
            messagebox.showerror("Error", "El DNI debe ser un número.")
            return

        # Verificar si el DNI ya existe en la base de datos
        query_verificar = "SELECT * FROM empleados WHERE dni = ?"
        params_verificar = (dni,)
        resultado = db.execute_query("Datos/datos.db", query_verificar, params_verificar, fetch=True)

        if resultado:
            messagebox.showerror("Error", "El DNI ingresado ya existe en la base de datos.")
            return

        # Insertar el nuevo empleado en la base de datos
        query_insertar = "INSERT INTO empleados (nombre, dni) VALUES (?, ?)"
        params_insertar = (nombre.strip(), dni.strip())
        db.execute_query("Datos/datos.db", query_insertar, params_insertar)

        # Actualizar la tabla de empleados en la interfaz
        self.TablaEmpleados(self.frame_nombre, self.frame_dni, "dni")

        # Cerrar la ventana y mostrar un mensaje de éxito
        ventana.destroy()
        messagebox.showinfo("Éxito", "Empleado agregado correctamente.")

    def guardar_cambios(self, nuevo_nombre, nuevo_dni, nombre, dni, ventana):
        # Actualizar la base de datos en la tabla "empleados"
        query = "UPDATE empleados SET nombre = ?, dni = ? WHERE nombre = ? AND dni = ?"
        params = (nuevo_nombre, nuevo_dni, nombre, dni)
        db.execute_query("Datos/datos.db", query, params)

        # Actualizar los registros asociados en la tabla registros
        query_registros = "UPDATE registros SET nombre = ?, dni = ? WHERE nombre = ? AND dni = ?"
        params_registros = (nuevo_nombre, nuevo_dni, nombre, dni)
        db.execute_query("Datos/datos.db", query_registros, params_registros)

        # Actualizar la tabla
        self.TablaEmpleados(self.frame_nombre, self.frame_dni, "dni")
        # Cerrar la ventana de edición
        ventana.destroy()
        messagebox.showinfo("Información", "Empleado actualizado correctamente")

#REGISTRAR ENTRADA Y SALIDA
    def registrar_entrada(self, dni,extra=0,motivo=None):
        # Verificar si el DNI existe en la tabla de empleados
        query_empleado = "SELECT nombre FROM empleados WHERE dni = ?"
        params_empleado = (dni,)
        empleado = db.execute_query("Datos/datos.db", query_empleado, params_empleado, fetch=True)

        if not empleado:
            messagebox.showerror("Error", "El DNI ingresado no existe en la base de datos.")
            return False

        # Verificar si hay un registro pendiente en la tabla de registros
        query_registro = "SELECT id FROM registros WHERE dni = ? AND hora_salida IS NULL"
        params_registro = (dni,)
        registro_pendiente = db.execute_query("Datos/datos.db", query_registro, params_registro, fetch=True)

        if registro_pendiente:
            messagebox.showerror("Error", "Ya existe un registro pendiente. Debe registrar la salida antes de ingresar nuevamente.")
            return False

        # Insertar un nuevo registro con la fecha y hora actuales
        fecha_actual = time.strftime("%Y-%m-%d")
        hora_actual = time.strftime("%H:%M:%S")
        query_insert = "INSERT INTO registros (dni, nombre, fecha, hora_entrada, extra, motivo) VALUES (?, ?, ?, ?, ? ,?)"
        params_insert = (dni, empleado[0][0], fecha_actual, hora_actual,extra,motivo)
        db.execute_query("Datos/datos.db", query_insert, params_insert)

        messagebox.showinfo("Éxito", "Registro de entrada realizado correctamente.")
        return True

    def registrar_salida(self,dni,forced=False):
        # Verificar si hay un registro pendiente en la tabla de registros
        if isinstance(dni, list) and len(dni) > 0 and isinstance(dni[0], tuple):
            dni = dni[0][0]  # Extraer el valor del primer elemento de la primera tupla
        query_registro = "SELECT id, hora_entrada FROM registros WHERE dni = ? AND hora_salida IS NULL"
        params_registro = (dni,)
        registro_pendiente = db.execute_query("Datos/datos.db", query_registro, params_registro, fetch=True)
        if not registro_pendiente:
            messagebox.showerror("Error", "No hay un registro pendiente. Debe registrar su entrada primero.")
            return
        
        # Obtener la hora actual
        hora_actual = time.strftime("%H:%M:%S")
        # Calcular el tiempo trabajado
        hora_entrada = registro_pendiente[0][1]
        formato_hora = "%H:%M:%S"
        
        if forced:
            # Calcular la hora de salida como hora de entrada + 1 minuto
            hora_salida = (datetime.strptime(hora_entrada, formato_hora) + timedelta(minutes=1)).strftime(formato_hora)

            # Registrar la salida con tiempo total de 1 minuto y marcar como expulsión
            query_update = """
                UPDATE registros
                SET hora_salida = ?, tiempo_total = ?, expulsion = ?
                WHERE id = ?
            """
            params_update = (hora_salida, "00:01:00", 1, registro_pendiente[0][0])
            db.execute_query("Datos/datos.db", query_update, params_update)
            messagebox.showinfo("Expulsión", "El empleado ha sido expulsado y su registro ha sido actualizado.")
        else:
            tiempo_trabajado = (
                datetime.strptime(hora_actual, formato_hora) - datetime.strptime(hora_entrada, formato_hora)
            )

            # Actualizar el registro con la hora de salida y el tiempo trabajado
            query_update = "UPDATE registros SET hora_salida = ?, tiempo_total = ? WHERE id = ?"
            params_update = (hora_actual, str(tiempo_trabajado), registro_pendiente[0][0])
            db.execute_query("Datos/datos.db", query_update, params_update)
            messagebox.showinfo("Éxito", "Registro de salida realizado correctamente.")

#CONSULTAR Y GENERAR INFORME DE EMPLEADOS
    def consultar_empleados(self):
        if app_state.is_admin:
            # Crear una ventana para seleccionar el rango de fechas
            ventana_fechas = tk.Toplevel(self.root, bg=color_menu_lateral)
            ventana_fechas.title("Consultar Empleados")
            ventana_fechas.geometry("560x400")
            #Frame de calendarios
            Frame_botones=tk.Frame(ventana_fechas,bg=color_menu_lateral,padx=10,pady=10)
            Frame_botones.pack(side=tk.BOTTOM,fill='both',expand=False)
            Frame_inicio=tk.Frame(ventana_fechas,bg=color_menu_lateral,padx=10,pady=10)
            Frame_inicio.pack(side=tk.LEFT,fill='both',expand=False)
            Frame_fin=tk.Frame(ventana_fechas,bg=color_menu_lateral,padx=10,pady=10)
            Frame_fin.pack(side=tk.LEFT,fill='both',expand=False)

            # Fecha actual
            fecha_actual = datetime.now()
            primer_dia_mes = fecha_actual.replace(day=1)

            # Etiqueta para la fecha de inicio
            label_inicio = tk.Label(Frame_inicio, text="Fecha de inicio:", font=('Calibri', 12), bg=color_menu_lateral, fg="white")
            label_inicio.pack(pady=10)

            # Calendario para la fecha de inicio
            calendario_inicio = Calendar(Frame_inicio, selectmode="day", date_pattern="yyyy-mm-dd")
            calendario_inicio.pack(pady=10)
            calendario_inicio.selection_set(primer_dia_mes.strftime("%Y-%m-%d"))  # Seleccionar el primer día del mes actual

            # Etiqueta para la fecha de fin
            label_fin = tk.Label(Frame_fin, text="Fecha de fin:", font=('Calibri', 12), bg=color_menu_lateral, fg="white")
            label_fin.pack(pady=10)

            # Calendario para la fecha de fin
            calendario_fin = Calendar(Frame_fin, selectmode="day", date_pattern="yyyy-mm-dd")
            calendario_fin.pack(pady=10)
            calendario_fin.selection_set(fecha_actual.strftime("%Y-%m-%d"))  # Seleccionar la fecha actual

            # Botón para generar el informe
            boton_generar = tk.Button(
                Frame_botones,
                text="Generar Informe",
                font=('Calibri', 12),
                bg='#6D8299',
                fg='white',
                command=lambda: self.generar_informe(calendario_inicio.get_date(), calendario_fin.get_date(), ventana_fechas)
            )
            boton_generar.pack(pady=10)

            # Botón para cancelar
            boton_cancelar = tk.Button(
                Frame_botones,
                text="Cancelar",
                font=('Calibri', 12),
                bg='#FF6B6B',
                fg='white',
                command=ventana_fechas.destroy
            )
            boton_cancelar.pack(pady=10)
        else:
            messagebox.showerror("Error", "No tienes permiso para acceder a esta función.")

    def generar_informe(self, fecha_inicio, fecha_fin, ventana):
        # Validar las fechas
        try:
            fecha_inicio = datetime.strptime(fecha_inicio, "%Y-%m-%d")
            fecha_fin = datetime.strptime(fecha_fin, "%Y-%m-%d")
        except ValueError:
            messagebox.showerror("Error", "Las fechas deben estar en formato YYYY-MM-DD.")
            return

        if fecha_inicio > fecha_fin:
            messagebox.showerror("Error", "La fecha de inicio no puede ser mayor que la fecha de fin.")
            return

        # Consultar los registros en el rango de fechas
        query = """
            SELECT dni, nombre, fecha, hora_entrada, hora_salida, tiempo_total , COALESCE(expulsion,0) AS expulsion
            FROM registros
            WHERE fecha BETWEEN ? AND ?
        """
        params = (fecha_inicio.strftime("%Y-%m-%d"), fecha_fin.strftime("%Y-%m-%d"))
        registros = db.execute_query("Datos/datos.db", query, params, fetch=True)

        if not registros:
            messagebox.showinfo("Sin resultados", "No se encontraron registros en el rango de fechas seleccionado.")
            return

        # Agrupar registros por empleado y sumar tiempos totales
        empleados = {}
        for registro in registros:
            dni, nombre, fecha, hora_entrada, hora_salida, tiempo_total, expulsion = registro
            if nombre not in empleados:
                empleados[nombre] = {"registros": [], "tiempo_total": datetime.strptime("00:00:00", "%H:%M:%S")}
            empleados[nombre]["registros"].append((fecha, hora_entrada, hora_salida, tiempo_total,expulsion))
            if tiempo_total:
                tiempo_total_dt = datetime.strptime(tiempo_total, "%H:%M:%S")
                empleados[nombre]["tiempo_total"] += timedelta(
                    hours=tiempo_total_dt.hour, minutes=tiempo_total_dt.minute, seconds=tiempo_total_dt.second
                )

        # Preguntar al usuario dónde guardar el archivo
        ruta_guardado = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF files", "*.pdf")])
        if not ruta_guardado:
            messagebox.showinfo("Cancelado", "No se guardó el informe.")
            return

        # Generar el PDF
        pdf = FPDF()
        pdf.set_auto_page_break(auto=True, margin=15)
        pdf.add_page()
        pdf.set_font("Arial", size=12)

        pdf.cell(200, 10, txt="Informe de Registros", ln=True, align="C")
        pdf.cell(200, 10, txt=f"Rango de fechas: {fecha_inicio.strftime('%Y-%m-%d')} - {fecha_fin.strftime('%Y-%m-%d')}", ln=True, align="C")
        pdf.ln(10)

        for nombre, datos in empleados.items():
            pdf.set_font("Arial", style="B", size=12)
            pdf.set_fill_color(200, 220, 255)
            pdf.cell(176, 10, txt=f"Empleado: {nombre}", ln=True, align="L",fill=True)
            pdf.set_font("Arial", size=10)
            pdf.cell(176, 10, txt=f"Tiempo total: {datos['tiempo_total'].strftime('%H:%M:%S')}", ln=True, align="L",fill=True)
            pdf.ln(5)

            # Encabezados de la tabla
            pdf.cell(44, 8, txt="Fecha", border=1, align="C")
            pdf.cell(44, 8, txt="Hora Entrada", border=1, align="C")
            pdf.cell(44, 8, txt="Hora Salida", border=1, align="C")
            pdf.cell(44, 8, txt="Tiempo Total", border=1, align="C")
            pdf.ln()

            # Registros del empleado
            for i,registro in enumerate(datos["registros"]):
                fecha, hora_entrada, hora_salida, tiempo_total,expulsion = registro

                # Asegurarse de que los valores no sean None
                fecha = fecha if fecha else "N/A"
                hora_entrada = hora_entrada if hora_entrada else "N/A"
                hora_salida = hora_salida if hora_salida else "N/A"
                tiempo_total = tiempo_total if tiempo_total else "N/A"

                # Alternar colores de fondo
                if expulsion == 1:
                    pdf.set_fill_color(255, 0, 0)  # Rojo
                elif i % 2 == 0:
                    pdf.set_fill_color(220, 240, 220)  # Verde clarito
                else:
                    pdf.set_fill_color(255, 255, 255)  # Blanco

                pdf.cell(44, 7, txt=str(fecha), border=1, align="C",fill=True)
                pdf.cell(44, 7, txt=str(hora_entrada), border=1, align="C",fill=True)
                pdf.cell(44, 7, txt=str(hora_salida), border=1, align="C",fill=True)
                pdf.cell(44, 7, txt=str(tiempo_total), border=1, align="C",fill=True)
                pdf.ln()

            # Espacio entre empleados
            pdf.ln(10)

        # Guardar el PDF
        pdf.output(ruta_guardado)
        messagebox.showinfo("Éxito", f"Informe guardado correctamente en {ruta_guardado}")

