class SolicitudCompraVO:
    def __init__(self, idSolicitud=None, descripcion=None, monto=0.0, estado=None):
        self.idSolicitud = idSolicitud
        self.descripcion = descripcion
        self.monto = monto
        self.estado = estado

    @property
    def descripcion(self):
        return self._descripcion

    @descripcion.setter
    def descripcion(self, value):
        if value and isinstance(value, str) and not value.strip():
            raise ValueError("La descripción de la solicitud no puede estar vacía.")
        self._descripcion = value

    @property
    def monto(self):
        return self._monto

    @monto.setter
    def monto(self, value):
        try:
            val_float = float(value)
            if val_float < 0.0:
                raise ValueError()
            self._monto = val_float
        except (ValueError, TypeError):
            raise ValueError(f"El monto de la solicitud no puede ser negativo ni inválido: {value}")

    def __eq__(self, otro):
        if not isinstance(otro, SolicitudCompraVO):
            return False
        return (self.idSolicitud == otro.idSolicitud and 
                self.descripcion == otro.descripcion and 
                self.monto == otro.monto and 
                self.estado == otro.estado)

    def __str__(self):
        return f"SolicitudCompraVO[ID: {self.idSolicitud} | Monto: {self.monto} | Estado: {self.estado}]"

    def __repr__(self):
        return self.__str__()