import re

class MiembroVO:
    def __init__(self, UsuarioID=None, Name=None, Surname=None, DNI=None, Email=None, NombreUsuario=None, Rol=None, Aceptado=None, Telefono=None):
        # El constructor usa directamente las propiedades para aplicar las validaciones desde el inicio
        self.UsuarioID = UsuarioID
        self.Name = Name
        self.Surname = Surname
        self.DNI = DNI
        self.Email = Email
        self.NombreUsuario = NombreUsuario
        self.Rol = Rol
        self.Aceptado = Aceptado
        self.Telefono = Telefono

    # --- VALIDACIONES Y ENCAPSULACIÓN ---
    
    @property
    def Email(self):
        return self._Email

    @Email.setter
    def Email(self, value):
        if value and str(value).strip() and str(value) != "None":
            email_regex = r"^[\w\.-]+@[\w\.-]+\.\w+$"
            if not re.match(email_regex, str(value)):
                raise ValueError(f"El formato del email '{value}' no es válido para el Miembro.")
        self._Email = value

    @property
    def Telefono(self):
        return self._Telefono

    @Telefono.setter
    def Telefono(self, value):
        if value and str(value).strip() and str(value) != "None":
            # Limpiamos posibles espacios o guiones del formato
            cleaned = str(value).replace(" ", "").replace("-", "")
            if not re.match(r"^[6789]\d{8}$", cleaned):
                raise ValueError(f"El teléfono '{value}' debe tener un formato válido de 9 dígitos.")
            self._Telefono = cleaned
        else:
            self._Telefono = value

    @property
    def DNI(self):
        return self._DNI

    @DNI.setter
    def DNI(self, value):
        if value and str(value).strip() and str(value) != "None":
            cleaned = str(value).upper().strip()
            if not re.match(r"^\d{8}[A-Z]$", cleaned):
                raise ValueError(f"El DNI '{value}' no cumple el formato español (8 números y 1 letra).")
            self._DNI = cleaned
        else:
            self._DNI = value

    @property
    def Name(self):
        return self._Name

    @Name.setter
    def Name(self, value):
        if value and isinstance(value, str) and not value.strip():
            raise ValueError("El nombre del miembro no puede ser una cadena de texto vacía.")
        self._Name = value

    # --- COMPARACIÓN ESTRUCTURAL ---
    def __eq__(self, otro):
        """Permite verificar si dos objetos contienen exactamente la misma información"""
        if not isinstance(otro, MiembroVO):
            return False
        return (self.UsuarioID == otro.UsuarioID and 
                self.Name == otro.Name and 
                self.Surname == otro.Surname and 
                self.DNI == otro.DNI and 
                self.Email == otro.Email and 
                self.NombreUsuario == otro.NombreUsuario and 
                self.Rol == otro.Rol and 
                self.Aceptado == otro.Aceptado and 
                self.Telefono == otro.Telefono)

    def __str__(self):
        return f"MiembroVO[ID: {self.UsuarioID} | Nombre: {self.Name} | Email: {self.Email} | Rol: {self.Rol}]"
    
    def __repr__(self):
        return self.__str__()
