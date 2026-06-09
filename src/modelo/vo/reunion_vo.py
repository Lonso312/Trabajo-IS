# archivo: VO/ReunionSecretariaVO.py

class ReunionSecretariaVO:
    def __init__(self, reunion_id=None, titulo="", fecha="", hora="", lugar="", secretario_id=None, estado="Programada"):
        self._reunion_id = reunion_id
        self._titulo = titulo
        self._fecha = fecha
        self._hora = hora
        self._lugar = lugar
        self._secretario_id = secretario_id
        self._estado = estado

    # --- GETTERS Y SETTERS ---
    @property
    def reunion_id(self): return self._reunion_id
    @reunion_id.setter
    def reunion_id(self, value): self._reunion_id = value

    @property
    def titulo(self): return self._titulo
    @titulo.setter
    def titulo(self, value): self._titulo = str(value).strip()

    @property
    def fecha(self): return self._fecha
    @fecha.setter
    def fecha(self, value): self._fecha = value

    @property
    def hora(self): return self._hora
    @hora.setter
    def hora(self, value): self._hora = str(value).strip()

    @property
    def lugar(self): return self._lugar
    @lugar.setter
    def lugar(self, value): self._lugar = str(value).strip()

    @property
    def estado(self): return self._estado
    @estado.setter
    def estado(self, value): self._estado = str(value).strip()

    def to_dict(self):
        """Convierte el objeto a un diccionario (útil para APIs o JSON)"""
        return {
            "reunion_id": self._reunion_id,
            "titulo": self._titulo,
            "fecha": self._fecha,
            "hora": self._hora,
            "lugar": self._lugar,
            "estado": self._estado
        }

    @staticmethod
    def from_fila_db(fila):
        """Construye un VO a partir de una tupla/fila de la base de datos"""
        if not fila:
            return None
        return ReunionSecretariaVO(
            reunion_id=fila[0],
            titulo=fila[1],
            fecha=fila[2],
            hora=fila[3],
            lugar=fila[4],
            estado=fila[5]
        )