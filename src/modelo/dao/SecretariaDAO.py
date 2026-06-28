# archivo: DAO/SecretariaDAO.py
from modelo.vo.reunion_vo import ReunionSecretariaVO

class SecretariaDAO:
    def __init__(self, conexion_db):
        self.conexion = conexion_db

    def obtener_reuniones_secretaria(self):
        """Trae todas las reuniones registradas devolviendo una lista de objetos VO"""
        cursor = self.conexion.cursor()
        sql = "SELECT ReunionID, Titulo, fecha, Hora, Lugar, Estado FROM Reuniones ORDER BY fecha DESC"
        lista_vo = []
        try:
            cursor.execute(sql)
            for fila in cursor.fetchall():
                # Utilizamos el método estático del VO para mapear la fila limpiamente
                reunion_vo = ReunionSecretariaVO.from_fila_db(fila)
                lista_vo.append(reunion_vo)
            return lista_vo
        except Exception as e:
            print(f"Error en SecretariaDAO.obtener_reuniones_secretaria: {e}")
            return []
        finally:
            cursor.close()

    def registrar_reunion(self, reunion_vo: ReunionSecretariaVO):
        """Permite al Secretario agendar una nueva reunión recibiendo un objeto VO"""
        cursor = self.conexion.cursor()
        sql = "INSERT INTO Reuniones (Titulo, fecha, Hora, Lugar, Estado, tipo) VALUES (?, ?, ?, ?, ?, ?)"
        try:
            cursor.execute(sql, [
                reunion_vo.titulo, 
                reunion_vo.fecha, 
                reunion_vo.hora, 
                reunion_vo.lugar,
                reunion_vo.estado,
                reunion_vo.titulo  # 'tipo' es NOT NULL en el esquema; reutilizamos el título
            ])
            self.conexion.commit()
            return True
        except Exception as e:
            print(f"Error en SecretariaDAO.registrar_reunion: {e}")
            return False
        finally:
            cursor.close()

    def actualizar_estado_reunion(self, reunion_id, nuevo_estado):
        """Modifica el estado de la reunión"""
        cursor = self.conexion.cursor()
        sql = "UPDATE Reuniones SET Estado = ? WHERE ReunionID = ?"
        try:
            cursor.execute(sql, [str(nuevo_estado), int(reunion_id)])
            self.conexion.commit()
            return True
        except Exception as e:
            print(f"Error en SecretariaDAO.actualizar_estado_reunion: {e}")
            return False
        finally:
            cursor.close()