from Utilitys.util_config import *
from modelos.store_model import StoreModel
from vistas.store_view import StoreView

class StoreController:
    def __init__(self, root, main_body, main_modelo):
        self.root = root
        self.main_modelo = main_modelo
        self.store_model = StoreModel()
        
        # El carrito de compras global
        self.lista_ventas = self.main_modelo.ventas_global 
        self.nombre_maquina = self.main_modelo.cargar_configuracion().get("nombre_maquina", "SIN_NOMBRE")
        
        self.vista = StoreView(main_body, self)
        self.actualizar_carrito_vista()

    # ==========================================
    # MANEJO DEL CARRITO
    # ==========================================
    def agregar_producto(self, producto_ingresado, cantidad_str, metodo_pago):
        producto_ingresado = producto_ingresado.strip()
        cantidad_str = cantidad_str.strip()

        if not producto_ingresado or not cantidad_str.isdigit():
            self.vista.mostrar_mensaje("warning", "Error", "Debe ingresar un nombre válido y una cantidad numérica.")
            return

        cantidad = int(cantidad_str)
        if cantidad <= 0: return

        prod_db = self.store_model.obtener_producto_exacto(producto_ingresado)
        if not prod_db:
            self.vista.mostrar_mensaje("error", "Error", "El producto no existe en la base de datos.")
            return

        nombre = prod_db[NOMBRE_PRODUCTO]
        precio = float(prod_db[PRECIO_PRODUCTO])
        stock = prod_db[STOCK_PRODUCTO]
        control_stock = prod_db[CONTROL_STOCK_PRODUCTO]

        if control_stock:
            if stock is None:
                self.vista.mostrar_mensaje("error", "Error", f"El producto '{nombre}' no tiene stock definido.")
                return
            if cantidad > stock:
                self.vista.mostrar_mensaje("error", "Error", f"No hay suficiente stock. Stock disponible: {stock}")
                return

        total = precio * cantidad
        # Estructura: (nombre, precio, cantidad, metodo, total, categoria, subcategoria, descripcion)
        self.lista_ventas.append((nombre, precio, cantidad, metodo_pago, total, prod_db[CATEGORIA_PRODUCTO], prod_db[SUBCATEGORIA_PRODUCTO], prod_db[DESCRIPCION_PRODUCTO]))
        
        self.actualizar_carrito_vista()
        self.vista.limpiar_entradas()

    def modificar_cantidad(self, index, operacion):
        if index < 0 or index >= len(self.lista_ventas): return
        prod = self.lista_ventas[index]
        nueva_cantidad = prod[2] + 1 if operacion == "+" else prod[2] - 1
        
        if nueva_cantidad < 1: return # No permite 0

        nuevo_total = float(prod[1]) * nueva_cantidad
        self.lista_ventas[index] = (prod[0], prod[1], nueva_cantidad, prod[3], nuevo_total, prod[5], prod[6], prod[7])
        self.actualizar_carrito_vista()

    def cambiar_metodo_pago(self, index):
        if index < 0 or index >= len(self.lista_ventas): return
        prod = self.lista_ventas[index]
        nuevo_metodo = "Transferencia" if prod[3] == "Efectivo" else "Efectivo"
        self.lista_ventas[index] = (prod[0], prod[1], prod[2], nuevo_metodo, prod[4], prod[5], prod[6], prod[7])
        self.actualizar_carrito_vista()

    def eliminar_producto(self, indices):
        # Eliminamos de atrás para adelante para no desfasar los índices
        for index in sorted(indices, reverse=True):
            if 0 <= index < len(self.lista_ventas):
                self.lista_ventas.pop(index)
        self.actualizar_carrito_vista()

    def actualizar_carrito_vista(self):
        efectivo = sum(item[4] for item in self.lista_ventas if item[3] == "Efectivo")
        transferencia = sum(item[4] for item in self.lista_ventas if item[3] == "Transferencia")
        descuento = 0 
        total = efectivo + transferencia - descuento

        self.vista.refrescar_tabla(self.lista_ventas)
        self.vista.actualizar_totales_ui( transferencia, descuento, total)

    # ==========================================
    # FINALIZAR VENTA
    # ==========================================
    def finalizar_venta(self, imprimir=False):
        if not self.lista_ventas:
            self.vista.mostrar_mensaje("warning", "Caja vacía", "No hay productos para cobrar.")
            return

        respuesta = self.vista.mostrar_mensaje("question", "Confirmar", "¿Desea finalizar la venta?")
        if not respuesta: return

        total_efectivo = sum(item[4] for item in self.lista_ventas if item[3] == "Efectivo")
        total_transferencia = sum(item[4] for item in self.lista_ventas if item[3] == "Transferencia")
        total_general = total_efectivo + total_transferencia
        
        metodo_pago = "Mixto" if total_efectivo > 0 and total_transferencia > 0 else ("Efectivo" if total_efectivo > 0 else "Transferencia")

        self.store_model.guardar_venta_completa(self.nombre_maquina, total_efectivo, total_transferencia, total_general, metodo_pago, self.lista_ventas)
        self.lista_ventas.clear()
        self.actualizar_carrito_vista()

        if imprimir:
            # Lógica futura para ticket
            self.vista.mostrar_mensaje("info", "Éxito", "Venta finalizada e impresa.")
        else:
            self.vista.mostrar_mensaje("info", "Éxito", "Venta finalizada correctamente.")

    # ==========================================
    # UTILIDADES Y REPORTES
    # ==========================================
    def obtener_sugerencias(self, texto):
        if not texto: return []
        resultados = self.store_model.buscar_sugerencias_producto(texto)
        return [row["nombre"] for row in resultados] if resultados else []

    def validar_producto_rapido(self, texto):
        return self.store_model.validar_existencia_producto(texto)

    def generar_informe_caja(self, fecha_inicio, fecha_fin, hora, ventana):
        resumen = self.store_model.obtener_resumen_caja(fecha_inicio, fecha_fin)
        if not resumen:
            self.vista.mostrar_mensaje("info", "Sin resultados", "No se encontraron ventas en el rango.")
            return

        productos_agrupados = {}
        for row in resumen:
            prod = row["producto"]
            metodo = row["metodo_pago"]
            cant = row["cantidad_total"]
            tot = row["total_ventas"]

            if prod not in productos_agrupados:
                productos_agrupados[prod] = {"Efectivo": [0, 0], "Transferencia": [0, 0]}
            productos_agrupados[prod][metodo][0] += cant
            productos_agrupados[prod][metodo][1] += tot

        self.vista.mostrar_resumen_caja(productos_agrupados, fecha_inicio, fecha_fin, hora)
        ventana.destroy()

    def obtener_historial_ventas(self):
        ventas = self.store_model.obtener_todas_las_ventas()
        return [tuple(row) for row in ventas] if ventas else []

    def obtener_detalle_venta(self, venta_id):
        detalles = self.store_model.obtener_detalle_de_venta(venta_id)
        return [tuple(row) for row in detalles] if detalles else []