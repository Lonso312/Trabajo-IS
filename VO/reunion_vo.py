class ReunionVO:
    def __init__(self, idReunion=None, fecha=None, tipo=None, estado=None):
        self.idReunion = idReunion
        self.fecha = fecha
        self.tipo = tipo
        self.estado = estado

    @property
    def tipo(self):
        return self._tipo

    @tipo.setter
    def tipo(self, value):
        if value and isinstance(value, str) and not value.strip():
            raise ValueError("El tipo de reunión no puede estar vacío o en blanco.")
        self._tipo = value

    @property
    def estado(self):
        return self._estado

    @estado.setter
    def estado(self, value):
        if value and isinstance(value, str) and not value.strip():
            raise ValueError("El estado de la reunión no puede estar vacío o en blanco.")
        self._estado = value

    def __eq__(self, otro):
        if not isinstance(otro, ReunionVO):
            return False
        return (self.idReunion == otro.idReunion and 
                self.fecha == otro.fecha and 
                self.tipo == otro.tipo and 
                self.estado == otro.estado)

    def __str__(self):
        return f"ReunionVO[ID: {self.idReunion} | Tipo: {self.tipo} | Estado: {self.estado} | Fecha: {self.fecha}]"

    def __repr__(self):
        return self.__str__()