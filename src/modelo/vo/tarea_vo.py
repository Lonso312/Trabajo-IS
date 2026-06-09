class TareaVO:
    def __init__(self, TareaID=None, GrupoID=None, Titulo=None, Descripcion=None, FechaLimite=None):
        self.TareaID = TareaID
        self.GrupoID = GrupoID
        self.Titulo = Titulo
        self.Descripcion = Descripcion
        self.FechaLimite = FechaLimite

    @property
    def Titulo(self):
        return self._Titulo

    @Titulo.setter
    def Titulo(self, value):
        if value and isinstance(value, str) and not value.strip():
            raise ValueError("El título de la tarea no puede consistir únicamente en espacios en blanco.")
        self._Titulo = value


    def __eq__(self, otro):
        if not isinstance(otro, TareaVO):
            return False
        return (self.TareaID == otro.TareaID and 
                self.GrupoID == otro.GrupoID and 
                self.Titulo == otro.Titulo and 
                self.Descripcion == otro.Descripcion and 
                self.FechaLimite == otro.FechaLimite)

    def __str__(self):
        return f"TareaVO[ID: {self.TareaID} | Título: {self.Titulo} | Grupo Asignado: {self.GrupoID}]"

    def __repr__(self):
        return self.__str__()
