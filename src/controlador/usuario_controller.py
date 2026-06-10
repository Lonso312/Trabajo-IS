# controlador/usuario_controller.py

class UsuarioController:
    def __init__(self, usuario_service):
        self.service = usuario_service  # ← solo habla con el servicio
        self.vista_gestion = None
        self.usuario_logueado = None

    def login(self, nombre_usuario, password):
        """Devuelve el miembro si las credenciales son correctas, None si no"""
        return self.service.validar_login(nombre_usuario, password)

    def abrir_pantalla_gestion(self):
        from vistas.gestion_miembros_view import GestionMiembrosView
        self.vista_gestion = GestionMiembrosView(
            callback_filtrar=self.filtrar_miembros,
            callback_seleccionar_miembro=self.cargar_detalle_miembro,
            callback_aceptar=self.procesar_aceptar_miembro,
            callback_eliminar=self.procesar_eliminar_miembro,
            callback_actualizar=self.procesar_actualizar_miembro,
            controller=self
        )
        miembros = self.service.obtener_todos_los_miembros()
        self.vista_gestion.llenar_tabla_miembros(miembros)

        departamentos, _ = self.service.obtener_catalogos_edicion()
        self.vista_gestion.llenar_combo_departamentos(departamentos)
        self.vista_gestion.show()

    def filtrar_miembros(self, tipo_departamento):
        miembros = self.service.obtener_todos_los_miembros(tipo_departamento)
        self.vista_gestion.llenar_tabla_miembros(miembros)

    def cargar_detalle_miembro(self, usuario_id):
        miembro = self.service.obtener_detalle_miembro(usuario_id)
        if miembro:
            self.vista_gestion.mostrar_panel_derecho(miembro)
        else:
            self.vista_gestion.mostrar_mensaje_error("No se pudo cargar la información del miembro.")

    def obtener_listados_para_edicion(self):
        return self.service.obtener_catalogos_edicion()

    def procesar_aceptar_miembro(self, usuario_id):
        if self.service.aceptar_miembro(usuario_id):
            self.vista_gestion.mostrar_mensaje_exito("Miembro aceptado correctamente.")
            self._refrescar_tabla()
            self.cargar_detalle_miembro(usuario_id)
        else:
            self.vista_gestion.mostrar_mensaje_error("No se pudo cambiar el estado del miembro.")

    def procesar_eliminar_miembro(self, usuario_id):
        if self.service.eliminar_miembro(usuario_id):
            self.vista_gestion.mostrar_mensaje_exito("Miembro eliminado correctamente.")
            self._refrescar_tabla()
            self.vista_gestion.limpiar_detalle()
        else:
            self.vista_gestion.mostrar_mensaje_error("Error al intentar eliminar el registro.")

    def procesar_actualizar_miembro(self, usuario_id, dni, nombre, apellido, telefono, email, rol, lista_deptos, lista_grupos):
        if self.service.actualizar_miembro(usuario_id, dni, nombre, apellido, telefono, email, rol, lista_deptos, lista_grupos):
            self.vista_gestion.mostrar_mensaje_exito("Miembro actualizado correctamente.")
            self._refrescar_tabla()
            self.cargar_detalle_miembro(usuario_id)
        else:
            self.vista_gestion.mostrar_mensaje_error("No se pudieron guardar los cambios.")

    def procesar_agregar_miembro(self, rol_operador, datos):
        return self.service.agregar_miembro(rol_operador, datos)

    def _refrescar_tabla(self):
        if self.vista_gestion:
            filtro = self.vista_gestion.obtener_filtro_actual()
            self.filtrar_miembros(filtro)