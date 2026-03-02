import Datos.Connect as db
import datetime

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

    def guardar_venta_completa(self, maquina, total_efectivo, total_transferencia, total_general, metodo_pago, lista_ventas):
        now = datetime.datetime.now()
        fecha = now.strftime("%Y-%m-%d")
        hora = now.strftime("%H:%M:%S")

        query_venta = """
            INSERT INTO ventas (fecha, hora, maquina, efectivo, transferencia, total, metodo_pago)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """
        db.execute_query("Datos/datos.db", query_venta, (fecha, hora, maquina, total_efectivo, total_transferencia, total_general, metodo_pago))

        query_id = "SELECT id FROM ventas WHERE maquina = ? ORDER BY id DESC LIMIT 1"
        venta_id = db.execute_query("Datos/datos.db", query_id, (maquina,), fetch=True)[0]["id"]

        for prod in lista_ventas:
            # prod: (nombre, precio, cantidad, metodo, total, categoria, subcategoria, descripcion)
            query_detalle = """
                INSERT INTO detalle_ventas (venta_id, producto, categoria, subcategoria, cantidad, precio_unitario, total, metodo_pago)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """
            db.execute_query(
                "Datos/datos.db", query_detalle,
                (venta_id, prod[0], prod[5], prod[6], prod[2], prod[1], prod[4], prod[3])
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