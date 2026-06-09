from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox
from PyQt5.QtCore import Qt

class LoginView(QWidget):
    def __init__(self, callback_login):
        super().__init__()
        self.callback_login = callback_login
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("SGA - Inicio de Sesión")
        self.setFixedSize(350, 250)

        # Layout principal vertical
        layout = QVBoxLayout()

        # Título
        lbl_titulo = QLabel("SGA DATABASE")
        lbl_titulo.setAlignment(Qt.AlignCenter)
        lbl_titulo.setStyleSheet("font-size: 18px; font-weight: bold; margin-bottom: 10px;")
        layout.addWidget(lbl_titulo)

        # Campos de texto
        layout.addWidget(QLabel("Usuario:"))
        self.txt_usuario = QLineEdit()
        self.txt_usuario.setPlaceholderText("Ingrese su nombre de usuario")
        layout.addWidget(self.txt_usuario)

        layout.addWidget(QLabel("Contraseña:"))
        self.txt_password = QLineEdit()
        self.txt_password.setPlaceholderText("Ingrese su contraseña")
        self.txt_password.setEchoMode(QLineEdit.Password) 
        layout.addWidget(self.txt_password)

        # Botón
        btn_entrar = QPushButton("Iniciar Sesión")
        btn_entrar.setStyleSheet("background-color: #0078D4; color: white; font-weight: bold; padding: 5px;")
        btn_entrar.clicked.connect(self.intentar_login)
        layout.addWidget(btn_entrar)

        self.setLayout(layout)

    def intentar_login(self):
        usuario = self.txt_usuario.text().strip()
        password = self.txt_password.text().strip()

        if not usuario or not password:
            QMessageBox.warning(self, "Campos vacíos", "Por favor, rellene todos los campos.")
            return

        self.callback_login(usuario, password)

    def mostrar_error(self, mensaje):
        QMessageBox.critical(self, "Error de Autenticación", mensaje)