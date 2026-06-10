# archivo: miembro_dao.py
from modelo.vo.MiembroVO import MiembroVO

class MiembroDAO:
    def __init__(self, conexion_db):
        self.conexion = conexion_db

    def insertar_nuevo_miembro(self, dni, nombre, apellido, telefono, email, rol, depto_id, grupo_id, password="12345"):
        """
        Inserta un nuevo miembro en la base de datos de manera explícita.
        Dependiendo de tu esquema SQL, ajusta los nombres de las columnas.
        """
        cursor = self.conexion.cursor()
        sql = """
            INSERT INTO Miembro (DNI, Name, Surname, Telefono, Email, Rol, DeptoID, GrupoID, Contrasena)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """
        
        try:
            cursor.execute(sql, [
                str(dni).strip(),
                str(nombre).strip(),
                str(apellido).strip(),
                str(telefono).strip(),
                str(email).strip(),
                str(rol).strip(),
                int(depto_id) if depto_id is not None else None,
                int(grupo_id) if grupo_id is not None else None,
                str(password) 
            ])
            self.conexion.commit()
            return True
        except Exception as e:
            print(f"Error en MiembroDAO.insertar_nuevo_miembro: {e}")
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

    def buscar_por_id(self, usuario_id):
        cursor = self.conexion.cursor()
        
        sql = """
            SELECT m.UsuarioID, m.DNI, m.Name, m.NombreUsuario, m.Surname, m.Rol, m.Aceptado, m.Telefono, m.Email,
                   (SELECT STRING_AGG(CAST(d.tipo AS VARCHAR(MAX)), ', ') 
                    FROM EstaEnDepartamento ed 
                    INNER JOIN Departamentos d ON ed.DepartamentoID = d.Num_Dep 
                    WHERE ed.UsuarioID = m.UsuarioID) AS Departamentos,
                   (SELECT STRING_AGG(CAST(g.Name AS VARCHAR(MAX)), ', ') 
                    FROM EstaEnGrupo eg 
                    INNER JOIN Grupos g ON eg.GrupoID = g.GrupoID 
                    WHERE eg.UsuarioID = m.UsuarioID) AS Grupos
            FROM Miembros m
            WHERE m.UsuarioID = ?
        """
        try:
            cursor.execute(sql, [usuario_id])
            fila = cursor.fetchone()
            if fila:
                from modelo.vo.MiembroVO import MiembroVO
                
                miembro = MiembroVO(
                    UsuarioID=fila[0],
                    DNI=str(fila[1]).strip() if fila[1] else "",
                    Name=str(fila[2]).strip() if fila[2] else "",
                    NombreUsuario=str(fila[3]).strip() if fila[3] else "",
                    Surname=str(fila[4]).strip() if fila[4] else "",
                    Rol=str(fila[5]).strip() if fila[5] else "MIEMBRO",
                    Aceptado=fila[6],
                    Telefono=fila[7],
                    Email=str(fila[8]).strip() if fila[8] else ""
                )
                
                miembro.Departamento = str(fila[9]).strip() if fila[9] else "Ninguno"
                miembro.Grupo = str(fila[10]).strip() if fila[10] else "Ninguno"
                
                return miembro
            return None
        except Exception as e:
            print(f"Error en MiembroDAO.obtener_miembro_por_id: {e}")
            return None
        finally:
            cursor.close()

    def actualizar_miembro(self, usuario_id, dni, nombre, apellido, telefono, email, rol):
        """Actualiza estrictamente los datos de la tabla maestra Miembros (7 parámetros)"""
        cursor = self.conexion.cursor()
        sql = """
            UPDATE Miembros 
            SET DNI = ?, [Name] = ?, Surname = ?, Telefono = ?, Email = ?, Rol = ?
            WHERE UsuarioID = ?
        """
        try:
            cursor.execute(sql, [dni, nombre, apellido, telefono, email, rol, usuario_id])
            self.conexion.commit()
            return cursor.rowcount > 0
        except Exception as e:
            print(f"Error en MiembroDAO.actualizar_miembro: {e}")
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

    def aceptar_miembro(self, usuario_id):
        """Cambia el estado de un miembro pendiente a aceptado (Aceptado = 1)"""
        cursor = self.conexion.cursor()
        try:
            cursor.execute("UPDATE Miembros SET Aceptado = 1 WHERE UsuarioID = ?", [usuario_id])
            self.conexion.commit()
            return True
        except Exception as e:
            print(f"Error en MiembroDAO.aceptar_miembro: {e}")
            return False
        finally:
            cursor.close()

    def eliminar_miembro(self, usuario_id):
        """Elimina por completo a un miembro (las claves foráneas se encargan del CASCADE)"""
        cursor = self.conexion.cursor()
        try:
            cursor.execute("DELETE FROM Miembros WHERE UsuarioID = ?", [usuario_id])
            self.conexion.commit()
            return True
        except Exception as e:
            print(f"Error en MiembroDAO.eliminar_miembro: {e}")
            return False
        finally:
            cursor.close()

    def existe_vinculo_departamento(self, usuario_id, nombre_depto):
        cursor = self.conexion.cursor()
        sql = """
            SELECT 1 FROM EstaEnDepartamento ed
            INNER JOIN Departamentos d ON ed.DepartamentoID = d.Num_Dep
            WHERE ed.UsuarioID = ? AND d.tipo = ?
        """
        cursor.execute(sql, [usuario_id, nombre_depto])
        res = cursor.fetchone()
        cursor.close()
        return res is not None


    def existe_vinculo_grupo(self, usuario_id, nombre_grupo):
        cursor = self.conexion.cursor()
        sql = """
            SELECT 1 FROM EstaEnGrupo eg
            INNER JOIN Grupos g ON eg.GrupoID = g.GrupoID
            WHERE eg.UsuarioID = ? AND g.Name = ?
        """
        cursor.execute(sql, [usuario_id, nombre_grupo])
        res = cursor.fetchone()
        cursor.close()
        return res is not None

    def limpiar_departamentos_usuario(self, usuario_id):
        cursor = self.conexion.cursor()
        cursor.execute("DELETE FROM EstaEnDepartamento WHERE UsuarioID = ?", [usuario_id])
        self.conexion.commit()
        cursor.close()

    def limpiar_grupos_usuario(self, usuario_id):
        cursor = self.conexion.cursor()
        cursor.execute("DELETE FROM EstaEnGrupo WHERE UsuarioID = ?", [usuario_id])
        self.conexion.commit()
        cursor.close()

    def vincular_a_departamento(self, usuario_id, nombre_depto):
        cursor = self.conexion.cursor()
        sql = """
            INSERT INTO EstaEnDepartamento (UsuarioID, DepartamentoID, FechaVinculacion)
            SELECT ?, Num_Dep, GETDATE() FROM Departamentos WHERE tipo = ?
        """
        cursor.execute(sql, [usuario_id, nombre_depto])
        self.conexion.commit()
        cursor.close()

    def vincular_a_grupo(self, usuario_id, nombre_grupo):
        cursor = self.conexion.cursor()
        sql = """
            INSERT INTO EstaEnGrupo (UsuarioID, GrupoID, FechaIngreso)
            SELECT ?, GrupoID, GETDATE() FROM Grupos WHERE Name = ?
        """
        cursor.execute(sql, [usuario_id, nombre_grupo])
        self.conexion.commit()
        cursor.close()


    def insertar_miembro_completo(self, dni, nombre, apellido, telefono, email, rol, usuario_nombre, password="12345"):
        """
        Inserta un nuevo miembro respetando el esquema real:
        1. Inserta en la tabla maestra 'Miembros' y obtiene el ID autogenerado.
        2. Inserta las credenciales en la tabla 'LoginUsuario'.
        """
        cursor = self.conexion.cursor()
        
        # SQL 1: Inserción en la tabla maestra (Devolviendo el ID generado)
        sql_miembro = """
            INSERT INTO Miembros (DNI, [Name], NombreUsuario, Surname, Rol, Aceptado, Telefono, Email)
            OUTPUT INSERTED.UsuarioID
            VALUES (?, ?, ?, ?, ?, 0, ?, ?)
        """
        
        # SQL 2: Inserción de la contraseña en la tabla de login secundaria
        sql_login = """
            INSERT INTO LoginUsuario (NombreUsuario, Contrasena)
            VALUES (?, ?)
        """
        
        try:
            # 1. Registrar los datos personales en Miembros
            cursor.execute(sql_miembro, [
                str(dni).strip(),
                str(nombre).strip(),
                str(usuario_nombre).strip(),
                str(apellido).strip(),
                str(rol).strip(),
                int(telefono),
                str(email).strip()
            ])
            
            fila = cursor.fetchone()
            if not fila:
                return None
            
            usuario_id = fila[0] # Guardamos el ID único numérico generado
            
            # 2. Registrar las credenciales en LoginUsuario usando el mismo NombreUsuario
            cursor.execute(sql_login, [
                str(usuario_nombre).strip(),
                str(password)
            ])
            
            # Confirmamos ambas operaciones en la base de datos simultáneamente
            self.conexion.commit()
            return usuario_id
            
        except Exception as e:
            print(f"Error crítico en MiembroDAO.insertar_miembro_completo: {e}")
            try:
                self.conexion.rollback() # Cancelamos todo si algo falló
            except Exception:
                pass
            return None
        finally:
            cursor.close()

    def actualizar_contrasena(self, nombre_usuario, nueva_contrasena):
        cursor = self.conexion.cursor()
        sql = """
            UPDATE LoginUsuario 
            SET Contrasena = ? 
            WHERE NombreUsuario = ?
        """
        try:
            cursor.execute(sql, [str(nueva_contrasena).strip(), str(nombre_usuario).strip()])
            self.conexion.commit()
            return cursor.rowcount > 0
        except Exception as e:
            print(f"Error en MiembroDAO.actualizar_contrasena: {e}")
            try:
                self.conexion.rollback()
            except Exception:
                pass
            return False
        finally:
            cursor.close()