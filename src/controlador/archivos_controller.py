class ArchivosController:
    def __init__(self, archivos_service, miembro_autenticado_vo):
        self.service = archivos_service
        self.usuario_actual = miembro_autenticado_vo
        self.vista_archivos = None

    def abrir_pantalla_archivos(self):
        from vistas.archivos_view import ArchivosView
        self.vista_archivos = ArchivosView(self)
        self.cargar_archivos()
        self.vista_archivos.show()

    def mostrar_vista(self):
        self.abrir_pantalla_archivos()

    def abrir_gestion_documental(self):
        self.abrir_pantalla_archivos()

    def cargar_archivos(self):
        if not self.vista_archivos:
            return
        archivos = self.service.obtener_archivos_por_rol(self.usuario_actual.Rol)
        self.vista_archivos.llenar_tabla_archivos(archivos)

    def descargar_archivo(self, archivo_id):
        try:
            return self.service.descargar_archivo(archivo_id)
        except Exception as e:
            return None, None, f"Error crítico al obtener el archivo: {str(e)}"

    def subir_nuevo_archivo(self, ruta_local, roles_permitidos):
        try:
            exito, msg = self.service.subir_archivo(ruta_local, roles_permitidos)
            if exito:
                self.cargar_archivos()
            return exito, msg
        except Exception as e:
            return False, f"Error de lectura en el archivo local: {str(e)}"