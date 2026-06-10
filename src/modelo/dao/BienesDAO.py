# archivo: DAO/BienesDAO.py
from  modelo.vo.BienVO import BienVO

class BienesDAO:
    def __init__(self, conexion_db):
        self.conexion = conexion_db

    def crear(self, bien: BienVO):
        """INSERT: Guarda un nuevo bien inventariado en la base de datos"""
        cursor = self.conexion.cursor()
        sql = "INSERT INTO Bienes (tipo, precio, cantidad) VALUES (?, ?, ?)"
        try:
            cursor.execute(sql, [
                bien.tipo,
                bien.precio,
                bien.cantidad
            ])
            self.conexion.commit()
            return True
        except Exception as e:
            print(f"Error al crear bien en inventario: {e}")
            return False
        finally:
            cursor.close()

    def obtener_todos(self):
        """SELECT ALL: Devuelve una lista con todos los bienes básicos como objetos VO"""
        lista_bienes = []
        cursor = self.conexion.cursor()
        sql = "SELECT BienID, tipo, precio, cantidad FROM Bienes"
        try:
            cursor.execute(sql)
            filas = cursor.fetchall()
            for fila in filas:
                vo = BienVO(BienID=fila[0], tipo=fila[1], precio=fila[2], cantidad=fila[3])
                lista_bienes.append(vo)
        except Exception as e:
            print(f"Error al obtener catálogo de bienes: {e}")
        finally:
            cursor.close()
        return lista_bienes

    def buscar_por_id(self, bien_id):
        """SELECT BY ID: Busca un bien detallado incluyendo qué tesoreros lo organizan (usando STRING_AGG)"""
        cursor = self.conexion.cursor()
        sql = """
            SELECT b.BienID, b.tipo, b.precio, b.cantidad,
                   (SELECT STRING_AGG(CAST(m.Name + ' ' + m.Surname AS VARCHAR(MAX)), ', ') 
                    FROM Organiza_Bien ob
                    INNER JOIN Miembros m ON ob.TesoreroID = m.UsuarioID
                    WHERE ob.BienID = b.BienID) AS TesorerosAsignados
            FROM Bienes b
            WHERE b.BienID = ?
        """
        try:
            cursor.execute(sql, [bien_id])
            fila = cursor.fetchone()
            if fila:
                bien = BienVO(
                    BienID=fila[0],
                    tipo=str(fila[1]).strip() if fila[1] else "",
                    precio=fila[2],
                    cantidad=fila[3]
                )
                bien.tesoreros_asignados = str(fila[4]).strip() if fila[4] else "Ninguno"
                return bien
            return None
        except Exception as e:
            print(f"Error en BienesDAO.buscar_por_id: {e}")
            return None
        finally:
            cursor.close()

    def actualizar_bien(self, bien_id, tipo, precio, cantidad):
        """UPDATE: Modifica los atributos raíz de un bien específico"""
        cursor = self.conexion.cursor()
        sql = """
            UPDATE Bienes 
            SET tipo = ?, precio = ?, cantidad = ?
            WHERE BienID = ?
        """
        try:
            cursor.execute(sql, [tipo, precio, cantidad, bien_id])
            self.conexion.commit()
            return cursor.rowcount > 0
        except Exception as e:
            print(f"Error en BienesDAO.actualizar_bien: {e}")
            return False
        finally:
            cursor.close()

    def eliminar_bien(self, bien_id):
        """DELETE: Elimina permanentemente el bien (Limpia primero la tabla intermedia Organiza_Bien)"""
        cursor = self.conexion.cursor()
        try:
            # Corrección preventiva: Al no tener ON DELETE CASCADE en el script SQL de Organiza_Bien,
            # limpiamos manualmente la relación intermedia para evitar violación de llaves foráneas.
            cursor.execute("DELETE FROM Organiza_Bien WHERE BienID = ?", [bien_id])
            
            # Eliminamos el registro de la tabla maestra
            cursor.execute("DELETE FROM Bienes WHERE BienID = ?", [bien_id])
            self.conexion.commit()
            return True
        except Exception as e:
            print(f"Error en BienesDAO.eliminar_bien: {e}")
            return False
        finally:
            cursor.close()

    def obtener_bienes_para_gestion(self):
        """Mapeador para UI: Devuelve un diccionario formateado para llenar el QTableWidget de la vista"""
        cursor = self.conexion.cursor()
        lista_resultados = []
        sql = "SELECT BienID, tipo, precio, cantidad FROM Bienes ORDER BY BienID ASC"
        try:
            cursor.execute(sql)
            filas = cursor.fetchall()
            for fila in filas:
                lista_resultados.append({
                    "id": fila[0],
                    "tipo": str(fila[1]).strip(),
                    "precio": f"{fila[2]:.2f} €",
                    "cantidad": fila[3]
                })
            return lista_resultados
        except Exception as e:
            print(f"Error en BienesDAO.obtener_bienes_para_gestion: {e}")
            return []
        finally:
            cursor.close()

    # =================================================================
    # GESTIÓN DE RELACIONES ASOCIADAS (CON TESOREROS)
    # =================================================================
    
    def limpiar_tesoreros_bien(self, bien_id):
        """Elimina todos los tesoreros vinculados a la organización de este bien"""
        cursor = self.conexion.cursor()
        try:
            cursor.execute("DELETE FROM Organiza_Bien WHERE BienID = ?", [bien_id])
            self.conexion.commit()
        except Exception as e:
            print(f"Error al limpiar tesoreros del bien: {e}")
        finally:
            cursor.close()

    def vincular_a_tesorero(self, bien_id, tesorero_id):
        """Asocia un tesorero específico a la administración/organización de este bien"""
        cursor = self.conexion.cursor()
        sql = "INSERT INTO Organiza_Bien (TesoreroID, BienID) VALUES (?, ?)"
        try:
            cursor.execute(sql, [tesorero_id, bien_id])
            self.conexion.commit()
            return True
        except Exception as e:
            print(f"Error al vincular bien {bien_id} al tesorero {tesorero_id}: {e}")
            return False
        finally:
            cursor.close()