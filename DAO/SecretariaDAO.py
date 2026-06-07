# archivo: DAO/SecretariaDAO.py

class SecretariaDAO:
    def __init__(self, conexion_db):
        self.conexion = conexion_db

    def obtener_reuniones_secretaria(self):
        """Trae todas las reuniones registradas en el sistema"""
        cursor = self.conexion.cursor()
        sql = "SELECT ReunionID, Titulo, Fecha, Hora, Lugar, Estado FROM SecretariaReuniones ORDER BY Fecha DESC"
        lista = []
        try:
            cursor.execute(sql)
            for fila in cursor.fetchall():
                lista.append({
                    "id": fila[0],
                    "titulo": str(fila[1]).strip(),
                    "fecha": str(fila[2]),
                    "hora": str(fila[3]).strip(),
                    "lugar": str(fila[4]).strip(),
                    "estado": str(fila[5]).strip()
                })
            return lista
        except Exception as e:
            print(f"Error en SecretariaDAO.obtener_reuniones_secretaria: {e}")
            return []
        finally:
            cursor.close()

    def registrar_reunion(self, titulo, fecha, hora, lugar):
        """Permite al Secretario agendar una nueva reunión"""
        cursor = self.conexion.cursor()
        sql = "INSERT INTO SecretariaReuniones (Titulo, Fecha, Hora, Lugar, Estado) VALUES (?, ?, ?, ?, 'Programada')"
        try:
            cursor.execute(sql, [str(titulo).strip(), str(fecha), str(hora).strip(), str(lugar).strip()])
            self.conexion.commit()
            return True
        except Exception as e:
            print(f"Error en SecretariaDAO.registrar_reunion: {e}")
            return False
        finally:
            cursor.close()

    def actualizar_estado_reunion(self, reunion_id, nuevo_estado):
        """Modifica el estado de la reunión (ej: 'Celebrada' o 'Cancelada')"""
        cursor = self.conexion.cursor()
        sql = "UPDATE SecretariaReuniones SET Estado = ? WHERE ReunionID = ?"
        try:
            cursor.execute(sql, [str(nuevo_estado), int(reunion_id)])
            self.conexion.commit()
            return True
        except Exception as e:
            print(f"Error en SecretariaDAO.actualizar_estado_reunion: {e}")
            return False
        finally:
            cursor.close()