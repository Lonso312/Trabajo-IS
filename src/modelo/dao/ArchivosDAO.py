import jpype

class ArchivosDAO:
    def __init__(self, conexion_db):
        self.conexion = conexion_db

    def obtener_archivos_por_rol(self, rol_usuario):
        cursor = self.conexion.cursor()
        try:
            rol_limpio = str(rol_usuario).strip().upper()

            if rol_limpio == 'PRESIDENTE':
                sql = """
                    SELECT ArchivoID, Nombre, Tipo, RolPermitido, Num_download, Num_view
                    FROM dbo.Archivos
                """
                cursor.execute(sql)
            else:
                sql = """
                    SELECT ArchivoID, Nombre, Tipo, RolPermitido, Num_download, Num_view
                    FROM dbo.Archivos
                    WHERE UPPER(RolPermitido) = ? OR UPPER(RolPermitido) = 'TODOS'
                """
                cursor.execute(sql, [rol_limpio])

            filas = cursor.fetchall()
            return [
                {
                    "id": int(fila[0]) if fila[0] is not None else 0,
                    "nombre": str(fila[1]) if fila[1] is not None else "",
                    "tipo": str(fila[2]) if fila[2] is not None else "",
                    "rol_permitido": str(fila[3]) if fila[3] is not None else "",
                    "descargas": int(fila[4]) if fila[4] is not None else 0,
                    "vistas": int(fila[5]) if fila[5] is not None else 0,
                }
                for fila in filas
            ]
        except Exception as e:
            print(f"Error en ArchivosDAO.obtener_archivos_por_rol: {e}")
            return []
        finally:
            cursor.close()

    def obtener_contenido_archivo(self, archivo_id):
        """
        Recupera el nombre y los bytes puros del archivo.
        Devuelve exactamente una tupla de 2 elementos (nombre, datos) 
        para alinearse con lo que espera la capa de servicio.
        """
        cursor = self.conexion.cursor()
        try:
            sql = "SELECT Nombre, Contenido FROM dbo.Archivos WHERE ArchivoID = ?"
            cursor.execute(sql, [archivo_id])
            fila = cursor.fetchone()
            if not fila:
                return None, None # Retorna 2 valores vacíos si no existe

            nombre = fila[0]
            contenido_bruto = fila[1]
            
            # EXTRACCIÓN ULTRA-ROBUSTA DE BYTES
            if contenido_bruto is None:
                datos_finales = b""
            elif isinstance(contenido_bruto, bytes):
                datos_finales = contenido_bruto
            elif isinstance(contenido_bruto, str):
                # Si por algún motivo el driver lo transformó a cadena hexadecimal o texto
                if contenido_bruto.startswith('0x'):
                    datos_finales = bytes.fromhex(contenido_bruto[2:])
                else:
                    datos_finales = contenido_bruto.encode('latin1', errors='ignore')
            elif hasattr(contenido_bruto, 'getBytes'): # Si es un objeto Blob nativo de Java
                datos_finales = bytes(contenido_bruto.getBytes(1, contenido_bruto.length()))
            else:
                # Cualquier otro tipo de array de bytes (JArray, bytearray, etc.)
                datos_finales = bytes(contenido_bruto)

            # Incrementamos el contador de descargas
            cursor.execute(
                "UPDATE dbo.Archivos SET Num_download = Num_download + 1 WHERE ArchivoID = ?",
                [archivo_id]
            )
            self.conexion.commit()
            
            # SOLUCIÓN AL BUG: Devolvemos exactamente 2 valores (nombre, datos)
            return nombre, datos_finales
            
        except Exception as e:
            print(f"Error al recuperar binario del archivo en DAO: {e}")
            return None, None # En caso de error, también devolvemos 2 valores
        finally:
            cursor.close()
            
    def guardar_archivo(self, nombre, tipo, contenido_bytes, rol_permitido):
        try:
            # Detectamos si estamos usando una conexión Java (JayDeBeApi)
            if hasattr(self.conexion, 'jconn'):
                # SOLUCIÓN MAESTRA: Usamos PreparedStatement nativo de Java
                java_conn = self.conexion.jconn
                sql = """
                    INSERT INTO dbo.Archivos
                    (Nombre, Tipo, Contenido, RolPermitido, Num_download, Num_view)
                    VALUES (?, ?, ?, ?, 0, 0)
                """
                stmt = java_conn.prepareStatement(sql)
                stmt.setString(1, str(nombre).strip())
                stmt.setString(2, str(tipo).strip().upper())
                
                # Preparamos los bytes para Java
                bytes_firmados = [b if b < 128 else b - 256 for b in contenido_bytes]
                java_bytes = jpype.JArray(jpype.JByte)(bytes_firmados)
                
                # .setBytes() le dice a SQL Server explícitamente: "ESTO ES BINARIO"
                stmt.setBytes(3, java_bytes)
                stmt.setString(4, str(rol_permitido).strip().upper())
                
                stmt.executeUpdate()
                stmt.close()
            else:
                # Fallback si en el futuro cambias a pyodbc u otro driver
                cursor = self.conexion.cursor()
                sql = """
                    INSERT INTO dbo.Archivos
                    (Nombre, Tipo, Contenido, RolPermitido, Num_download, Num_view)
                    VALUES (?, ?, ?, ?, 0, 0)
                """
                cursor.execute(sql, [
                    str(nombre).strip(), str(tipo).strip().upper(),
                    bytearray(contenido_bytes), str(rol_permitido).strip().upper()
                ])
                cursor.close()
                
            self.conexion.commit()
            return True

        except Exception as e:
            print(f"Error crítico en DAO al guardar archivo: {e}")
            return False
