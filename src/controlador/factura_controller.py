# archivo: controlador/factura_controller.py

class FacturaController:
    def __init__(self, factura_service):
        self.service = factura_service
        self.vista_factura = None  # reservado para futuros usos

    # ------------------------------------------------------------------
    # CONSULTA
    # ------------------------------------------------------------------
    def obtener_todas_las_facturas(self):
        """
        Solicita la lista de facturas al servicio.
        Devuelve una lista de diccionarios lista para mostrar en la vista.
        """
        try:
            return self.service.obtener_todas_las_facturas()
        except Exception as e:
            print(f"[FacturaController] Error obteniendo facturas: {e}")
            return []

    # ------------------------------------------------------------------
    # CREACIÓN
    # ------------------------------------------------------------------
    def procesar_crear_factura(self, datos: dict):
        """
        Recibe los datos del formulario de la vista, los delega al servicio
        y devuelve (True, msg) o (False, msg) para que la vista los muestre.
        """
        if not datos:
            return False, "No se recibieron datos para crear la factura."

        try:
            return self.service.crear_factura(datos)
        except ValueError as e:
            return False, f"Dato inválido: {str(e)}"
        except Exception as e:
            print(f"[FacturaController] Error creando factura: {e}")
            return False, f"Error inesperado al crear la factura: {str(e)}"

    # ------------------------------------------------------------------
    # ACTUALIZACIÓN
    # ------------------------------------------------------------------
    def procesar_actualizar_factura(self, factura_id, datos: dict):
        """
        Recibe el ID de la factura y los datos modificados, los delega al
        servicio y devuelve (True, msg) o (False, msg).
        """
        if factura_id is None:
            return False, "No se especificó el ID de la factura a actualizar."

        if not datos:
            return False, "No se recibieron datos para actualizar la factura."

        try:
            return self.service.actualizar_factura(factura_id, datos)
        except ValueError as e:
            return False, f"Dato inválido: {str(e)}"
        except Exception as e:
            print(f"[FacturaController] Error actualizando factura {factura_id}: {e}")
            return False, f"Error inesperado al actualizar la factura: {str(e)}"