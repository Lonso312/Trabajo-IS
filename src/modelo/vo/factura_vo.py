class FacturaVO:
    def __init__(self, idFactura=None, concepto=None, monto=0.0, fecha=None, estado=None):
        if concepto is not None and isinstance(concepto, str) and not concepto.strip():
            raise ValueError("El concepto de la factura no puede estar en blanco.")
        self._concepto = concepto

        try:
            val_float = float(monto)
            if val_float < 0.0:
                raise ValueError()
            self._monto = val_float
        except (ValueError, TypeError):
            raise ValueError(f"El monto de la factura no puede ser negativo ni inválido: {monto}")

        if estado is not None and isinstance(estado, str) and not estado.strip():
            raise ValueError("El estado de la factura no puede estar en blanco.")
        self._estado = estado

        self._idFactura = idFactura
        self._fecha = fecha


    @property
    def idFactura(self):
        return self._idFactura

    @property
    def concepto(self):
        return self._concepto

    @property
    def monto(self):
        return self._monto

    @property
    def fecha(self):
        return self._fecha

    @property
    def estado(self):
        return self._estado


    def __eq__(self, otro):
        if not isinstance(otro, FacturaVO):
            return False
        return (self._idFactura == otro._idFactura and
                self._concepto == otro._concepto and
                self._monto == otro._monto and
                self._fecha == otro._fecha and
                self._estado == otro._estado)

    def __str__(self):
        return (f"FacturaVO[ID: {self._idFactura} | Concepto: {self._concepto} "
                f"| Monto: {self._monto:.2f} € | Estado: {self._estado}]")

    def __repr__(self):
        return self.__str__()