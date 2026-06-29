class BienesController:
    def __init__(self, bienes_service, miembro_autenticado_vo):
        self.service = bienes_service
        self.usuario_actual = miembro_autenticado_vo
        self.vista_gestion = None       # inyectada desde fuera (menu_view)

    def abrir_pantalla_bienes(self):
        """
        Verifica acceso y carga los datos en la vista de bienes.
        La vista ya debe haber sido inyectada en self.vista_gestion
        antes de llamar a este método (lo hace menu_view).
        Devuelve (False, msg) si el rol no tiene permiso, para que
        menu_view pueda mostrar el aviso sin que el controlador lo haga.
        """
        acceso, msg = self.service.verificar_acceso(self.usuario_actual.Rol)
        if not acceso:
            return False, msg

        if not self.vista_gestion:
            return False, "La vista de bienes no está disponible."

        self.cargar_bienes()
        self.vista_gestion.show()
        return True, ""


    def cargar_bienes(self):
        if not self.vista_gestion:
            return
        self.vista_gestion.llenar_tabla_bienes(self.service.obtener_bienes())

    def seleccionar_bien(self, bien_id):
        if not self.vista_gestion:
            return
        bien_vo = self.service.obtener_bien(bien_id)
        if bien_vo:
            self.vista_gestion.mostrar_detalle_bien(bien_vo)


    def añadir_bien(self, datos):
        if not self.vista_gestion:
            return
        try:
            if self.service.añadir_bien(datos):
                self.vista_gestion.mostrar_mensaje_exito(
                    "Bien añadido correctamente al inventario."
                )
                self.cargar_bienes()
                self.vista_gestion.mostrar_mensaje_vacio()
            else:
                self.vista_gestion.mostrar_mensaje_error("Error al insertar el bien.")
        except Exception as e:
            self.vista_gestion.mostrar_mensaje_error(f"Error al añadir el bien: {str(e)}")


    def actualizar_bien(self, bien_id, datos):
        if not self.vista_gestion:
            return
        try:
            if self.service.actualizar_bien(bien_id, datos):
                self.vista_gestion.mostrar_mensaje_exito("Bien modificado correctamente.")
                self.cargar_bienes()
                self.seleccionar_bien(bien_id)
            else:
                self.vista_gestion.mostrar_mensaje_error(
                    "No se pudieron guardar las modificaciones."
                )
        except Exception as e:
            self.vista_gestion.mostrar_mensaje_error(f"Error al actualizar el bien: {str(e)}")


    def eliminar_bien(self, bien_id):
        if not self.vista_gestion:
            return
        try:
            if self.service.eliminar_bien(bien_id):
                self.vista_gestion.mostrar_mensaje_exito("Bien eliminado del inventario.")
                self.cargar_bienes()
                self.vista_gestion.mostrar_mensaje_vacio()
            else:
                self.vista_gestion.mostrar_mensaje_error("Error al eliminar el registro.")
        except Exception as e:
            self.vista_gestion.mostrar_mensaje_error(f"Error al eliminar el bien: {str(e)}")