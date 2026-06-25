# archivo: tarea_vo.py

class TareaVO:
    def __init__(self, TareaID=None, GrupoID=None, Titulo=None,
                 Descripcion=None, FechaLimite=None):

        # Validación: Titulo
        if Titulo is not None and isinstance(Titulo, str) and not Titulo.strip():
            raise ValueError(
                "El título de la tarea no puede consistir únicamente en espacios en blanco."
            )
        self._Titulo = Titulo

        self._TareaID = TareaID
        self._GrupoID = GrupoID
        self._Descripcion = Descripcion
        self._FechaLimite = FechaLimite

    # --- PROPIEDADES DE SOLO LECTURA ---

    @property
    def TareaID(self):
        return self._TareaID

    @property
    def GrupoID(self):
        return self._GrupoID

    @property
    def Titulo(self):
        return self._Titulo

    @property
    def Descripcion(self):
        return self._Descripcion

    @property
    def FechaLimite(self):
        return self._FechaLimite

    # --- COMPARACIÓN ESTRUCTURAL ---

    def __eq__(self, otro):
        if not isinstance(otro, TareaVO):
            return False
        return (self._TareaID == otro._TareaID and
                self._GrupoID == otro._GrupoID and
                self._Titulo == otro._Titulo and
                self._Descripcion == otro._Descripcion and
                self._FechaLimite == otro._FechaLimite)

    def __str__(self):
        return f"TareaVO[ID: {self._TareaID} | Título: {self._Titulo} | Grupo Asignado: {self._GrupoID}]"

    def __repr__(self):
        return self.__str__()
