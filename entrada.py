class Entrada:
    def __init__(self, pedido, fecha, descripcion, cantidad, importe, planta, nota):
        self.pedido = pedido
        self.fecha = fecha
        self.descripcion = descripcion
        self.planta = planta
        self.nota = nota       
        
        if "Servicio" in descripcion:
            self.importe = importe * 1.16
            self.precio = get_precio_servicio(planta)
            self.cantidad = importe / self.precio
        else:
            self.cantidad = cantidad
            self.importe = importe
            self.precio = self.importe / self.cantidad
    
    # Imprimimos la entrada    
    def __str__(self) -> str:
        return f"""{self.pedido}  {self.fecha} {self.descripcion}   {self.cantidad}      {self.precio}      {self.importe}   {self.planta}    {self.nota}
        --------------------------------------------------------------------------------------------------------"""


    # Devolvemos el precio del servicio de carga y descarga dependiente de la planta       
    def get_precio_servicio(planta):
        if 'Esc' in planta:
            return 0.7308
        elif 'Cande' in planta:
            return 1.2296
        elif 'Chetu' in planta:
            return 2.0532
        else:
            return 0.0