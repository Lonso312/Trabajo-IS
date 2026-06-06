class DepartamentoDAO:
    def __init__(self, conexion_db):
        self.conexion = conexion_db

    def obtener_todos_los_tipos(self):
        """SELECT: Devuelve una lista de strings con los nombres de los departamentos"""
        cursor = self.conexion.cursor()
        sql = "SELECT tipo FROM Departamentos ORDER BY tipo ASC"
        lista_departamentos = []
        try:
            cursor.execute(sql)
            filas = cursor.fetchall()
            for fila in filas:
                if fila[0]:
                    lista_departamentos.append(str(fila[0]).strip())
            return lista_departamentos
        except Exception as e:
            print(f"Error en DepartamentoDAO.obtener_todos_los_tipos: {e}")
            return []
        finally:
            cursor.close()