# archivo: vistas/gestion_bienes_view.py
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, \
                             QTableWidget, QTableWidgetItem, QFrame, QAbstractItemView, \
                             QHeaderView, QPushButton, QMessageBox, QDialog)
from PyQt5.QtCore import Qt

class GestionBienesView(QWidget):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self.bien_actual_vo = None 
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("SGA - Gestión de Inventario de Bienes")
        self.resize(950, 600)
        self.setStyleSheet("background-color: #F8F9FA; font-family: 'Segoe UI', Arial;")

        layout_principal = QHBoxLayout(self)
        layout_principal.setContentsMargins(20, 20, 20, 20)
        layout_principal.setSpacing(20)

        # =================================================================
        # PANEL IZQUIERDO: TABLA DE INVENTARIO GENERAL
        # =================================================================
        panel_izquierdo = QVBoxLayout()
        
        lbl_titulo = QLabel("Inventario de Bienes")
        lbl_titulo.setStyleSheet("font-size: 18px; font-weight: bold; color: #2C3E50; margin-bottom: 10px;")
        panel_izquierdo.addWidget(lbl_titulo)

        # Condición 1: Pasamos de 4 a 3 columnas (Eliminamos visualmente la columna ID)
        self.tabla_bienes = QTableWidget()
        self.tabla_bienes.setColumnCount(3)
        self.tabla_bienes.setHorizontalHeaderLabels(["Tipo", "Cantidad", "Precio"])
        self.tabla_bienes.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.tabla_bienes.setSelectionMode(QAbstractItemView.SingleSelection)
        self.tabla_bienes.setEditTriggers(QAbstractItemView.NoEditTriggers)
        
        header = self.tabla_bienes.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.Stretch)         # El Tipo se expande
        header.setSectionResizeMode(1, QHeaderView.ResizeToContents) # Cantidad ajustada
        header.setSectionResizeMode(2, QHeaderView.ResizeToContents) # Precio ajustado
        
        self.tabla_bienes.itemSelectionChanged.connect(self.on_fila_seleccionada)
        panel_izquierdo.addWidget(self.tabla_bienes)

        # Botón de inserción directa
        self.btn_anadir = QPushButton("+ Añadir Nuevo Bien")
        self.btn_anadir.setStyleSheet("""
            QPushButton { background-color: #2ECC71; color: white; font-weight: bold; padding: 10px; border-radius: 5px; border: none; font-size: 13px; }
            QPushButton:hover { background-color: #27AE60; }
        """)
        self.btn_anadir.clicked.connect(self.abrir_formulario_crear)
        panel_izquierdo.addWidget(self.btn_anadir)

        # =================================================================
        # PANEL DERECHO: DETALLES Y ACCIONES EXCLUSIVAS
        # =================================================================
        self.layout_derecho = QVBoxLayout()
        self.frame_derecho = QFrame()
        self.frame_derecho.setFrameShape(QFrame.StyledPanel)
        self.frame_derecho.setStyleSheet("background-color: #FFFFFF; border: 1px solid #E0E0E0; border-radius: 8px;")
        self.frame_derecho.setLayout(self.layout_derecho)
        
        layout_principal.addLayout(panel_izquierdo, 6)
        layout_principal.addWidget(self.frame_derecho, 4)

        self.mostrar_mensaje_vacio()

    def llenar_tabla_bienes(self, lista_bienes):
        """Llena la tabla ocultando el ID en los metadatos de la celda"""
        self.tabla_bienes.setRowCount(0)
        for bien in lista_bienes:
            row = self.tabla_bienes.rowCount()
            self.tabla_bienes.insertRow(row)

            # Guardamos el ID de forma oculta en la celda del Tipo mediante 'Qt.UserRole'
            item_tipo = QTableWidgetItem(bien["tipo"])
            item_tipo.setData(Qt.UserRole, bien["id"]) 
            
            item_cantidad = QTableWidgetItem(str(bien["cantidad"]))
            item_cantidad.setTextAlignment(Qt.AlignCenter)
            
            item_precio = QTableWidgetItem(bien["precio"])
            item_precio.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)

            # Insertamos solo en las 3 columnas visibles
            self.tabla_bienes.setItem(row, 0, item_tipo)
            self.tabla_bienes.setItem(row, 1, item_cantidad)
            self.tabla_bienes.setItem(row, 2, item_precio)

    def on_fila_seleccionada(self):
        filas_seleccionadas = self.tabla_bienes.selectedItems()
        if not filas_seleccionadas:
            return
        
        # Recuperamos el ID oculto de la primera columna (Tipo)
        item_tipo = self.tabla_bienes.item(self.tabla_bienes.currentRow(), 0)
        if item_tipo:
            bien_id = item_tipo.data(Qt.UserRole)
            if bien_id is not None:
                self.controller.seleccionar_bien(int(bien_id))

    def mostrar_detalle_bien(self, bien_vo):
        self.bien_actual_vo = bien_vo
        self.limpiar_layout_derecho()

        lbl_title = QLabel("Detalle del Bien / Activo")
        lbl_title.setStyleSheet("font-size: 16px; font-weight: bold; color: #2C3E50; margin-bottom: 15px; border: none;")
        self.layout_derecho.addWidget(lbl_title)

        def agregar_campo(lbl_text, val_text):
            layout_h = QHBoxLayout()
            l_lbl = QLabel(f"<b>{lbl_text}:</b>")
            l_lbl.setStyleSheet("font-size: 13px; color: #34495E; border: none;")
            l_val = QLabel(str(val_text))
            l_val.setStyleSheet("font-size: 13px; color: #2C3E50; border: none;")
            layout_h.addWidget(l_lbl)
            layout_h.addWidget(l_val)
            self.layout_derecho.addLayout(layout_h)

        # Condición 1: El ID del Bien se muestra de manera exclusiva en este panel de detalles
        agregar_campo("ID Bien", bien_vo.BienID)
        agregar_campo("Tipo", bien_vo.tipo)
        agregar_campo("Cantidad Disp.", bien_vo.cantidad)
        agregar_campo("Precio Unitario", f"{bien_vo.precio:.2f} €" if isinstance(bien_vo.precio, (int, float)) else str(bien_vo.precio))
        
        # Condición 2: Se elimina permanentemente el atributo 'Tesoreros Asignados' de la vista de detalles

        self.layout_derecho.addSpacing(20)

        # Acciones operativas
        layout_btn = QHBoxLayout()
        btn_editar = QPushButton("Editar Ficha")
        btn_editar.setStyleSheet("background-color: #3498DB; color: white; font-weight: bold; padding: 8px; border-radius: 4px; border: none;")
        btn_editar.clicked.connect(self.abrir_formulario_editar)
        
        btn_eliminar = QPushButton("Eliminar")
        btn_eliminar.setStyleSheet("background-color: #E74C3C; color: white; font-weight: bold; padding: 8px; border-radius: 4px; border: none;")
        btn_eliminar.clicked.connect(lambda: self.confirmar_eliminacion(bien_vo.BienID))

        layout_btn.addWidget(btn_editar)
        layout_btn.addWidget(btn_eliminar)
        self.layout_derecho.addLayout(layout_btn)
        self.layout_derecho.addStretch()

    def mostrar_mensaje_vacio(self):
        self.limpiar_layout_derecho()
        lbl_vacio = QLabel("Selecciona un bien de la lista izquierda para ver su información detallada.")
        lbl_vacio.setStyleSheet("color: #888888; font-size: 13px; font-style: italic; border: none;")
        lbl_vacio.setAlignment(Qt.AlignCenter)
        lbl_vacio.setWordWrap(True)
        self.layout_derecho.addWidget(lbl_vacio)

    def limpiar_layout_derecho(self):
        while self.layout_derecho.count():
            item = self.layout_derecho.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()
            elif item.layout():
                self.limpiar_sub_layout(item.layout())

    def limpiar_sub_layout(self, layout):
        while layout.count():
            item = layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()

    def abrir_formulario_crear(self):
        from vistas.formulario_bien_vista import FormularioBienDialog
        dialogo = FormularioBienDialog(parent=self)
        if dialogo.exec_() == QDialog.Accepted:
            datos = dialogo.obtener_datos()
            self.controller.añadir_bien(datos)

    def abrir_formulario_editar(self):
        if not self.bien_actual_vo: return
        from vistas.formulario_bien_vista import FormularioBienDialog
        dialogo = FormularioBienDialog(bien_vo=self.bien_actual_vo, parent=self)
        if dialogo.exec_() == QDialog.Accepted:
            datos = dialogo.obtener_datos()
            self.controller.actualizar_bien(self.bien_actual_vo.BienID, datos)

    def confirmar_eliminacion(self, bien_id):
        msg = QMessageBox.question(self, "Confirmar Eliminación", 
                                   f"¿Seguro que deseas eliminar permanentemente el bien con ID {bien_id}?",
                                   QMessageBox.Yes | QMessageBox.No)
        if msg == QMessageBox.Yes:
            self.controller.eliminar_bien(bien_id)

    def mostrar_mensaje_exito(self, msg):
        QMessageBox.information(self, "Éxito", msg)

    def mostrar_mensaje_error(self, msg):
        QMessageBox.critical(self, "Error", msg)