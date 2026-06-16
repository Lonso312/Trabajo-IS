# archivo: modelo/negocio/factura_service.py
import datetime
from modelo.vo.factura_vo import FacturaVO


class FacturaService:
    def __init__(self, factura_dao):
        self.factura_dao = factura_dao

    # ------------------------------------------------------------------
    # CONSULTA
    # ------------------------------------------------------------------
    def obtener_todas_las_facturas(self):
        """Devuelve la lista de facturas formateadas como diccionarios."""
        try:
            return self.factura_dao.obtener_todas_las_facturas()
        except Exception as e:
            print(f"[FacturaService] Error obteniendo facturas: {e}")
            return []

    # ------------------------------------------------------------------
    # CREACIÓN
    # ------------------------------------------------------------------
    def crear_factura(self, datos: dict):
        """
        Valida los datos recibidos desde el controlador y persiste
        una nueva factura.  Devuelve (True, mensaje) o (False, error).
        """
        concepto = str(datos.get("concepto", "")).strip()
        monto_raw = str(datos.get("monto", "0")).strip().replace(",", ".")
        fecha = datos.get("fecha") or datetime.date.today().strftime("%Y-%m-%d")
        estado = str(datos.get("estado", "Pendiente")).strip()

        # --- Validaciones de negocio ---
        if not concepto:
            return False, "El concepto no puede estar vacío."

        if not estado:
            return False, "El estado no puede estar vacío."

        try:
            monto_float = float(monto_raw)
        except (ValueError, TypeError):
            return False, f"El monto '{monto_raw}' no es un número válido."

        if monto_float < 0:
            return False, "El monto no puede ser negativo."

        # Construcción del VO (el setter también valida)
        try:
            factura = FacturaVO(
                concepto=concepto,
                monto=monto_float,
                fecha=fecha,
                estado=estado,
            )
        except ValueError as e:
            return False, str(e)

        # Persistencia
        exito = self.factura_dao.insertar_factura(factura)
        if exito:
            return True, "Factura registrada correctamente."
        return False, "No se pudo guardar la factura en la base de datos."

    # ------------------------------------------------------------------
    # ACTUALIZACIÓN
    # ------------------------------------------------------------------
    def actualizar_factura(self, factura_id: int, datos: dict):
        """
        Valida los datos y actualiza una factura existente.
        Devuelve (True, mensaje) o (False, error).
        """
        concepto = str(datos.get("concepto", "")).strip()
        monto_raw = str(datos.get("monto", "0")).strip().replace(",", ".")
        estado = str(datos.get("estado", "Pendiente")).strip()

        # --- Validaciones de negocio ---
        if not factura_id:
            return False, "ID de factura inválido."

        if not concepto:
            return False, "El concepto no puede estar vacío."

        if not estado:
            return False, "El estado no puede estar vacío."

        try:
            monto_float = float(monto_raw)
        except (ValueError, TypeError):
            return False, f"El monto '{monto_raw}' no es un número válido."

        if monto_float < 0:
            return False, "El monto no puede ser negativo."

        # Validación adicional con el VO
        try:
            FacturaVO(concepto=concepto, monto=monto_float, estado=estado)
        except ValueError as e:
            return False, str(e)

        # Persistencia
        exito = self.factura_dao.actualizar_factura(factura_id, concepto, monto_float, estado)
        if exito:
            return True, "Factura actualizada correctamente."
        return False, "No se pudo actualizar la factura en la base de datos."