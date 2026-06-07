# archivo: VO/solicitud_material_vo.py

class SolicitudMaterialVO:
    def __init__(self, idSolicitud=None, concepto=None, cantidad=0, solicitante=None, estado="Pendiente"):
        self.idSolicitud = idSolicitud
        self.concepto = concepto
        self.cantidad = cantidad
        self.solicitante = solicitante
        self.estado = estado

    @property
    def concepto(self):
        return self._concepto

    @concepto.setter
    def concepto(self, value):
        if value and isinstance(value, str) and not value.strip():
            raise ValueError("El concepto de la solicitud no puede estar vacío.")
        self._concepto = value

    @property
    def cantidad(self):
        return self._cantidad

    @cantidad.setter
    def cantidad(self, value):
        try:
            val_int = int(value)
            if val_int < 0:
                raise ValueError()
            self._cantidad = val_int
        except (ValueError, TypeError):
            raise ValueError(f"La cantidad no puede ser negativa ni inválida: {value}")

    @property
    def solicitante(self):
        return self._solicitante

    @solicitante.setter
    def solicitante(self, value):
        if value and isinstance(value, str) and not value.strip():
            raise ValueError("El nombre del solicitante no puede estar vacío.")
        self._solicitante = value

    @property
    def estado(self):
        return self._estado

    @estado.setter
    def estado(self, value):
        if value and isinstance(value, str) and not value.strip():
            raise ValueError("El estado no puede estar vacío.")
        self._estado = value

    def __eq__(self, otro):
        if not isinstance(otro, SolicitudMaterialVO):
            return False
        return (self.idSolicitud == otro.idSolicitud and 
                self.concepto == otro.concepto and 
                self.cantidad == otro.cantidad and 
                self.solicitante == otro.solicitante and 
                self.estado == otro.estado)

    def __str__(self):
        return f"SolicitudMaterialVO[ID: {self.idSolicitud} | Concepto: {self.concepto} | Cantidad: {self.cantidad} | Solicitante: {self.solicitante} | Estado: {self.estado}]"

    def __repr__(self):
        return self.__str__()