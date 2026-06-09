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
        cursor = self.conexion.cursor()
        try:
            sql = """
                SELECT Nombre, Contenido
                FROM dbo.Archivos
                WHERE ArchivoID = ?
            """
            cursor.execute(sql, [archivo_id])
            fila = cursor.fetchone()
            if not fila:
                return None, None

            cursor.execute(
                "UPDATE dbo.Archivos SET Num_download = Num_download + 1 WHERE ArchivoID = ?",
                [archivo_id]
            )
            self.conexion.commit()
            return fila[0], fila[1]
        except Exception as e:
            print(f"Error al recuperar binario del archivo: {e}")
            return None, None
        finally:
            cursor.close()

    def guardar_archivo(self, nombre, tipo, contenido_bytes, rol_permitido):
        """Inserta un archivo PDF binario directamente en la base de datos"""
        cursor = self.conexion.cursor()
        try:
            # Asegura que realmente sea bytes de Python
            contenido_binario = bytes(contenido_bytes)

            # Lo convierte a byte[] de Java para JDBC
            contenido_java = jpype.JArray(jpype.JByte)(contenido_binario)

            sql = """
                INSERT INTO dbo.Archivos
                (Nombre, Tipo, Contenido, RolPermitido, Num_download, Num_view)
                VALUES (?, ?, ?, ?, 0, 0)
            """
            cursor.execute(sql, [
                str(nombre).strip(),
                str(tipo).strip().upper(),
                contenido_java,
                str(rol_permitido).strip().upper()
            ])
            self.conexion.commit()
            return True

        except Exception as e:
            print(f"Error al insertar binario en la tabla Archivos: {e}")
            return False
        finally:
            cursor.close()