class ItemInventarioVO:
    def __init__(self, idItem=None, nombre=None, cantidad=0, valor=0.0):
        self.idItem = idItem
        self.nombre = nombre
        self.cantidad = cantidad
        self.valor = valor

    @property
    def nombre(self):
        return self._nombre

    @nombre.setter
    def nombre(self, value):
        if value and isinstance(value, str) and not value.strip():
            raise ValueError("El nombre del ítem no puede estar vacío.")
        self._nombre = value

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
    def valor(self):
        return self._valor

    @valor.setter
    def valor(self, value):
        try:
            val_float = float(value)
            if val_float < 0.0:
                raise ValueError()
            self._valor = val_float
        except (ValueError, TypeError):
            raise ValueError(f"El valor monetario no puede ser negativo ni inválido: {value}")

    def __eq__(self, otro):
        if not isinstance(otro, ItemInventarioVO):
            return False
        return (self.idItem == otro.idItem and 
                self.nombre == otro.nombre and 
                self.cantidad == otro.cantidad and 
                self.valor == otro.valor)

    def __str__(self):
        return f"ItemInventarioVO[ID: {self.idItem} | Nombre: {self.nombre} | Cantidad: {self.cantidad} | Valor: {self.valor}]"

    def __repr__(self):
        return self.__str__()