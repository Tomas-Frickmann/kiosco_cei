import Datos.Connect as db
import datetime
from Utilitys.util_config import *

# (Si no tenés estas constantes en util_config, dejalas acá)


class StoreModel:
    def __init__(self):
        pass

    def buscar_sugerencias_producto(self, texto):
        query = "SELECT nombre FROM productos WHERE nombre LIKE ? LIMIT 5"
        return db.execute_query("Datos/datos.db", query, (texto + "%",), fetch=True)

    def obtener_producto_exacto(self, producto_ingresado):
        query = "SELECT nombre, precio, descripcion, categoria, subcategoria, ControlStock, stock FROM productos WHERE nombre = ? OR codigo = ?"
        resultado = db.execute_query("Datos/datos.db", query, (producto_ingresado, producto_ingresado), fetch=True)
        if resultado:
            return dict(resultado[0]) # Lo devolvemos como diccionario puro
        return None

    def validar_existencia_producto(self, producto_ingresado):
        query = "SELECT 1 FROM productos WHERE nombre = ? OR codigo = ? LIMIT 1"
        return db.execute_query("Datos/datos.db", query, (producto_ingresado, producto_ingresado), fetch=True)

    def guardar_venta_completa(self, nombre_maquina, efectivo, transferencia, total_general, metodo_pago):
        now = datetime.datetime.now()
        fecha = now.strftime("%Y-%m-%d")
        hora = now.strftime("%H:%M:%S")

        query_venta = """
            INSERT INTO ventas (fecha, hora, maquina, efectivo, transferencia, total, metodo_pago)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """
        # Se agregan los 7 parámetros correctos
        db.execute_query("Datos/datos.db", query_venta, (fecha, hora, nombre_maquina, efectivo, transferencia, total_general, metodo_pago))

        query_id = "SELECT id FROM ventas WHERE maquina = ? ORDER BY id DESC LIMIT 1"
        venta_id = db.execute_query("Datos/datos.db", query_id, (nombre_maquina,), fetch=True)[0]["id"]
        lista_ventas = self.obtener_carrito()

        for prod in lista_ventas:
            # Insertamos en detalle_ventas inyectando el metodo_pago de la venta general
            query_detalle = """
                INSERT INTO detalle_ventas (venta_id, producto, categoria, subcategoria, cantidad, precio_unitario, total, metodo_pago)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """
            db.execute_query(
                "Datos/datos.db", query_detalle,
                (venta_id, prod[COL_CARRITO_PRODUCTO], prod[COL_CARRITO_CATEGORIA], prod[COL_CARRITO_SUBCATEGORIA], prod[COL_CARRITO_CANTIDAD], prod[COL_CARRITO_PRECIO], prod[COL_CARRITO_TOTAL], metodo_pago)
            )

    def obtener_resumen_caja(self, fecha_inicio, fecha_fin):
        query = """
            SELECT d.producto, d.metodo_pago, SUM(d.cantidad) as cantidad_total, SUM(d.total) as total_ventas
            FROM detalle_ventas d
            JOIN ventas v ON d.venta_id = v.id
            WHERE v.fecha BETWEEN ? AND ?
            GROUP BY d.producto, d.metodo_pago
            ORDER BY d.producto, d.metodo_pago
        """
        return db.execute_query("Datos/datos.db", query, (fecha_inicio, fecha_fin), fetch=True)

    def obtener_todas_las_ventas(self):
        query = "SELECT id, fecha, hora, total, metodo_pago, maquina FROM ventas ORDER BY id DESC"
        return db.execute_query("Datos/datos.db", query, fetch=True)

    def obtener_detalle_de_venta(self, venta_id):
        query = "SELECT producto, cantidad, precio_unitario, total, metodo_pago FROM detalle_ventas WHERE venta_id = ?"
        return db.execute_query("Datos/datos.db", query, (venta_id,), fetch=True)
    
  
    # MANEJO DEL CARRITO TEMPORAL (BASE DE DATOS)
  

    def obtener_carrito(self):
        # Eliminamos método de pago del SELECT
        query = f"SELECT {COL_CARRITO_ID}, {COL_CARRITO_PRODUCTO}, {COL_CARRITO_PRECIO}, {COL_CARRITO_CANTIDAD}, {COL_CARRITO_TOTAL}, {COL_CARRITO_CATEGORIA}, {COL_CARRITO_SUBCATEGORIA} FROM {TABLA_CARRITO}"
        return db.execute_query("Datos/datos.db", query, fetch=True)

    def actualizar_cantidad_carrito(self, id_item, nueva_cantidad, nuevo_total):
        query = f"UPDATE {TABLA_CARRITO} SET {COL_CARRITO_CANTIDAD} = ?, {COL_CARRITO_TOTAL} = ? WHERE id = ?"
        db.execute_query("Datos/datos.db", query, (nueva_cantidad, nuevo_total, id_item))

    def calcular_total_carrito(self):
        # Consulta directa del total, evitando errores de llamadas
        query = f"SELECT SUM({COL_CARRITO_TOTAL}) FROM {TABLA_CARRITO}"
        resultado = db.execute_query("Datos/datos.db", query, fetch=True)
        
        if resultado and resultado[0][0] is not None:
            return float(resultado[0][0])
        return 0.0   

    def eliminar_del_carrito(self, id_item):
        query = f"DELETE FROM {TABLA_CARRITO} WHERE id = ?"
        db.execute_query("Datos/datos.db", query, (id_item,))

    def vaciar_carrito(self):
        query = f"DELETE FROM {TABLA_CARRITO}"
        db.execute_query("Datos/datos.db", query)
    
    def agregar_producto_carrito(self, params):
        # Insertamos solo 7 valores al carrito (sin el método de pago)
        query = f""" INSERT INTO {TABLA_CARRITO} ({COL_CARRITO_PRODUCTO}, {COL_CARRITO_PRECIO}, {COL_CARRITO_CANTIDAD}, {COL_CARRITO_TOTAL}, {COL_CARRITO_CATEGORIA}, {COL_CARRITO_SUBCATEGORIA}) VALUES (?,?,?,?,?,?)"""
        db.execute_query("Datos/datos.db", query, params)

    def carrito_vacio(self):
        query = f"SELECT COUNT(*) FROM {TABLA_CARRITO}"
        resultado = db.execute_query("Datos/datos.db", query, fetch=True)
        return resultado[0][0] == 0 # Devuelve True si es 0, False si hay algo