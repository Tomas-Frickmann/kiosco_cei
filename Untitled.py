import tkinter as tk
from tkcalendar import Calendar
from tkinter import filedialog
from fpdf import FPDF
import time
from datetime import datetime,timedelta
from tkinter import messagebox
import Datos.Connect as db
from Utilitys.util_config import color_barra_superior,color_cuerpo_principal,color_menu_cursor_encima,color_menu_lateral,color_iconos2
from vistas.setting_view import Setting, app_state
def PanelFichaje(self,panel_principal):
        #Titulo para fichaje
        borde_sup_sup=tk.Frame(panel_principal,background=color_barra_superior)
        borde_sup_sup.pack(side=tk.TOP,fill='both',expand=False)
        label_sup_sup=tk.Label(borde_sup_sup,text="Panel Fichajes",font=("Roboto",15),bg=color_barra_superior,fg="white")
        label_sup_sup.pack(side=tk.LEFT,fill='both',expand=False)

        #Modulo para fichaje
        fichaje = tk.Frame(panel_principal,background=color_menu_lateral)
        fichaje.pack(side=tk.TOP, fill='both',expand=True)
        #Bordes para fichaje
        borde_fichaje_sup=tk.Frame(fichaje,bg=color_menu_lateral,height=20)
        borde_fichaje_sup.pack(side=tk.TOP,fill='both',expand=False)
        borde_fichaje_inf=tk.Frame(fichaje,bg=color_menu_lateral,height=20)
        borde_fichaje_inf.pack(side=tk.BOTTOM,fill='both',expand=False)
        borde_fichaje_izq=tk.Frame(fichaje,bg=color_menu_lateral,width=20)
        borde_fichaje_izq.pack(side=tk.LEFT,fill='both',expand=False)
        borde_fichaje_der=tk.Frame(fichaje,bg=color_menu_lateral,width=20)
        borde_fichaje_der.pack(side=tk.RIGHT,fill='both',expand=False)

        #Modulo para entrar Dni
        frame_Dni=tk.Frame(fichaje,bg=color_menu_lateral)
        frame_Dni.pack(side=tk.LEFT, fill='both',expand=False)

        #Entrada de Dni
        label_Dni = tk.Label(frame_Dni, text="Ingrese DNI",font=('Calibri', 12), bg=color_barra_superior,fg="white", width=20)
        label_Dni.pack(side=tk.TOP,fill='both',expand=False,padx=5,pady=5)
        entry_Dni = tk.Entry(frame_Dni,font=('Calibri', 12),bg=color_cuerpo_principal,fg="black")
        entry_Dni.pack(side=tk.TOP,fill='both',expand=False,padx=5,pady=5)
        entry_Dni.bind("<Return>", lambda event: self.manejar_dni(entry_Dni))

        #Modulo para ver los activos
        self.frame_fichados=tk.Frame(fichaje,bg=color_menu_lateral)
        self.frame_fichados.pack(side=tk.LEFT, fill='both',expand=False,padx=10)
        self.frame_horas_fichados=tk.Frame(fichaje,bg=color_menu_lateral)
        self.frame_horas_fichados.pack(side=tk.LEFT, fill='both',expand=False,padx=10)

        #Lista de empleados activos
        label_empleados_activos=tk.Label(self.frame_fichados,text="Empleados activos",font=('Calibri', 12),bg=color_barra_superior,fg="white",width=20)
        label_empleados_activos.grid(row=0,padx=5,pady=5)

        #Lista de las horas de los empleados activos
        label_horas_activas=tk.Label(self.frame_horas_fichados,text="Tiempo en Actividad",font=('Calibri', 12),bg=color_barra_superior,fg="white",width=20)
        label_horas_activas.grid(row=0,padx=5,pady=5)

        boton_fichar = tk.Button(frame_Dni, text="Ingreso", font=('Calibri', 12), command=lambda: self.manejar_dni(entry_Dni), bg='#6D8299', fg='white')
        boton_fichar.pack(side=tk.TOP, fill='both', expand=False, padx=5, pady=5)
        separador1=tk.Frame(fichaje,bg=color_menu_lateral,width=20)
        separador1.pack(side=tk.LEFT,fill='both',expand=False)