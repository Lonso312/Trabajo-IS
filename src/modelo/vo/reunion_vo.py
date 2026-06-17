
class ReunionSecretariaVO:
    """Value Object que representa una reunion de la Secretaria (junta o pleno)."""

    ESTADOS_VALIDOS = ("Programada", "Celebrada", "Cancelada")

    def __init__(self, reunion_id=None, titulo=None, fecha=None, hora=None,
                 lugar=None, estado="Programada"):
        self.reunion_id = reunion_id
        self.titulo = titulo
        self.fecha = fecha
        self.hora = hora
        self.lugar = lugar
        self.estado = estado

    # ------------------------------------------------------------------
    # PROPIEDADES CON VALIDACION
    # ------------------------------------------------------------------
    @property
    def titulo(self):
        return self._titulo

    @titulo.setter
    def titulo(self, value):
        if value is not None and isinstance(value, str) and not value.strip():
            raise ValueError("El titulo de la reunion no puede estar en blanco.")
        self._titulo = value.strip() if isinstance(value, str) else value

    @property
    def fecha(self):
        return self._fecha

    @fecha.setter
    def fecha(self, value):
        if value is not None and isinstance(value, str) and not value.strip():
            raise ValueError("La fecha de la reunion no puede estar en blanco.")
        self._fecha = value.strip() if isinstance(value, str) else value

    @property
    def hora(self):
        return self._hora

    @hora.setter
    def hora(self, value):
        if value is not None and isinstance(value, str) and not value.strip():
            raise ValueError("La hora de la reunion no puede estar en blanco.")
        self._hora = value.strip() if isinstance(value, str) else value

    @property
    def lugar(self):
        return self._lugar

    @lugar.setter
    def lugar(self, value):
        if value is not None and isinstance(value, str) and not value.strip():
            raise ValueError("El lugar de la reunion no puede estar en blanco.")
        self._lugar = value.strip() if isinstance(value, str) else value

    @property
    def estado(self):
        return self._estado

    @estado.setter
    def estado(self, value):
        valor = str(value).strip() if value else "Programada"
        if valor not in self.ESTADOS_VALIDOS:
            raise ValueError(
                f"Estado de reunion invalido: '{valor}'. "
                f"Debe ser uno de: {', '.join(self.ESTADOS_VALIDOS)}"
            )
        self._estado = valor

    # ------------------------------------------------------------------
    # CONSTRUCTOR AUXILIAR
    # ------------------------------------------------------------------
    @staticmethod
    def from_fila_db(fila):
        """Construye un ReunionSecretariaVO a partir de una fila devuelta por el cursor JDBC."""
        return ReunionSecretariaVO(
            reunion_id=int(fila[0]) if fila[0] is not None else None,
            titulo=str(fila[1]).strip() if fila[1] else "Sin titulo",
            fecha=str(fila[2]) if fila[2] else "",
            hora=str(fila[3]) if fila[3] else "",
            lugar=str(fila[4]).strip() if fila[4] else "Sin especificar",
            estado=str(fila[5]).strip() if fila[5] else "Programada",
        )

    # ------------------------------------------------------------------
    # UTILIDADES
    # ------------------------------------------------------------------
    def __eq__(self, otro):
        if not isinstance(otro, ReunionSecretariaVO):
            return False
        return (self.reunion_id == otro.reunion_id and
                self.titulo == otro.titulo and
                self.fecha == otro.fecha and
                self.hora == otro.hora and
                self.lugar == otro.lugar and
                self.estado == otro.estado)

    def __str__(self):
        return (f"ReunionSecretariaVO[ID: {self.reunion_id} | {self.titulo} | "
                f"{self.fecha} {self.hora} | {self.lugar} | {self.estado}]")

    def __repr__(self):
        return self.__str__()