import tkinter as tk
from Utilitys.util_config import color_cuerpo_principal
from Utilitys.util_gestorimagenes import GestorImagenes as gi

class StatisticsView():

    def __init__(self,panel_principal,controller):
        
        self.logo = gi.obtener_imagen("construction","./Images/Construccion.png",(220,220))

        self.barra_superior = tk.Frame(panel_principal)
        self.barra_superior.pack(side=tk.TOP, fill='both',expand=True)

        self.barra_inferior = tk.Frame(panel_principal)
        self.barra_inferior.pack(side=tk.BOTTOM,fill='both',expand=True)

        self.labelTitulo=tk.Label(self.barra_superior,text="Página en construccion")
        self.labelTitulo.config(fg="#222d33",font=("Roboto",30),bg=color_cuerpo_principal)
        self.labelTitulo.pack(side=tk.TOP,fill='both',expand=True)

        self.label_imagen= tk.Label(self.barra_inferior,image=self.logo)
        self.label_imagen.place(x=0,y=0,relwidth=1,relheight=1)
        self.label_imagen.config(fg='#fff',font=("Roboto",10),bg=color_cuerpo_principal)
    