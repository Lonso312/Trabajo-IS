class FacturaController:
    def __init__(self, factura_service):
        self.service = factura_service
        self.vista_factura = None

    def obtener_todas_las_facturas(self):
        try:
            return self.service.obtener_todas_las_facturas()
        except Exception as e:
            print(f"[FacturaController] Error obteniendo facturas: {e}")
            return []

    def procesar_crear_factura(self, datos):
        try:
            return self.service.crear_factura(datos)
        except ValueError as e:
            return False, f"Dato inválido: {str(e)}"
        except Exception as e:
            print(f"[FacturaController] Error creando factura: {e}")
            return False, f"Error al crear la factura: {str(e)}"

    def procesar_actualizar_factura(self, factura_id, datos):
        try:
            return self.service.actualizar_factura(factura_id, datos)
        except ValueError as e:
            return False, f"Dato inválido: {str(e)}"
        except Exception as e:
            print(f"[FacturaController] Error actualizando factura {factura_id}: {e}")
            return False, f"Error al actualizar la factura: {str(e)}"