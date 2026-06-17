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
from modelo.dao.ArchivosDAO import ArchivosDAO

from modelo.negocio.usuario_service import UsuarioService
from modelo.negocio.tarea_service import TareaService
from modelo.negocio.grupo_service import GrupoService
from modelo.negocio.bienes_service import BienesService
from modelo.negocio.archivos_service import ArchivosService
from modelo.negocio.factura_service import FacturaService
from modelo.negocio.solicitud_service import SolicitudService
from modelo.negocio.secretaria_service import SecretariaService

from controlador.usuario_controller import UsuarioController
from controlador.tarea_controller import TareaController
from controlador.grupo_controller import GrupoController
from controlador.bienes_controller import BienesController
from controlador.archivos_controller import ArchivosController
from controlador.factura_controller import FacturaController
from controlador.solicitud_controller import SolicitudController
from controlador.secretaria_controller import SecretariaController

from vistas.login_view import LoginView
from vistas.menu_view import MenuView


class ControladorApp:
    def __init__(self):
        try:
            self.conexion = obtener_conexion()

            # DAOs
            miembro_dao      = MiembroDAO(self.conexion)
            grupo_dao        = GrupoDAO(self.conexion)
            tarea_dao        = TareaDAO(self.conexion)
            departamento_dao = DepartamentoDAO(self.conexion)
            bienes_dao       = BienesDAO(self.conexion)
            factura_dao      = FacturaDAO(self.conexion)
            solicitud_dao    = SolicitudDAO(self.conexion)
            secretaria_dao   = SecretariaDAO(self.conexion)
            archivos_dao     = ArchivosDAO(self.conexion)

            # Servicios (negocio)
            self.usuario_service   = UsuarioService(miembro_dao, departamento_dao, grupo_dao)
            self.tarea_service     = TareaService(tarea_dao)
            self.grupo_service     = GrupoService(grupo_dao)
            self.bienes_service    = BienesService(bienes_dao)
            self.archivos_service  = ArchivosService(archivos_dao)
            self.factura_service   = FacturaService(factura_dao)
            self.solicitud_service = SolicitudService(solicitud_dao)
            self.secretaria_service= SecretariaService(secretaria_dao)

            # Controladores (reciben servicios, no DAOs)
            self.usuario_controller   = UsuarioController(self.usuario_service)
            self.tarea_controller     = TareaController(self.tarea_service)
            self.grupo_controller     = GrupoController(self.grupo_service)
            self.factura_controller   = FacturaController(self.factura_service)
            self.solicitud_controller = SolicitudController(self.solicitud_service)
            self.secretaria_controller= SecretariaController(self.secretaria_service)

        except Exception as e:
            print(f"Error crítico: {e}")
            sys.exit(1)

        self.login_view = LoginView(callback_login=self.validar_login)
        self.menu_view = None
        self.miembro = None
        self.bienes_controller = None
        self.archivos_controller = None

        self.login_view.show()

    def validar_login(self, usuario, contrasena):
        exito, resultado = self.usuario_service.autenticar(usuario, contrasena)

        if exito:
            self.miembro = resultado

            grupos_formateados = self.grupo_controller.obtener_grupos_usuario(
                self.miembro.UsuarioID,
                self.miembro.Rol
            )

            # Controladores que dependen del usuario autenticado
            self.bienes_controller   = BienesController(self.bienes_service, self.miembro)
            self.archivos_controller = ArchivosController(self.archivos_service, self.miembro)
            self.secretaria_controller.usuario_logueado = self.miembro

            self.login_view.hide()

            self.menu_view = MenuView(
                miembro=self.miembro,
                lista_grupos=grupos_formateados,
                callback_cargar_tareas=self.tarea_controller.obtener_tareas_y_sesiones,
                callback_abrir_gestion=self.abrir_gestion_miembros,
                callback_logout=self.cerrar_sesion
            )

            # Inyección de controladores en la vista del menú
            self.menu_view.grupo_controller     = self.grupo_controller
            self.menu_view.tarea_controller     = self.tarea_controller
            self.menu_view.bienes_controller    = self.bienes_controller
            self.menu_view.archivos_controller  = self.archivos_controller
            self.menu_view.factura_controller   = self.factura_controller
            self.menu_view.solicitud_controller = self.solicitud_controller
            self.menu_view.secretaria_controller= self.secretaria_controller

            self.menu_view.show()
        else:
            self.login_view.mostrar_error(resultado)

    def cerrar_sesion(self):
        if self.menu_view:
            self.menu_view.close()
            self.menu_view = None

        self.miembro = None
        self.bienes_controller = None
        self.archivos_controller = None
        self.secretaria_controller.usuario_logueado = None

        # Limpia el campo contraseña y vuelve a mostrar el login
        self.login_view.ContrasenaEdit.clear()
        self.login_view.UsuarioEdit.clear()
        self.login_view.show()

    def abrir_gestion_miembros(self):
        if self.miembro:
            self.usuario_controller.usuario_logueado = self.miembro
        self.usuario_controller.abrir_pantalla_gestion()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    controlador = ControladorApp()
    sys.exit(app.exec_())