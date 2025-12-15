import sqlite3 as sql
from datetime import datetime

# Definimos la ruta en una variable constante. 
# Si el día de mañana cambia la ruta, solo la cambias aquí.
DB_PATH = "Datos/datos.db"

def execute_query(query, params=(), fetch=False):
    """
    Función CENTRAL. En el futuro, aquí cambiaremos 'sqlite3' por 
    'mysql.connector' o 'psycopg2' para conectarnos a la nube.
    """
    try:
        # check_same_thread=False es necesario para Tkinter a veces, 
        # pero cuidado con escribir desde dos lugares al mismo tiempo.
        conn = sql.connect(DB_PATH, check_same_thread=False)
        cursor = conn.cursor()
        
        cursor.execute(query, params)
        
        if fetch:
            result = cursor.fetchall()
        else:
            conn.commit() # Solo hacemos commit si no es lectura
            result = None

        cursor.close()
        conn.close()
        return result
        
    except sql.Error as e:
        print(f"Error en la base de datos: {e}")
        return None

# --- Funciones de Negocio (Ahora mucho más limpias) ---

def GetEmpleados():
    query = "SELECT * FROM empleados ORDER BY nombre"
    # Reutilizamos la función central. ¡Mucho más limpio!
    datos = execute_query(query, fetch=True) 
    return datos

# Ejemplo de cómo sería agregar un producto (para tu kiosco)
def AgregarProducto(nombre, precio, stock):
    query = "INSERT INTO productos (nombre, precio, stock) VALUES (?, ?, ?)"
    execute_query(query, (nombre, precio, stock))