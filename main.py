# archivo: main.py
import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from PyQt5.QtWidgets import QApplication
from database.Conexion import obtener_conexion
from DAO.MiembroDAO import MiembroDAO
from DAO.grupo_dao import GrupoDAO
from DAO.tarea_dao import TareaDAO
from DAO.departamentoDAO import DepartamentoDAO # Importación ya existente
from vistas.login_view import LoginView
from vistas.menu_view import MenuView

# Importamos ambos controladores arquitectónicos
from controller.tarea_controller import TareaController
from controller.grupo_controller import GrupoController
from controller.usuario_controller import UsuarioController 

class ControladorApp:
    def __init__(self):
        try:
            self.conexion = obtener_conexion()

            self.miembro_dao = MiembroDAO(self.conexion)
            self.grupo_dao = GrupoDAO(self.conexion)
            self.tarea_dao = TareaDAO(self.conexion)
            self.departamento_dao = DepartamentoDAO(self.conexion) 
            self.tarea_controller = TareaController(self.tarea_dao)
            self.grupo_controller = GrupoController(self.grupo_dao)
            self.usuario_controller = UsuarioController(self.miembro_dao, self.departamento_dao, self.grupo_dao) 
            
        except Exception as e:
            print(f"Error crítico: {e}")
            sys.exit(1)

        self.login_view = LoginView(callback_login=self.validar_login)
        self.menu_view = None
        self.login_view.show()

    def validar_login(self, usuario, contrasena):
        exito, resultado = self.miembro_dao.autenticar(usuario, contrasena)
        
        if exito:
            miembro_logueado = resultado
            grupos_formateados = self.grupo_controller.obtener_grupos_usuario(
                miembro_logueado.UsuarioID, miembro_logueado.Rol
            )
            
            self.login_view.hide()
            
            self.menu_view = MenuView(
                miembro=miembro_logueado, 
                lista_grupos=grupos_formateados,
                callback_cargar_tareas=self.tarea_controller.obtener_tareas_y_sesiones,
                callback_abrir_gestion=self.usuario_controller.abrir_pantalla_gestion, 
                callback_logout=self.cerrar_sesion
            )
            self.menu_view.show()
        else:
            self.login_view.mostrar_error(resultado)

    def cerrar_sesion(self):
        """Cierra el panel de control y regresa de forma limpia a la pantalla de Login"""
        if self.menu_view:
            self.menu_view.close()
        
        self.login_view.txt_password.clear() 
        self.login_view.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    controlador = ControladorApp()
    sys.exit(app.exec_())