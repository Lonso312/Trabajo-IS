class ArchivosController:
    def __init__(self, archivos_service, miembro_autenticado_vo):
        self.service = archivos_service
        self.usuario_actual = miembro_autenticado_vo
        self.vista_archivos = None      # inyectada desde fuera (menu_view)

    def abrir_pantalla_archivos(self):
        """
        Carga los archivos en la vista documental.
        La vista ya debe haber sido inyectada en self.vista_archivos
        antes de llamar a este método (lo hace menu_view).
        """
        if not self.vista_archivos:
            return
        self.cargar_archivos()
        self.vista_archivos.show()

    # Alias mantenidos por compatibilidad con menu_view
    def mostrar_vista(self):
        self.abrir_pantalla_archivos()

    def abrir_gestion_documental(self):
        self.abrir_pantalla_archivos()


    def cargar_archivos(self):
        if not self.vista_archivos:
            return
        try:
            archivos = self.service.obtener_archivos_por_rol(self.usuario_actual.Rol)
            self.vista_archivos.llenar_tabla_archivos(archivos)
        except Exception as e:
            print(f"[ArchivosController] Error cargando archivos: {e}")
            self.vista_archivos.llenar_tabla_archivos([])


    def descargar_archivo(self, archivo_id):
        """
        Bug 5 fix: garantiza que siempre se devuelve una tupla (nombre, datos, error).
        """
        try:
            resultado = self.service.descargar_archivo(archivo_id)
            if resultado is None:
                return None, None, "El servicio no devolvió datos para este archivo."
            return resultado
        except Exception as e:
            print(f"[ArchivosController] Error descargando archivo {archivo_id}: {e}")
            return None, None, f"Error crítico al obtener el archivo: {str(e)}"


    def subir_nuevo_archivo(self, ruta_local, roles_permitidos):
        try:
            exito, msg = False, "No se seleccionaron roles válidos."

            if "TODOS" in roles_permitidos:
                exito, msg = self.service.subir_archivo(ruta_local, "TODOS")
            else:
                for rol in roles_permitidos:
                    exito, msg = self.service.subir_archivo(ruta_local, rol)

            if exito:
                self.cargar_archivos()
            return exito, msg

        except Exception as e:
            print(f"[ArchivosController] Error crítico en subida: {e}")
            return False, f"Error en el proceso de subida: {str(e)}"