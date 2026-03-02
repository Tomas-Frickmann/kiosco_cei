
from Utilitys.util_config import DB_DIRECTORY
from Datos import Connect as db

class ProductsModel():
    def __init__(self):
        pass



    def consultadb(self, query:str, param:tuple, fetch:bool):
        if param:
            return db.execute_query(db_path=DB_DIRECTORY, query=query, params=param, fetch=fetch)
        else:
            return db.execute_query(db_path=DB_DIRECTORY, query=query, fetch=fetch)
    