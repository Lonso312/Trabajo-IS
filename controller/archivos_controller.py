import os
from PyQt5.QtWidgets import QFileDialog, QMessageBox

class ArchivosController:
    def __init__(self, archivos_dao, miembro_autenticado_vo):
        self.archivos_dao = archivos_dao
        self.usuario_actual = miembro_autenticado_vo
        self.vista_archivos = None

    def abrir_pantalla_archivos(self):
        from vistas.archivos_view import ArchivosView
        self.vista_archivos = ArchivosView(self)
        self.cargar_archivos()
        self.vista_archivos.show()

    # =================================================================
    # ALIASES DE SEGURIDAD (Corrige incompatibilidades de nombres)
    # =================================================================
    def mostrar_vista(self):
        """Redirecciona al método de apertura real para evitar fallos de atributo"""
        self.abrir_pantalla_archivos()

    def abrir_gestion_documental(self):
        """Redirecciona al método de apertura real para evitar fallos de atributo"""
        self.abrir_pantalla_archivos()
    # =================================================================

    def cargar_archivos(self):
        if not self.vista_archivos:
            return
        # Carga los archivos restringidos según el rol del miembro logueado
        archivos_permitidos = self.archivos_dao.obtener_archivos_por_rol(self.usuario_actual.Rol)
        self.vista_archivos.llenar_tabla_archivos(archivos_permitidos)

    def descargar_archivo(self, archivo_id):
        try:
            nombre, contenido_bytes = self.archivos_dao.obtener_contenido_archivo(archivo_id)
            if not contenido_bytes:
                QMessageBox.warning(self.vista_archivos, "Error", "No se pudo extraer el archivo de la Base de Datos.")
                return

            nombre = str(nombre)
            if not nombre.lower().endswith(".pdf"):
                nombre += ".pdf"

            ruta, _ = QFileDialog.getSaveFileName(
                self.vista_archivos if self.vista_archivos else None,
                "Guardar Archivo PDF",
                nombre,
                "Archivos PDF (*.pdf)"
            )

            if ruta:
                with open(ruta, "wb") as archivo_disco:
                    archivo_disco.write(contenido_bytes)

                QMessageBox.information(
                    self.vista_archivos,
                    "Éxito",
                    f"Archivo PDF guardado con éxito en:\n{ruta}"
                )
                self.cargar_archivos()

        except Exception as e:
            QMessageBox.critical(
                self.vista_archivos,
                "Error",
                f"Error crítico al guardar el PDF: {str(e)}"
            )

    def subir_nuevo_archivo(self, ruta_local, roles_permitidos):
        try:
            if not os.path.exists(ruta_local):
                return False

            nombre_archivo = os.path.basename(ruta_local)
            tipo = "PDF"

            with open(ruta_local, "rb") as archivo_local:
                contenido_bytes = archivo_local.read()

            if isinstance(roles_permitidos, (list, tuple)):
                roles_guardar = ",".join(roles_permitidos)
            else:
                roles_guardar = str(roles_permitidos)

            if self.archivos_dao.guardar_archivo(nombre_archivo, tipo, contenido_bytes, roles_guardar):
                QMessageBox.information(None, "Operación Exitosa", "El PDF se almacenó correctamente en la Base de Datos.")
                self.cargar_archivos()
                return True
            else:
                QMessageBox.critical(None, "Error", "Error interno en el DAO al guardar el archivo.")
                return False

        except Exception as e:
            QMessageBox.critical(None, "Error", f"Error de lectura en el archivo local: {str(e)}")
            return False