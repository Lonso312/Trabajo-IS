import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from PyQt5.QtWidgets import QApplication
from database.Conexion import obtener_conexion
from DAO.MiembroDAO import MiembroDAO
from DAO.grupo_dao import GrupoDAO
from DAO.tarea_dao import TareaDAO
from vistas.login_view import LoginView
from vistas.menu_view import MenuView

class ControladorApp:
    def __init__(self):
        try:
            self.conexion = obtener_conexion()
            self.miembro_dao = MiembroDAO(self.conexion)
            self.grupo_dao = GrupoDAO(self.conexion)
            self.tarea_dao = TareaDAO(self.conexion)
        except Exception as e:
            print(f"Error crítico al conectar o inicializar DAOs: {e}")
            sys.exit(1)

        self.login_view = LoginView(callback_login=self.validar_login)
        self.menu_view = None

        self.login_view.show()

    def validar_login(self, usuario, contrasena):
        exito, resultado = self.miembro_dao.autenticar(usuario, contrasena)
        
        if exito:
            miembro_logueado = resultado
            grupos_formateados = self.grupo_dao.obtener_grupos_segun_rol(
                miembro_logueado.UsuarioID, miembro_logueado.Rol
            )

            self.login_view.hide()
            self.menu_view = MenuView(
                miembro=miembro_logueado, 
                lista_grupos=grupos_formateados,
                callback_cargar_tareas=self.obtener_tareas_de_grupo,
                callback_logout=self.cerrar_sesion
            )
            self.menu_view.show()
        else:
            self.login_view.mostrar_error(resultado)

    def obtener_tareas_de_grupo(self, id_grupo):
        tareas = self.tarea_dao.obtener_tareas_formateadas(id_grupo)
        sesiones = self.tarea_dao.obtener_sesiones_formateadas(id_grupo)
        return tareas + sesiones

    def cerrar_sesion(self):
        if self.menu_view:
            self.menu_view.close()
        self.login_view.txt_password.clear() 
        self.login_view.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    controlador = ControladorApp()
    sys.exit(app.exec_())