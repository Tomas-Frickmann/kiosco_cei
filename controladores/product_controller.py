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
        try:
            if query == "Busqueda":
                print("Param: ", param)
                query = f"SELECT {self.lista_to_string(self.productModel.ColumnasProductos)}FROM productos WHERE LOWER({self.productModel.Nombre}) LIKE LOWER(?) OR LOWER({self.productModel.Codigo}) LIKE LOWER(?)"
            elif query == "BuscaID":
                query = f"SELECT * FROM Productos WHERE {self.productModel.ColumnasProductos[0]} = ?"
            elif query == "Columnas":
                #Columnas no es un buen nombre pero no voy a cambiarlo ahora
                query = f"SELECT {self.lista_to_string(self.productModel.ColumnasProductos)} FROM productos"
            elif query == "Agregar":
                pass
            elif query == "Editar":
                cabeceras = self.cabeceras_db()
                query = f"UPDATE productos SET {self.lista_to_string_param(cabeceras[1:])} WHERE {cabeceras[0]}=?"
                print("Controlador linea 35: \n", query)
            else:
                raise Exception("Consulta erronea")
        except Exception as e:
            print(e.args[0])
        
        return self.productModel.consultadb(query, param, fetch)
    
    def lista_to_string(self, lista:list):
        string = lista[0]
        for x in lista[1:]:
            string += ", " + x
        return string + " "
    
    def lista_to_string_param(self, lista:list):
        string = lista[0] + "=?"
        for x in lista[1:]:
            string += ", " + x + "=?"
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

    def actualizar_producto(self, id: str, resultados:list = []):
        """O llega con id o llega " " """
        print("Controlador linea 56: ", resultados)


        pass

    def cabeceras_db(self):
        return self.productModel.consultadb("SELECT * FROM productos", None)[0].keys()
    




