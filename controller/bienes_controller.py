from VO.BienVO import BienVO
from PyQt5.QtWidgets import QMessageBox

class BienesController:
    def __init__(self, bienes_dao, miembro_autenticado_vo):
        self.bienes_dao = bienes_dao
        self.usuario_actual = miembro_autenticado_vo
        self.vista_gestion = None

    def abrir_pantalla_bienes(self):
        # Control estricto de accesos según la jerarquía solicitada
        if self.usuario_actual.Rol not in ['PRESIDENTE', 'TESORERO', 'JEFE DEPARTAMENTO']:
            QMessageBox.critical(None, "Acceso Denegado", "Solo Tesoreros o Presidentes pueden gestionar los bienes.")
            return
    
        from vistas.gestion_bienes_view import GestionBienesView
        self.vista_gestion = GestionBienesView(self)
        self.cargar_bienes()
        self.vista_gestion.show()

    def cargar_bienes(self):
        """Consulta directa al origen de datos mapeado sin filtros redundantes"""
        if not self.vista_gestion:
            return
        bienes_formateados = self.bienes_dao.obtener_bienes_para_gestion()
        self.vista_gestion.llenar_tabla_bienes(bienes_formateados)

    def seleccionar_bien(self, bien_id):
        if not self.vista_gestion:
            return
        bien_vo = self.bienes_dao.buscar_por_id(bien_id)
        if bien_vo:
            self.vista_gestion.mostrar_detalle_bien(bien_vo)

    def añadir_bien(self, datos):
        try:
            nuevo_bien = BienVO(tipo=datos['tipo'], precio=float(datos['precio']), cantidad=int(datos['cantidad']))
            if self.bienes_dao.crear(nuevo_bien):
                self.vista_gestion.mostrar_mensaje_exito("El bien se ha añadido correctamente al inventario.")
                self.cargar_bienes()
                self.vista_gestion.mostrar_mensaje_vacio()
            else:
                self.vista_gestion.mostrar_mensaje_error("Error interno del DAO al intentar insertar el bien.")
        except Exception as e:
            self.vista_gestion.mostrar_mensaje_error(f"Error al añadir el bien: {str(e)}")

    def actualizar_bien(self, bien_id, datos):
        try:
            if self.bienes_dao.actualizar_bien(bien_id, datos['tipo'], float(datos['precio']), int(datos['cantidad'])):
                self.vista_gestion.mostrar_mensaje_exito("El bien se ha modificado correctamente.")
                self.cargar_bienes()
                self.seleccionar_bien(bien_id) # Refresca el panel informativo derecho
            else:
                self.vista_gestion.mostrar_mensaje_error("No se pudieron guardar las modificaciones en la base de datos.")
        except Exception as e:
            self.vista_gestion.mostrar_mensaje_error(f"Error al actualizar el bien: {str(e)}")

    def eliminar_bien(self, bien_id):
        try:
            if self.bienes_dao.eliminar_bien(bien_id):
                self.vista_gestion.mostrar_mensaje_exito("El bien seleccionado se ha eliminado del inventario.")
                self.cargar_bienes()
                self.vista_gestion.mostrar_mensaje_vacio()
            else:
                self.vista_gestion.mostrar_mensaje_error("Error al intentar eliminar el registro.")
        except Exception as e:
            self.vista_gestion.mostrar_mensaje_error(f"Error al eliminar el bien: {str(e)}")

    # =================================================================
    # ALIAS DE SEGURIDAD
    # =================================================================
    def abrir_vista_bienes(self):
        """Método puente para redirigir llamadas antiguas y evitar crashes de atributo"""
        self.abrir_pantalla_bienes()