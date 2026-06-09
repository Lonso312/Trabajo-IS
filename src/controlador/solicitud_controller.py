# archivo: controller/solicitud_controller.py

class SolicitudController:
    def __init__(self, solicitud_dao):
        self.solicitud_dao = solicitud_dao
        self.vista_solicitud = None