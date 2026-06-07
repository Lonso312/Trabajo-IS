# archivo: main.py
import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from PyQt5.QtWidgets import QApplication
from database.Conexion import obtener_conexion

from DAO.MiembroDAO import MiembroDAO
from DAO.grupo_dao import GrupoDAO
from DAO.tarea_dao import TareaDAO
from DAO.departamentoDAO import DepartamentoDAO
from DAO.BienesDAO import BienesDAO
from DAO.FacturaDAO import FacturaDAO

from vistas.login_view import LoginView
from vistas.menu_view import MenuView

from controller.tarea_controller import TareaController
from controller.grupo_controller import GrupoController
from controller.usuario_controller import UsuarioController
from controller.bienes_controller import BienesController


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

        # Pasar usuario actual al controlador
        if self.miembro is not None:
            self.usuario_controller.usuario_logueado = self.miembro

        self.usuario_controller.abrir_pantalla_gestion()

        from PyQt5.QtWidgets import QApplication
        from vistas.gestion_miembros_view import GestionMiembrosView

        for widget in QApplication.topLevelWidgets():
            if isinstance(widget, GestionMiembrosView):

                original_callback = widget.callback_actualizar

                def callback_actualizar_wrapper(*args, **kwargs):
                    resultado = original_callback(*args, **kwargs)

                    if self.menu_view:
                        self.menu_view.refrescar_grupos()

                    return resultado

                widget.callback_actualizar = callback_actualizar_wrapper
                break


if __name__ == '__main__':
    app = QApplication(sys.argv)
    controlador = ControladorApp()
    sys.exit(app.exec_())