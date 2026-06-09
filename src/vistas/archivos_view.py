from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QTableWidget, QTableWidgetItem, QPushButton,
    QHeaderView, QFileDialog, QDialog, QFormLayout,
    QDialogButtonBox, QCheckBox, QGroupBox
)
from PyQt5.QtCore import Qt


class ArchivosView(QWidget):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("SGA - Repositorio General de Documentos")
        self.resize(850, 480)
        self.setStyleSheet("background-color: #F8F9FA; font-family: 'Segoe UI', Arial;")

        layout_principal = QVBoxLayout(self)
        layout_principal.setContentsMargins(20, 20, 20, 20)

        lbl_titulo = QLabel("Repositorio de Documentación Compartida")
        lbl_titulo.setStyleSheet("font-size: 18px; font-weight: bold; color: #2C3E50; margin-bottom: 4px;")
        layout_principal.addWidget(lbl_titulo)

        lbl_subtitulo = QLabel("Los archivos mostrados están regulados estrictamente bajo tus permisos de credenciales.")
        lbl_subtitulo.setStyleSheet("font-size: 11px; color: #7F8C8D; margin-bottom: 15px;")
        layout_principal.addWidget(lbl_subtitulo)

        self.btn_subir = QPushButton("+ Subir Nuevo PDF")
        self.btn_subir.setCursor(Qt.PointingHandCursor)
        self.btn_subir.setStyleSheet("""
            QPushButton { background-color: #34495E; color: white; font-weight: bold; padding: 7px 15px; border-radius: 5px; border: none; }
            QPushButton:hover { background-color: #2C3E50; }
        """)
        self.btn_subir.clicked.connect(self.abrir_dialogo_subida)

        top_layout = QHBoxLayout()
        top_layout.addWidget(self.btn_subir)
        top_layout.addStretch()
        layout_principal.addLayout(top_layout)
        layout_principal.addSpacing(10)

        self.tabla = QTableWidget()
        self.tabla.setColumnCount(5)
        self.tabla.setHorizontalHeaderLabels(["ID", "Nombre del Archivo", "Rol Permitido", "Descargas", "Acción"])
        self.tabla.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tabla.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeToContents)
        self.tabla.horizontalHeader().setSectionResizeMode(4, QHeaderView.ResizeToContents)
        self.tabla.setStyleSheet("QTableWidget { background-color: white; border: 1px solid #E0E0E0; border-radius: 4px; }")
        self.tabla.setSelectionMode(QTableWidget.NoSelection)
        layout_principal.addWidget(self.tabla)

    def llenar_tabla_archivos(self, lista_archivos):
        self.tabla.setRowCount(0)
        for archivo in lista_archivos:
            row = self.tabla.rowCount()
            self.tabla.insertRow(row)

            self.tabla.setItem(row, 0, QTableWidgetItem(str(archivo['id'])))
            self.tabla.setItem(row, 1, QTableWidgetItem(str(archivo['nombre'])))
            self.tabla.setItem(row, 2, QTableWidgetItem(str(archivo['rol_permitido'])))
            self.tabla.setItem(row, 3, QTableWidgetItem(str(archivo['descargas'])))

            btn_descargar = QPushButton("Descargar PDF")
            btn_descargar.setCursor(Qt.PointingHandCursor)
            btn_descargar.setStyleSheet("""
                QPushButton { background-color: #2ECC71; color: white; padding: 4px 12px; border-radius: 4px; border: none; font-weight: bold; }
                QPushButton:hover { background-color: #27AE60; }
            """)

            btn_descargar.clicked.connect(
                lambda checked, aid=archivo['id']: self.controller.descargar_archivo(aid)
            )
            self.tabla.setCellWidget(row, 4, btn_descargar)

    def abrir_dialogo_subida(self):
        ruta, _ = QFileDialog.getOpenFileName(
            self,
            "Seleccionar archivo PDF",
            "",
            "Archivos PDF (*.pdf)"
        )
        if not ruta:
            return

        dialogo = QDialog(self)
        dialogo.setWindowTitle("Privacidad del Documento")
        dialogo.setMinimumWidth(320)

        layout = QVBoxLayout(dialogo)

        lbl = QLabel("Selecciona los roles que podrán ver el documento:")
        layout.addWidget(lbl)

        grupo_roles = QGroupBox("Permitir acceso a:")
        roles_layout = QVBoxLayout()

        chk_todos = QCheckBox("TODOS")
        chk_presidente = QCheckBox("PRESIDENTE")
        chk_secretario = QCheckBox("SECRETARIO")
        chk_tesorero = QCheckBox("TESORERO")
        chk_jefe = QCheckBox("JEFE DEPARTAMENTO")

        for cb in (chk_todos, chk_presidente, chk_secretario, chk_tesorero, chk_jefe):
            roles_layout.addWidget(cb)

        grupo_roles.setLayout(roles_layout)
        layout.addWidget(grupo_roles)

        def on_todos_changed(state):
            if state == Qt.Checked:
                for cb in (chk_presidente, chk_secretario, chk_tesorero, chk_jefe):
                    cb.setChecked(False)
                    cb.setEnabled(False)
            else:
                for cb in (chk_presidente, chk_secretario, chk_tesorero, chk_jefe):
                    cb.setEnabled(True)

        chk_todos.stateChanged.connect(on_todos_changed)

        botones = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        botones.accepted.connect(dialogo.accept)
        botones.rejected.connect(dialogo.reject)
        layout.addWidget(botones)

        if dialogo.exec_() == QDialog.Accepted:
            roles = []

            if chk_todos.isChecked():
                roles = ["TODOS"]
            else:
                if chk_presidente.isChecked():
                    roles.append("PRESIDENTE")
                if chk_secretario.isChecked():
                    roles.append("SECRETARIO")
                if chk_tesorero.isChecked():
                    roles.append("TESORERO")
                if chk_jefe.isChecked():
                    roles.append("JEFE DEPARTAMENTO")

            if not roles:
                return

            self.controller.subir_nuevo_archivo(ruta, ",".join(roles))