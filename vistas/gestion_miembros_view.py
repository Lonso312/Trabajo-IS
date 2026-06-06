# archivo: vistas/gestion_miembros_view.py
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, QComboBox, 
                             QTableWidget, QTableWidgetItem, QFrame, QAbstractItemView, 
                             QHeaderView, QPushButton, QMessageBox, QDialog)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont

# Importamos la ventana modal de edición aislada
from vistas.formulario_editar_vista import FormularioEditarDialog 

class GestionMiembrosView(QWidget):
    def __init__(self, callback_filtrar, callback_seleccionar_miembro, callback_aceptar, callback_eliminar, callback_actualizar, controller):
        super().__init__()
        self.callback_filtrar = callback_filtrar
        self.callback_seleccionar_miembro = callback_seleccionar_miembro
        self.callback_aceptar = callback_aceptar
        self.callback_eliminar = callback_eliminar
        self.callback_actualizar = callback_actualizar
        self.controller = controller # 
        
        self.miembro_actual_vo = None 
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("SGA - Gestión de Miembros Administrativos")
        self.resize(950, 600)
        self.setStyleSheet("background-color: #F8F9FA; font-family: 'Segoe UI', Arial;")

        layout_principal = QHBoxLayout(self)
        layout_principal.setContentsMargins(20, 20, 20, 20)
        layout_principal.setSpacing(20)

        # =================================================================
        # PANEL IZQUIERDO: FILTRO Y TABLA DE MIEMBROS
        # =================================================================
        panel_izquierdo = QVBoxLayout()
        fila_filtro = QHBoxLayout()
        
        lbl_titulo = QLabel("Miembros del Sistema")
        lbl_titulo.setStyleSheet("font-size: 18px; font-weight: bold; color: #333333;")
        fila_filtro.addWidget(lbl_titulo)
        fila_filtro.addStretch()

        lbl_filtrar = QLabel("Filtrar por Departamento:")
        lbl_filtrar.setStyleSheet("font-size: 13px; font-weight: bold; color: #555555;")
        fila_filtro.addWidget(lbl_filtrar)

        self.combo_departamentos = QComboBox()
        self.combo_departamentos.addItem("Todos")
        self.combo_departamentos.setFixedWidth(180)
        self.combo_departamentos.setStyleSheet("""
            QComboBox {
                background-color: #FFFFFF;
                border: 2px solid #000000;
                border-radius: 5px;
                padding: 4px 10px;
                font-size: 13px;
            }
            QComboBox::drop-down {
                border: none;
            }
        """)
        self.combo_departamentos.currentTextChanged.connect(self.callback_filtrar)
        fila_filtro.addWidget(self.combo_departamentos)
        
        panel_izquierdo.addLayout(fila_filtro)
        panel_izquierdo.addSpacing(10)

        # Tabla de Miembros
        self.tabla_miembros = QTableWidget()
        self.tabla_miembros.setColumnCount(3)
        self.tabla_miembros.setHorizontalHeaderLabels(["Nombre Completo", "Rol", "Correo Electrónico"])
        self.tabla_miembros.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.tabla_miembros.setSelectionMode(QAbstractItemView.SingleSelection)
        self.tabla_miembros.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.tabla_miembros.setStyleSheet("""
            QTableWidget {
                background-color: #FFFFFF;
                border: 2px solid #000000;
                border-radius: 5px;
                gridline-color: #E0E0E0;
            }
            QHeaderView::section {
                background-color: #EFEFEF;
                color: #000000;
                font-weight: bold;
                font-size: 13px;
                border: 1px solid #000000;
                padding: 5px;
            }
            QTableWidget::item:selected {
                background-color: #2ECC71;
                color: #FFFFFF;
            }
        """)
        
        header = self.tabla_miembros.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.Stretch)
        header.setSectionResizeMode(1, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(2, QHeaderView.Stretch)
        
        self.tabla_miembros.itemSelectionChanged.connect(self.on_fila_seleccionada)
        
        panel_izquierdo.addWidget(self.tabla_miembros)
        layout_principal.addLayout(panel_izquierdo, stretch=3)

        # =================================================================
        # PANEL DERECHO: DETALLES DE UN MIEMBRO
        # =================================================================
        self.panel_derecho = QFrame()
        self.panel_derecho.setStyleSheet("QFrame { background-color: #FFFFFF; border: 2px solid #000000; border-radius: 5px; }")
        self.layout_derecho = QVBoxLayout(self.panel_derecho)
        self.layout_derecho.setContentsMargins(20, 20, 20, 20)
        self.mostrar_mensaje_vacio()

        layout_principal.addWidget(self.panel_derecho, stretch=2)

    # =================================================================
    # MÉTODOS DE CONTROL DE DATOS
    # =================================================================

    def llenar_combo_departamentos(self, lista_departamentos):
        self.combo_departamentos.blockSignals(True) 
        self.combo_departamentos.clear()
        self.combo_departamentos.addItem("Todos")
        for depto in lista_departamentos:
            self.combo_departamentos.addItem(str(depto))
        self.combo_departamentos.blockSignals(False)

    def llenar_tabla_miembros(self, lista_miembros):
        self.tabla_miembros.blockSignals(True)
        self.tabla_miembros.setRowCount(0)
        
        for miembro in lista_miembros:
            row_position = self.tabla_miembros.rowCount()
            self.tabla_miembros.insertRow(row_position)
            
            item_nombre = QTableWidgetItem(str(miembro["nombre_completo"]))
            item_nombre.setData(Qt.UserRole, miembro["id"]) 
            
            item_rol = QTableWidgetItem(str(miembro["rol"]))        
            item_email = QTableWidgetItem(str(miembro["email"]))

            self.tabla_miembros.setItem(row_position, 0, item_nombre)
            self.tabla_miembros.setItem(row_position, 1, item_rol)
            self.tabla_miembros.setItem(row_position, 2, item_email)
            
        self.tabla_miembros.blockSignals(False)
        self.mostrar_mensaje_vacio()

    def mostrar_panel_derecho(self, miembro_vo):
        self.miembro_actual_vo = miembro_vo
        self.limpiar_layout_derecho()

        lbl_ficha = QLabel("Ficha del Miembro")
        lbl_ficha.setStyleSheet("font-size: 16px; font-weight: bold; color: #6B46C1; border: none; margin-bottom: 10px;")
        self.layout_derecho.addWidget(lbl_ficha)

        def agregar_campo(titulo, valor):
            # Forzamos conversión a string nativo de Python para curarnos en salud
            texto_valor = str(valor).strip() if valor else "No asignado"
            lbl = QLabel(f"<b>{titulo}:</b> {texto_valor}")
            lbl.setStyleSheet("font-size: 13px; color: #333333; border: none; margin-bottom: 6px;")
            self.layout_derecho.addWidget(lbl)

        # Datos básicos del Miembro extraídos de tu tabla Miembros
        agregar_campo("Nombre completo", f"{miembro_vo.Name} {miembro_vo.Surname}")
        agregar_campo("Usuario", miembro_vo.NombreUsuario)
        agregar_campo("Rol asignado", miembro_vo.Rol)
        agregar_campo("DNI / Identificación", miembro_vo.DNI)
        agregar_campo("Teléfono", miembro_vo.Telefono)
        agregar_campo("Email", miembro_vo.Email)
        
        agregar_campo("Departamentos Asignados", getattr(miembro_vo, 'Departamento', 'Ninguno'))
        agregar_campo("Grupos de Trabajo", getattr(miembro_vo, 'Grupo', 'Ninguno'))
        
        # Estado de aceptación
        estado_texto = "Aceptado en el Sistema" if miembro_vo.Aceptado == 1 else "Pendiente de Aceptación"
        lbl_estado = QLabel(f"<b>Estado:</b> {estado_texto}")
        if miembro_vo.Aceptado == 1:
            lbl_estado.setStyleSheet("font-size: 13px; color: #2ECC71; font-weight: bold; border: none;")
        else:
            lbl_estado.setStyleSheet("font-size: 13px; color: #E74C3C; font-weight: bold; border: none;")
            
        self.layout_derecho.addWidget(lbl_estado)
        self.layout_derecho.addSpacing(15)

        style_botones = """
            QPushButton {
                color: #FFFFFF;
                font-weight: bold;
                font-size: 12px;
                border: 2px solid #000000;
                border-radius: 5px;
                padding: 6px;
            }
            QPushButton:hover { opacity: 0.9; }
        """
        
        if miembro_vo.Aceptado != 1:
            btn_aceptar = QPushButton("Aceptar en el Sistema")
            btn_aceptar.setStyleSheet(style_botones + "QPushButton { background-color: #2ECC71; }")
            btn_aceptar.clicked.connect(lambda: self.callback_aceptar(miembro_vo.UsuarioID))
            self.layout_derecho.addWidget(btn_aceptar)
            
        btn_editar = QPushButton("Editar Datos")
        btn_editar.setStyleSheet(style_botones + "QPushButton { background-color: #3498DB; }")
        btn_editar.clicked.connect(self.abrir_dialogo_edicion)
        self.layout_derecho.addWidget(btn_editar)
        
        btn_eliminar = QPushButton("Eliminar Miembro")
        btn_eliminar.setStyleSheet(style_botones + "QPushButton { background-color: #E74C3C; }")
        btn_eliminar.clicked.connect(lambda: self.confirmar_eliminacion(miembro_vo.UsuarioID))
        self.layout_derecho.addWidget(btn_eliminar)

        self.layout_derecho.addStretch()

    def abrir_dialogo_edicion(self):
        if self.miembro_actual_vo:
            deptos, grupos = self.controller.obtener_listados_para_edicion(self.miembro_actual_vo)
            
            dialogo = FormularioEditarDialog(self, self.miembro_actual_vo, deptos, grupos)
            
            if dialogo.exec_() == QDialog.Accepted:
                datos = dialogo.obtener_datos()

                self.callback_actualizar(
                    self.miembro_actual_vo.UsuarioID,
                    datos["dni"], 
                    datos["nombre"], 
                    datos["apellido"],
                    datos["telefono"], 
                    datos["email"], 
                    datos["rol"],
                    datos["departamentos_lista"],  
                    datos["grupos_lista"]          
                )


    def confirmar_eliminacion(self, usuario_id):
        msg = QMessageBox.question(self, "Confirmar Eliminación", 
                                   "¿Estás completamente seguro de eliminar a este miembro?\nEsta acción no se puede deshacer.",
                                   QMessageBox.Yes | QMessageBox.No)
        if msg == QMessageBox.Yes:
            self.callback_eliminar(usuario_id)


    def mostrar_mensaje_vacio(self):
        self.limpiar_layout_derecho()
        lbl_vacio = QLabel("Selecciona un miembro de la lista izquierda para ver su información detallada.")
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

    def on_fila_seleccionada(self):
        filas_seleccionadas = self.tabla_miembros.selectedItems()
        if not filas_seleccionadas:
            return
            
        item_nombre = self.tabla_miembros.item(self.tabla_miembros.currentRow(), 0)
        if item_nombre:
            usuario_id = item_nombre.data(Qt.UserRole)
            if usuario_id is not None:
                self.callback_seleccionar_miembro(int(usuario_id))

    def obtener_filtro_actual(self):
        return self.combo_departamentos.currentText()

    def limpiar_detalle(self):
        self.limpiar_layout_derecho()

    def mostrar_mensaje_exito(self, mensaje):
        QMessageBox.information(self, "Operación Exitosa", mensaje)

    def mostrar_mensaje_error(self, mensaje):
        QMessageBox.critical(self, "Error de Operación", mensaje)