class GrupoVO:
    def __init__(self, GrupoID=None, Name=None, CantidadMiembros=0):
        self.GrupoID = GrupoID
        self.Name = Name  
        self.CantidadMiembros = CantidadMiembros


    @property
    def Name(self):
        return self._Name

    @Name.setter
    def Name(self, value):
        if value and isinstance(value, str) and not value.strip():
            raise ValueError("El nombre del grupo no puede estar en blanco.")
        self._Name = value

    @property
    def CantidadMiembros(self):
        return self._CantidadMiembros

    @CantidadMiembros.setter
    def CantidadMiembros(self, value):
        try:
            val_int = int(value)
            if val_int < 0:
                raise ValueError()
            self._CantidadMiembros = val_int
        except (ValueError, TypeError):
            raise ValueError(f"La cantidad de miembros del grupo no puede ser negativa ni inválida: {value}")

    def __eq__(self, otro):
        if not isinstance(otro, GrupoVO):
            return False
        return (self.GrupoID == otro.GrupoID and 
                self.Name == otro.Name and 
                self.CantidadMiembros == otro.CantidadMiembros)

    def __str__(self):
        return f"GrupoVO[ID: {self.GrupoID} | Nombre: {self.Name} | Miembros: {self.CantidadMiembros}]"

    def __repr__(self):
        return self.__str__()
