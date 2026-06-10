class GrupoService:
    def __init__(self, grupo_dao):
        self.grupo_dao = grupo_dao

    def obtener_grupos_usuario(self, usuario_id, rol):
        return self.grupo_dao.obtener_grupos_segun_rol(usuario_id, rol)

    def crear_grupo(self, rol_usuario, nombre_grupo, usuario_id):
        rol = str(rol_usuario).strip().upper()
        if rol not in ["PRESIDENTE", "JEFE DEPARTAMENTO"]:
            return False, "No tienes permisos de administración para crear grupos."
        if not nombre_grupo.strip():
            return False, "El nombre del grupo no puede estar vacío."
        exito = self.grupo_dao.crear_grupo(nombre_grupo)
        if exito:
            return True, "Grupo creado con éxito."
        return False, "Error al insertar el grupo (puede que ya exista)."