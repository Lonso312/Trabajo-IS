from VO.grupo_vo import GrupoVO

class GrupoDAO:
    def __init__(self, conexion):
        self.conexion = conexion

    def obtener_grupos_por_miembro(self, usuario_id):
        """Trae los grupos a los que pertenece el miembro usando la tabla EstaEnGrupo"""
        cursor = self.conexion.cursor()
        sql = """
            SELECT g.GrupoID, g.Name, g.Num_miembros
            FROM Grupos g
            INNER JOIN EstaEnGrupo eg ON g.GrupoID = eg.GrupoID
            WHERE eg.UsuarioID = ?
        """
        lista_grupos = []
        try:
            cursor.execute(sql, [usuario_id])
            filas = cursor.fetchall()
            
            for fila in filas:
                grupo = GrupoVO(
                    GrupoID=fila[0],
                    Name=str(fila[1]) if fila[1] else "Sin Nombre",
                    CantidadMiembros=fila[2] if fila[2] else 0
                )
                lista_grupos.append(grupo)
                
            return lista_grupos
        except Exception as e:
            print(f"Error en GrupoDAO.obtener_grupos_por_miembro: {e}")
            return []
        finally:
            cursor.close()

    def obtener_grupos_segun_rol(self, usuario_id, rol_usuario):
        """Trae los grupos formateados según el rol del usuario (Si es PRESIDENTE ve todo)"""
        cursor = self.conexion.cursor()
        rol = str(rol_usuario).strip().upper() if rol_usuario else "MIEMBRO"
        
        try:
            if rol == 'PRESIDENTE':
                sql = "SELECT GrupoID, Name, Num_miembros FROM Grupos"
                cursor.execute(sql)
            else:
                sql = """
                    SELECT g.GrupoID, g.Name, g.Num_miembros
                    FROM Grupos g
                    INNER JOIN EstaEnGrupo eg ON g.GrupoID = eg.GrupoID
                    WHERE eg.UsuarioID = ?
                """
                cursor.execute(sql, [usuario_id])
                
            filas = cursor.fetchall()
            
            lista_formateada = []
            for fila in filas:
                lista_formateada.append({
                    "id": fila[0],
                    "nombre": fila[1],  
                    "cantidad_miembros": str(fila[2]) if fila[2] else "0",
                })
            return lista_formateada
        except Exception as e:
            print(f"Error en GrupoDAO.obtener_grupos_segun_rol: {e}")
            return []
        finally:
            cursor.close()

    def crear_grupo(self, nombre_grupo):
        """Inserta un nuevo grupo en la tabla Grupos"""
        cursor = self.conexion.cursor()
        sql = "INSERT INTO Grupos (Name, Num_miembros) VALUES (?, 0)"
        try:
            cursor.execute(sql, [str(nombre_grupo).strip()])
            self.conexion.commit()
            return True
        except Exception as e:
            print(f"Error en GrupoDAO.crear_grupo: {e}")
            return False
        finally:
            cursor.close()