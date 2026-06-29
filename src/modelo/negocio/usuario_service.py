class UsuarioService:
    def __init__(self, miembro_dao, departamento_dao, grupo_dao):
        self.miembro_dao = miembro_dao
        self.departamento_dao = departamento_dao
        self.grupo_dao = grupo_dao

    def autenticar(self, usuario, contrasena):
        return self.miembro_dao.autenticar(usuario, contrasena)

    def obtener_todos_los_miembros(self, tipo_departamento=None):
        return self.miembro_dao.obtener_miembros_para_gestion(tipo_departamento)

    def obtener_detalle_miembro(self, usuario_id):
        return self.miembro_dao.buscar_por_id(usuario_id)

    def obtener_catalogos_edicion(self):
        departamentos = self.departamento_dao.obtener_todos_los_tipos()
        grupos = self.grupo_dao.obtener_nombres_grupos()
        return departamentos, grupos

    def aceptar_miembro(self, usuario_id):
        return self.miembro_dao.aceptar_miembro(usuario_id)

    def eliminar_miembro(self, usuario_id):
        return self.miembro_dao.eliminar_miembro(usuario_id)

    def actualizar_miembro(self, usuario_id, dni, nombre, apellido, telefono, email, rol, lista_deptos, lista_grupos):
        exito = self.miembro_dao.actualizar_miembro(usuario_id, dni, nombre, apellido, telefono, email, rol)
        if exito:
            self.miembro_dao.limpiar_departamentos_usuario(usuario_id)
            for depto in lista_deptos:
                self.miembro_dao.vincular_a_departamento(usuario_id, depto)
            self.miembro_dao.limpiar_grupos_usuario(usuario_id)
            for grupo in lista_grupos:
                self.miembro_dao.vincular_a_grupo(usuario_id, grupo)
        return exito

    def agregar_miembro(self, rol_operador, datos):
        rol_op = str(rol_operador).strip().upper()
        if rol_op not in ["PRESIDENTE", "JEFE DEPARTAMENTO"]:
            return False, "No tienes privilegios para registrar nuevos miembros."
        if not datos.get("dni") or not datos.get("nombre") or not datos.get("apellido"):
            return False, "El DNI, Nombre y Apellidos son campos obligatorios."

        primera_letra = datos['nombre'][0].lower() if datos['nombre'] else 'u'
        primer_apellido = datos['apellido'].split()[0].lower() if datos['apellido'] else 'usuario'
        nombre_usuario = f"{primera_letra}{primer_apellido}"

        usuario_id = self.miembro_dao.insertar_miembro_completo(
            dni=datos["dni"], nombre=datos["nombre"], apellido=datos["apellido"],
            telefono=datos["telefono"], email=datos["email"], rol=datos["rol"],
            usuario_nombre=nombre_usuario, password="12345"
        )
        if usuario_id:
            for depto in datos.get("departamentos_lista", []):
                self.miembro_dao.vincular_a_departamento(usuario_id, depto)
            for grupo in datos.get("grupos_lista", []):
                self.miembro_dao.vincular_a_grupo(usuario_id, grupo)
            return True, f"Miembro '{datos['nombre']} {datos['apellido']}' registrado con usuario '{nombre_usuario}'."
        return False, "No se pudo completar el registro. Verifique que el DNI no esté duplicado."