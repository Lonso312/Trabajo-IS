class TareaVO:
    def __init__(self, TareaID=None, GrupoID=None, Titulo=None, Descripcion=None, FechaLimite=None):
        self.TareaID = TareaID
        self.GrupoID = GrupoID
        self.Titulo = Titulo
        self.Descripcion = Descripcion
        self.FechaLimite = FechaLimite

    def __str__(self):
        return f"TareaVO[ID: {self.TareaID} | Título: {self.Titulo}]"