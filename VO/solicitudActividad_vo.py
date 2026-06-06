class SesionActividadVO:
    def __init__(self, idSesion=None, nombre=None, fecha=None, lugar=None):
        self.idSesion = idSesion
        self.nombre = nombre
        self.fecha = fecha
        self.lugar = lugar

    @property
    def nombre(self):
        return self._nombre

    @nombre.setter
    def nombre(self, value):
        if value and isinstance(value, str) and not value.strip():
            raise ValueError("El nombre de la sesión no puede estar vacío.")
        self._nombre = value

    @property
    def lugar(self):
        return self._lugar

    @lugar.setter
    def lugar(self, value):
        if value and isinstance(value, str) and not value.strip():
            raise ValueError("El lugar de la sesión no puede estar vacío.")
        self._lugar = value

    def __eq__(self, otro):
        if not isinstance(otro, SesionActividadVO):
            return False
        return (self.idSesion == otro.idSesion and 
                self.nombre == otro.nombre and 
                self.fecha == otro.fecha and 
                self.lugar == otro.lugar)

    def __str__(self):
        return f"SesionActividadVO[ID: {self.idSesion} | Nombre: {self.nombre} | Lugar: {self.lugar}]"

    def __repr__(self):
        return self.__str__()