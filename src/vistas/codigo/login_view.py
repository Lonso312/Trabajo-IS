# archivo: vistas/login_view.py
import os
from PyQt5.QtWidgets import QMainWindow, QMessageBox
from PyQt5 import uic

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

UI_PATH = os.path.join(
    BASE_DIR,
    "..",
    "UI",
    "login_view.ui"
)

UI_PATH = os.path.normpath(UI_PATH)

class LoginView(QMainWindow):
    def __init__(self, callback_login):
        super().__init__()
        self.callback_login = callback_login
        uic.loadUi(UI_PATH, self)

        # Nombres reales del .ui: UsuarioEdit, ContrasenaEdit, BotonAceptar
        self.BotonAceptar.clicked.connect(self.intentar_login)
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