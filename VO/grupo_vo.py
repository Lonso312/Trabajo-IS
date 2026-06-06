# archivo: vo/grupo_vo.py

class GrupoVO:
    def __init__(self, GrupoID=None, Name=None, CantidadMiembros=0):
        self.GrupoID = GrupoID
        self.Name = Name  
        self.CantidadMiembros = CantidadMiembros

    def __str__(self):
        return f"GrupoVO[ID: {self.GrupoID} | Nombre: {self.Name}]"