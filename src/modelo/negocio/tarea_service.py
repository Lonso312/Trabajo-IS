class TareaService:
    def __init__(self, tarea_dao):
        self.tarea_dao = tarea_dao

    def obtener_tareas_y_sesiones(self, id_grupo):
        tareas = self.tarea_dao.obtener_tareas_formateadas(id_grupo)
        sesiones = self.tarea_dao.obtener_sesiones_formateadas(id_grupo)
        return tareas + sesiones

    def crear_tarea(self, rol_usuario, grupo_id, titulo, descripcion, fecha_limite):
        rol = str(rol_usuario).strip().upper()
        if rol not in ["PRESIDENTE", "JEFE DEPARTAMENTO"]:
            return False, "No tienes permisos de administrador para asignar tareas."
        if not titulo:
            return False, "El título de la tarea es obligatorio."
        exito = self.tarea_dao.crear_tarea_en_grupo(grupo_id, titulo, descripcion, fecha_limite)
        if exito:
            return True, f"Tarea '{titulo}' asignada correctamente al grupo."
        return False, "Ocurrió un error en la base de datos al guardar la tarea."