from tkinter.tix import IMAGE


color_barra_superior = "#1f2329"
color_fondo_gris = "#2a3130"
color_menu_lateral = "#2a3138"
color_cuerpo_principal = "#f1faff"
color_menu_cursor_encima = "#2f88c5"
color_iconos="#77E0C4"
color_iconos_turquesa_oscuro="#00D6C1"
color_iconos_oscuro='#0A3631'
color_iconos2="#2a3138"
color_fondo_precio = "#041228"
TAMAÑO_LETRA_CAJA=18

NOMBRE="nombre"
DNI="dni"
DELETE="delete"
EDIT="edit"
ADD="add"

CONSULTAR="consulta"

EFECTIVO="efectivo"
TRANSFERENCIA="transferencia"
MIXTO="mixto"
CAJA="caja"
COBRO="cobro"
CONSULTAR="consulta"

# CONSTANTES DE LA BASE DE DATOS

# TABLA: CARRITO TEMPORAL  ---
TABLA_CARRITO = "carrito_temporal"
COL_CARRITO_ID = "id"
COL_CARRITO_PRODUCTO = "Producto"
COL_CARRITO_CATEGORIA = "Categoria"
COL_CARRITO_SUBCATEGORIA = "SubCategoria"
COL_CARRITO_CANTIDAD = "Cantidad"
COL_CARRITO_PRECIO = "Precio"
COL_CARRITO_TOTAL = "Total"
COL_CARRITO_CONTROL_STOCK = "ControlStock"
COL_CARRITO_LUGAR = "Lugar"

# TABLA: DETALLE DE VENTAS
TABLA_DETALLE_VENTAS = "detalle_ventas"
COL_DETALLE_ID = "Id"
COL_DETALLE_VENTA_ID = "venta_id"
COL_DETALLE_PRODUCTO = "producto"
COL_DETALLE_CATEGORIA = "categoria"
COL_DETALLE_SUBCATEGORIA = "subcategoria"
COL_DETALLE_CANTIDAD = "cantidad"
COL_DETALLE_PRECIO_UNIT = "precio_unitario"
COL_DETALLE_TOTAL = "total"
COL_DETALLE_METODO_PAGO = "metodo_pago"

# TABLA: PRODUCTOS
TABLA_PRODUCTOS = "Productos"
COL_PROD_ID = "Id"
COL_PROD_CODIGO = "Codigo"
COL_PROD_BARRAS = "Barras"
COL_PROD_NOMBRE = "Nombre"
COL_PROD_PRECIO = "Precio"
COL_PROD_DESCRIPCION = "Descripcion"
COL_PROD_STOCK = "Stock"
COL_PROD_CATEGORIA = "Categoria"
COL_PROD_SUBCATEGORIA = "SubCategoria"
COL_PROD_PROVEEDOR = "Proveedor"
COL_PROD_IMAGEN = "Imagen"
COL_PROD_CONTROL_STOCK = "ControlStock"

# TABLA: VENTAS 
TABLA_VENTAS = "ventas"
COL_VENTAS_ID = "Id"
COL_VENTAS_FECHA = "fecha"
COL_VENTAS_HORA = "hora"
COL_VENTAS_MAQUINA = "maquina"
COL_VENTAS_EFECTIVO = "efectivo"
COL_VENTAS_TRANSFERENCIA = "transferencia"
COL_VENTAS_TOTAL = "total"
COL_VENTAS_METODO_PAGO = "metodo_pago"

# TABLA: REGISTROS
TABLA_REGISTROS = "registros"
COL_REG_ID = "id"
COL_REG_DNI = "dni"
COL_REG_NOMBRE = "nombre"
COL_REG_FECHA = "fecha"
COL_REG_HORA_ENTRADA = "hora_entrada"
COL_REG_HORA_SALIDA = "hora_salida"
COL_REG_TIEMPO_TOTAL = "tiempo_total"
COL_REG_EXPULSION = "expulsion"
COL_REG_LUGAR = "lugar"
COL_REG_EXTRA = "extra"
COL_REG_MOTIVO = "motivo"

# TABLA: EMPLEADOS 
TABLA_EMPLEADOS = "empleados"
COL_EMP_DNI = "dni"
COL_EMP_NOMBRE = "nombre"


#TABLA: PRODUCTOS 
ID = "Id"
CODIGO_PRODUCTO="Codigo"
BARRAS_PRODUCTO="Barras"
NOMBRE_PRODUCTO="Nombre"
PRECIO_PRODUCTO="Precio"
DESCRIPCION_PRODUCTO="Descripcion"
STOCK_PRODUCTO="Stock"
CATEGORIA_PRODUCTO="Categoria"
SUBCATEGORIA_PRODUCTO="SubCategoria"
PROVEDOOR_PRODUCTO="Proveedor"
IMAGEN_PRODUCTO="Imagen"
CONTROL_STOCK_PRODUCTO="ControlStock"
PRODUCTS_COLUMNS = [ID,CODIGO_PRODUCTO,NOMBRE_PRODUCTO,DESCRIPCION_PRODUCTO,PRECIO_PRODUCTO,STOCK_PRODUCTO, CONTROL_STOCK_PRODUCTO]
PRODUCTS_TABLE = "Productos"

#Direcciones
DB_DIRECTORY = "Datos/datos.db"

#VALIDACIONES FORMATO
LONG_CODIGO = 6