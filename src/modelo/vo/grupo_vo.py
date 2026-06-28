class GrupoVO:
    def __init__(self, GrupoID=None, Name=None, CantidadMiembros=0):
        if Name is not None and isinstance(Name, str) and not Name.strip():
            raise ValueError("El nombre del grupo no puede estar en blanco.")
        self._Name = Name

        try:
            val_int = int(CantidadMiembros)
            if val_int < 0:
                raise ValueError()
            self._CantidadMiembros = val_int
        except (ValueError, TypeError):
            raise ValueError(
                f"La cantidad de miembros no puede ser negativa ni inválida: {CantidadMiembros}"
            )

        self._GrupoID = GrupoID


    @property
    def GrupoID(self):
        return self._GrupoID

    @property
    def Name(self):
        return self._Name

    @property
    def CantidadMiembros(self):
        return self._CantidadMiembros


    def __eq__(self, otro):
        if not isinstance(otro, GrupoVO):
            return False
        return (self._GrupoID == otro._GrupoID and
                self._Name == otro._Name and
                self._CantidadMiembros == otro._CantidadMiembros)

    def __str__(self):
        return f"GrupoVO[ID: {self._GrupoID} | Nombre: {self._Name} | Miembros: {self._CantidadMiembros}]"

    def __repr__(self):
        return self.__str__()