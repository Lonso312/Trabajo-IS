# archivo: miembro_dao.py
from VO.MiembroVO import MiembroVO

class MiembroDAO:
    def __init__(self, conexion_db):
        self.conexion = conexion_db

    def crear(self, miembro: MiembroVO):
        """INSERT: Guarda un nuevo miembro en la base de datos"""
        cursor = self.conexion.cursor()
        sql = "INSERT INTO Miembros (Name, Surname, Rol, DNI, NombreUsuario, Aceptado, Telefono, Email) VALUES (?, ?, ?, ?, ?, ?, ?, ?)"
        try:
            
            cursor.execute(sql, [
                miembro.Name,           
                miembro.Surname,        
                miembro.Rol,            
                miembro.DNI,            
                miembro.NombreUsuario,  
                miembro.Aceptado,       
                miembro.Telefono,       
                miembro.Email           
            ])
            return True
        except Exception as e:
            print(f"Error al crear miembro: {e}")
            return False
        finally:
            cursor.close()

    def obtener_todos(self):
        """SELECT ALL: Devuelve una lista con todos los miembros como objetos VO"""
        lista_miembros = []
        cursor = self.conexion.cursor()
        sql = "SELECT UsuarioID, Name, Email, DNI FROM miembros"
        try:
            cursor.execute(sql)
            filas = cursor.fetchall()
            for fila in filas:
                # Convertimos la fila de la BD a un objeto MiembroVO (El orden coincide con el SELECT: 0, 1, 2, 3)
                vo = MiembroVO(UsuarioID=fila[0], Name=fila[1], Email=fila[2], DNI=fila[3])
                lista_miembros.append(vo)
        except Exception as e:
            print(f"Error al obtener miembros: {e}")
        finally:
            cursor.close()
        return lista_miembros

    def buscar_por_id(self, UsuarioID):
        """SELECT BY ID: Busca un miembro específico por su llave primaria"""
        cursor = self.conexion.cursor()
        
        sql = "SELECT UsuarioID, Name, Surname, DNI, Email, NombreUsuario, Rol, Aceptado, Telefono FROM Miembros WHERE UsuarioID = ?"
        try:
            cursor.execute(sql, [UsuarioID])
            fila = cursor.fetchone()
            if fila:
                return MiembroVO(
                    UsuarioID=fila[0], 
                    Name=str(fila[1]) if fila[1] else None, 
                    Surname=str(fila[2]) if fila[2] else None, 
                    DNI=str(fila[3]) if fila[3] else None, 
                    Email=str(fila[4]) if fila[4] else None, 
                    NombreUsuario=str(fila[5]) if fila[5] else None, 
                    Rol=str(fila[6]) if fila[6] else None,  
                    Aceptado=fila[7], 
                    Telefono=fila[8]
                )
            return None
        except Exception as e:
            print(f"Error al buscar miembro {UsuarioID}: {e}")
            return None
        finally:
            cursor.close()

    def actualizar(self, miembro: MiembroVO):
        """UPDATE: Modifica los datos de un miembro existente"""
        cursor = self.conexion.cursor()
        
        sql = "UPDATE miembros SET Name = ?, Surname = ?, Rol = ?, DNI = ?, NombreUsuario = ?, Aceptado = ?, Telefono = ?, Email = ? WHERE UsuarioID = ?"
        try:
            
            cursor.execute(sql, [
                miembro.Name,
                miembro.Surname,
                miembro.Rol,
                miembro.DNI,
                miembro.NombreUsuario,
                miembro.Aceptado,
                miembro.Telefono,
                miembro.Email,
                miembro.UsuarioID  
            ])
            return True
        except Exception as e:
            print(f"Error al actualizar miembro: {e}")
            return False
        finally:
            cursor.close()

    def eliminar(self, UsuarioID):
        """DELETE: Borra un miembro por su ID"""
        cursor = self.conexion.cursor()
        sql = "DELETE FROM miembros WHERE UsuarioID = ?"
        try:
            cursor.execute(sql, [UsuarioID])
            return True
        except Exception as e:
            print(f"Error al eliminar miembro: {e}")
            return False
        finally:
            cursor.close()

    def autenticar(self, usuario, contrasena):
        """Valida las credenciales en LoginUsuario y devuelve (True, MiembroVO) o (False, "Mensaje de error")"""
        cursor = self.conexion.cursor()
        sql_login = "SELECT NombreUsuario, Contrasena FROM LoginUsuario WHERE NombreUsuario = ?"
        try:
            cursor.execute(sql_login, [usuario])
            resultado = cursor.fetchone()
            
            if not resultado:
                return False, "El usuario ingresado no existe."
                
            password_db = str(resultado[1]).strip() if resultado[1] else ""
            if password_db != contrasena:
                return False, "Contraseña incorrecta."
                
            sql_miembro = "SELECT UsuarioID FROM Miembros WHERE NombreUsuario = ?"
            cursor.execute(sql_miembro, [usuario])
            fila = cursor.fetchone()
            
            if not fila:
                return False, "El usuario de login existe, pero no está asignado a ningún Miembro."
                
            id_miembro = fila[0]
            miembro_logueado = self.buscar_por_id(id_miembro)
            
            if miembro_logueado:
                return True, miembro_logueado
            else:
                return False, "Error al construir el perfil del miembro."
        except Exception as e:
            print(f"Error en MiembroDAO.autenticar: {e}")
            return False, "Ocurrió un error interno al conectar con el servidor."
        finally:
            cursor.close()

    def obtener_miembros_para_gestion(self, departamento=None):
        """Trae los miembros de la BD adaptado al esquema real de SGA_Database"""
        cursor = self.conexion.cursor()
        lista_resultados = []
        
        try:
            if not departamento or departamento == "Todos":
                sql = """
                    SELECT UsuarioID, [Name], Surname, Rol, Email 
                    FROM Miembros
                """
                cursor.execute(sql)
                
            else:
                sql = """
                    SELECT m.UsuarioID, m.[Name], m.Surname, m.Rol, m.Email
                    FROM Miembros m
                    INNER JOIN EstaEnDepartamento ed ON m.UsuarioID = ed.UsuarioID
                    INNER JOIN Departamentos d ON ed.DepartamentoID = d.Num_Dep
                    WHERE d.tipo = ?
                """
                cursor.execute(sql, [departamento])
                
            filas = cursor.fetchall()

            for fila in filas:
                nombre = str(fila[1]).strip()
                apellido = str(fila[2]).strip()
                
                lista_resultados.append({
                    "id": fila[0],
                    "nombre_completo": f"{nombre} {apellido}",
                    "rol": str(fila[3]).strip(),
                    "email": str(fila[4]).strip()
                })
                
            return lista_resultados

        except Exception as e:
            print(f"Error en MiembroDAO.obtener_miembros_para_gestion: {e}")
            return []
        finally:
            cursor.close()