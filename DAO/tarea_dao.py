# archivo: dao/tarea_dao.py
from VO.tarea_vo import TareaVO

class TareaDAO:
    def __init__(self, conexion):
        self.conexion = conexion

    def obtener_tareas_por_grupo(self, grupo_id):
        """Trae las tareas/alertas asociadas a un GrupoID mediante la tabla TieneTarea"""
        cursor = self.conexion.cursor()
        
        sql = """
            SELECT t.Name, t.Descripcion, t.Fecha_limite 
            FROM Tareas t
            INNER JOIN TieneTarea tt ON t.Name = tt.TareaID
            WHERE tt.GrupoID = ?
        """
        lista_tareas = []
        try:
            cursor.execute(sql, [grupo_id])
            filas = cursor.fetchall()
            
            for fila in filas:
                fecha_raw = fila[2]
                if fecha_raw:
                    fecha_texto = fecha_raw.strftime('%Y-%m-%d') if hasattr(fecha_raw, 'strftime') else str(fecha_raw)
                else:
                    fecha_texto = "Sin fecha"

                tarea = TareaVO(
                    TareaID=None, 
                    GrupoID=grupo_id,
                    Titulo=str(fila[0]).strip() if fila[0] else "Tarea sin título",
                    Descripcion=str(fila[1]).strip() if fila[1] else "Sin descripción",
                    FechaLimite=fecha_texto
                )
                lista_tareas.append(tarea)
                
            return lista_tareas
        except Exception as e:
            print(f"Error en TareaDAO.obtener_tareas_por_grupo: {e}")
            return []
        finally:
            cursor.close()


    def obtener_tareas_formateadas(self, id_grupo):
        """Trae las tareas de un grupo estructuradas para el panel visual"""
        cursor = self.conexion.cursor()
        sql = """
            SELECT LTRIM(RTRIM(t.Name)), LTRIM(RTRIM(t.Descripcion)), t.Fecha_limite 
            FROM Tareas t
            INNER JOIN TieneTarea tt ON LTRIM(RTRIM(t.Name)) = LTRIM(RTRIM(tt.TareaID))
            WHERE tt.GrupoID = ?
        """
        lista_tareas = []
        try:
            cursor.execute(sql, [id_grupo])
            filas = cursor.fetchall()
            for fila in filas:
                fecha_raw = fila[2]
                if fecha_raw:
                    fecha = fecha_raw.strftime('%d-%m-%Y') if hasattr(fecha_raw, 'strftime') else str(fecha_raw).split()[0]
                else:
                    fecha = "XX-XX-XXXX"

                lista_tareas.append({
                    "tipo_tarjeta": "TAREA",
                    "titulo": f"Tarea: {str(fila[0]).strip()}",
                    "info_derecha": f"Límite: {fecha}",
                    "descripcion": f"Desc: {str(fila[1]).strip()}" if fila[1] else "Sin descripción"
                })
            return lista_tareas
        except Exception as e:
            print(f"Error en TareaDAO.obtener_tareas_formateadas: {e}")
            return []
        finally:
            cursor.close()

    def obtener_sesiones_formateadas(self, id_grupo):
        """Trae las sesiones de trabajo de un grupo estructuradas para el panel visual"""
        cursor = self.conexion.cursor()
        sql = """
            SELECT s.Name, s.Ubicacion, ts.AsistenciaObligatoria
            FROM Sesiones s
            INNER JOIN TieneSesion ts ON s.Name LIKE '%' + ts.SesionID + '%'
            WHERE ts.GrupoID = ?
        """
        lista_sesiones = []
        try:
            cursor.execute(sql, [id_grupo])
            filas = cursor.fetchall()
            for fila in filas:
                lista_sesiones.append({
                    "tipo_tarjeta": "SESION",
                    "titulo": f"Sesión de trabajo: {str(fila[0]).strip()}",
                    "info_derecha": "Obligatoria" if fila[2] == 1 else "Opcional",
                    "descripcion": f"Aula / Ubicación: {str(fila[1]).strip()}"
                })
            return lista_sesiones
        except Exception as e:
            print(f"Error en TareaDAO.obtener_sesiones_formateadas: {e}")
            return []
        finally:
            cursor.close()