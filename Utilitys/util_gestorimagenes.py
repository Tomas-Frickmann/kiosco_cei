import Utilitys.util_images as util_img

class GestorImagenes:
    # Este diccionario (caché) guardará las imágenes para que Tkinter no las borre
    _cache_imagenes = {}

    @classmethod
    def obtener_imagen(cls, nombre_clave, ruta, tamaño):
        """
        Busca la imagen en la caché. Si no existe, la carga, la guarda y la devuelve.
        """
        if nombre_clave not in cls._cache_imagenes:
            # Usamos tu función util_img que ya tienes creada
            imagen = util_img.leer_imagen(ruta, tamaño)
            cls._cache_imagenes[nombre_clave] = imagen
            
        return cls._cache_imagenes[nombre_clave]