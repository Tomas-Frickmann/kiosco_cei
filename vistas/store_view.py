import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import Calendar
import datetime

from Utilitys.util_config import *
# from controladores.store_contrller import StoreController
class StoreView:
    def __init__(self, root, panel_principal, controlador):# StoreController):
        self.controlador = controlador
        self.root = self.controlador.root
        self.root = root

        # Estilos  "#1e293b"
        self.style = ttk.Style()
        self.style.theme_use('clam')
        self.style.configure("Store.Treeview.Heading", font=('Calibri', TAMAÑO_LETRA_CAJA, 'bold'), background="#ff0000", foreground="white", borderwidth=0, highlightthickness=0, relief="flat")
        self.style.map("Store.Treeview.Heading", background=[('active', '#334155'), ('!active', '#1e293b')])

        self.style.layout("CustomCombobox.TCombobox", [("CustomCombobox.TCombobox", {'side': 'right', 'sticky': ''}),
                            ("CustomCombobox.padding", {'expand': '1', 'children': [("CustomCombobox.focus", {'expand': '1', 'sticky': 'nswe', 'children': [("CustomCombobox.textarea", {'sticky': 'nswe'})]})]})])
        self.style.configure("CustomCombobox.TCombobox", fieldbackground="white", background="white", foreground="black", arrowcolor="black",
                             selectbackground="white", selectforeground="black", font=('Calibri', TAMAÑO_LETRA_CAJA), borderwidth=0, relief="flat")

        self.subcuerpo = tk.Frame(panel_principal, bg=color_barra_superior)
        self.subcuerpo.pack(side=tk.TOP, fill='both', expand=True)

        self.frame_encabezado = tk.Frame(self.subcuerpo, bg=color_barra_superior)
        self.frame_encabezado.pack(side=tk.TOP, fill='x', expand=False, anchor='n')

        # Botones Superiores (Izquierda)
        self.cuboizq = tk.Frame(self.frame_encabezado, bg="#1e293b")
        self.cuboizq.pack(side=tk.LEFT, fill='both', expand=True)

        tk.Button(self.cuboizq, text="Cerrar Caja", font=('Calibri',TAMAÑO_LETRA_CAJA), bg=color_fondo_precio, fg="white", command=self.abrir_ventana_cierre_caja).grid(row=3, column=0,  padx=10, pady=10)
        tk.Button(self.cuboizq, text="Visualizar Ventas", font=('Calibri', TAMAÑO_LETRA_CAJA), bg=color_fondo_precio, fg="white", command=self.abrir_visualizador_ventas).grid(row=3, column=1,  padx=10, pady=10)

        # Totales (Derecha)
        self.cuboder = tk.Frame(self.frame_encabezado, bg=color_barra_superior)
        self.cuboder.pack(side=tk.RIGHT, fill='both', expand=True)
        self.dibujar_panel_precio()

        # Centro (Ingreso de productos y Tabla)
        self.frame_central = tk.Frame(self.subcuerpo, bg=color_fondo_gris)
        self.frame_central.pack(side=tk.TOP, fill='both', expand=True)

        self.dibujar_entrada_producto()
        self.dibujar_vista_ventas()

    # ==========================================
    # DIBUJO DE INTERFAZ PRINCIPAL
    # ==========================================
    def dibujar_panel_precio(self):
        # 1e293b
        self.frame_precio = tk.Frame(self.cuboder, bg="#1e293b")
        self.frame_precio.pack(side=tk.TOP, fill='x', expand=False, anchor='n')

        tk.Label(self.frame_precio, text=" TOTAL:", font=('Calibri', 38, 'bold'), bg=color_fondo_precio, fg="white", anchor="w").grid(row=3, column=0, sticky="nsew", padx=5, pady=5)
        self.label_total_val = tk.Label(self.frame_precio, text="$0.00", font=('Calibri', 38, 'bold'), bg=color_fondo_precio, fg="white", anchor="e", width=12)
        self.label_total_val.grid(row=3, column=1, sticky="nsew", padx=5, pady=5)

        self.frame_precio.grid_columnconfigure(0, weight=1)  
        self.frame_precio.grid_columnconfigure(1, weight=5)   

    def dibujar_entrada_producto(self):
        self.frame_entrada_producto = tk.Frame(self.frame_central, bg=color_barra_superior)
        self.frame_entrada_producto.pack(side=tk.TOP, fill='x', padx=10, pady=10)

        # Entry Producto
        self.entry_producto = tk.Entry(self.frame_entrada_producto, font=('Calibri', TAMAÑO_LETRA_CAJA), bg=color_cuerpo_principal)
        self.entry_producto.pack(side=tk.LEFT, fill='x', expand=True, padx=5)
        self.entry_producto.insert(0, "Nombre del producto")
        self.entry_producto.bind("<FocusIn>", self._clear_entry_producto)
        self.entry_producto.bind("<KeyRelease>", self.autocomplete_producto_suggestions)
        self.entry_producto.bind("<Down>", self._move_suggestion_down)
        self.entry_producto.bind("<Up>", self._move_suggestion_up)
        self.entry_producto.bind("<Return>", self._select_suggestion_with_enter)

        # Listbox Flotante
        self.suggestion_box_producto = tk.Listbox(self.frame_central, font=('Calibri', TAMAÑO_LETRA_CAJA), height=4)
        self.suggestion_box_producto.place_forget()
        self.suggestion_box_producto.bind("<<ListboxSelect>>", self.select_producto_suggestion)
        self.entry_producto.bind("<FocusOut>", lambda e: self.suggestion_box_producto.place_forget())
        
        self.suggestion_box_producto.bind("<FocusOut>", lambda e: self.suggestion_box_producto.place_forget())

        # Entry Cantidad
        self.entry_cantidad = tk.Entry(self.frame_entrada_producto, font=('Calibri', TAMAÑO_LETRA_CAJA), bg=color_cuerpo_principal, width=7)
        self.entry_cantidad.pack(side=tk.LEFT, fill='x', expand=True, padx=5)
        self.entry_cantidad.insert(0, "1")
        

        # CORREGIDO: Llamar a enviar_producto sin pasar los parámetros viejos
        self.entry_cantidad.bind("<Return>", lambda e: self.enviar_producto())

        # Botón Agregar CORREGIDO: Se usa command=self.enviar_producto (sin paréntesis)
        self.btn_agregar = tk.Button(self.frame_entrada_producto, text="Agregar", command=self.enviar_producto, bg=color_iconos_turquesa_oscuro, fg="Black", width=15)
        self.btn_agregar.pack(side=tk.LEFT, padx=5)

        self._producto_cleared = False
        self._cantidad_cleared = False

    def dibujar_vista_ventas(self):
        self.frame_lista = tk.Frame(self.frame_central, bg=color_fondo_gris)
        self.frame_lista.pack(side=tk.TOP, fill='both', expand=True)

        columnas = ('Producto', 'Precio Unitario', 'Cantidad', 'Total')
        self.tree = ttk.Treeview(self.frame_lista, columns=columnas, show='headings', style="Store.Treeview")

        for col in columnas:
            self.tree.heading(col, text=col, anchor='center' if col != 'Producto' else 'w')
        
        self.tree.heading('Total', text='Total', anchor='e')
        self.tree.column('Producto', anchor='w', width=150, stretch=True)
        self.tree.column('Precio Unitario', anchor='center', width=100)
        self.tree.column('Cantidad', anchor='center', width=70)
        self.tree.column('Total', anchor='e', width=120)
        self.tree.pack(fill='both', expand=True, padx=10, pady=10)

        # Atajos de Teclado del Treeview
        self.tree.bind('<Delete>', lambda e: self.controlador.eliminar_producto(self._get_selected_indices()))
        self.tree.bind('<BackSpace>', lambda e: self.controlador.eliminar_producto(self._get_selected_indices()))
        self.tree.bind('<Key-plus>', lambda e: self.controlador.modificar_cantidad(self._get_first_selected_index(), "+"))
        self.tree.bind('<KP_Add>', lambda e: self.controlador.modificar_cantidad(self._get_first_selected_index(), "+"))
        self.tree.bind('<Key-minus>', lambda e: self.controlador.modificar_cantidad(self._get_first_selected_index(), "-"))
        self.tree.bind('<KP_Subtract>', lambda e: self.controlador.modificar_cantidad(self._get_first_selected_index(), "-"))

        # Frame Botones Inferiores
        self.frame_botones = tk.Frame(self.frame_central, bg=color_barra_superior)
        self.frame_botones.pack(side=tk.BOTTOM, fill='x')
        color_boton = "#1e293b"

        tk.Button(self.frame_botones, text="Finalizar venta\n(F12)", command=lambda: self.controlador.finalizar_venta(), bg=color_boton, fg="white", width=15).pack(side=tk.RIGHT, padx=5, pady=5)
        tk.Button(self.frame_botones, text="Finalizar e Imprimir\n(F11)", command=lambda: self.controlador.finalizar_venta(imprimir=True), bg=color_boton, fg="white", width=18).pack(side=tk.RIGHT, padx=5, pady=5)
        self.root.bind_all('<F12>', lambda e: self.controlador.finalizar_venta())

        tk.Button(self.frame_botones, text="Borrar producto\n(Del)", command=lambda: self.controlador.eliminar_producto(self._get_selected_indices()), bg=color_boton, fg="white", width=15).pack(side=tk.LEFT, padx=5, pady=5)
        tk.Button(self.frame_botones, text="Agregar\n(+)", command=lambda: self.controlador.modificar_cantidad(self._get_first_selected_index(), "+"), bg=color_boton, fg="white", width=12).pack(side=tk.LEFT, padx=5, pady=5)
        tk.Button(self.frame_botones, text="Restar\n(-)", command=lambda: self.controlador.modificar_cantidad(self._get_first_selected_index(), "-"), bg=color_boton, fg="white", width=12).pack(side=tk.LEFT, padx=5, pady=5)

    # ==========================================
    # ACTUALIZADORES DESDE EL CONTROLADOR
    # ==========================================

    def refrescar_tabla(self, lista_ventas):
        for item in self.tree.get_children():
            self.tree.delete(item)
        for prod in lista_ventas:
            # prod[-1] agarra siempre el Total sin importar si el Controlador manda 4 o 5 datos
            self.tree.insert('', 'end', values=(prod[0], f"${prod[1]:.2f}", prod[2], f"${prod[-1]:.2f}"))

    # CORREGIDO: Se usa *args para atrapar cualquier cantidad de valores que envíe el Controlador y sacar solo el último (el Total General)
    def actualizar_totales_ui(self, *args):
        if args:
            total_general = args[-1]
            self.label_total_val.config(text=f"${total_general:.2f}")
    #  Se usa *args para atrapar cualquier cantidad de valores que envíe el Controlador y sacar solo el último (el Total General)
    def actualizar_totales_ui(self, total_general):
       self.label_total_val.config(text=f"${total_general:.2f}")

    def limpiar_entradas(self,lugar):
        if lugar == CAJA:
            self.entry_producto.delete(0, tk.END)
            self.entry_cantidad.delete(0, tk.END)
            self.entry_cantidad.insert(0, "1")
            self.entry_producto.focus_set()
        elif lugar == COBRO:
            self.entry_efectivo.delete(0, tk.END)
            self.entry_transf.delete(0, tk.END)
            self.entry_efectivo.insert(0, "0.00")
            self.entry_transf.insert(0, "0.00")


    def limpiar_entradas(self):
        self.entry_producto.delete(0, tk.END)
        self.entry_cantidad.delete(0, tk.END)
        self.entry_cantidad.insert(0, "1")
        self.entry_producto.focus_set()

    def enviar_producto(self):
        # CORREGIDO: Solo se mandan 2 valores (producto y cantidad)
        self.controlador.agregar_producto(self.entry_producto.get(), self.entry_cantidad.get())

    # ==========================================
    # AYUDANTES (HELPERS) DE LA TABLA Y CAJAS
    # ==========================================
   
    def _get_selected_indices(self):
        return [self.tree.index(item) for item in self.tree.selection()]

    def _get_first_selected_index(self):
        indices = self._get_selected_indices()
        return indices[0] if indices else -1

    def _clear_entry_producto(self, event):
        if not self._producto_cleared:
            self.entry_producto.delete(0, tk.END)
            self._producto_cleared = True

    def _clear_entry_cantidad(self, event):
        if not self._cantidad_cleared:
            self.entry_cantidad.delete(0, tk.END)
            self._cantidad_cleared = True

    # ==========================================
    # AUTOCOMPLETADO
    # ==========================================

    def autocomplete_producto_suggestions(self, event):
        if event.keysym in ("Up", "Down", "Return"): return

        text = self.entry_producto.get().strip()
        if not text or text == "Nombre del producto":
            self.suggestion_box_producto.place_forget()
            return

        if self.controlador.validar_producto_rapido(text):
            self.suggestion_box_producto.place_forget()
            return
        sugerencias = self.controlador.obtener_sugerencias(text)
        self.suggestion_box_producto.delete(0, tk.END)

        if sugerencias:
            for s in sugerencias:
                self.suggestion_box_producto.insert(tk.END, s)
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
            self.entry_cantidad.focus_set()

    def _move_suggestion_down(self, event):
        if self.suggestion_box_producto.size() > 0:
            current = self.suggestion_box_producto.curselection()
            if not current: self.suggestion_box_producto.selection_set(0)
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
            if not current: self.suggestion_box_producto.selection_set(0)
            else:
                idx = current[0]
                if idx > 0:
                    self.suggestion_box_producto.selection_clear(idx)
                    self.suggestion_box_producto.selection_set(idx - 1)
            self.suggestion_box_producto.activate(self.suggestion_box_producto.curselection())
            return "break"

    def _select_suggestion_with_enter(self, event):
        if self.suggestion_box_producto.size() > 0 and self.suggestion_box_producto.curselection():
            self.select_producto_suggestion(None)
            self.entry_producto.focus_set()
            
            self.suggestion_box_producto.selection_clear(0,tk.END)
            return "break"
        elif not self.suggestion_box_producto.winfo_ismapped():
            valido = self.controlador.validar_producto_rapido(self.entry_producto.get().strip())
            
            if not valido:
                self.entry_producto.focus_set()
                self.entry_producto.selection_range(0, tk.END)
            else:
                self.entry_cantidad.focus_set()
            self.suggestion_box_producto.selection_clear(0,tk.END)
            return "break"

    # ==========================================
    # VENTANAS EMERGENTES (TOPLEVELS)
    # ==========================================
  

    def mostrar_mensaje(self, tipo, titulo, mensaje):
        if tipo == "info": messagebox.showinfo(titulo, mensaje)
        elif tipo == "error": messagebox.showerror(titulo, mensaje)
        elif tipo == "warning": messagebox.showwarning(titulo, mensaje)
        elif tipo == "question": return messagebox.askyesno(titulo, mensaje)

    def abrir_ventana_cierre_caja(self):
        ventana = tk.Toplevel(self.root)
        ventana.title("Cierre de Caja")
        ventana.geometry("560x420")
        ventana.config(bg=color_menu_lateral)

        fecha_actual = datetime.datetime.now()

        frame_calendarios = tk.Frame(ventana, bg=color_menu_lateral)
        frame_calendarios.pack(side=tk.TOP, fill='x', pady=10)

        frame_inicio = tk.Frame(frame_calendarios, bg=color_menu_lateral, padx=10)
        frame_inicio.pack(side=tk.LEFT, fill='both', expand=True)
        tk.Label(frame_inicio, text="Fecha inicio:", font=('Calibri', TAMAÑO_LETRA_CAJA), bg=color_menu_lateral, fg="white").pack(pady=5)
        cal_inicio = Calendar(frame_inicio, selectmode="day", date_pattern="yyyy-mm-dd")
        cal_inicio.pack(pady=5)
        cal_inicio.selection_set(fecha_actual.strftime("%Y-%m-%d"))

        frame_fin = tk.Frame(frame_calendarios, bg=color_menu_lateral, padx=10)
        frame_fin.pack(side=tk.LEFT, fill='both', expand=True)
        tk.Label(frame_fin, text="Fecha fin:", font=('Calibri', TAMAÑO_LETRA_CAJA), bg=color_menu_lateral, fg="white").pack(pady=5)
        cal_fin = Calendar(frame_fin, selectmode="day", date_pattern="yyyy-mm-dd")
        cal_fin.pack(pady=5)
        cal_fin.selection_set(fecha_actual.strftime("%Y-%m-%d"))

        frame_botones = tk.Frame(ventana, bg=color_menu_lateral, padx=10, pady=10)
        frame_botones.pack(side=tk.TOP, fill='x')

        tk.Label(frame_botones, text="Hora:", font=('Calibri', TAMAÑO_LETRA_CAJA), bg=color_menu_lateral, fg="white").pack(pady=5)
        entry_hora = tk.Entry(frame_botones, font=('Calibri', TAMAÑO_LETRA_CAJA))
        entry_hora.pack(pady=5)
        entry_hora.insert(0, fecha_actual.strftime("%H:%M:%S"))

        f_botones_c = tk.Frame(frame_botones, bg=color_menu_lateral)
        f_botones_c.pack(pady=10)
        tk.Button(f_botones_c, text="Generar Informe", font=('Calibri', TAMAÑO_LETRA_CAJA), bg='#6D8299', fg='white', 
                  command=lambda: self.controlador.generar_informe_caja(cal_inicio.get_date(), cal_fin.get_date(), entry_hora.get(), ventana)).pack(side=tk.LEFT, padx=10)
        tk.Button(f_botones_c, text="Cancelar", font=('Calibri', TAMAÑO_LETRA_CAJA), bg='#FF6B6B', fg='white', command=ventana.destroy).pack(side=tk.LEFT, padx=10)

    def mostrar_resumen_caja(self, productos_agrupados, fecha_inicio, fecha_fin, hora):
        preview = tk.Toplevel(self.root)
        preview.title("Cierre de Caja Resumido")
        preview.title("Cierre de Caja")
        preview.geometry("900x600")
        preview.config(bg=color_menu_lateral)

        tk.Label(preview, text=f"Cierre de Caja - Rango: {fecha_inicio} a {fecha_fin} - Hora: {hora}", font=('Calibri', TAMAÑO_LETRA_CAJA, 'bold'), bg=color_menu_lateral, fg="white").pack(pady=10)

        frame_tabla = tk.Frame(preview, bg=color_menu_lateral)
        frame_tabla.pack(fill='both', expand=True, padx=10, pady=10)

        columnas = ["Producto", "Cant. Ef", "Total Ef", "Cant. Tr", "Total Tr", "Cant Total", "Total General"]
        tree = ttk.Treeview(frame_tabla, columns=columnas, show='headings', height=20)
        for col in columnas:
            tree.heading(col, text=col)
            tree.column(col, anchor='center', width=120 if col != "Producto" else 180)
        tree.pack(fill='both', expand=True)

        for producto, pagos in productos_agrupados.items():
            cant_ef, tot_ef = pagos["Efectivo"]
            cant_tr, tot_tr = pagos["Transferencia"]
            tree.insert('', 'end', values=(
                producto, cant_ef, f"${tot_ef:.2f}", cant_tr, f"${tot_tr:.2f}",
                cant_ef + cant_tr, f"${tot_ef + tot_tr:.2f}"
            ))

        tk.Button(preview, text="Cerrar", font=('Calibri', TAMAÑO_LETRA_CAJA), bg='#FF6B6B', fg='white', command=preview.destroy).pack(pady=10)

    def abrir_visualizador_ventas(self):
        ventana = tk.Toplevel(self.root)
        ventana.title("Historial de Ventas")
        ventana.geometry("1100x600")
        ventana.config(bg=color_menu_lateral)

        frame_tablas = tk.Frame(ventana, bg=color_menu_lateral)
        frame_tablas.pack(side=tk.TOP, fill='both', expand=True)

        # Tabla Ventas
        frame_ventas = tk.Frame(frame_tablas, bg=color_menu_lateral)
        frame_ventas.pack(side=tk.LEFT, fill='y', padx=10, pady=10)
        columnas_v = ["ID", "Fecha", "Hora", "Total", "Método", "Máquina"]
        tree_ventas = ttk.Treeview(frame_ventas, columns=columnas_v, show='headings', height=20)
        for col in columnas_v:
            tree_ventas.heading(col, text=col)
            tree_ventas.column(col, anchor='center', width=100)
        tree_ventas.pack(fill='y', expand=True)

        # Tabla Detalles
        frame_detalle = tk.Frame(frame_tablas, bg=color_menu_lateral)
        frame_detalle.pack(side=tk.RIGHT, fill='both', expand=True, padx=10, pady=10)
        columnas_d = ["Producto", "Cantidad", "Precio", "Total", "Método"]
        tree_detalle = ttk.Treeview(frame_detalle, columns=columnas_d, show='headings', height=20)
        for col in columnas_d:
            tree_detalle.heading(col, text=col)
            tree_detalle.column(col, anchor='center', width=120)
        tree_detalle.pack(fill='both', expand=True)

        # Cargar datos
        ventas = self.controlador.obtener_historial_ventas()
        for v in ventas:
            tree_ventas.insert('', 'end', values=v)

        def mostrar_detalle(event):
            selected = tree_ventas.selection()
            if not selected: return
            venta_id = tree_ventas.item(selected[0], 'values')[0]

            for item in tree_detalle.get_children():
                tree_detalle.delete(item)

            detalles = self.controlador.obtener_detalle_venta(venta_id)
            for d in detalles:
                tree_detalle.insert('', 'end', values=d)

        tree_ventas.bind('<<TreeviewSelect>>', mostrar_detalle)
        tk.Button(ventana, text="Cerrar", font=('Calibri', TAMAÑO_LETRA_CAJA), bg='#FF6B6B', fg='white', command=ventana.destroy, width=15).pack(side=tk.BOTTOM, pady=10)

    def abrir_ventana_cobro(self, total_general, imprimir=False):
        ventana = tk.Toplevel(self.root)
        ventana.transient(self.root)  
        ventana.grab_set()  
        ventana.title("Finalizar Venta - Cobro")
        ventana.geometry("400x420")
        ventana.config(bg=color_menu_lateral)

        # Esto hace que la ventana quede por encima y no puedas tocar el panel de atrás hasta que cobres
        ventana.grab_set() 

        self.desabilita_atajos()
        ventana.bind( '<Escape>',lambda e: self.cerrar_y_reactivar(ventana))
        ventana.protocol("WM_DELETE_WINDOW", lambda: self.cerrar_y_reactivar(ventana))
        # Título con el Total
        tk.Label(ventana, text=f"Total a Cobrar:\n${total_general:.2f}", font=('Calibri', 24, 'bold'), bg=color_menu_lateral, fg="#f7fa3e").pack(pady=20)

        # Desplegable de Método
        tk.Label(ventana, text="Seleccione Método de Pago:", font=('Calibri', TAMAÑO_LETRA_CAJA), bg=color_menu_lateral, fg="white").pack(pady=5)
        metodo_var = tk.StringVar(value="Efectivo")
        combo = ttk.Combobox(ventana, textvariable=metodo_var, values=["Efectivo", "Transferencia", "Mixto"], state="readonly", font=('Calibri', TAMAÑO_LETRA_CAJA))
        combo.pack(pady=5)

        # Cuadros de texto para los montos
        frame_montos = tk.Frame(ventana, bg=color_menu_lateral)

        frame_montos.pack(pady=20)

        tk.Label(frame_montos, text="Monto Efectivo ($):", font=('Calibri', TAMAÑO_LETRA_CAJA), bg=color_menu_lateral, fg="white").grid(row=0, column=0, padx=10, pady=10, sticky="e")
        entry_efectivo = tk.Entry(frame_montos, font=('Calibri', TAMAÑO_LETRA_CAJA), width=12, justify="center")
        entry_efectivo.grid(row=0, column=1, padx=10, pady=10)
        self.entry_efectivo = tk.Entry(frame_montos, font=('Calibri', TAMAÑO_LETRA_CAJA), width=12, justify="center")
        self.entry_efectivo.grid(row=0, column=1, padx=10, pady=10)

        tk.Label(frame_montos, text="Monto Transf. ($):", font=('Calibri', TAMAÑO_LETRA_CAJA), bg=color_menu_lateral, fg="white").grid(row=1, column=0, padx=10, pady=10, sticky="e")
        entry_transf = tk.Entry(frame_montos, font=('Calibri', TAMAÑO_LETRA_CAJA), width=12, justify="center")
        entry_transf.grid(row=1, column=1, padx=10, pady=10)
        self.entry_transf = tk.Entry(frame_montos, font=('Calibri', TAMAÑO_LETRA_CAJA), width=12, justify="center")
        self.entry_transf.grid(row=1, column=1, padx=10, pady=10)
        
        combo.focus_set() 

        combo.bind('<Return>', lambda e: self.entry_efectivo.focus_set())   
        combo.bind('m', lambda e: metodo_var.set("Mixto"))
        combo.bind('e', lambda e: metodo_var.set("Efectivo"))
        combo.bind('t', lambda e: metodo_var.set("Transferencia"))
       
        combo.bind('<Return>', lambda e: self.entry_efectivo.focus_set())   
        self.entry_efectivo.bind('<Return>', lambda e: self.entry_transf.focus_set())
        self.entry_efectivo.bind('<FocusIn>', lambda e: self.entry_efectivo.delete(0, tk.END))
        
        # --- NUEVAS FUNCIONES PARA EL CÁLCULO AUTOMÁTICO (MIXTO) ---
        # def calcular_resto_efectivo(event):
            # Solo hace el cálculo si estamos en Mixto
        def calcular_resto(TIPO):
                       
            if metodo_var.get() == "Mixto":
                try:
                    # Intenta leer lo que escribiste, si está vacío o hay un error, usa 0
                    ingresado = float(entry_efectivo.get())
                    if TIPO == EFECTIVO:
                        ingresado = float(self.entry_efectivo.get())
                    else:
                        ingresado = float(self.entry_transf.get())
                    
                    if ingresado >=0 and ingresado <= total_general:
                        resto = total_general - ingresado
                        
                        if TIPO == EFECTIVO:
                            self.entry_transf.delete(0, tk.END)
                            self.entry_transf.insert(0, f"{resto:.2f}")
                        else:
                            self.entry_efectivo.delete(0, tk.END)
                            self.entry_efectivo.insert(0, f"{resto:.2f}")
                    else:
                        self.mostrar_mensaje("error", "Error", "El monto ingresado no es válido")
                        
                        if TIPO == EFECTIVO:
                            self.entry_efectivo.delete(0, tk.END)
                            self.entry_transf.delete(0, tk.END)
                            self.entry_transf.insert(0, f"{0:.2f}")
                        else:
                            self.entry_transf.delete(0, tk.END)
                            self.entry_efectivo.delete(0, tk.END)
                            self.entry_efectivo.insert(0, f"{0:.2f}")
                except ValueError:
                    ingresado = 0.0

                resto = total_general - ingresado

                # Actualiza la cajita de Transferencia con lo que falta
                entry_transf.delete(0, tk.END)
                entry_transf.insert(0, f"{resto:.2f}")

        def calcular_resto_transf(event):
            # Lo mismo, pero a la inversa
            if metodo_var.get() == "Mixto":
                try:
                    ingresado = float(entry_transf.get())
                except ValueError:
                    ingresado = 0.0
                    
                
                
                

                resto = total_general - ingresado

                # Actualiza la cajita de Efectivo con lo que falta
                entry_efectivo.delete(0, tk.END)
                entry_efectivo.insert(0, f"{resto:.2f}")

        # Le conectamos los sensores de teclado a las cajitas
        entry_efectivo.bind("<KeyRelease>", calcular_resto_efectivo)
        entry_transf.bind("<KeyRelease>", calcular_resto_transf)
        self.entry_efectivo.bind("<KeyRelease>", lambda e: calcular_resto(EFECTIVO))
        self.entry_transf.bind("<KeyRelease>", lambda e: calcular_resto(TRANSFERENCIA))

        # --- FUNCIÓN MÁGICA PRINCIPAL ---
        def actualizar_montos(*args):
            metodo = metodo_var.get()
            entry_efectivo.config(state='normal')
            entry_transf.config(state='normal')
            entry_efectivo.delete(0, tk.END)
            entry_transf.delete(0, tk.END)
            self.entry_efectivo.config(state='normal')
            self.entry_transf.config(state='normal')
            self.entry_efectivo.delete(0, tk.END)
            self.entry_transf.delete(0, tk.END)

            if metodo == "Efectivo":
                entry_efectivo.insert(0, f"{total_general:.2f}")
                entry_transf.insert(0, "0.00")
                entry_efectivo.config(state='readonly')
                entry_transf.config(state='readonly')
                self.entry_efectivo.insert(0, f"{total_general:.2f}")
                self.entry_transf.insert(0, "0.00")
                self.entry_efectivo.config(state='readonly')
                self.entry_transf.config(state='readonly')
            elif metodo == "Transferencia":
                entry_efectivo.insert(0, "0.00")
                entry_transf.insert(0, f"{total_general:.2f}")
                entry_efectivo.config(state='readonly')
                entry_transf.config(state='readonly')
                self.entry_efectivo.insert(0, "0.00")
                self.entry_transf.insert(0, f"{total_general:.2f}")
                self.entry_efectivo.config(state='readonly')
                self.entry_transf.config(state='readonly')
            else:
                # Si es Mixto, arranca con todo en Transferencia para que empieces a escribir en Efectivo (o viceversa)
                entry_efectivo.insert(0, "0.00")
                entry_transf.insert(0, f"{total_general:.2f}")
                entry_efectivo.config(state='normal')
                entry_transf.config(state='normal')
                self.entry_efectivo.insert(0, "0.00")
                self.entry_transf.insert(0, f"{0:.2f}")
                self.entry_efectivo.config(state='normal')
                self.entry_transf.config(state='normal')

        # Conecta la función al desplegable
        metodo_var.trace("w", actualizar_montos)
        actualizar_montos() # Arranca en Efectivo por defecto

        # Botón Confirmar
        btn_confirmar = tk.Button(ventana, text="Confirmar Pago", font=('Calibri', TAMAÑO_LETRA_CAJA, 'bold'), bg="#13eb33", fg="black", width=20,
                                  command=lambda: self.controlador.procesar_pago_final(
                                      metodo_var.get(), entry_efectivo.get(), entry_transf.get(), total_general, imprimir, ventana
                                      metodo_var.get(), self.entry_efectivo.get(), self.entry_transf.get(), total_general, imprimir, ventana
                                  ))
        btn_confirmar.pack(pady=10)
        btn_confirmar.pack(pady=10)
    
    def desabilita_atajos(self):
        self.root.unbind_all('<F12>')
        self.root.unbind_all('<F11>')
        
        
    def cerrar_y_reactivar(self, ventana):
            self.root.bind_all('<F12>', lambda e: self.controlador.finalizar_venta())
            self.root.bind_all('<F11>', lambda e: self.controlador.finalizar_venta(imprimir=True))
            ventana.destroy()