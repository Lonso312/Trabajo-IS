class ArchivoVO:
    def __init__(self, idArchivo=None, nombre=None, ruta=None, tipo=None):

        # Validación: nombre
        if nombre is not None and isinstance(nombre, str) and not nombre.strip():
            raise ValueError("El nombre del archivo no puede estar en blanco.")
        self._nombre = nombre

        # Validación: ruta
        if ruta is not None and isinstance(ruta, str) and not ruta.strip():
            raise ValueError("La ruta del archivo no puede estar vacía.")
        self._ruta = ruta

        self._idArchivo = idArchivo
        self._tipo = tipo


    @property
    def idArchivo(self):
        return self._idArchivo

    @property
    def nombre(self):
        return self._nombre

    @property
    def ruta(self):
        return self._ruta

    @property
    def tipo(self):
        return self._tipo


    def __eq__(self, otro):
        if not isinstance(otro, ArchivoVO):
            return False
        return (self._idArchivo == otro._idArchivo and
                self._nombre == otro._nombre and
                self._ruta == otro._ruta and
                self._tipo == otro._tipo)

    def __str__(self):
        return f"ArchivoVO[ID: {self._idArchivo} | Nombre: {self._nombre} | Tipo: {self._tipo}]"

    def __repr__(self):
        return self.__str__()