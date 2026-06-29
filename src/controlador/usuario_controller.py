class UsuarioController:
    def __init__(self, usuario_service):
        self.service = usuario_service
        self.vista_gestion = None       # inyectada desde fuera (menu_view o main)
        self.usuario_logueado = None


    def login(self, nombre_usuario, password):
        """Devuelve el miembro si las credenciales son correctas, None si no."""
        return self.service.validar_login(nombre_usuario, password)


    def abrir_pantalla_gestion(self):
        """
        Carga los datos iniciales en la vista de gestión de miembros.
        La vista ya debe haber sido inyectada en self.vista_gestion
        antes de llamar a este método (lo hace ControladorApp o menu_view).
        """
        if not self.vista_gestion:
            return

        miembros = self.service.obtener_todos_los_miembros()
        self.vista_gestion.llenar_tabla_miembros(miembros)

        departamentos, _ = self.service.obtener_catalogos_edicion()
        self.vista_gestion.llenar_combo_departamentos(departamentos)

        self.vista_gestion.show()


    def filtrar_miembros(self, tipo_departamento):
        miembros = self.service.obtener_todos_los_miembros(tipo_departamento)
        if self.vista_gestion:
            self.vista_gestion.llenar_tabla_miembros(miembros)


    def cargar_detalle_miembro(self, usuario_id):
        miembro = self.service.obtener_detalle_miembro(usuario_id)
        if not self.vista_gestion:
            return
        if miembro:
            self.vista_gestion.mostrar_panel_derecho(miembro)
        else:
            self.vista_gestion.mostrar_mensaje_error(
                "No se pudo cargar la información del miembro."
            )

    def obtener_listados_para_edicion(self):
        return self.service.obtener_catalogos_edicion()


    def procesar_aceptar_miembro(self, usuario_id):
        """
        Bug 2 fix: comprueba MiembroVO.Aceptado antes de llamar al servicio,
        evitando re-aceptar miembros ya activos.
        """
        if not self.vista_gestion:
            return
        try:
            miembro = self.service.obtener_detalle_miembro(usuario_id)
            if miembro and miembro.Aceptado:
                self.vista_gestion.mostrar_mensaje_error("Este miembro ya está aceptado.")
                return
            if self.service.aceptar_miembro(usuario_id):
                self.vista_gestion.mostrar_mensaje_exito("Miembro aceptado correctamente.")
                self._refrescar_tabla()
                self.cargar_detalle_miembro(usuario_id)
            else:
                self.vista_gestion.mostrar_mensaje_error(
                    "No se pudo cambiar el estado del miembro."
                )
        except Exception as e:
            self.vista_gestion.mostrar_mensaje_error(f"Error al aceptar miembro: {str(e)}")

    def procesar_eliminar_miembro(self, usuario_id):
        if not self.vista_gestion:
            return
        try:
            if self.service.eliminar_miembro(usuario_id):
                self.vista_gestion.mostrar_mensaje_exito("Miembro eliminado correctamente.")
                self._refrescar_tabla()
                self.vista_gestion.limpiar_detalle()
            else:
                self.vista_gestion.mostrar_mensaje_error(
                    "Error al intentar eliminar el registro."
                )
        except Exception as e:
            self.vista_gestion.mostrar_mensaje_error(f"Error al eliminar miembro: {str(e)}")


    def procesar_actualizar_miembro(
        self, usuario_id, dni, nombre, apellido,
        telefono, email, rol, lista_deptos, lista_grupos
    ):
        """
        Bug 1 fix: captura ValueError lanzado por los setters de MiembroVO
        (DNI, Email, Telefono, Name) y lo muestra en la UI sin crashear.
        """
        if not self.vista_gestion:
            return
        try:
            if self.service.actualizar_miembro(
                usuario_id, dni, nombre, apellido,
                telefono, email, rol, lista_deptos, lista_grupos
            ):
                self.vista_gestion.mostrar_mensaje_exito("Miembro actualizado correctamente.")
                self._refrescar_tabla()
                self.cargar_detalle_miembro(usuario_id)
            else:
                self.vista_gestion.mostrar_mensaje_error("No se pudieron guardar los cambios.")
        except ValueError as e:
            self.vista_gestion.mostrar_mensaje_error(f"Dato inválido: {str(e)}")
        except Exception as e:
            self.vista_gestion.mostrar_mensaje_error(f"Error inesperado al actualizar: {str(e)}")


    def procesar_agregar_miembro(self, rol_operador, datos):
        return self.service.agregar_miembro(rol_operador, datos)


    def _refrescar_tabla(self):
        if self.vista_gestion:
            filtro = self.vista_gestion.obtener_filtro_actual()
            self.filtrar_miembros(filtro)