class GrupoController:
    def __init__(self, grupo_dao):
        """Recibe el GrupoDAO para poder interactuar con los datos de los grupos"""
        self.grupo_dao = grupo_dao

    def obtener_grupos_usuario(self, usuario_id, rol):
        
        return self.grupo_dao.obtener_grupos_segun_rol(usuario_id, rol)