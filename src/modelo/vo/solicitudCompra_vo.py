class SolicitudMaterialVO:
    def __init__(self, idSolicitud=None, concepto=None, cantidad=0,
                 solicitante=None, estado="Pendiente"):

        if concepto is not None and isinstance(concepto, str) and not concepto.strip():
            raise ValueError("El concepto de la solicitud no puede estar vacío.")
        self._concepto = concepto

        try:
            val_int = int(cantidad)
            if val_int < 0:
                raise ValueError()
            self._cantidad = val_int
        except (ValueError, TypeError):
            raise ValueError(f"La cantidad no puede ser negativa ni inválida: {cantidad}")

        if solicitante is not None and isinstance(solicitante, str) and not solicitante.strip():
            raise ValueError("El nombre del solicitante no puede estar vacío.")
        self._solicitante = solicitante

        if estado is not None and isinstance(estado, str) and not estado.strip():
            raise ValueError("El estado no puede estar vacío.")
        self._estado = estado

        self._idSolicitud = idSolicitud


    @property
    def idSolicitud(self):
        return self._idSolicitud

    @property
    def concepto(self):
        return self._concepto

    @property
    def cantidad(self):
        return self._cantidad

    @property
    def solicitante(self):
        return self._solicitante

    @property
    def estado(self):
        return self._estado


    def __eq__(self, otro):
        if not isinstance(otro, SolicitudMaterialVO):
            return False
        return (self._idSolicitud == otro._idSolicitud and
                self._concepto == otro._concepto and
                self._cantidad == otro._cantidad and
                self._solicitante == otro._solicitante and
                self._estado == otro._estado)

    def __str__(self):
        return (f"SolicitudMaterialVO[ID: {self._idSolicitud} | Concepto: {self._concepto} "
                f"| Cantidad: {self._cantidad} | Solicitante: {self._solicitante} "
                f"| Estado: {self._estado}]")

    def __repr__(self):
        return self.__str__()