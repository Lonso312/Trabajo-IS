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
        try:
            archivos = self.service.obtener_archivos_por_rol(self.usuario_actual.Rol)
            self.vista_archivos.llenar_tabla_archivos(archivos)
        except Exception as e:
            print(f"[ArchivosController] Error cargando archivos: {e}")
            self.vista_archivos.llenar_tabla_archivos([])

    def descargar_archivo(self, archivo_id):
        """
        Bug 5 fix: garantiza que siempre se devuelve una tupla (nombre, datos, error).
        Antes podía devolver el resultado crudo del servicio (sin desempaquetar),
        lo que provocaba que la vista fallara al esperar 3 valores.
        """
        try:
            resultado = self.service.descargar_archivo(archivo_id)
            if resultado is None:
                return None, None, "El servicio no devolvió datos para este archivo."
            # El servicio debe retornar (nombre_archivo, datos_bytes, None) o
            # (None, None, mensaje_error) — lo propagamos tal cual
            return resultado
        except Exception as e:
            print(f"[ArchivosController] Error descargando archivo {archivo_id}: {e}")
            return None, None, f"Error crítico al obtener el archivo: {str(e)}"

    def subir_nuevo_archivo(self, ruta_local, roles_permitidos):
        try:
            exito, msg = self.service.subir_archivo(ruta_local, roles_permitidos)
            if exito:
                self.cargar_archivos()
            return exito, msg
        except Exception as e:
            print(f"[ArchivosController] Error subiendo archivo: {e}")
            return False, f"Error de lectura en el archivo local: {str(e)}"