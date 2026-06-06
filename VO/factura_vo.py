class FacturaVO:
    def __init__(self, idFactura=None, monto=0.0, fecha=None, tipo=None):
        self.idFactura = idFactura
        self.monto = monto
        self.fecha = fecha
        self.tipo = tipo

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
            raise ValueError(f"El monto de la factura no puede ser negativo ni inválido: {value}")

    @property
    def tipo(self):
        return self._tipo

    @tipo.setter
    def tipo(self, value):
        if value and isinstance(value, str) and not value.strip():
            raise ValueError("El tipo de factura no puede estar en blanco.")
        self._tipo = value

    def __eq__(self, otro):
        if not isinstance(otro, FacturaVO):
            return False
        return (self.idFactura == otro.idFactura and 
                self.monto == otro.monto and 
                self.fecha == otro.fecha and 
                self.tipo == otro.tipo)

    def __str__(self):
        return f"FacturaVO[ID: {self.idFactura} | Monto: {self.monto} | Tipo: {self.tipo}]"

    def __repr__(self):
        return self.__str__()