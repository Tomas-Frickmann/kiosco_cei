from vistas.product_view import ProductsPanel
from modelos.product_model import ProductsModel


class ProductsController():
    def __init__(self, main_body, main_model):
        self.mainBody = main_body
        self.mainModel = main_model

        self.productBody = ProductsPanel(self.mainBody, self) #(vista ppal; controlador)
        self.productModel = ProductsModel()

    def consulta_mid(self, query:str, param:tuple, fetch:bool):
        """Query es reutilizado, primero indica la accion y luego la consulta"""
        if query == "Busqueda":
            query = "SELECT id, codigo, nombre, descripcion, precio, stock FROM productos WHERE LOWER(nombre) LIKE LOWER(?) OR LOWER(codigo) LIKE LOWER(?)"
        elif query == "BuscaID":
            query = "SELECT * FROM productos WHERE id = ?"
        
        self.productModel.consultadb(query, param, fetch)



