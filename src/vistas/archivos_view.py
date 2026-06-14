# archivo: vistas/archivos_view.py
import os
from PyQt5.QtWidgets import (QWidget, QMessageBox, QTableWidgetItem, QPushButton,
                              QFileDialog, QDialog, QVBoxLayout, QLabel, QGroupBox,
                              QCheckBox, QDialogButtonBox, QHeaderView, QAbstractItemView)
from PyQt5.QtCore import Qt
from PyQt5 import uic

UI_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "archivos_view.ui")

class ArchivosView(QWidget):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        uic.loadUi(UI_PATH, self)

        # Configura la tabla — nombre real del .ui: tabla_archivos
        self.tabla_archivos.setColumnCount(5)
        self.tabla_archivos.setHorizontalHeaderLabels(["ID", "Nombre del Archivo", "Rol Permitido", "Descargas", "Acción"])
        self.tabla_archivos.setSelectionMode(QAbstractItemView.SingleSelection)
        self.tabla_archivos.setEditTriggers(QAbstractItemView.NoEditTriggers)
        header = self.tabla_archivos.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.Stretch)
        header.setSectionResizeMode(0, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(4, QHeaderView.ResizeToContents)

        # Conecta botones — nombres reales del .ui: btn_subir, btn_descargar, btn_eliminar
        self.btn_subir.clicked.connect(self.abrir_dialogo_subida)
        self.btn_descargar.clicked.connect(self._descargar_seleccionado)
        self.btn_eliminar.setVisible(False)  # deshabilitado hasta implementar eliminar

    def llenar_tabla_archivos(self, lista_archivos):
        self.tabla_archivos.setRowCount(0)
        for archivo in lista_archivos:
            row = self.tabla_archivos.rowCount()
            self.tabla_archivos.insertRow(row)
            self.tabla_archivos.setItem(row, 0, QTableWidgetItem(str(archivo['id'])))
            self.tabla_archivos.setItem(row, 1, QTableWidgetItem(str(archivo['nombre'])))
            self.tabla_archivos.setItem(row, 2, QTableWidgetItem(str(archivo['rol_permitido'])))
            self.tabla_archivos.setItem(row, 3, QTableWidgetItem(str(archivo['descargas'])))
            btn = QPushButton("Descargar PDF")
            btn.setCursor(Qt.PointingHandCursor)
            btn.setStyleSheet("background-color: #2ECC71; color: white; padding: 4px 12px; border-radius: 4px; border: none; font-weight: bold;")
            btn.clicked.connect(lambda checked, aid=archivo['id']: self.controller.descargar_archivo(aid))
            self.tabla_archivos.setCellWidget(row, 4, btn)

    def _descargar_seleccionado(self):
        fila = self.tabla_archivos.currentRow()
        if fila < 0:
            QMessageBox.warning(self, "Sin selección", "Selecciona un archivo de la tabla primero.")
            return
        item_id = self.tabla_archivos.item(fila, 0)
        if item_id:
            self.controller.descargar_archivo(int(item_id.text()))

    def abrir_dialogo_subida(self):
        ruta, _ = QFileDialog.getOpenFileName(self, "Seleccionar archivo PDF", "", "Archivos PDF (*.pdf)")
        if not ruta:
            return
        dialogo = QDialog(self)
        dialogo.setWindowTitle("Privacidad del Documento")
        dialogo.setMinimumWidth(320)
        layout = QVBoxLayout(dialogo)
        layout.addWidget(QLabel("Selecciona los roles que podrán ver el documento:"))
        grupo = QGroupBox("Permitir acceso a:")
        g_layout = QVBoxLayout()
        chk_todos      = QCheckBox("TODOS")
        chk_presidente = QCheckBox("PRESIDENTE")
        chk_secretario = QCheckBox("SECRETARIO")
        chk_tesorero   = QCheckBox("TESORERO")
        chk_jefe       = QCheckBox("JEFE DEPARTAMENTO")
        for cb in (chk_todos, chk_presidente, chk_secretario, chk_tesorero, chk_jefe):
            g_layout.addWidget(cb)
        grupo.setLayout(g_layout)
        layout.addWidget(grupo)
        def on_todos(state):
            for cb in (chk_presidente, chk_secretario, chk_tesorero, chk_jefe):
                cb.setChecked(False)
                cb.setEnabled(state != Qt.Checked)
        chk_todos.stateChanged.connect(on_todos)
        botones = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        botones.accepted.connect(dialogo.accept)
        botones.rejected.connect(dialogo.reject)
        layout.addWidget(botones)
        if dialogo.exec_() == QDialog.Accepted:
            roles = ["TODOS"] if chk_todos.isChecked() else [
                cb.text() for cb in (chk_presidente, chk_secretario, chk_tesorero, chk_jefe) if cb.isChecked()
            ]
            if roles:
                exito, msg = self.controller.subir_nuevo_archivo(ruta, roles)
                if exito:
                    QMessageBox.information(self, "Éxito", msg)
                else:
                    QMessageBox.critical(self, "Error", msg)