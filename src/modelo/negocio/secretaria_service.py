
# archivo: modelo/negocio/secretaria_service.py
import datetime
from modelo.vo.reunion_vo import ReunionSecretariaVO

ROLES_QUE_PUEDEN_CONVOCAR = ("SECRETARIO",)
ROLES_QUE_PUEDEN_CAMBIAR_ESTADO = ("SECRETARIO", "PRESIDENTE")


class SecretariaService:
    def __init__(self, secretaria_dao):
        self.secretaria_dao = secretaria_dao

    def obtener_reuniones(self):
        """Devuelve la lista de reuniones (objetos ReunionSecretariaVO)."""
        try:
            return self.secretaria_dao.obtener_reuniones_secretaria()
        except Exception as e:
            print(f"[SecretariaService] Error obteniendo reuniones: {e}")
            return []

    def crear_reunion(self, datos: dict, rol_operador: str):
        """
        Valida los datos de la nueva reunion y la persiste.
        Devuelve (True, mensaje) o (False, error).
        """
        rol_limpio = str(rol_operador).strip().upper() if rol_operador else "MIEMBRO"
        if rol_limpio not in ROLES_QUE_PUEDEN_CONVOCAR:
            return False, "Solo el Secretario puede convocar reuniones."

        titulo = str(datos.get("titulo", "")).strip()
        fecha = str(datos.get("fecha", "")).strip()
        hora = str(datos.get("hora", "")).strip()
        lugar = str(datos.get("lugar", "")).strip()

        if not titulo:
            return False, "El titulo/motivo de la reunion es obligatorio."
        if not lugar:
            return False, "El lugar de la reunion es obligatorio."

        if not fecha:
            fecha = datetime.date.today().strftime("%Y-%m-%d")
        try:
            datetime.datetime.strptime(fecha, "%Y-%m-%d")
        except ValueError:
            return False, "La fecha debe tener el formato AAAA-MM-DD."

        if not hora:
            return False, "La hora de la reunion es obligatoria."
        if len(hora) == 5 and ":" in hora:
            hora = f"{hora}:00"
        try:
            datetime.datetime.strptime(hora, "%H:%M:%S")
        except ValueError:
            return False, "La hora debe tener el formato HH:MM."

        try:
            reunion = ReunionSecretariaVO(
                titulo=titulo,
                fecha=fecha,
                hora=hora,
                lugar=lugar,
                estado="Programada",
            )
        except ValueError as e:
            return False, str(e)

        exito = self.secretaria_dao.registrar_reunion(reunion)
        if exito:
            return True, "Reunion convocada correctamente."
        return False, "No se pudo registrar la reunion en la base de datos."

    def cambiar_estado_reunion(self, reunion_id, nuevo_estado: str, rol_operador: str):
        """
        Valida permisos y el estado solicitado antes de actualizar la reunion.
        Devuelve (True, mensaje) o (False, error).
        """
        rol_limpio = str(rol_operador).strip().upper() if rol_operador else "MIEMBRO"
        if rol_limpio not in ROLES_QUE_PUEDEN_CAMBIAR_ESTADO:
            return False, "No tienes permiso para cambiar el estado de la reunion."

        if not reunion_id:
            return False, "ID de reunion invalido."

        estado_limpio = str(nuevo_estado).strip() if nuevo_estado else ""
        if estado_limpio not in ReunionSecretariaVO.ESTADOS_VALIDOS:
            return False, f"Estado '{nuevo_estado}' no es valido."

        exito = self.secretaria_dao.actualizar_estado_reunion(reunion_id, estado_limpio)
        if exito:
            return True, f"Reunion marcada como '{estado_limpio}'."
        return False, "No se pudo actualizar el estado de la reunion."