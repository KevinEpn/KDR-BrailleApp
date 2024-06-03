def centrar_ventana(ventana, ancho, alto):
    ventana_ancho = ventana.winfo_screenwidth()
    ventana_alto = ventana.winfo_screenheight()

    x = int((ventana_ancho/2) - (ancho/2))
    y = int((ventana_alto/2) - (alto/2))

    return ventana.geometry(f"{ancho}x{alto}+{x}+{y}")