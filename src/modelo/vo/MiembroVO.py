import re

class MiembroVO:
    def __init__(self, UsuarioID=None, Name=None, Surname=None, DNI=None,
                 Email=None, NombreUsuario=None, Rol=None, Aceptado=None, Telefono=None):

        if Name is not None and isinstance(Name, str) and not Name.strip():
            raise ValueError("El nombre del miembro no puede ser una cadena de texto vacía.")
        self._Name = Name

        if Email is not None and str(Email).strip() and str(Email) != "None":
            email_regex = r"^[\w\.-]+@[\w\.-]+\.\w+$"
            if not re.match(email_regex, str(Email)):
                raise ValueError(f"El formato del email '{Email}' no es válido para el Miembro.")
        self._Email = Email

        if DNI is not None and str(DNI).strip() and str(DNI) != "None":
            cleaned_dni = str(DNI).upper().strip()
            if not re.match(r"^\d{8}[A-Z]$", cleaned_dni):
                raise ValueError(f"El DNI '{DNI}' no cumple el formato español (8 números y 1 letra).")
            self._DNI = cleaned_dni
        else:
            self._DNI = DNI

        if Telefono is not None and str(Telefono).strip() and str(Telefono) != "None":
            cleaned_tel = str(Telefono).replace(" ", "").replace("-", "")
            if not re.match(r"^[6789]\d{8}$", cleaned_tel):
                raise ValueError(f"El teléfono '{Telefono}' debe tener un formato válido de 9 dígitos.")
            self._Telefono = cleaned_tel
        else:
            self._Telefono = Telefono

        self._UsuarioID = UsuarioID
        self._Surname = Surname
        self._NombreUsuario = NombreUsuario
        self._Rol = Rol
        self._Aceptado = Aceptado


    @property
    def UsuarioID(self):
        return self._UsuarioID

    @property
    def Name(self):
        return self._Name

    @property
    def Surname(self):
        return self._Surname

    @property
    def DNI(self):
        return self._DNI

    @property
    def Email(self):
        return self._Email

    @property
    def NombreUsuario(self):
        return self._NombreUsuario

    @property
    def Rol(self):
        return self._Rol

    @property
    def Aceptado(self):
        return self._Aceptado

    @property
    def Telefono(self):
        return self._Telefono


    def __eq__(self, otro):
        if not isinstance(otro, MiembroVO):
            return False
        return (self._UsuarioID == otro._UsuarioID and
                self._Name == otro._Name and
                self._Surname == otro._Surname and
                self._DNI == otro._DNI and
                self._Email == otro._Email and
                self._NombreUsuario == otro._NombreUsuario and
                self._Rol == otro._Rol and
                self._Aceptado == otro._Aceptado and
                self._Telefono == otro._Telefono)

    def __str__(self):
        return f"MiembroVO[ID: {self._UsuarioID} | Nombre: {self._Name} | Email: {self._Email} | Rol: {self._Rol}]"

    def __repr__(self):
        return self.__str__()