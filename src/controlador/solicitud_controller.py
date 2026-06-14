class SolicitudController:
    def __init__(self, solicitud_service):
        self.service = solicitud_service
        self.vista_solicitud = None
        self.usuario_actual = None

    def abrir_pantalla_solicitudes(self, usuario_actual):
        """
        Bug 4 fix: el controlador estaba vacío. Abre la vista
        e inyecta el usuario para filtrar solicitudes por rol/id.
        """
        from vistas.solicitud_view import SolicitudView
        self.usuario_actual = usuario_actual
        self.vista_solicitud = SolicitudView(self)
        self.cargar_solicitudes()
        self.vista_solicitud.show()

    def cargar_solicitudes(self):
        if not self.vista_solicitud or not self.usuario_actual:
            return
        try:
            solicitudes = self.service.obtener_solicitudes(self.usuario_actual)
            self.vista_solicitud.llenar_tabla(solicitudes)
        except Exception as e:
            print(f"[SolicitudController] Error cargando solicitudes: {e}")
            self.vista_solicitud.mostrar_mensaje_error(f"Error al cargar solicitudes: {str(e)}")

    def procesar_crear_solicitud(self, datos):
        try:
            exito, msg = self.service.crear_solicitud(datos)
            if exito:
                self.cargar_solicitudes()
            return exito, msg
        except ValueError as e:
            return False, f"Dato inválido: {str(e)}"
        except Exception as e:
            print(f"[SolicitudController] Error creando solicitud: {e}")
            return False, f"Error al crear la solicitud: {str(e)}"

    def procesar_eliminar_solicitud(self, solicitud_id):
        try:
            exito, msg = self.service.eliminar_solicitud(solicitud_id)
            if exito:
                self.cargar_solicitudes()
            return exito, msg
        except Exception as e:
            print(f"[SolicitudController] Error eliminando solicitud {solicitud_id}: {e}")
            return False, f"Error al eliminar la solicitud: {str(e)}"