from vistas.product_view import ProductsPanel
from modelos.product_model import ProductsModel


class ProductsController():
    def __init__(self, main_body, main_model):
        self.mainBody = main_body
        self.mainModel = main_model

        self.controllerBody = ProductsPanel(self.mainBody, self) #(vista ppal; controlador)
        self.controllerModel = ProductsModel()

