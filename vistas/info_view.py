import tkinter as tk
import Utilitys.util_ventana as util_ventana

class InfoView(tk.Toplevel):
    def __init__(self) -> None:
        super().__init__()
    

        self.title('Kiosco')
        self.iconbitmap("./images/shop.ico")
        w, h = 600, 100
        util_ventana.centrar_ventana(self , w , h)

        self.labelVersion = tk.Label(self, text="Version : 1.5")
        # Le quitamos el width=30
        self.labelVersion.config(fg='#000000', font=("Roboto", 15), pady=10) 
        self.labelVersion.pack()
        
        self.labelAutor = tk.Label(self, text="Autores : Federico Rodriguez-Tomás Frickmann")
        # Le quitamos el width=30
        self.labelAutor.config(fg='#000000', font=("Roboto", 15), pady=10) 
        self.labelAutor.pack()