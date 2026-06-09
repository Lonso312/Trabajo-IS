# archivo: factura_vo.py

class FacturaVO:
    def __init__(self, idFactura=None, concepto=None, monto=0.0, fecha=None, estado=None):
        self.idFactura = idFactura
        self.concepto = concepto
        self.monto = monto
        self.fecha = fecha
        self.estado = estado

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
    def concepto(self):
        return self._concepto

    @concepto.setter
    def concepto(self, value):
        if value and isinstance(value, str) and not value.strip():
            raise ValueError("El concepto de la factura no puede estar en blanco.")
        self._concepto = value

    @property
    def estado(self):
        return self._estado

    @estado.setter
    def estado(self, value):
        if value and isinstance(value, str) and not value.strip():
            raise ValueError("El estado de la factura no puede estar en blanco.")
        self._estado = value

    def __eq__(self, otro):
        if not isinstance(otro, FacturaVO):
            return False
        return (self.idFactura == otro.idFactura and 
                self.concepto == otro.concepto and 
                self.monto == otro.monto and 
                self.fecha == otro.fecha and 
                self.estado == otro.estado)

    def __str__(self):
        return f"FacturaVO[ID: {self.idFactura} | Concepto: {self.concepto} | Monto: {self.monto:.2f} € | Estado: {self.estado}]"

    def __repr__(self):
        return self.__str__()