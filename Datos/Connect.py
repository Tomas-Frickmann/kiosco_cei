import sqlite3 as sql
from datetime import datetime

ruta_base="Datos/datos.db"

def execute_query(db_path,query, params=(), fetch=False):
    """
    Ejecuta una consulta en la base de datos SQLite.
    
    :param db_path: Ruta del archivo de la base de datos.
        Por defecto seria "Datos/datos.db"
    :param query: Consulta SQL a ejecutar.
    :param params: Parámetros opcionales para la consulta (tupla).
    :param fetch: Si es True, retorna los resultados de la consulta.
    :return: Resultado de la consulta si fetch es True, de lo contrario None.
    """
    try:
        conn = sql.connect(db_path,check_same_thread=False) 
        conn.row_factory = sql.Row 
        cursor = conn.cursor()
       
        cursor.execute(query, params)
        
        if fetch:
            result = cursor.fetchall()
        else: 
            result = None

        conn.commit()
        cursor.close()
        conn.close()
        return result
    except sql.Error as e:
        conn.commit()
        cursor.close()
        conn.close()
        print(f"Error en la base de datos: {e}")
        return None
    
def GetEmpleados():
    #Para leer filas
    conexion=sql.connect(ruta_base,check_same_thread=False)
    conexion.row_factory = sql.Row 
    cursor=conexion.cursor()
    
    instruccion =f"SELECT dni,nombre FROM empleados ORDER BY nombre" 
    cursor.execute(instruccion)
    datos = cursor.fetchall() #Devuelve Tuplas de (Dni,Nombre,fichado)
    conexion.commit()
    return datos

def crear_tabla():
    conexion=sql.connect(ruta_base,check_same_thread=False)
    cursor = conexion.cursor()
    conexion.row_factory = sql.Row 
    # Creamos la tabla temporal del carrito
    query = """CREATE TABLE IF NOT EXISTS carrito_temporal (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        Producto TEXT NOT NULL,
        Categoria TEXT NOT NULL,
        SubCategoria TEXT NOT NULL,
        Cantidad REAL NOT NULL,
        Precio REAL NOT NULL,
        Total REAL NOT NULL
        
    )"""
    cursor.execute(query)
    conexion.commit()
    cursor.close()
    conexion.close()
    print("✅ Tabla 'carrito_temporal' verificada/creada con éxito.")

