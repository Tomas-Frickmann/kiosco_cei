import tkinter as tk
from controladores.main_controller import MainController

def main():
    root = tk.Tk()
    app = MainController(root)
    # app.iniciar() 
    root.mainloop()

if __name__ == "__main__":
    main()