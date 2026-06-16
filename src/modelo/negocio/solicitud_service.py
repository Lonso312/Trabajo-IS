class SolicitudService:
    def __init__(self, solicitud_dao):
        self.solicitud_dao = solicitud_dao

    def obtener_solicitudes(self, usuario_actual):
        """
        Devuelve solicitudes según el rol del usuario:
        - Tesorero/Presidente: ve todas las pendientes (para aprobar/rechazar)
        - Jefe de Departamento: ve todas (las suyas incluidas)
        """
        return self.solicitud_dao.obtener_solicitudes_pendientes_vo()

    def crear_solicitud(self, datos):
        """
        Crea una nueva solicitud de material.
        datos: dict con 'concepto', 'cantidad', 'solicitante'
        """
        from modelo.vo.solicitudCompra_vo import SolicitudMaterialVO

        concepto = str(datos.get("concepto", "")).strip()
        solicitante = str(datos.get("solicitante", "")).strip()

        if not concepto:
            return False, "El concepto no puede estar vacío."

        try:
            cantidad = int(datos.get("cantidad", 0))
        except (ValueError, TypeError):
            return False, "La cantidad debe ser un número entero."

        if cantidad <= 0:
            return False, "La cantidad debe ser mayor que cero."

        vo = SolicitudMaterialVO(
            concepto=concepto,
            cantidad=cantidad,
            solicitante=solicitante,
            estado="Pendiente"
        )

        exito = self.solicitud_dao.registrar_solicitud_vo(vo)
        if exito:
            return True, "Solicitud enviada correctamente."
        return False, "Error al registrar la solicitud en la base de datos."

    def eliminar_solicitud(self, solicitud_id):
        """Cambia el estado a 'Eliminado' (o borra, según el DAO disponible)."""
        exito = self.solicitud_dao.cambiar_estado_solicitud(solicitud_id, "Eliminado")
        if exito:
            return True, "Solicitud eliminada."
        return False, "No se pudo eliminar la solicitud."

    def aprobar_solicitud(self, solicitud_id):
        exito = self.solicitud_dao.cambiar_estado_solicitud(solicitud_id, "Aprobado")
        if exito:
            return True, "Solicitud aprobada."
        return False, "No se pudo aprobar la solicitud."

    def rechazar_solicitud(self, solicitud_id):
        exito = self.solicitud_dao.cambiar_estado_solicitud(solicitud_id, "Rechazado")
        if exito:
            return True, "Solicitud rechazada."
        return False, "No se pudo rechazar la solicitud."