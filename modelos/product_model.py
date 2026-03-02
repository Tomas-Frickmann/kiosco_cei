
from Utilitys.util_config import DB_DIRECTORY
from Datos import Connect as db

class ProductsModel():
    def __init__(self):
        pass



    def consultadb(self, query:str, param:tuple, fetch:bool):
        return db.execute_query(DB_DIRECTORY, query, param, fetch)