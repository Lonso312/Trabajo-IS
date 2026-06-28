class TareaController:
    def __init__(self, tarea_service):
        self.service = tarea_service

    def obtener_tareas_y_sesiones(self, id_grupo):
        try:
            return self.service.obtener_tareas_y_sesiones(id_grupo)
        except Exception as e:
            print(f"[TareaController] Error obteniendo tareas del grupo {id_grupo}: {e}")
            return []

    def procesar_crear_tarea(self, rol_usuario, grupo_id, titulo, descripcion, fecha_limite):
        """
        Bug 3 fix: captura errores del servicio y devuelve (False, msg)
        en lugar de propagar la excepción a la vista.
        """
        try:
            return self.service.crear_tarea(rol_usuario, grupo_id, titulo, descripcion, fecha_limite)
        except ValueError as e:
            return False, f"Dato inválido: {str(e)}"
        except Exception as e:
            print(f"[TareaController] Error creando tarea en grupo {grupo_id}: {e}")
            return False, f"Error al crear la tarea: {str(e)}"