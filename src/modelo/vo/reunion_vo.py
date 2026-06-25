# archivo: reunion_vo.py

class ReunionSecretariaVO:
    """Value Object que representa una reunion de la Secretaria (junta o pleno)."""

    ESTADOS_VALIDOS = ("Programada", "Celebrada", "Cancelada")

    def __init__(self, reunion_id=None, titulo=None, fecha=None, hora=None,
                 lugar=None, estado="Programada"):

        # Validación: titulo
        if titulo is not None and isinstance(titulo, str) and not titulo.strip():
            raise ValueError("El titulo de la reunion no puede estar en blanco.")
        self._titulo = titulo.strip() if isinstance(titulo, str) else titulo

        # Validación: fecha
        if fecha is not None and isinstance(fecha, str) and not fecha.strip():
            raise ValueError("La fecha de la reunion no puede estar en blanco.")
        self._fecha = fecha.strip() if isinstance(fecha, str) else fecha

        # Validación: hora
        if hora is not None and isinstance(hora, str) and not hora.strip():
            raise ValueError("La hora de la reunion no puede estar en blanco.")
        self._hora = hora.strip() if isinstance(hora, str) else hora

        # Validación: lugar
        if lugar is not None and isinstance(lugar, str) and not lugar.strip():
            raise ValueError("El lugar de la reunion no puede estar en blanco.")
        self._lugar = lugar.strip() if isinstance(lugar, str) else lugar

        # Validación: estado
        valor_estado = str(estado).strip() if estado else "Programada"
        if valor_estado not in self.ESTADOS_VALIDOS:
            raise ValueError(
                f"Estado de reunion invalido: '{valor_estado}'. "
                f"Debe ser uno de: {', '.join(self.ESTADOS_VALIDOS)}"
            )
        self._estado = valor_estado

        self._reunion_id = reunion_id

    # --- PROPIEDADES DE SOLO LECTURA ---

    @property
    def reunion_id(self):
        return self._reunion_id

    @property
    def titulo(self):
        return self._titulo

    @property
    def fecha(self):
        return self._fecha

    @property
    def hora(self):
        return self._hora

    @property
    def lugar(self):
        return self._lugar

    @property
    def estado(self):
        return self._estado

    # --- CONSTRUCTOR AUXILIAR ---

    @staticmethod
    def from_fila_db(fila):
        """Construye un ReunionSecretariaVO a partir de una fila devuelta por el cursor."""
        return ReunionSecretariaVO(
            reunion_id=int(fila[0]) if fila[0] is not None else None,
            titulo=str(fila[1]).strip() if fila[1] else "Sin titulo",
            fecha=str(fila[2]) if fila[2] else "",
            hora=str(fila[3]) if fila[3] else "",
            lugar=str(fila[4]).strip() if fila[4] else "Sin especificar",
            estado=str(fila[5]).strip() if fila[5] else "Programada",
        )

    # --- COMPARACIÓN ESTRUCTURAL ---

    def __eq__(self, otro):
        if not isinstance(otro, ReunionSecretariaVO):
            return False
        return (self._reunion_id == otro._reunion_id and
                self._titulo == otro._titulo and
                self._fecha == otro._fecha and
                self._hora == otro._hora and
                self._lugar == otro._lugar and
                self._estado == otro._estado)

    def __str__(self):
        return (f"ReunionSecretariaVO[ID: {self._reunion_id} | {self._titulo} | "
                f"{self._fecha} {self._hora} | {self._lugar} | {self._estado}]")

    def __repr__(self):
        return self.__str__()