class TareaController:
    def __init__(self, tarea_dao):
        """El controlador recibe el DAO para poder pedirle datos"""
        self.tarea_dao = tarea_dao

    def obtener_tareas_y_sesiones(self, id_grupo):
        tareas = self.tarea_dao.obtener_tareas_formateadas(id_grupo)
        sesiones = self.tarea_dao.obtener_sesiones_formateadas(id_grupo)
        return tareas + sesiones