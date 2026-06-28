# archivo: DAO/SolicitudDAO.py
from modelo.vo.solicitudCompra_vo import SolicitudMaterialVO
class SolicitudDAO:
    def __init__(self, conexion_db):
        self.conexion = conexion_db

    def registrar_solicitud_vo(self, solicitud: SolicitudMaterialVO):
        """Registra una nueva petición usando el objeto VO"""
        cursor = self.conexion.cursor()
        sql = """
            INSERT INTO SolicitudesMateriales (Concepto, Cantidad, Solicitante, Estado)
            VALUES (?, ?, ?, 'Pendiente')
        """
        try:
            # El VO ya viene validado desde la vista
            cursor.execute(sql, [solicitud.concepto, solicitud.cantidad, solicitud.solicitante])
            self.conexion.commit()
            return True
        except Exception as e:
            print(f"Error en SolicitudDAO.registrar_solicitud_vo: {e}")
            return False
        finally:
            cursor.close()

    def obtener_solicitudes_pendientes_vo(self):
        """Trae las solicitudes pendientes formateadas como diccionarios limpios para la vista"""
        cursor = self.conexion.cursor()
        sql = "SELECT SolicitudID, Concepto, Cantidad, Solicitante, Estado FROM SolicitudesMateriales WHERE Estado = 'Pendiente'"
        lista_resultados = []
        try:
            cursor.execute(sql)
            for fila in cursor.fetchall():
                lista_resultados.append({
                    "id": fila[0],
                    "concepto": str(fila[1]) if fila[1] else "Sin Concepto",
                    "cantidad": int(fila[2]) if fila[2] is not None else 0,
                    "solicitante": str(fila[3]) if fila[3] else "Anónimo",
                    "estado": str(fila[4]).strip() if fila[4] else "Pendiente"
                })
            return lista_resultados
        except Exception as e:
            print(f"Error en SolicitudDAO.obtener_solicitudes_pendientes_vo: {e}")
            return []
        finally:
            cursor.close()

    def cambiar_estado_solicitud(self, solicitud_id, nuevo_estado):
        """Acepta o rechaza una solicitud cambiando su estado"""
        cursor = self.conexion.cursor()
        sql = "UPDATE SolicitudesMateriales SET Estado = ? WHERE SolicitudID = ?"
        try:
            cursor.execute(sql, [str(nuevo_estado), int(solicitud_id)])
            self.conexion.commit()
            return True
        except Exception as e:
            print(f"Error en SolicitudDAO.cambiar_estado_solicitud: {e}")
            return False
        finally:
            cursor.close()