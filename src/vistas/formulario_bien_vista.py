# archivo: vistas/formulario_bien_vista.py
import os
from PyQt5.QtWidgets import QDialog
from PyQt5 import uic

UI_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "formulario_bien_vista.ui")

class FormularioBienDialog(QDialog):
    def __init__(self, bien_vo=None, parent=None):
        super().__init__(parent)
        self.bien_vo = bien_vo

        # Carga el .ui — widgets: txt_tipo, txt_precio, txt_cantidad, botones
        uic.loadUi(UI_PATH, self)

        # Título dinámico según si es edición o creación
        self.setWindowTitle("Editar Bien / Activo" if bien_vo else "Añadir Nuevo Bien")

        # Conecta los botones estándar del QDialogButtonBox
        self.botones.accepted.connect(self.accept)
        self.botones.rejected.connect(self.reject)

        # Placeholders
        self.txt_tipo.setPlaceholderText("Ej. Computadora portátil, Silla...")
        self.txt_precio.setPlaceholderText("Ej. 450.00")
        self.txt_cantidad.setPlaceholderText("Ej. 10")

        # Si es edición, rellena los campos con los datos actuales
        if bien_vo:
            self.txt_tipo.setText(str(bien_vo.tipo) if bien_vo.tipo else "")
            self.txt_precio.setText(str(bien_vo.precio) if bien_vo.precio is not None else "")
            self.txt_cantidad.setText(str(bien_vo.cantidad) if bien_vo.cantidad is not None else "")

    def obtener_datos(self):
        return {
            'tipo':     self.txt_tipo.text().strip(),
            'precio':   self.txt_precio.text().strip() or "0",
            'cantidad': self.txt_cantidad.text().strip() or "0"
        }