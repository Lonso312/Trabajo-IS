# archivo: DAO/FacturaDAO.py
from VO.factura_vo import FacturaVO

class FacturaDAO:
    def __init__(self, conexion_db):
        self.conexion = conexion_db

    def obtener_todas_las_facturas(self):
        """Recupera todas las facturas de la base de datos formateadas como diccionarios"""
        cursor = self.conexion.cursor()
        sql = "SELECT FacturaID, Concepto, Monto, Fecha, EstadoFactura FROM Facturas"
        lista_facturas = []
        try:
            cursor.execute(sql)
            filas = cursor.fetchall()
            for fila in filas:
                lista_facturas.append({
                    "id": fila[0],
                    "concepto": str(fila[1]) if fila[1] else "Sin Concepto",
                    "monto": f"{fila[2]:.2f} €" if fila[2] is not None else "0.00 €",
                    "fecha": str(fila[3]) if fila[3] else "",
                    "estado": str(fila[4]).strip() if fila[4] else "Pendiente"
                })
            return lista_facturas
        except Exception as e:
            print(f"Error en FacturaDAO.obtener_todas_las_facturas: {e}")
            return []
        finally:
            cursor.close()

    def insertar_factura(self,factura:FacturaVO):
        """Inserta una nueva factura en la base de datos"""
        cursor = self.conexion.cursor()
        sql = """
            INSERT INTO Facturas (Concepto, Monto, Fecha, EstadoFactura) 
            VALUES (?, ?, ?, ?)
        """
        try:
            cursor.execute(sql, [factura.concepto, factura.monto, factura.fecha, factura.estado])
            self.conexion.commit()
            return True
        except Exception as e:
            print(f"Error en FacturaDAO.insertar_factura: {e}")
            return False
        finally:
            cursor.close()

    def actualizar_factura(self, factura_id, concepto, monto, estado):
        """Modifica los datos de una factura existente"""
        cursor = self.conexion.cursor()
        sql = """
            UPDATE Facturas 
            SET Concepto = ?, Monto = ?, EstadoFactura = ? 
            WHERE FacturaID = ?
        """
        try:
            cursor.execute(sql, [str(concepto).strip(), float(monto), str(estado).strip(), int(factura_id)])
            self.conexion.commit()
            return True
        except Exception as e:
            print(f"Error en FacturaDAO.actualizar_factura: {e}")
            return False
        finally:
            cursor.close()
