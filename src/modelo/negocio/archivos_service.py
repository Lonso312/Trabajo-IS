import os

class ArchivosService:
    def __init__(self, archivos_dao):
        self.archivos_dao = archivos_dao

    def obtener_archivos_por_rol(self, rol):
        return self.archivos_dao.obtener_archivos_por_rol(rol)

    def descargar_archivo(self, archivo_id):
        nombre, contenido_bytes = self.archivos_dao.obtener_contenido_archivo(archivo_id)
        if not contenido_bytes:
            return None, None, "No se pudo extraer el archivo de la Base de Datos."
        nombre = str(nombre)
        if not nombre.lower().endswith(".pdf"):
            nombre += ".pdf"
        return nombre, contenido_bytes, ""

    def subir_archivo(self, ruta_local, roles_permitidos):
        if not os.path.exists(ruta_local):
            return False, "El archivo no existe en la ruta indicada."
        nombre_archivo = os.path.basename(ruta_local)
        with open(ruta_local, "rb") as f:
            contenido_bytes = f.read()
        roles_guardar = ",".join(roles_permitidos) if isinstance(roles_permitidos, (list, tuple)) else str(roles_permitidos)
        if self.archivos_dao.guardar_archivo(nombre_archivo, "PDF", contenido_bytes, roles_guardar):
            return True, "El PDF se almacenó correctamente en la Base de Datos."
        return False, "Error interno en el DAO al guardar el archivo."