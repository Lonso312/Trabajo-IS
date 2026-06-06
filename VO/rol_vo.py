class RolVO:
    def __init__(self, idRol=None, nombre=None):
        self.idRol = idRol
        self.nombre = nombre

    @property
    def nombre(self):
        return self._nombre

    @nombre.setter
    def nombre(self, value):
        if value and isinstance(value, str) and not value.strip():
            raise ValueError("El nombre del rol no puede consistir únicamente en espacios en blanco.")
        self._nombre = value

    def __eq__(self, otro):
        if not isinstance(otro, RolVO):
            return False
        return self.idRol == otro.idRol and self.nombre == otro.nombre

    def __str__(self):
        return f"RolVO[ID: {self.idRol} | Nombre: {self.nombre}]"

    def __repr__(self):
        return self.__str__()