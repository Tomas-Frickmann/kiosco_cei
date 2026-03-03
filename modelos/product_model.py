
from Utilitys.util_config import DB_DIRECTORY, PRODUCTS_COLUMNS, CONTROL_STOCK_PRODUCTO, CODIGO_PRODUCTO, NOMBRE_PRODUCTO
from Datos import Connect as db

class ProductsModel():
    def __init__(self):
        self.ColumnasProductos = PRODUCTS_COLUMNS
        self.ControlStock = CONTROL_STOCK_PRODUCTO
        self.Codigo = CODIGO_PRODUCTO
        self.Nombre = NOMBRE_PRODUCTO



    def consultadb(self, query:str, param:tuple, fetch:bool):
        if param:
            return db.execute_query(db_path=DB_DIRECTORY, query=query, params=param, fetch=fetch)
        else:
            return db.execute_query(db_path=DB_DIRECTORY, query=query, fetch=fetch)
    