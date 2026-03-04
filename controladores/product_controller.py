from vistas.product_view import ProductsPanel
from modelos.product_model import ProductsModel


class ProductsController():
    def __init__(self, main_body, main_model):
        self.mainBody = main_body
        self.mainModel = main_model

        self.productModel = ProductsModel()
        self.productBody = ProductsPanel(self.mainBody, self) #(vista ppal; controlador)
        

    def consulta_mid(self, query:str, param:tuple = None, fetch:bool=True):
        """Columnas: Devuelve todos los valores de las columnas especificadas por la constante de columnas de productos
            Busqueda: Lo mismo que columnas pero bajo ciertas condiciones
            BuscaID: Devuelve toda la tabla para un id especifico


            consultadb devuelve una lista de row, el elemento 0 son las cabeceras
        """
        if query == "Busqueda":
            print("Param: ", param)
            query = f"SELECT {self.lista_to_string(self.productModel.ColumnasProductos)}FROM productos WHERE LOWER({self.productModel.Nombre}) LIKE LOWER(?) OR LOWER({self.productModel.Codigo}) LIKE LOWER(?)"
        elif query == "BuscaID":
            query = "SELECT * FROM productos WHERE Id = ?"
        elif query == "Columnas":
            #Columnas no es un buen nombre pero no voy a cambiarlo ahora
            query = f"SELECT {self.lista_to_string(self.productModel.ColumnasProductos)} FROM productos"
        else:
            pass
        
        return self.productModel.consultadb(query, param, fetch)
    
    def lista_to_string(self, lista:list):
        string = lista[0]
        for x in lista[1:]:
            string += ", " + x
        return string + " "
    
    def columnas(self, row):
        """Devuelve una fila en base a las cabeceras enviadas"""
        controla = "Sí" if row[self.productModel.ControlStock] else "No"
        categorias = (i for i in self.productModel.ColumnasProductos) #De está manera el controlador no conoce las constantes, las conoce el modelo
        values = []
        for x in categorias:
            values.append(row[x])
        values.append(controla)
        return tuple(values)
    
    def validar_len_codigo(self, text:str):
        return len(text) <= self.productModel.LongCodigo

    def actualizar_producto(id: str):
        """O llega con id o llega " " """


        pass

    def cabeceras_db(self):
        return self.productModel.consultadb("SELECT * FROM productos", None)[0].keys()
    




