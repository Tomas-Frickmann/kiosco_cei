import sqlite3 as sql
from datetime import datetime


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
        print(f"Error en la base de datos: {e}")
        return None
    
def GetEmpleados(self):
    #Para leer filas
    self.conexion=sql.connect("Datos/datos.db",check_same_thread=False)
    self.cursor=self.conexion.cursor()
    instruccion =f"SELECT * FROM empleados ORDER BY nombre" 
    self.cursor.execute(instruccion)
    datos = self.cursor.fetchall() #Devuelve Tuplas de (Dni,Nombre,fichado)
    self.conexion.commit()
    return datos
