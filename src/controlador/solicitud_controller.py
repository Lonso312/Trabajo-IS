class SolicitudController:
    def __init__(self, solicitud_service):
        self.service = solicitud_service
        self.vista_solicitud = None
        self.usuario_actual = None

    def obtener_solicitudes_pendientes(self):
        """Usado por menu_view para cargar el panel de solicitudes."""
        try:
            return self.service.obtener_solicitudes(self.usuario_actual)
        except Exception as e:
            print(f"[SolicitudController] Error obteniendo solicitudes: {e}")
            return []

    def procesar_crear_solicitud(self, datos):
        try:
            exito, msg = self.service.crear_solicitud(datos)
            return exito, msg
        except ValueError as e:
            return False, f"Dato inválido: {str(e)}"
        except Exception as e:
            print(f"[SolicitudController] Error creando solicitud: {e}")
            return False, f"Error al crear la solicitud: {str(e)}"

    def procesar_aprobar_solicitud(self, solicitud_id):
        try:
            exito, msg = self.service.aprobar_solicitud(solicitud_id)
            return exito, msg
        except Exception as e:
            print(f"[SolicitudController] Error aprobando solicitud {solicitud_id}: {e}")
            return False, f"Error al aprobar la solicitud: {str(e)}"

    def procesar_rechazar_solicitud(self, solicitud_id):
        try:
            exito, msg = self.service.rechazar_solicitud(solicitud_id)
            return exito, msg
        except Exception as e:
            print(f"[SolicitudController] Error rechazando solicitud {solicitud_id}: {e}")
            return False, f"Error al rechazar la solicitud: {str(e)}"

    def procesar_eliminar_solicitud(self, solicitud_id):
        try:
            exito, msg = self.service.eliminar_solicitud(solicitud_id)
            return exito, msg
        except Exception as e:
            print(f"[SolicitudController] Error eliminando solicitud {solicitud_id}: {e}")
            return False, f"Error al eliminar la solicitud: {str(e)}"