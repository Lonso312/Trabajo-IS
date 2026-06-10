class TareaController:
    def __init__(self, tarea_service):
        self.service = tarea_service

    def obtener_tareas_y_sesiones(self, id_grupo):
        return self.service.obtener_tareas_y_sesiones(id_grupo)

    def procesar_crear_tarea(self, rol_usuario, grupo_id, titulo, descripcion, fecha_limite):
        return self.service.crear_tarea(rol_usuario, grupo_id, titulo, descripcion, fecha_limite)