# archivo: DAO/SolicitudDAO.py

class SolicitudDAO:
    def __init__(self, conexion_db):
        self.conexion = conexion_db

    def registrar_solicitud(self, concepto, cantidad, solicitante):
        """Registra una nueva petición de materiales con estado Pendiente"""
        cursor = self.conexion.cursor()
        sql = """
            INSERT INTO SolicitudesMateriales (Concepto, Cantidad, Solicitante, Estado)
            VALUES (?, ?, ?, 'Pendiente')
        """
        try:
            cursor.execute(sql, [str(concepto).strip(), int(cantidad), str(solicitante).strip()])
            self.conexion.commit()
            return True
        except Exception as e:
            print(f"Error en SolicitudDAO.registrar_solicitud: {e}")
            return False
        finally:
            cursor.close()

    def obtener_solicitudes_pendientes(self):
        """Trae todas las solicitudes que esperan aprobación del Tesorero"""
        cursor = self.conexion.cursor()
        sql = "SELECT SolicitudID, Concepto, Cantidad, Solicitante, Estado FROM SolicitudesMateriales WHERE Estado = 'Pendiente'"
        lista = []
        try:
            cursor.execute(sql)
            for fila in cursor.fetchall():
                lista.append({
                    "id": fila[0],
                    "concepto": fila[1],
                    "cantidad": fila[2],
                    "solicitante": fila[3],
                    "estado": fila[4]
                })
            return lista
        except Exception as e:
            print(f"Error en SolicitudDAO.obtener_solicitudes_pendientes: {e}")
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