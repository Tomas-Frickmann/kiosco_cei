from Utilitys.util_config import *
from modelos.store_model import StoreModel
from vistas.store_view import StoreView

class StoreController:
    def __init__(self, root, main_body, main_modelo):
        self.root = root
        self.main_modelo = main_modelo
        self.store_model = StoreModel()
        
        self.nombre_maquina = self.main_modelo.cargar_configuracion().get("nombre_maquina", "SIN_NOMBRE")
        
        self.vista = StoreView(main_body, self)
        self.actualizar_carrito_vista()

    # ==========================================
    # MANEJO DEL CARRITO (BASE DE DATOS)
    # ==========================================
    def agregar_producto(self, producto_ingresado, cantidad_str):
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
        
        nombre = prod_db[COL_PROD_NOMBRE]
        precio = float(prod_db[COL_PROD_PRECIO]) # O prod_db[PRECIO_PRODUCTO] según tus constantes
        stock = prod_db[COL_PROD_STOCK]
        control_stock = prod_db[COL_PROD_CONTROL_STOCK]

        if control_stock:
            if stock is None:
                self.vista.mostrar_mensaje("error", "Error", f"El producto '{nombre}' no tiene stock definido.")
                return
            if cantidad > stock:
                self.vista.mostrar_mensaje("error", "Error", f"No hay suficiente stock. Stock disponible: {stock}")
                return

        total = precio * cantidad
        
        # Estructura EXACTA de 7 parámetros para el carrito_temporal
        params = (
            nombre, 
            precio, 
            cantidad, 
            total, 
            prod_db.get("categoria", ""), 
            prod_db.get("subcategoria", ""), 
            
        )
        self.store_model.agregar_producto_carrito(params)
        
        self.actualizar_carrito_vista()
        self.vista.limpiar_entradas()

    def modificar_cantidad(self, index, operacion):
        carrito_db = self.store_model.obtener_carrito()
        if not carrito_db or index < 0 or index >= len(carrito_db): 
            return
        
        item = carrito_db[index]
        id_item = item[COL_CARRITO_ID]
        precio = float(item[COL_CARRITO_PRECIO])
        cantidad_actual = int(item[COL_CARRITO_CANTIDAD])

        nueva_cantidad = cantidad_actual + 1 if operacion == "+" else cantidad_actual - 1
        
        if nueva_cantidad < 1: return # No permite 0

        nuevo_total = precio * nueva_cantidad
        
        self.store_model.actualizar_cantidad_carrito(id_item, nueva_cantidad, nuevo_total)
        self.actualizar_carrito_vista()

    def eliminar_producto(self, indices):
        carrito_db = self.store_model.obtener_carrito()
        if not carrito_db: return

        # Eliminamos de atrás para adelante por ID
        for index in sorted(indices, reverse=True):
            if 0 <= index < len(carrito_db):
                id_item = carrito_db[index]["id"]
                self.store_model.eliminar_del_carrito(id_item)
                
        self.actualizar_carrito_vista()

    def actualizar_carrito_vista(self):
        carrito_db = self.store_model.obtener_carrito()
        if carrito_db is None: carrito_db = []

        total_general = self.store_model.calcular_total_carrito()

        datos_tabla = []
        for item in carrito_db:
            
            datos_tabla.append((
                item[COL_CARRITO_PRODUCTO], 
                item[COL_CARRITO_PRECIO], 
                item[COL_CARRITO_CANTIDAD], 
                item[COL_CARRITO_TOTAL]
            ))

        self.vista.refrescar_tabla(datos_tabla)
        
        # Efectivo y Transferencia se muestran en 0 porque se definen al final. El Descuento también en 0.
        # SI tu funcion actualizar_totales_ui pide 4 parámetros, dejalos así:
        self.vista.actualizar_totales_ui(0.0, 0.0, 0.0, total_general)

    # ==========================================
    # FINALIZAR VENTA
    # ==========================================
    def finalizar_venta(self, imprimir=False):
        # CORREGIDO: "Si está vacío", no "Si NO está vacío"
        if self.store_model.carrito_vacio():
            self.vista.mostrar_mensaje("warning", "Caja vacía", "No hay productos para cobrar.")
            return

        respuesta = self.vista.mostrar_mensaje("question", "Confirmar", "¿Desea finalizar la venta?")
        if not respuesta: return

        total_general = self.store_model.calcular_total_carrito()
        self.vista.abrir_ventana_cobro(total_general, imprimir)
            
    def procesar_pago_final(self, metodo_pago, monto_efectivo, monto_transf, total_general, imprimir, ventana):
        try:
            efectivo = float(monto_efectivo) if monto_efectivo else 0.0
            transferencia = float(monto_transf) if monto_transf else 0.0
        except ValueError:
            self.vista.mostrar_mensaje("error", "Error", "Los montos ingresados deben ser numéricos.")
            return

        if round(efectivo + transferencia, 2) != round(total_general, 2):
            self.vista.mostrar_mensaje("error", "Error matemático", f"La suma de los pagos (${efectivo + transferencia:.2f}) no coincide con el total de la venta (${total_general:.2f}).")
            return

        # CORREGIDO: Le mandamos solo los 5 argumentos que pide el modelo (sin lista_ventas)
        self.store_model.guardar_venta_completa(self.nombre_maquina, efectivo, transferencia, total_general, metodo_pago)
        
        self.store_model.vaciar_carrito()
        self.actualizar_carrito_vista()

        ventana.destroy()

        if imprimir:
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