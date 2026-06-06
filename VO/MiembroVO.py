class MiembroVO:
    def __init__(self, UsuarioID=None, Name=None, Surname=None, DNI=None, Email=None, NombreUsuario = None, Rol=None, Aceptado=None, Telefono=None):
        self.UsuarioID = UsuarioID
        self.Name = Name
        self.Email = Email
        self.Rol = Rol
        self.DNI= DNI
        self.NombreUsuario= NombreUsuario
        self.Surname=Surname
        self.Aceptado=Aceptado
        self.Telefono=Telefono
        

    
    def __str__(self):
        return f"MiembroVO[ID: {self.UsuarioID} | Nombre: {self.Name} | Email: {self.Email} | DNI: {self.DNI}]"