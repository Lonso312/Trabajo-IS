# archivo: VO/BienVO.py

class BienVO:
    def __init__(self, BienID=None, tipo=None, precio=None, cantidad=None):
        self.BienID = BienID
        self.tipo = tipo
        self.precio = precio
        self.cantidad = cantidad
        
        # Atributo extendido para almacenar la información agregada de tesoreros vinculados
        self.tesoreros_asignados = "Ninguno"