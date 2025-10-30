import tkinter as tk
import datetime
import sqlite3
#from ttkbootstrap import Style
from PIL import Image, ImageTk
from tkinter import ttk
from tkinter import messagebox
from tkinter import PhotoImage
from tkinter import filedialog
from tkcalendar import Calendar
import Datos.Connect as db
from Forms.form_setting import app_state
from Forms.form_setting import cargar_configuracion
from config import color_barra_superior,color_cuerpo_principal,color_menu_cursor_encima,color_menu_lateral,color_iconos_turquesa_oscuro,color_fondo_gris

class PanelStore():
    
    def __init__(self, panel_principal,lista_ventas):
        self.nombre_maquina = cargar_configuracion().get("nombre_maquina", "SIN_NOMBRE")
        #Estilo
        self.style = ttk.Style()
        self.style.theme_use('clam')

        self.style.configure("Store.Treeview.Heading", font=('Calibri', 12, 'bold'), background="#1e293b", foreground="white"
                             ,borderwidth=0,highlightthickness=0,relief="flat")
        self.style.map("Store.Treeview.Heading", background=[('active', '#334155'), ('!active', '#1e293b')])

        self.style.layout("CustomCombobox.TCombobox",[("CustomCombobox.TCombobox", {'side': 'right', 'sticky': ''}),
                            ("CustomCombobox.padding", {'expand': '1', 'children': [("CustomCombobox.focus",{'expand':'1','sticky':'nswe','children':[("CustomCombobox.textarea", {'sticky': 'nswe'})]})]})])
        self.style.configure("CustomCombobox.TCombobox",fieldbackground="white", background="white",foreground="black",arrowcolor="black",
                             selectbackground="white",selectforeground="black",font=('Calibri', 12),borderwidth=0, relief="flat")
        self.style.map("Custom.TCombobox",
            fieldbackground=[("readonly", "black"),("!focus", "black"), ("!disabled", "black")],
            background=[("readonly", "black"),("!focus", "black"), ("!disabled", "black")],
            foreground=[("readonly", "black"), ("!focus", "black"), ("!disabled", "black")])

        self.subcuerpo = tk.Frame(panel_principal, bg=color_barra_superior)
        self.subcuerpo.pack(side=tk.TOP, fill='both', expand=True)
        self.lista_ventas = lista_ventas  # Lista para almacenar los productos agregados

        self.frame_encabezado = tk.Frame(self.subcuerpo, bg=color_barra_superior)
        self.frame_encabezado.pack(side=tk.TOP, fill='x', expand=False,anchor='n')

        self.cuboizq = tk.Frame(self.frame_encabezado, bg='#1ff11f')
        self.cuboizq.pack(side=tk.LEFT, fill='both', expand=True)
        btn_cerrar_caja = tk.Button( self.cuboizq, text="Cerrar Caja",font=('Calibri', 14),bg="#1e293b",fg="white",command=self.abrir_ventana_cierre_caja)
        btn_cerrar_caja.pack(side=tk.TOP, padx=10, pady=10)
        btn_visualizador = tk.Button(self.cuboizq, text="Visualizar Ventas", font=('Calibri', 14), bg="#1e293b", fg="white", command=self.abrir_visualizador_ventas)
        btn_visualizador.pack(side=tk.TOP, padx=10, pady=10)


        self.cuboder = tk.Frame(self.frame_encabezado, bg='#4f41af')
        self.cuboder.pack(side=tk.RIGHT, fill='both', expand=True)
        self.Precio()

        #Frame central para entrada y lista
        self.frame_central = tk.Frame(self.subcuerpo, bg=color_fondo_gris)
        self.frame_central.pack(side=tk.TOP, fill='both', expand=True)

        self.entrada_producto()
        self.vista_ventas()
        self.cargar_ventas_en_treeview()

    def Precio(self):
        color_fondo_precio = "#041228"
        self.frame_precio = tk.Frame(self.cuboder, bg="#1e293b")
        self.frame_precio.pack(side=tk.TOP, fill='x',expand=False, anchor='n')

        # Efectivo
        self.label_Efectivo_text = tk.Label(self.frame_precio, text="Efectivo:", font=('Calibri', 16), bg=color_fondo_precio, fg="#13eb33", anchor="w")
        self.label_Efectivo_text.grid(row=0, column=0, sticky="nsew", padx=5, pady=2)
        self.label_Efectivo_val = tk.Label(self.frame_precio, text="$0.00", font=('Calibri', 16), bg=color_fondo_precio, fg="#13eb33", anchor="e",width=12)
        self.label_Efectivo_val.grid(row=0, column=1, sticky="nsew", padx=5, pady=2)

        #Transferencia
        self.label_transferencia_text = tk.Label(self.frame_precio, text="Transferencia:", font=('Calibri', 16), bg=color_fondo_precio, fg="#58d6fc", anchor="w")
        self.label_transferencia_text.grid(row=1, column=0, sticky="nsew", padx=5, pady=2)
        self.label_transferencia_val = tk.Label(self.frame_precio, text="$0.00", font=('Calibri', 16), bg=color_fondo_precio, fg="#58d6fc", anchor="e",width=12)
        self.label_transferencia_val.grid(row=1, column=1, sticky="nsew", padx=5, pady=2)

        # Descuento
        self.label_descuento_text = tk.Label(self.frame_precio, text="Descuento:", font=('Calibri', 12), bg=color_fondo_precio, fg="#f7fa3e", anchor="w")
        self.label_descuento_text.grid(row=2, column=0, sticky="nsew", padx=5, pady=2)
        self.label_descuento_val = tk.Label(self.frame_precio, text="$0.00", font=('Calibri', 12), bg=color_fondo_precio, fg="#f7fa3e", anchor="e",width=12)
        self.label_descuento_val.grid(row=2, column=1, sticky="nsew", padx=5, pady=2)

        # TOTAL (en grande)
        self.label_total_text = tk.Label(self.frame_precio, text="TOTAL:", font=('Calibri', 38, 'bold'), bg=color_fondo_precio, fg="white", anchor="w")
        self.label_total_text.grid(row=3, column=0, sticky="nsew", padx=5, pady=5)
        self.label_total_val = tk.Label(self.frame_precio, text="$0.00", font=('Calibri', 38, 'bold'), bg=color_fondo_precio, fg="white", anchor="e",width=12)
        self.label_total_val.grid(row=3, column=1, sticky="nsew", padx=5, pady=5)

        # Configurar el ancho relativo de las columnas
        self.frame_precio.grid_columnconfigure(0, weight=1)  
        self.frame_precio.grid_columnconfigure(1, weight=5)   


    def entrada_producto(self):
        self.frame_entrada_producto = tk.Frame(self.frame_central, bg=color_barra_superior)
        self.frame_entrada_producto.pack(side=tk.TOP, fill='x', padx=10, pady=10)

        # Entrada para nombre de producto
        self.entry_producto = tk.Entry(self.frame_entrada_producto, font=('Calibri', 12), bg=color_cuerpo_principal)
        self.entry_producto.pack(side=tk.LEFT, fill='x', expand=True, padx=5)
        self.entry_producto.insert(0, "Nombre del producto")
        self.entry_producto.bind("<FocusIn>", self._clear_entry_producto)
        self.entry_producto.bind("<KeyRelease>", self.autocomplete_producto_suggestions)
        self.entry_producto.bind("<Down>", self._move_suggestion_down)
        self.entry_producto.bind("<Up>", self._move_suggestion_up)
        self.entry_producto.bind("<Return>", self._select_suggestion_with_enter)
   

        # Listbox para sugerencias (flotante)
        self.suggestion_box_producto = tk.Listbox(self.frame_central, font=('Calibri', 12), height=4)
        self.suggestion_box_producto.place_forget()
        self.suggestion_box_producto.bind("<<ListboxSelect>>", self.select_producto_suggestion)
        self.entry_producto.bind("<FocusOut>", lambda event: self.suggestion_box_producto.place_forget())
        self.suggestion_box_producto.bind("<FocusOut>", lambda event: self.suggestion_box_producto.place_forget())

        # Entrada para cantidad
        self.entry_cantidad = tk.Entry(self.frame_entrada_producto, font=('Calibri', 12), bg=color_cuerpo_principal,width=7)
        self.entry_cantidad.pack(side=tk.LEFT, fill='x', expand=True, padx=5)
        self.entry_cantidad.insert(0, "Cantidad")
        self.entry_cantidad.bind("<FocusIn>", self._clear_entry_cantidad)

        # Entrada para método de pago
        self.metodos_pago = ["Efectivo", "Transferencia"]
        self.combo_metodo_pago = ttk.Combobox(self.frame_entrada_producto,values=self.metodos_pago,state="readonly",font=('Calibri', 12), width=14,style="CustomCombobox.TCombobox")
        self.combo_metodo_pago.set("Efectivo")  # Valor por defecto
        self.combo_metodo_pago.pack(side=tk.LEFT, fill='x', expand=False, padx=5)

        


        # Botón para agregar
        self.btn_agregar = tk.Button(self.frame_entrada_producto, text="Agregar", command=self.agregar_producto, bg=color_iconos_turquesa_oscuro, fg="Black",width=15)
        self.btn_agregar.pack(side=tk.LEFT, padx=5)
        self.btn_agregar.bind('<Return>', lambda event: self.agregar_producto())

        # Bandera para limpiar solo la primera vez
        self._producto_cleared = False
        self._cantidad_cleared = False


    def vista_ventas(self):
        self.frame_lista = tk.Frame(self.frame_central, bg=color_fondo_gris)
        self.frame_lista.pack(side=tk.TOP, fill='both', expand=True)


        # Treeview para mostrar productos
        columnas = ('Producto','Precio Unitario' ,'Cantidad','Método de Pago','Total')
        self.tree = ttk.Treeview(self.frame_lista, columns=columnas, show='headings', style="Store.Treeview")

        # Encabezados
        self.tree.heading('Producto', text='Producto', anchor='w')
        self.tree.heading('Precio Unitario', text='Precio Unitario', anchor='center')
        self.tree.heading('Cantidad', text='Cantidad', anchor='center')
        self.tree.heading('Método de Pago', text='Método de Pago', anchor='center')
        self.tree.heading('Total', text='Total', anchor='e')

        # Columnas
        self.tree.column('Producto', anchor='w', width=150,stretch=True)
        self.tree.column('Precio Unitario', anchor='center', width=100)
        self.tree.column('Cantidad', anchor='center', width=70)
        self.tree.column('Método de Pago', anchor='center', width=120)
        self.tree.column('Total', anchor='e', width=120)


        self.tree.pack(fill='both', expand=True, padx=10, pady=10)

        # Bind para eliminar con la tecla Delete
        self.tree.bind('<Delete>', self.eliminar_producto_seleccionado)
        self.tree.bind('<BackSpace>', self.eliminar_producto_seleccionado)
        # Bind para aumentar/disminuir cantidad con + y -
        self.tree.bind('<Key-plus>', self.aumentar_cantidad_producto)
        self.tree.bind('<Key-minus>', self.reducir_cantidad_producto)
        self.tree.bind('<KP_Add>', self.aumentar_cantidad_producto)   # Teclado numérico +
        self.tree.bind('<KP_Subtract>', self.reducir_cantidad_producto) # Teclado numérico -
        self.tree.bind('t', self.cambiar_metodo_pago_producto) #Tecla t

        self.entry_cantidad.bind('<Return>', lambda event: self.agregar_producto())

        # Frame para botones debajo de la tabla
        self.frame_botones = tk.Frame(self.frame_central, bg=color_barra_superior)
        self.frame_botones.pack(side=tk.BOTTOM, fill='x')
        color_boton = "#1e293b"

        self.btn_finalizar = tk.Button(self.frame_botones,text="Finalizar venta\n(F12)",command=self.finalizar_venta,bg=color_boton, fg="white", width=15)
        self.btn_finalizar.pack(side=tk.RIGHT, padx=5, pady=5)
        self.frame_botones.bind_all('<F12>', lambda event: self.finalizar_venta())

        self.btn_finalizar_imprimir = tk.Button(self.frame_botones,text="Finalizar e Imprimir\n(F11)",command=self.finalizar_venta_imprimir,bg=color_boton, fg="white", width=18)
        self.btn_finalizar_imprimir.pack(side=tk.RIGHT, padx=5, pady=5)

        self.btn_borrar = tk.Button(self.frame_botones,text="Borrar producto\n(Del)",command=self.eliminar_producto_seleccionado,bg=color_boton,fg="white",width=15)
        self.btn_borrar.pack(side=tk.LEFT, padx=5, pady=5)

        self.btn_sumar = tk.Button(self.frame_botones,text="Agregar\n(+)",command=self.aumentar_cantidad_producto,bg=color_boton,fg="white",width=12)
        self.btn_sumar.pack(side=tk.LEFT, padx=5, pady=5) 

        self.btn_restar = tk.Button(self.frame_botones,text="Restar\n(-)",command=self.reducir_cantidad_producto,bg=color_boton,fg="white",width=12)
        self.btn_restar.pack(side=tk.LEFT, padx=5, pady=5)

        self.btn_cambiar_metodo = tk.Button(self.frame_botones, text="Cambiar método\n(T)",command=self.cambiar_metodo_pago_producto,bg=color_boton,fg="white",width=15)
        self.btn_cambiar_metodo.pack(side=tk.LEFT, padx=5, pady=5)

    def cargar_ventas_en_treeview(self):
        # Limpia el treeview si es necesario
        for item in self.tree.get_children():
            self.tree.delete(item)
        # Vuelve a cargar los productos
        for nombre, precio, cantidad,metodo_pago, total,*_ in self.lista_ventas:
            self.tree.insert('', 'end', values=(nombre, precio, cantidad,metodo_pago, total))
        self.actualizar_totales()


    def agregar_producto(self):
        producto = self.entry_producto.get().strip()
        cantidad = self.entry_cantidad.get().strip()
        metodo_pago = self.combo_metodo_pago.get()

        if not producto or not cantidad.isdigit():
            messagebox.showwarning("Error", "Debe ingresar un nombre válido y una cantidad numérica.")
            return
        
        # Traer todos los datos del producto
        query = "SELECT nombre, precio, descripcion, categoria, subcategoria, ControlStock, stock FROM productos WHERE nombre = ? OR codigo = ?"
        resultado = db.execute_query("Datos/datos.db", query, (producto, producto), fetch=True)
        if not resultado:
            messagebox.showerror("Error", "El producto no existe en la base de datos.")
            return
        nombre, precio, descripcion, categoria, subcategoria, control_stock, stock = resultado[0]
        cantidad = int(cantidad)

        if control_stock:
            if stock is None:
                messagebox.showerror("Error", f"El producto '{nombre}' no tiene stock definido.")
                return
            if cantidad > stock:
                messagebox.showerror("Error", f"No hay suficiente stock. Stock disponible: {stock}")
                return

        total = precio * cantidad
        self.lista_ventas.append((nombre, precio, cantidad, metodo_pago,total,categoria, subcategoria,descripcion))
        self.tree.insert('', 'end', values=(nombre, precio, cantidad,metodo_pago,total))

        # Limpiar entradas
        self.entry_producto.delete(0, tk.END)
        self.entry_cantidad.delete(0, tk.END)
        self.combo_metodo_pago.set("Efectivo")  # Resetear el método de pago a Efectivo

        # Actualizar el subtotal, descuento y total
        self.actualizar_totales()
        # Poner el foco en el entry de producto
        self.entry_producto.focus_set()


    def actualizar_totales(self):
        efectivo = sum(item[4] for item in self.lista_ventas if item[3] == "Efectivo")
        transferencia = sum(item[4] for item in self.lista_ventas if item[3] == "Transferencia")
        descuento = 0  # Aquí puedes implementar lógica para aplicar descuentos si es necesario
        total = efectivo + transferencia - descuento

        self.label_Efectivo_val.config(text=f"${efectivo:.2f}")
        self.label_transferencia_val.config(text=f"${transferencia:.2f}")
        self.label_descuento_val.config(text=f"${descuento:.2f}")
        self.label_total_val.config(text=f"${total:.2f}")

    def eliminar_producto_seleccionado(self, event=None):
        selected_item = self.tree.selection()
        if not selected_item:
            return
        for item in selected_item:
            values = self.tree.item(item, 'values')
            # Elimina de la lista interna
            for i, prod in enumerate(self.lista_ventas):
                if (str(prod[0]), str(prod[1]), str(prod[2]), str(prod[3])) == tuple(map(str, values)):
                    self.lista_ventas.pop(i)
                    break
            # Elimina del Treeview
            self.tree.delete(item)
        # Actualiza los totales
        self.actualizar_totales()

    def _clear_entry_producto(self, event):
        if not self._producto_cleared:
            self.entry_producto.delete(0, tk.END)
            self._producto_cleared = True

    def _clear_entry_cantidad(self, event):
        if not self._cantidad_cleared:
            self.entry_cantidad.delete(0, tk.END)
            self._cantidad_cleared = True

    def autocomplete_producto_suggestions(self, event):
        # Ignorar flechas y Enter para no recargar el Listbox
        if event.keysym in ("Up", "Down", "Return"):
            return
        
        text = self.entry_producto.get()
        if not text or text == "Nombre del producto":
            self.suggestion_box_producto.place_forget()
            return

        query = "SELECT nombre FROM productos WHERE nombre LIKE ? LIMIT 5"
        results = db.execute_query("Datos/datos.db", query, (text + "%",), fetch=True)
        self.suggestion_box_producto.delete(0, tk.END)
        if results:
            for row in results:
                self.suggestion_box_producto.insert(tk.END, row[0])
            # Posicionar el Listbox justo debajo del entry_producto
            x = self.entry_producto.winfo_rootx() - self.frame_central.winfo_rootx()
            y = self.entry_producto.winfo_rooty() - self.frame_central.winfo_rooty() + self.entry_producto.winfo_height()
            self.suggestion_box_producto.place(x=x, y=y, width=self.entry_producto.winfo_width())
            self.suggestion_box_producto.lift()
        else:
            self.suggestion_box_producto.place_forget()

    def select_producto_suggestion(self, event):
        if self.suggestion_box_producto.curselection():
            selected = self.suggestion_box_producto.get(self.suggestion_box_producto.curselection())
            self.entry_producto.delete(0, tk.END)
            self.entry_producto.insert(0, selected)
            self.suggestion_box_producto.place_forget()

    def _move_suggestion_down(self, event):
        if self.suggestion_box_producto.size() > 0:
            current = self.suggestion_box_producto.curselection()
            if not current:
                self.suggestion_box_producto.selection_set(0)
            else:
                idx = current[0]
                if idx < self.suggestion_box_producto.size() - 1:
                    self.suggestion_box_producto.selection_clear(idx)
                    self.suggestion_box_producto.selection_set(idx + 1)
            self.suggestion_box_producto.activate(self.suggestion_box_producto.curselection())
            return "break"

    def _move_suggestion_up(self, event):
        if self.suggestion_box_producto.size() > 0:
            current = self.suggestion_box_producto.curselection()
            if not current:
                self.suggestion_box_producto.selection_set(0)
            else:
                idx = current[0]
                if idx > 0:
                    self.suggestion_box_producto.selection_clear(idx)
                    self.suggestion_box_producto.selection_set(idx - 1)
            self.suggestion_box_producto.activate(self.suggestion_box_producto.curselection())
            return "break"

    def _select_suggestion_with_enter(self, event):
        # Si hay sugerencias y alguna está seleccionada, autocompleta y deja el foco en producto
        if self.suggestion_box_producto.size() > 0 and self.suggestion_box_producto.curselection():
            self.select_producto_suggestion(None)
            self.entry_producto.focus_set()
            return "break"
        # Si no hay sugerencias visibles
        elif not self.suggestion_box_producto.winfo_ismapped():
                producto_ingresado = self.entry_producto.get().strip()
                # Consulta directa a la base de datos para validar el producto
                query = "SELECT 1 FROM productos WHERE nombre = ? OR codigo = ? LIMIT 1"
                resultado = db.execute_query("Datos/datos.db", query, (producto_ingresado, producto_ingresado), fetch=True)
                if not resultado:
                    # Si no es válido, queda el foco en producto
                    self.entry_producto.focus_set()
                    self.entry_producto.selection_range(0, tk.END)
                    return "break"
                else:
                    # Si es válido, pasa a cantidad
                    self.entry_cantidad.focus_set()
                    return "break"
        
    def finalizar_venta(self):
        if messagebox.askyesno("Confirmar", "¿Desea finalizar la venta?"):
            self.guardar_ventas()
            self.lista_ventas.clear()
            self.cargar_ventas_en_treeview()  # Esto limpia el Treeview y actualiza totales
            messagebox.showinfo("Venta finalizada", "La venta se finalizó correctamente.")

    def finalizar_venta_imprimir(self):
        if messagebox.askyesno("Confirmar", "¿Desea finalizar la venta e imprimir el ticket?"):
            self.guardar_ventas()
            self.lista_ventas.clear()
            self.cargar_ventas_en_treeview()
            # Lógica para imprimir el ticket
            messagebox.showinfo("Venta finalizada", "La venta se finalizó e imprimió el ticket.")
    
    def guardar_ventas(self):
        now = datetime.datetime.now()
        fecha = now.strftime("%Y-%m-%d")
        hora = now.strftime("%H:%M:%S")

        # Calcular totales por método de pago
        total_efectivo = sum(item[4] for item in self.lista_ventas if item[3] == "Efectivo")
        total_transferencia = sum(item[4] for item in self.lista_ventas if item[3] == "Transferencia")
        total_general = total_efectivo + total_transferencia

        # Puedes elegir cómo guardar el total y el método de pago principal (aquí solo como ejemplo)
        metodo_pago = "Mixto" if total_efectivo > 0 and total_transferencia > 0 else (
            "Efectivo" if total_efectivo > 0 else "Transferencia"
        )

        # Insertar en ventas
        query_venta = """
            INSERT INTO ventas (fecha, hora, maquina,efectivo, transferencia, total, metodo_pago)
            VALUES (?, ?, ?, ?, ?, ?,?)
        """
        db.execute_query("Datos/datos.db", query_venta, (fecha, hora, self.nombre_maquina,total_efectivo,total_transferencia, total_general, metodo_pago))

        query_id = "SELECT id FROM ventas WHERE maquina = ? ORDER BY id DESC LIMIT 1"
        venta_id = db.execute_query("Datos/datos.db", query_id, (self.nombre_maquina,), fetch=True)[0][0]

        # 2. Insertar cada producto en detalle_ventas
        for nombre, precio, cantidad, metodo_pago_detalle, total, categoria, subcategoria, descripcion in self.lista_ventas:
            query_detalle = """
                INSERT INTO detalle_ventas (venta_id, producto, categoria, subcategoria, cantidad, precio_unitario, total, metodo_pago)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """
            db.execute_query(
                "Datos/datos.db",
                query_detalle,
                (venta_id, nombre, categoria, subcategoria, cantidad, precio, total, metodo_pago_detalle)
            )

    def aumentar_cantidad_producto(self, event=None):
        selected = self.tree.selection()
        if not selected:
            return
        item = selected[0]
        values = list(self.tree.item(item, 'values'))
        nombre, precio, cantidad, metodo_pago, total = values
        cantidad = int(cantidad) + 1
        total = float(precio) * cantidad
        # Actualiza en lista_ventas
        for prod in self.lista_ventas:
            if str(prod[0]) == str(nombre) and str(prod[1]) == str(precio) and str(prod[3]) == str(metodo_pago):
                prod_index = self.lista_ventas.index(prod)
                self.lista_ventas[prod_index] = (prod[0], prod[1], cantidad, prod[3], total, prod[5], prod[6], prod[7])
                break
        # Actualiza en Treeview
        self.tree.item(item, values=(nombre, precio, cantidad, metodo_pago, total))
        self.actualizar_totales()

    def reducir_cantidad_producto(self, event=None):
        selected = self.tree.selection()
        if not selected:
            return
        item = selected[0]
        values = list(self.tree.item(item, 'values'))
        nombre, precio, cantidad, metodo_pago, total = values
        cantidad = int(cantidad) - 1
        if cantidad < 1:
            return  # No permite cantidades menores a 1
        total = float(precio) * cantidad
        # Actualiza en lista_ventas
        for prod in self.lista_ventas:
            if str(prod[0]) == str(nombre) and str(prod[1]) == str(precio) and str(prod[3]) == str(metodo_pago):
                prod_index = self.lista_ventas.index(prod)
                self.lista_ventas[prod_index] = (prod[0], prod[1], cantidad, prod[3], total, prod[5], prod[6], prod[7])
                break
        # Actualiza en Treeview
        self.tree.item(item, values=(nombre, precio, cantidad, metodo_pago, total))
        self.actualizar_totales()

    def cambiar_metodo_pago_producto(self, event=None):
        selected = self.tree.selection()
        if not selected:
            return
        item = selected[0]
        values = list(self.tree.item(item, 'values'))
        nombre, precio, cantidad, metodo_pago, total = values

        # Cambia el método de pago
        nuevo_metodo = "Transferencia" if metodo_pago == "Efectivo" else "Efectivo"

        # Actualiza en lista_ventas
        for idx, prod in enumerate(self.lista_ventas):
            if (str(prod[0]), str(prod[1]), str(prod[2]), str(prod[3])) == (nombre, precio, cantidad, metodo_pago):
                self.lista_ventas[idx] = (prod[0], prod[1], prod[2], nuevo_metodo, prod[4], prod[5], prod[6], prod[7])
                break

        # Actualiza en Treeview
        self.tree.item(item, values=(nombre, precio, cantidad, nuevo_metodo, total))
        self.actualizar_totales()

    def abrir_ventana_cierre_caja(self):
        ventana = tk.Toplevel(self.cuboizq)
        ventana.title("Cierre de Caja")
        ventana.geometry("560x420")
        ventana.iconphoto(True, self.icono)
        ventana.config(bg=color_menu_lateral)

        # Fecha actual y hora actual
        fecha_actual = datetime.datetime.now()
        hora_actual = fecha_actual.strftime("%H:%M:%S")

        # Frame horizontal para los calendarios
        frame_calendarios = tk.Frame(ventana, bg=color_menu_lateral)
        frame_calendarios.pack(side=tk.TOP, fill='x', pady=10)

        # Frame para fecha de inicio
        frame_inicio = tk.Frame(frame_calendarios, bg=color_menu_lateral, padx=10)
        frame_inicio.pack(side=tk.LEFT, fill='both', expand=True)
        tk.Label(frame_inicio, text="Fecha de inicio:", font=('Calibri', 12), bg=color_menu_lateral, fg="white").pack(pady=5)
        cal_inicio = Calendar(frame_inicio, selectmode="day", date_pattern="yyyy-mm-dd")
        cal_inicio.pack(pady=5)
        cal_inicio.selection_set(fecha_actual.strftime("%Y-%m-%d"))

        # Frame para fecha de fin
        frame_fin = tk.Frame(frame_calendarios, bg=color_menu_lateral, padx=10)
        frame_fin.pack(side=tk.LEFT, fill='both', expand=True)
        tk.Label(frame_fin, text="Fecha de fin:", font=('Calibri', 12), bg=color_menu_lateral, fg="white").pack(pady=5)
        cal_fin = Calendar(frame_fin, selectmode="day", date_pattern="yyyy-mm-dd")
        cal_fin.pack(pady=5)
        cal_fin.selection_set(fecha_actual.strftime("%Y-%m-%d"))

        # Frame para hora y botones (debajo de los calendarios)
        frame_botones = tk.Frame(ventana, bg=color_menu_lateral, padx=10, pady=10)
        frame_botones.pack(side=tk.TOP, fill='x')

        # Hora
        tk.Label(frame_botones, text="Hora:", font=('Calibri', 12), bg=color_menu_lateral, fg="white").pack(pady=5)
        entry_hora = tk.Entry(frame_botones, font=('Calibri', 12))
        entry_hora.pack(pady=5)
        entry_hora.insert(0, hora_actual)

        # Botón para generar el informe
        frame_botones_centrados = tk.Frame(frame_botones, bg=color_menu_lateral)
        frame_botones_centrados.pack(pady=10)

        btn_generar = tk.Button(
            frame_botones_centrados,
            text="Generar Informe",
            font=('Calibri', 12),
            bg='#6D8299',
            fg='white',
            command=lambda: self.generar_informe_caja(
                cal_inicio.get_date(),
                cal_fin.get_date(),
                entry_hora.get(),
                ventana
            )
        )
        btn_generar.pack(side=tk.LEFT, padx=10)

        btn_cancelar = tk.Button(
            frame_botones_centrados,
            text="Cancelar",
            font=('Calibri', 12),
            bg='#FF6B6B',
            fg='white',
            command=ventana.destroy
        )
        btn_cancelar.pack(side=tk.LEFT, padx=10)
        
    def generar_informe_caja(self, fecha_inicio, fecha_fin, hora, ventana):
        # Consulta agrupada solo por producto y método de pago
        query = """
            SELECT 
                d.producto,
                d.metodo_pago,
                SUM(d.cantidad) as cantidad_total,
                SUM(d.total) as total_ventas
            FROM detalle_ventas d
            JOIN ventas v ON d.venta_id = v.id
            WHERE v.fecha BETWEEN ? AND ?
            GROUP BY d.producto, d.metodo_pago
            ORDER BY d.producto, d.metodo_pago
        """
        params = (fecha_inicio, fecha_fin)
        resumen = db.execute_query("Datos/datos.db", query, params, fetch=True)

        if not resumen:
            messagebox.showinfo("Sin resultados", "No se encontraron ventas en el rango seleccionado.")
            return

        # Organizar los datos para mostrar totales por producto y por método de pago
        productos = {}
        for producto, metodo_pago, cantidad, total in resumen:
            if producto not in productos:
                productos[producto] = {"Efectivo": [0, 0], "Transferencia": [0, 0]}
            productos[producto][metodo_pago][0] += cantidad
            productos[producto][metodo_pago][1] += total

        # Crear ventana de preview
        preview = tk.Toplevel(self.cuboizq)
        preview.title("Cierre de Caja Resumido")
        preview.geometry("900x600")
        preview.config(bg=color_menu_lateral)

        # Título y rango
        tk.Label(preview, text=f"Cierre de Caja - Rango: {fecha_inicio} a {fecha_fin} - Hora de cierre: {hora}",
                font=('Calibri', 14, 'bold'), bg=color_menu_lateral, fg="white").pack(pady=10)

        # Frame para la tabla
        frame_tabla = tk.Frame(preview, bg=color_menu_lateral)
        frame_tabla.pack(fill='both', expand=True, padx=10, pady=10)

        columnas = ["Producto", "Cant. Efectivo", "Total Efectivo", "Cant. Transferencia", "Total Transferencia","Cantidad Total", "Total General"]
        tree = ttk.Treeview(frame_tabla, columns=columnas, show='headings', height=20)
        for col in columnas:
            tree.heading(col, text=col)
            tree.column(col, anchor='center', width=120 if col != "Producto" else 180)
        tree.pack(fill='both', expand=True)

        # Insertar datos agrupados
        suma_cant_ef = 0
        suma_cant_tr = 0
        suma_cant_total = 0
        total_efectivo = 0
        total_transferencia = 0
        total_general = 0
        for producto, pagos in productos.items():
            cant_ef, tot_ef = pagos["Efectivo"]
            cant_tr, tot_tr = pagos["Transferencia"]
            cant_total = cant_ef + cant_tr
            total_prod = tot_ef + tot_tr
            suma_cant_ef += cant_ef
            suma_cant_tr += cant_tr
            suma_cant_total += cant_total
            total_efectivo += tot_ef
            total_transferencia += tot_tr
            total_general += total_prod
            tree.insert('', 'end', values=(
                producto,
                cant_ef, f"${tot_ef:.2f}",
                cant_tr, f"${tot_tr:.2f}",
                cant_total,  # Nueva columna
                f"${total_prod:.2f}"
            ))

        # Botón para cerrar
        btn_cerrar = tk.Button(preview, text="Cerrar", font=('Calibri', 12), bg='#FF6B6B', fg='white', command=preview.destroy)
        btn_cerrar.pack(pady=10)

        ventana.destroy()

    def abrir_visualizador_ventas(self):
        ventana = tk.Toplevel(self.subcuerpo)
        ventana.title("Visualizador de Ventas")
        ventana.geometry("1300x600")
        ventana.config(bg=color_menu_lateral)

        # Frame principal para todo
        frame_principal = tk.Frame(ventana, bg=color_menu_lateral)
        frame_principal.pack(fill='both', expand=True)

        # Frame para las tablas (ventas y detalle)
        frame_tablas = tk.Frame(frame_principal, bg=color_menu_lateral)
        frame_tablas.pack(side=tk.TOP, fill='both', expand=True)

        # Frame para la tabla de ventas
        frame_ventas = tk.Frame(frame_tablas, bg=color_menu_lateral)
        frame_ventas.pack(side=tk.LEFT, fill='y', padx=10, pady=10)

        columnas_ventas = ["ID", "Fecha", "Hora", "Total", "Método", "Máquina"]
        tree_ventas = ttk.Treeview(frame_ventas, columns=columnas_ventas, show='headings', height=20)
        for col in columnas_ventas:
            tree_ventas.heading(col, text=col)
            tree_ventas.column(col, anchor='center', width=100)
        tree_ventas.pack(fill='y', expand=True)

        # Frame para los detalles de la venta seleccionada
        frame_detalle = tk.Frame(frame_tablas, bg=color_menu_lateral)
        frame_detalle.pack(side=tk.RIGHT, fill='both', expand=True, padx=10, pady=10)

        columnas_detalle = ["Producto", "Cantidad", "Precio", "Total", "Método"]
        tree_detalle = ttk.Treeview(frame_detalle, columns=columnas_detalle, show='headings', height=20)
        for col in columnas_detalle:
            tree_detalle.heading(col, text=col)
            tree_detalle.column(col, anchor='center', width=120)
        tree_detalle.pack(fill='both', expand=True)

        # Cargar ventas
        query = "SELECT id, fecha, hora, total, metodo_pago, maquina FROM ventas ORDER BY id DESC"
        ventas = db.execute_query("Datos/datos.db", query, fetch=True)
        for venta in ventas:
            tree_ventas.insert('', 'end', values=venta)

        # Función para cargar detalles al seleccionar una venta
        def mostrar_detalle(event):
            selected = tree_ventas.selection()
            if not selected:
                return
            venta_id = tree_ventas.item(selected[0], 'values')[0]
            # Limpiar detalles anteriores
            for item in tree_detalle.get_children():
                tree_detalle.delete(item)
            # Cargar detalles de la venta seleccionada
            query_detalle = """
                SELECT producto, cantidad, precio_unitario, total, metodo_pago
                FROM detalle_ventas
                WHERE venta_id = ?
            """
            detalles = db.execute_query("Datos/datos.db", query_detalle, (venta_id,), fetch=True)
            for det in detalles:
                tree_detalle.insert('', 'end', values=det)

        tree_ventas.bind('<<TreeviewSelect>>', mostrar_detalle)

        # Frame para los botones abajo
        frame_botones = tk.Frame(frame_principal, bg=color_menu_lateral)
        frame_botones.pack(side=tk.BOTTOM, fill='x', pady=10)

        # Botón para cerrar (puedes agregar más botones aquí en el futuro)
        btn_cerrar = tk.Button(
            frame_botones,
            text="Cerrar",
            font=('Calibri', 12),
            bg='#FF6B6B',
            fg='white',
            command=ventana.destroy,
            width=15
        )
        btn_cerrar.pack(side=tk.RIGHT, padx=10)
