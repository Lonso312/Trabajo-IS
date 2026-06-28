# archivo: vistas/gestion_bienes_view.py
import os
from PyQt5.QtWidgets import QWidget, QMessageBox, QTableWidgetItem, QDialog, QHeaderView, QAbstractItemView
from PyQt5.QtCore import Qt
from PyQt5 import uic

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

UI_PATH = os.path.join(
    BASE_DIR,
    "..",
    "UI",
    "gestion_bienes_view.ui"
)

UI_PATH = os.path.normpath(UI_PATH)

class GestionBienesView(QWidget):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self.bien_actual_vo = None
        uic.loadUi(UI_PATH, self)

        # Configura la tabla — nombre real del .ui: tabla_bienes
        self.tabla_bienes.setColumnCount(3)
        self.tabla_bienes.setHorizontalHeaderLabels(["Tipo", "Cantidad", "Precio"])
        self.tabla_bienes.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.tabla_bienes.setSelectionMode(QAbstractItemView.SingleSelection)
        self.tabla_bienes.setEditTriggers(QAbstractItemView.NoEditTriggers)
        header = self.tabla_bienes.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.Stretch)
        header.setSectionResizeMode(1, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(2, QHeaderView.ResizeToContents)

        # Conecta señales — nombres reales del .ui: btn_anadir, btn_editar, btn_eliminar, lbl_detalles
        self.tabla_bienes.itemSelectionChanged.connect(self.on_fila_seleccionada)
        self.btn_anadir.clicked.connect(self.abrir_formulario_crear)
        self.btn_editar.clicked.connect(self.abrir_formulario_editar)
        self.btn_eliminar.clicked.connect(self._eliminar_bien_actual)

        self.btn_editar.setEnabled(False)
        self.btn_eliminar.setEnabled(False)
        self.lbl_detalles.setText("Selecciona un bien para ver sus detalles")

    def llenar_tabla_bienes(self, lista_bienes):
        self.tabla_bienes.setRowCount(0)
        for bien in lista_bienes:
            row = self.tabla_bienes.rowCount()
            self.tabla_bienes.insertRow(row)
            item_tipo = QTableWidgetItem(bien["tipo"])
            item_tipo.setData(Qt.UserRole, bien["id"])
            item_cantidad = QTableWidgetItem(str(bien["cantidad"]))
            item_cantidad.setTextAlignment(Qt.AlignCenter)
            item_precio = QTableWidgetItem(bien["precio"])
            item_precio.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
            self.tabla_bienes.setItem(row, 0, item_tipo)
            self.tabla_bienes.setItem(row, 1, item_cantidad)
            self.tabla_bienes.setItem(row, 2, item_precio)

    def on_fila_seleccionada(self):
        item_tipo = self.tabla_bienes.item(self.tabla_bienes.currentRow(), 0)
        if item_tipo:
            bien_id = item_tipo.data(Qt.UserRole)
            if bien_id is not None:
                self.controller.seleccionar_bien(int(bien_id))

    def mostrar_detalle_bien(self, bien_vo):
        self.bien_actual_vo = bien_vo
        self.btn_editar.setEnabled(True)
        self.btn_eliminar.setEnabled(True)
        precio_str = f"{bien_vo.precio:.2f} €" if isinstance(bien_vo.precio, (int, float)) else str(bien_vo.precio)
        self.lbl_detalles.setText(
            f"<b>ID:</b> {bien_vo.BienID}<br>"
            f"<b>Tipo:</b> {bien_vo.tipo}<br>"
            f"<b>Cantidad:</b> {bien_vo.cantidad}<br>"
            f"<b>Precio:</b> {precio_str}"
        )
        self.lbl_detalles.setWordWrap(True)

    def mostrar_mensaje_vacio(self):
        self.bien_actual_vo = None
        self.btn_editar.setEnabled(False)
        self.btn_eliminar.setEnabled(False)
        self.lbl_detalles.setText("Selecciona un bien para ver sus detalles")

    def abrir_formulario_crear(self):
        from vistas.codigo.formulario_bien_vista import FormularioBienDialog
        dialogo = FormularioBienDialog(parent=self)
        if dialogo.exec_() == QDialog.Accepted:
            self.controller.añadir_bien(dialogo.obtener_datos())

    def abrir_formulario_editar(self):
        if not self.bien_actual_vo:
            return
        from vistas.codigo.formulario_bien_vista import FormularioBienDialog
        dialogo = FormularioBienDialog(bien_vo=self.bien_actual_vo, parent=self)
        if dialogo.exec_() == QDialog.Accepted:
            self.controller.actualizar_bien(self.bien_actual_vo.BienID, dialogo.obtener_datos())

    def _eliminar_bien_actual(self):
        if self.bien_actual_vo:
            self.confirmar_eliminacion(self.bien_actual_vo.BienID)

    def confirmar_eliminacion(self, bien_id):
        resp = QMessageBox.question(self, "Confirmar Eliminación",
                                    f"¿Seguro que deseas eliminar el bien con ID {bien_id}?",
                                    QMessageBox.Yes | QMessageBox.No)
        if resp == QMessageBox.Yes:
            self.controller.eliminar_bien(bien_id)

    def mostrar_mensaje_exito(self, msg):
        QMessageBox.information(self, "Éxito", msg)

    def mostrar_mensaje_error(self, msg):
        QMessageBox.critical(self, "Error", msg)