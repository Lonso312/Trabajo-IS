class SolicitudController:
    def __init__(self, solicitud_service):
        self.service = solicitud_service
        self.vista_solicitud = None
