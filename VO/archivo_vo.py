class ArchivoVO:
    def __init__(self, idArchivo=None, nombre=None, ruta=None, tipo=None):
        self.idArchivo = idArchivo
        self.nombre = nombre
        self.ruta = ruta
        self.tipo = tipo

    @property
    def nombre(self):
        return self._nombre

    @nombre.setter
    def nombre(self, value):
        if value and isinstance(value, str) and not value.strip():
            raise ValueError("El nombre del archivo no puede estar en blanco.")
        self._nombre = value

    @property
    def ruta(self):
        return self._ruta

    @ruta.setter
    def ruta(self, value):
        if value and isinstance(value, str) and not value.strip():
            raise ValueError("La ruta del archivo no puede estar vacía.")
        self._ruta = value

    def __eq__(self, otro):
        if not isinstance(otro, ArchivoVO):
            return False
        return (self.idArchivo == otro.idArchivo and 
                self.nombre == otro.nombre and 
                self.ruta == otro.ruta and 
                self.tipo == otro.tipo)

    def __str__(self):
        return f"ArchivoVO[ID: {self.idArchivo} | Nombre: {self.nombre} | Tipo: {self.tipo}]"

    def __repr__(self):
        return self.__str__()