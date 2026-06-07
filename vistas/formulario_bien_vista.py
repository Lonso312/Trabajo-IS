# archivo: vistas/formulario_bien_vista.py
from PyQt5.QtWidgets import QDialog, QFormLayout, QLineEdit, QDialogButtonBox, QVBoxLayout

class FormularioBienDialog(QDialog):
    def __init__(self, bien_vo=None, parent=None):
        super().__init__(parent)
        self.bien_vo = bien_vo
        self.init_ui()

    def init_ui(self):
        if self.bien_vo:
            self.setWindowTitle("Editar Bien / Activo")
        else:
            self.setWindowTitle("Añadir Nuevo Bien")
            
        self.resize(380, 180)
        self.setStyleSheet("font-family: 'Segoe UI', Arial; font-size: 12px;")
        
        layout_principal = QVBoxLayout(self)
        form_layout = QFormLayout()
        
        # Condición 3: Solo se solicita Tipo, Precio y Cantidad
        self.txt_tipo = QLineEdit(self)
        self.txt_precio = QLineEdit(self)
        self.txt_cantidad = QLineEdit(self)
        
        # Mensajes de ayuda visual en los campos
        self.txt_tipo.setPlaceholderText("Ej. Computadora portatil, Silla, depto...")
        self.txt_precio.setPlaceholderText("Ej. 450.00")
        self.txt_cantidad.setPlaceholderText("Ej. 10")
        
        form_layout.addRow("Tipo / Nombre del Bien:", self.txt_tipo)
        form_layout.addRow("Precio Unitario (€):", self.txt_precio)
        form_layout.addRow("Cantidad a Añadir:", self.txt_cantidad)
        
        layout_principal.addLayout(form_layout)
        
        # Botones de Aceptar y Cancelar estándar
        self.botones = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel, self)
        self.botones.accepted.connect(self.accept)
        self.botones.rejected.connect(self.reject)
        layout_principal.addWidget(self.botones)
        
        # Condición 1 Corregida: Cargar los datos usando '.tipo' en lugar del inexistente '.Nombre'
        if self.bien_vo:
            self.txt_tipo.setText(str(self.bien_vo.tipo if self.bien_vo.tipo else ""))
            self.txt_precio.setText(str(self.bien_vo.precio if self.bien_vo.precio is not None else ""))
            self.txt_cantidad.setText(str(self.bien_vo.cantidad if self.bien_vo.cantidad is not None else ""))

    def obtener_datos(self):
        """Devuelve el diccionario con las claves exactas que espera el BienesController"""
        return {
            'tipo': self.txt_tipo.text().strip(),
            'precio': self.txt_precio.text().strip() if self.txt_precio.text().strip() else "0",
            'cantidad': self.txt_cantidad.text().strip() if self.txt_cantidad.text().strip() else "0"
        }