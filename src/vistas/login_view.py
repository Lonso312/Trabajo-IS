# archivo: vistas/login_view.py
import os
from PyQt5.QtWidgets import QMainWindow, QMessageBox
from PyQt5 import uic

# Ruta al archivo .ui (está en la misma carpeta que este .py)
UI_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "VistaLogin.ui")

class LoginView(QMainWindow):
    def __init__(self, callback_login):
        super().__init__()
        self.callback_login = callback_login

        # Carga el diseño desde el archivo .ui
        uic.loadUi(UI_PATH, self)

        # Conecta el botón del .ui con el método de login
        # El botón se llama "BotonAceptar" en el .ui
        self.BotonAceptar.clicked.connect(self.intentar_login)

        # También permite pulsar Enter en el campo contraseña
        self.ContrasenaEdit.returnPressed.connect(self.intentar_login)

    def intentar_login(self):
        usuario = self.UsuarioEdit.text().strip()
        password = self.ContrasenaEdit.text().strip()

        if not usuario or not password:
            QMessageBox.warning(self, "Campos vacíos", "Por favor, rellene todos los campos.")
            return

        self.callback_login(usuario, password)

    def mostrar_error(self, mensaje):
        QMessageBox.critical(self, "Error de Autenticación", mensaje)