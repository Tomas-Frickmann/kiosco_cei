

import tkinter as tk
from PIL import Image, ImageTk
from tkinter import ttk, messagebox

from Utilitys.util_config import color_barra_superior,color_cuerpo_principal,color_menu_cursor_encima,color_menu_lateral,color_iconos_turquesa_oscuro,color_fondo_gris

class ProductsPanel():

    def __init__(self, main_body, controlador):
        self.controlador = controlador
        self.subcuerpo = tk.Frame(main_body, bg=color_barra_superior)
        self.subcuerpo.pack(side=tk.TOP, fill='both', expand=True)
        imagen_original_on = Image.open("images/Si.png")
        imagen_original_off = Image.open("images/No.png")
        imagen_redimensionada_on = imagen_original_on.resize((20, 20), Image.Resampling.LANCZOS)
        imagen_redimensionada_off = imagen_original_off.resize((20, 20), Image.Resampling.LANCZOS)
        self.check_on = ImageTk.PhotoImage(imagen_redimensionada_on)
        self.check_off = ImageTk.PhotoImage(imagen_redimensionada_off)

        self.check = None #Button de check

        # Crear el panel de productos
        self.FrameSearchProduct()
        self.TableProducts()

    def FrameSearchProduct(self):
        panelSearch = tk.Frame(self.subcuerpo, bg=color_menu_lateral,height=10)
        panelSearch.pack(side=tk.TOP, fill='both', expand=False)

        # Crear el marco para el campo de búsqueda
        frame_search = tk.Frame(panelSearch, bg=color_fondo_gris)
        frame_search.pack(side=tk.TOP, fill='both', expand=True, pady=20)

        # Etiqueta y campo de entrada para la búsqueda
        label_search = tk.Label(frame_search, text="Buscar Producto:", font=('Calibri', 12), bg=color_barra_superior, fg="White", width=20)
        label_search.pack(side=tk.LEFT, fill='both', expand=False, padx=5, pady=5)
        self.entry_search = tk.Entry(frame_search, font=('Calibri', 12), bg=color_cuerpo_principal, fg="black")
        self.entry_search.pack(side=tk.LEFT, fill='both', expand=True, padx=5, pady=5)
        self.entry_search.bind("<KeyRelease>", self.search_product)


        # Botón para agregar producto
        button_add_product = tk.Button(frame_search, text="Agregar Producto", font=('Calibri', 12),
                                    bg=color_iconos_turquesa_oscuro,
                                    fg="Black", command=self.producto)
        button_add_product.pack(side=tk.RIGHT, fill='both', expand=False, padx=5, pady=5)

        # Botón para editar producto seleccionado
        btn_editar = tk.Button(frame_search, text="Editar Producto", font=('Calibri', 12),
                            bg=color_iconos_turquesa_oscuro, fg="Black", command=lambda: self.producto(edicion = True))
        btn_editar.pack(side=tk.RIGHT, fill='x', padx=5, pady=5)

        # Botón para buscar producto
        button_actualizar = tk.Button(frame_search, text="Actualizar", font=('Calibri', 12), bg=color_iconos_turquesa_oscuro,
                                fg="Black", command=self.update_treeview)
        button_actualizar.pack(side=tk.RIGHT, fill='both', expand=False, padx=5, pady=5)
        button_search = tk.Button(frame_search, text="Buscar", font=('Calibri', 12), bg=color_iconos_turquesa_oscuro,
                                fg="Black", command=self.search_product)
        button_search.pack(side=tk.RIGHT, fill='both', expand=False, padx=5, pady=5)

    def TableProducts(self):
        # Destruir el frame anterior si existe
        if hasattr(self, 'Frame_cuerpotabla') and self.Frame_cuerpotabla.winfo_exists():
            self.Frame_cuerpotabla.destroy()

        style = ttk.Style()
        style.theme_use('clam')
        style.configure("Product.Treeview.Heading", font=('Calibri', 12, 'bold'), background="#1e293b", foreground="white",borderwidth=0,highlightthickness=0)
        style.map("Product.Treeview.Heading", background=[('active',  '#334155'), ('!active','#1e293b')])

        # Crear y guardar el nuevo frame
        self.Frame_cuerpotabla = tk.Frame(self.subcuerpo)
        self.Frame_cuerpotabla.pack(fill='both', expand=True, padx=5)

        label_products = tk.Label(self.Frame_cuerpotabla, text="Lista de Productos", font=('Calibri', 14), bg=color_barra_superior,
                                fg="white", width=20)
        label_products.pack(side=tk.TOP, fill='both', expand=False, padx=5, pady=5)

        # Frame para la tabla y el scrollbar
        frame_tabla = tk.Frame(self.Frame_cuerpotabla)
        frame_tabla.pack(fill='both', expand=True)

        # Definir columnas a mostrar
        columnas = self.controlador.consulta_mid("Columnas", None, True)
        ##Columnas es una lista de Row

        listaCabeceras = columnas[0].keys()

        ancho_columnas = dict(zip(listaCabeceras, [len(str(x))*10 for x in listaCabeceras]))
        # Crear Treeview
        """TREE"""
        self.tree = ttk.Treeview(frame_tabla, columns=listaCabeceras, show="headings", selectmode="browse",style="Product.Treeview",)
        """TREE"""
        for col in listaCabeceras:
            self.tree.heading(col, text=col.capitalize(), command=lambda c=col: self.sort_by_column(c, False))
            self.tree.column(col, width=ancho_columnas.get(col, 100), anchor="center")

        # Scrollbar vertical
        scrollbar = ttk.Scrollbar(frame_tabla, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Llenar la tabla con productos
        self.update_treeview()

    def get_products(self):
        try:
            productos = self.controlador.consulta_mid("Columnas", None, True)
            return productos
        except Exception as e:
            messagebox.showerror("Error", str(e))
            return []

    def update_treeview(self):
        # Borrar todos los ítems anteriores
        for item in self.tree.get_children():
            self.tree.delete(item)
            
        productos = self.get_products()
        for row in productos:
            values = self.controlador.columnas(row)
            self.tree.insert("", tk.END, values=values)
   
    def search_product(self, event=None):
        # Obtener el texto de búsqueda
        search_text = self.entry_search.get().strip()
        # Buscar productos cuyo nombre contenga el texto (insensible a mayúsculas/minúsculas)
        param = "%" + search_text + "%"
        results = self.controlador.consulta_mid("Busqueda", (param, param), True)

        for item in self.tree.get_children():
            self.tree.delete(item)
        # Si hay resultados, mostrarlos; si no, la tabla queda vacía
        if results:
            for row in results:
                values = self.controlador.columnas(row)
                self.tree.insert("", tk.END, values=values)
    
    def ventanaEditarAgregar(self, edicion=False, id_prod:str = ""):

        self.new_window = tk.Toplevel(self.subcuerpo)
        self.new_window.geometry("600x600")
        self.new_window.config(bg=color_menu_lateral)
        frame_product = tk.Frame(self.new_window, bg=color_menu_lateral)
        frame_product.pack(side=tk.TOP, fill='both', expand=True, pady=20)

        self.campos = {}
        self.checks = {}

        self.new_window.title("Editar Producto" if edicion else "Agregar Producto")
        self.creacionCampos(self.controlador.consulta_mid("BuscaId",(id_prod,None)),frame_product)

    def producto(self,edicion=False, event = None):
        """Está función es llamada por los botones AgregarProducto y EditarProducto """
        ##Edicion
        if edicion:
            selected = self.tree.focus()
            if not selected:
                messagebox.showwarning("Atención", "Seleccione un producto para editar.")
                return
            valores = self.tree.item(selected, "values")
            producto_id = valores[0]
        else:
            producto_id = None

        self.ventanaEditarAgregar(edicion, producto_id)

        # Si hay un ID, cargar los datos
        print("Producto_id: ", producto_id)
        if producto_id:
            resultado = self.controlador.consulta_mid("BuscaID", ("%"+producto_id+"%",), True)
            if resultado is None:
                messagebox.showerror("Error", f"No se pudo obtener el producto")
                return None
            print("Resultado: ",resultado)  # obtener la tupla

        
        
########################################################
    def crear_campo(self,frame_product: tk.Frame, texto:str, valor_inicial:str =""):
        """======Ventana ======"""
        Frame_casilla = tk.Frame(frame_product, bg=color_menu_lateral)
        Frame_casilla.pack(side=tk.TOP, fill='both', expand=False, padx=5, pady=5)
        label = tk.Label(Frame_casilla, text=texto, font=('Calibri', 12), bg=color_barra_superior, fg="white", width=20)
        label.pack(side=tk.LEFT, fill='both', expand=False, padx=5, pady=5)
        entry = tk.Entry(Frame_casilla, font=('Calibri', 12), bg=color_cuerpo_principal, fg="black")
        """============"""

        if valor_inicial:
            entry.insert(0, valor_inicial)
        entry.pack(side=tk.RIGHT, fill='both', expand=True, padx=5, pady=5)

        self.campos[texto.lower()] = entry

    def actualizar_color_check(self, event=None):
        if self.checks["controlstock"].get():
            self.check.config(
                bg="#084722", fg="black",
                activebackground="#084722",
                highlightbackground="#084722"
            )
        else:
            self.check.config(
                bg="#5a1d10", fg="white",
                activebackground="#5a1d10",
                highlightbackground="#5a1d10"
            )

    """!!!"""
    def creacionCampos(self, resultado:list, frame_product: tk.Frame):
        print("Linea 216: ", resultado)

        columnas = self.controlador.cabeceras_db()

        resultado = [i for i in " "*len(columnas)]
        
        for i in range(1,len(columnas)):
            self.crear_campo(frame_product,f"{columnas[i]}:", resultado[i])

        self.checks["controlstock"] = tk.IntVar(value=resultado[12] if resultado[0] != " " and resultado[-1] is not None else 0)

        self.check = tk.Checkbutton(
            frame_product, text="Control de Stock",
            variable=self.checks["controlstock"],
            image=self.check_off,
            selectimage=self.check_on,
            onvalue=1, offvalue=0,
            compound="left",
            indicatoron=False,
            font=("Calibri", 14),
            bg="#5a1d10",
            fg="white",
            activebackground="#27ae60",
            activeforeground="#2ecc71",
            highlightbackground="#5a1d10",  # <- importante
            command=self.actualizar_color_check
        )
        self.check.pack(pady=10)


        # Falta esto nomas
        texto_boton = "Guardar Cambios" if resultado[0] != " " else "Agregar Producto"
        comando = lambda: self.controlador.actualizar_producto(resultado[0])
        btn_guardar = tk.Button(frame_product, text=texto_boton, font=('Calibri', 12),
                                bg=color_menu_cursor_encima, fg="white", command=comando)
        btn_guardar.pack(side=tk.TOP, fill='both', expand=False, padx=5, pady=5)
