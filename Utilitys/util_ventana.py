def centrar_ventana(ventana, aplicacion_ancho, aplicacion_largo):
    pantalla_ancho = ventana.winfo_screenwidth()
    panlalla_largo = ventana.winfo_screenheight()
    x = int((pantalla_ancho/2)-(aplicacion_ancho/2))
    y = int((panlalla_largo/2)-(aplicacion_largo/2))
    return ventana.geometry(f"{aplicacion_ancho}x{aplicacion_largo}+{x}+{y}")
