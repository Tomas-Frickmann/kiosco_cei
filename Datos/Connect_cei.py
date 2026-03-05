import sqlite3 as sql
from datetime import datetime
import hashlib
import os

# Definimos la ruta de la base de datos como una constante global
DB_PATH = "Datos/datos_cei.db"

def execute_query(query, params=(), fetch=False):
    """Ejecuta cualquier consulta SQL de forma segura.
    
    :param query: Consulta SQL a ejecutar.SS
    :param params: Parámetros opcionales para la consulta (tupla).
    :param fetch: Si es True, retorna los resultados de la consulta.
    :return: Resultado de la consulta si fetch es True, de lo contrario None.
    """
    try:
        if not os.path.exists("Datos"):
            os.makedirs("Datos")
            
        conn = sql.connect(DB_PATH, check_same_thread=False)
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
        print(f"❌ Error en la base de datos: {e}")
        conn.commit()
        cursor.close()
        conn.close()
        return None

def inicializar_base_de_datos():
    """Crea la estructura de tablas desde cero si el archivo no existe."""
    
    #  1. Tabla de Empleados (Para Login Multi-usuario)
    execute_query("""
        CREATE TABLE IF NOT EXISTS Empleados (
            dni INTEGER PRIMARY KEY ,
            nombre TEXT NOT NULL UNIQUE,
            contrasena_hash TEXT NOT NULL,
            nombre_completo TEXT,
            rol TEXT NOT NULL DEFAULT 'empleado'
        )
    """)

    # 2. Tabla de Productos (Tu Inventario)
    # execute_query("""
    #     CREATE TABLE IF NOT EXISTS productos (
    #         id INTEGER PRIMARY KEY AUTOINCREMENT,
    #         nombre TEXT NOT NULL UNIQUE,
    #         precio_compra REAL NOT NULL,
    #         precio_venta REAL NOT NULL,
    #         stock_actual INTEGER NOT NULL DEFAULT 0
    #     )
    # """)

    # # 3. Tabla de Ventas (El Ticket)
    # execute_query("""
    #     CREATE TABLE IF NOT EXISTS ventas (
    #         id INTEGER PRIMARY KEY AUTOINCREMENT,
    #         fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    #         total REAL NOT NULL,
    #         usuario_id INTEGER,
    #         FOREIGN KEY (usuario_id) REFERENCES usuarios(id)
    #     )
    # """)

    # # 4. Tabla de Detalles de Venta (Los productos dentro de cada ticket)
    # execute_query("""
    #     CREATE TABLE IF NOT EXISTS detalles_venta (
    #         id INTEGER PRIMARY KEY AUTOINCREMENT,
    #         venta_id INTEGER NOT NULL,
    #         producto_id INTEGER NOT NULL,
    #         cantidad INTEGER NOT NULL,
    #         precio_unitario REAL NOT NULL,
    #         FOREIGN KEY (venta_id) REFERENCES ventas(id),
    #         FOREIGN KEY (producto_id) REFERENCES productos(id)
    #     )
    # """)
    print("✅ Base de datos verificada/inicializada.")

def crear_usuario(usuario, password, rol="empleado"):
    """Registra un nuevo usuario con contraseña hasheada."""
    hash_password = hashlib.sha256(password.encode()).hexdigest()
    query = "INSERT OR IGNORE INTO usuarios (usuario, contrasena_hash, rol) VALUES (?, ?, ?)"
    execute_query(query, (usuario, hash_password, rol))

def GetEmpleados():
    """Obtiene la lista de empleados usando la función genérica."""
    query = "SELECT * FROM usuarios ORDER BY usuario"
    return execute_query(query, fetch=True)