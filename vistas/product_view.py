

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
        self.entry_search.bind("<KeyRelease>", lambda event: self.search_product())
        self.entry_search.bind("<Return>", lambda event: self.search_product())


        # Botón para agregar producto
        button_add_product = tk.Button(frame_search, text="Agregar Producto", font=('Calibri', 12),
                                    bg=color_iconos_turquesa_oscuro,
                                    fg="Black", command=self.producto)
        button_add_product.pack(side=tk.RIGHT, fill='both', expand=False, padx=5, pady=5)

        # Botón para editar producto seleccionado
        btn_editar = tk.Button(frame_search, text="Editar Producto", font=('Calibri', 12),
                            bg=color_iconos_turquesa_oscuro, fg="Black", command=lambda: self.producto(True))
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
        columnas = ("id", "codigo", "nombre", "descripcion", "precio", "stock","controlstock")
        # Ancho de cada columna
        ancho_columnas = {"id":10,"codigo": 50,"nombre": 100,"descripcion": 300,"precio": 100,"stock": 50,"controlstock": 50}

        # Crear Treeview
        """TREE"""
        self.tree = ttk.Treeview(frame_tabla, columns=columnas, show="headings", selectmode="browse",style="Product.Treeview",)
        """TREE"""
        for col in columnas:
            self.tree.heading(col, text=col.capitalize(), command=lambda c=col: self.sort_by_column(c, False))
            self.tree.column(col, width=ancho_columnas.get(col, 100), anchor="center")

        # Scrollbar vertical
        scrollbar = ttk.Scrollbar(frame_tabla, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Llenar la tabla con productos
        self.update_treeview()

    def update_treeview(self):
        productos = self.get_products()

        # Borrar todos los ítems anteriores
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Insertar nuevos productos
        for prod in productos:
            controla = "Sí" if prod["controlstock"] else "No"
            self.tree.insert("", tk.END, values=(
                prod["id"], prod["codigo"], prod["nombre"], prod["descripcion"], prod["precio"], prod["stock"],controla))
    
    def search_product(self):
        # Obtener el texto de búsqueda
        search_text = self.entry_search.get().strip()
        # Buscar productos cuyo nombre contenga el texto (insensible a mayúsculas/minúsculas)
        text = f"%{search_text}%"
        param = (text, text)

        results = self.controlador.consulta_mid("Busqueda", param, True)

        # Limpiar la tabla
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Si hay resultados, mostrarlos; si no, la tabla queda vacía
        if results:
            for row in results:
                self.tree.insert("", tk.END, values=row)
    
    def producto(self,edicion=False, producto_id=None):


        ##Edicion 
        if edicion:
            # Si es edición, cargar el producto seleccionado
            selected = self.tree.focus()
            if not selected:
                messagebox.showwarning("Atención", "Seleccione un producto para editar.")
                return
            valores = self.tree.item(selected, "values")
            producto_id = valores[0]
            pass
        else:
            pass
        """"""
        self.new_window = tk.Toplevel(self.subcuerpo)
        self.new_window.title("Editar Producto" if producto_id else "Agregar Producto")
        self.new_window.geometry("600x600")
        self.new_window.config(bg=color_menu_lateral)

        frame_product = tk.Frame(self.new_window, bg=color_menu_lateral)
        frame_product.pack(side=tk.TOP, fill='both', expand=True, pady=20)

        self.campos = {}
        self.checks = {}
        

        def crear_campo(texto, clave, valor_inicial=""):
            """Buenisimo seria entender que hace está mierda"""

            """======Ventana======"""
            Frame_casilla = tk.Frame(frame_product, bg=color_menu_lateral)
            Frame_casilla.pack(side=tk.TOP, fill='both', expand=False, padx=5, pady=5)
            label = tk.Label(Frame_casilla, text=texto, font=('Calibri', 12), bg=color_barra_superior, fg="white", width=20)
            label.pack(side=tk.LEFT, fill='both', expand=False, padx=5, pady=5)
            entry = tk.Entry(Frame_casilla, font=('Calibri', 12), bg=color_cuerpo_principal, fg="black")
            """============"""

            """Valor inicial???"""

            if valor_inicial:
                entry.insert(0, valor_inicial)
            entry.pack(side=tk.RIGHT, fill='both', expand=True, padx=5, pady=5)

            self.campos[clave] = entry


        # Si hay un ID, cargar los datos
        if producto_id:
            resultado = self.controlador.consulta_mid("SELECT * FROM productos WHERE id = ?", (producto_id,), True)
            if resultado is None:
                messagebox.showerror("Error", f"No se pudo obtener el producto")
                return
            resultado = resultado[0]  # obtener la tupla
            """Mas tarde resuelvo esto"""
        # else:
        #     resultado = [None] * 13  # ajustá al número de columnas de tu tabla

        def safe_str(val):
            return str(val) if val is not None else ""

        crear_campo("Código:", "codigo", safe_str(resultado[1]))
        def validar_codigo(new_value):
            return len(new_value) <= 6

        vcmd = (self.new_window.register(validar_codigo), '%P')
        self.campos["codigo"].config(validate="key", validatecommand=vcmd)

        crear_campo("Nombre del Producto:", "nombre", safe_str(resultado[3]))
        crear_campo("Precio:", "precio", safe_str(resultado[4]))
        crear_campo("Descripción:", "descripcion", safe_str(resultado[5]))
        crear_campo("Stock:", "stock", safe_str(resultado[6]))
        crear_campo("Categoría:", "categoria", safe_str(resultado[8]))
        crear_campo("Subcategoría:", "subcategoria", safe_str(resultado[9]))
        crear_campo("Proveedor:", "proveedor", safe_str(resultado[10]))
        crear_campo("Imagen:", "imagen", safe_str(resultado[11]))

        self.checks["controlstock"] = tk.IntVar(value=resultado[12] if producto_id and resultado[12] is not None else 0)

        def actualizar_color_check():
            if self.checks["controlstock"].get():
                check.config(
                    bg="#27ae60", fg="black",
                    activebackground="#27ae60",
                    highlightbackground="#27ae60"
                )
            else:
                check.config(
                    bg="#5a1d10", fg="white",
                    activebackground="#5a1d10",
                    highlightbackground="#5a1d10"
                )

        check = tk.Checkbutton(
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
            command=actualizar_color_check
        )
        check.pack(pady=10)

        # Llama una vez para que el color inicial sea correcto
        actualizar_color_check()


        # Botón
        texto_boton = "Guardar Cambios" if producto_id else "Agregar Producto"
        comando = lambda: self.actualizar_producto(producto_id) if producto_id else self.save_product()
        btn_guardar = tk.Button(frame_product, text=texto_boton, font=('Calibri', 12),
                                bg=color_menu_cursor_encima, fg="white", command=comando)
        btn_guardar.pack(side=tk.TOP, fill='both', expand=False, padx=5, pady=5)
