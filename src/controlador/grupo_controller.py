class GrupoController:
    def __init__(self, grupo_service):
        self.service = grupo_service
        self.menu_view = None

    def obtener_grupos_usuario(self, usuario_id, rol):
        return self.service.obtener_grupos_usuario(usuario_id, rol)

    def procesar_crear_grupo(self, rol_usuario, nombre_grupo, usuario_id):
        return self.service.crear_grupo(rol_usuario, nombre_grupo, usuario_id)