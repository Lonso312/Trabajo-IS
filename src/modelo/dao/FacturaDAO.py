# archivo: modelo/dao/FacturaDAO.py
from modelo.vo.factura_vo import FacturaVO


class FacturaDAO:
    def __init__(self, conexion_db):
        self.conexion = conexion_db

    # ------------------------------------------------------------------
    # CONSULTA
    # ------------------------------------------------------------------
    def obtener_todas_las_facturas(self):
        """
        Recupera todas las facturas de la BD y las devuelve como lista
        de diccionarios.  El monto se formatea con símbolo € para la vista.
        """
        cursor = self.conexion.cursor()
        sql = """
            SELECT FacturaID, Concepto, Monto, Fecha, EstadoFactura
            FROM Facturas
            ORDER BY Fecha DESC, FacturaID DESC
        """
        lista_facturas = []
        try:
            cursor.execute(sql)
            filas = cursor.fetchall()
            for fila in filas:
                # Compatibilidad con jaydebeapi: los valores pueden venir
                # envueltos en objetos Java; str() y float() los normalizan.
                try:
                    monto_val = float(fila[2]) if fila[2] is not None else 0.0
                    monto_str = f"{monto_val:.2f} €"
                except (TypeError, ValueError):
                    monto_str = "0.00 €"

                lista_facturas.append({
                    "id":       int(fila[0]),
                    "concepto": str(fila[1]).strip() if fila[1] else "Sin Concepto",
                    "monto":    monto_str,
                    "fecha":    str(fila[3]) if fila[3] else "",
                    "estado":   str(fila[4]).strip() if fila[4] else "Pendiente",
                })
            return lista_facturas
        except Exception as e:
            print(f"[FacturaDAO] Error en obtener_todas_las_facturas: {e}")
            return []
        finally:
            cursor.close()

    # ------------------------------------------------------------------
    # INSERCIÓN
    # ------------------------------------------------------------------
    def insertar_factura(self, factura: FacturaVO) -> bool:
        """Inserta una nueva factura.  Devuelve True si tuvo éxito."""
        cursor = self.conexion.cursor()
        sql = """
            INSERT INTO Facturas (Concepto, Monto, Fecha, EstadoFactura)
            VALUES (?, ?, ?, ?)
        """
        try:
            cursor.execute(
                sql,
                [
                    str(factura.concepto).strip(),
                    float(factura.monto),
                    str(factura.fecha),
                    str(factura.estado).strip(),
                ],
            )
            self.conexion.commit()
            return True
        except Exception as e:
            print(f"[FacturaDAO] Error en insertar_factura: {e}")
            try:
                self.conexion.rollback()
            except Exception:
                pass
            return False
        finally:
            cursor.close()

    # ------------------------------------------------------------------
    # ACTUALIZACIÓN
    # ------------------------------------------------------------------
    def actualizar_factura(self, factura_id, concepto, monto, estado) -> bool:
        """
        Actualiza los campos editables de una factura existente.
        Devuelve True si tuvo éxito.
        """
        cursor = self.conexion.cursor()
        sql = """
            UPDATE Facturas
            SET Concepto     = ?,
                Monto        = ?,
                EstadoFactura = ?
            WHERE FacturaID  = ?
        """
        try:
            cursor.execute(
                sql,
                [
                    str(concepto).strip(),
                    float(monto),
                    str(estado).strip(),
                    int(factura_id),
                ],
            )
            self.conexion.commit()
            # Comprobamos que realmente se modificó alguna fila
            if cursor.rowcount == 0:
                print(f"[FacturaDAO] Advertencia: no existe factura con ID {factura_id}.")
                return False
            return True
        except Exception as e:
            print(f"[FacturaDAO] Error en actualizar_factura (ID={factura_id}): {e}")
            try:
                self.conexion.rollback()
            except Exception:
                pass
            return False
        finally:
            cursor.close()
