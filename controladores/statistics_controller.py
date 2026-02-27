from modelos.main_model import MainModel
from vistas.statistics_view import StatisticsView

class StatisticsController:
    def __init__(self, parent, main_modelo):
        self.main_modelo = main_modelo
        
       
        # Instanciamos la vista pasándole el contenedor, a sí mismo, y el dato inicial
        self.vista = StatisticsView(parent, self)

   