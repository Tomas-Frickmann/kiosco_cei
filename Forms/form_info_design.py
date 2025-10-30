import tkinter as tk
import Utilitys.util_ventana as util_ventana

class FormularioInfoDesign(tk.Toplevel):
    def __init__(self) -> None:
        super().__init__()
        self.config_window()
        self.construirWidget()

    def config_window(self):
        #Configuracion inicial de la ventana
        self.title('Kiosco')
        self.iconbitmap("./images/shop.ico")
        w, h = 400, 100
        util_ventana.centrar_ventana(self , w , h)

    def construirWidget(self):

        self.labelVersion=tk.Label(self, text="Version : 1.0")
        self.labelVersion.config(fg='#000000',font=("Roboto",15),pady=10,width=30)
        self.labelVersion.pack()
        self.labelAutor=tk.Label(self, text="Autor : Federico Rodriguez")
        self.labelAutor.config(fg='#000000', font=("Roboto",15),pady=10,width=30)
        self.labelAutor.pack()
