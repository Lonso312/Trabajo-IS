# archivo: main.py
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from PyQt5.QtWidgets import QApplication
from modelo.conexion.Conexion import obtener_conexion

from modelo.dao.MiembroDAO import MiembroDAO
from modelo.dao.grupo_dao import GrupoDAO
from modelo.dao.tarea_dao import TareaDAO
from modelo.dao.departamentoDAO import DepartamentoDAO
from modelo.dao.BienesDAO import BienesDAO
from modelo.dao.FacturaDAO import FacturaDAO
from modelo.dao.SolicitudDAO import SolicitudDAO
from modelo.dao.SecretariaDAO import SecretariaDAO

from vistas.login_view import LoginView
from vistas.menu_view import MenuView

from controlador.tarea_controller import TareaController
from controlador.grupo_controller import GrupoController
from controlador.usuario_controller import UsuarioController
from controlador.bienes_controller import BienesController


class ControladorApp:
    def __init__(self):
        try:
            self.conexion = obtener_conexion()

            # DAOs
            self.miembro_dao = MiembroDAO(self.conexion)
            self.grupo_dao = GrupoDAO(self.conexion)
            self.tarea_dao = TareaDAO(self.conexion)
            self.departamento_dao = DepartamentoDAO(self.conexion)
            self.bienes_dao = BienesDAO(self.conexion)
            self.factura_dao = FacturaDAO(self.conexion)
            self.solicitud_dao = SolicitudDAO(self.conexion)
            self.secretaria_dao = SecretariaDAO(self.conexion)

            # Controladores
            self.tarea_controller = TareaController(self.tarea_dao)
            self.grupo_controller = GrupoController(self.grupo_dao)
            self.usuario_controller = UsuarioController(
                self.miembro_dao,
                self.departamento_dao,
                self.grupo_dao
            )

        except Exception as e:
            print(f"Error crítico: {e}")
            sys.exit(1)

        self.login_view = LoginView(callback_login=self.validar_login)
        self.menu_view = None
        self.miembro = None
        self.bienes_controller = None

        self.login_view.show()

    def validar_login(self, usuario, contrasena):
        exito, resultado = self.miembro_dao.autenticar(usuario, contrasena)

        if exito:
            self.miembro = resultado

            grupos_formateados = self.grupo_controller.obtener_grupos_usuario(
                self.miembro.UsuarioID,
                self.miembro.Rol
            )

            self.login_view.hide()

            # Controlador de bienes ligado al usuario autenticado
            self.bienes_controller = BienesController(
                self.bienes_dao,
                self.miembro
            )

            from DAO.ArchivosDAO import ArchivosDAO
            from controller.archivos_controller import ArchivosController
            self.archivos_dao = ArchivosDAO(self.conexion)
            self.archivos_controller = ArchivosController(self.archivos_dao, self.miembro)

            self.menu_view = MenuView(
                miembro=self.miembro,
                lista_grupos=grupos_formateados,
                callback_cargar_tareas=self.tarea_controller.obtener_tareas_y_sesiones,
                callback_abrir_gestion=self.abrir_gestion_miembros_con_refresh,
                callback_logout=self.cerrar_sesion
            )

            # Inyección de controladores
            self.menu_view.grupo_controller = self.grupo_controller
            self.menu_view.tarea_controller = self.tarea_controller
            self.menu_view.bienes_controller = self.bienes_controller
            self.menu_view.factura_dao = self.factura_dao
            self.menu_view.solicitud_dao = self.solicitud_dao
            self.menu_view.secretaria_dao = self.secretaria_dao
            self.menu_view.archivos_controller = self.archivos_controller


            self.menu_view.show()

        else:
            self.login_view.mostrar_error(resultado)

    def cerrar_sesion(self):
        if self.menu_view:
            self.menu_view.close()

        self.miembro = None

        self.login_view.txt_password.clear()
        self.login_view.show()

    def abrir_gestion_miembros_con_refresh(self):
        """Abre la gestión de miembros. El refresco ocurre mediante EventBus."""
        if self.miembro is not None:
            self.usuario_controller.usuario_logueado = self.miembro

        self.usuario_controller.abrir_pantalla_gestion()

    


if __name__ == '__main__':
    app = QApplication(sys.argv)
    controlador = ControladorApp()
    sys.exit(app.exec_())