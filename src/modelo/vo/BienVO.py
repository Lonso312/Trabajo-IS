# archivo: BienVO.py

class BienVO:
    def __init__(self, BienID=None, tipo=None, precio=None, cantidad=None):

        # Validación: tipo
        if tipo is not None and isinstance(tipo, str) and not tipo.strip():
            raise ValueError("El tipo del bien no puede estar en blanco.")
        self._tipo = tipo

        # Validación: precio
        if precio is not None:
            try:
                val_precio = float(precio)
                if val_precio < 0.0:
                    raise ValueError()
                self._precio = val_precio
            except (ValueError, TypeError):
                raise ValueError(f"El precio del bien no puede ser negativo ni inválido: {precio}")
        else:
            self._precio = None

        # Validación: cantidad
        if cantidad is not None:
            try:
                val_cantidad = int(cantidad)
                if val_cantidad < 0:
                    raise ValueError()
                self._cantidad = val_cantidad
            except (ValueError, TypeError):
                raise ValueError(f"La cantidad del bien no puede ser negativa ni inválida: {cantidad}")
        else:
            self._cantidad = None

        self._BienID = BienID

        # Atributo extendido para información agregada de tesoreros vinculados
        self._tesoreros_asignados = "Ninguno"

    # --- PROPIEDADES DE SOLO LECTURA ---

    @property
    def BienID(self):
        return self._BienID

    @property
    def tipo(self):
        return self._tipo

    @property
    def precio(self):
        return self._precio

    @property
    def cantidad(self):
        return self._cantidad

    @property
    def tesoreros_asignados(self):
        return self._tesoreros_asignados

    # --- COMPARACIÓN ESTRUCTURAL ---

    def __eq__(self, otro):
        if not isinstance(otro, BienVO):
            return False
        return (self._BienID == otro._BienID and
                self._tipo == otro._tipo and
                self._precio == otro._precio and
                self._cantidad == otro._cantidad)

    def __str__(self):
        return (f"BienVO[ID: {self._BienID} | Tipo: {self._tipo} "
                f"| Precio: {self._precio} | Cantidad: {self._cantidad}]")

    def __repr__(self):
        return self.__str__()