class FacturaController:
    def __init__(self, factura_service):
        self.service = factura_service
        self.vista_factura = None
