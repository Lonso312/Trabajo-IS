# archivo: vistas/gestion_miembros_view.py
import os
from PyQt5.QtWidgets import QWidget, QMessageBox, QTableWidgetItem, QDialog, QHeaderView, QAbstractItemView
from PyQt5.QtCore import Qt
from PyQt5 import uic

UI_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "gestion_miembros_view.ui")

class GestionMiembrosView(QWidget):
    def __init__(self, callback_filtrar, callback_seleccionar_miembro,
                 callback_aceptar, callback_eliminar, callback_actualizar, controller):
        super().__init__()
        self.callback_filtrar             = callback_filtrar
        self.callback_seleccionar_miembro = callback_seleccionar_miembro
        self.callback_aceptar             = callback_aceptar
        self.callback_eliminar            = callback_eliminar
        self.callback_actualizar          = callback_actualizar
        self.controller                   = controller
        self.miembro_actual_vo            = None

        # Carga el .ui — widgets: lbl_titulo, cb_filtro_estado, cb_filtro_depto,
        # tabla_miembros, panel_derecho, layout_derecho, lbl_perfil,
        # btn_aceptar, btn_registrar, btn_actualizar, btn_eliminar
        uic.loadUi(UI_PATH, self)

        # Configura la tabla
        self.tabla_miembros.setColumnCount(3)
        self.tabla_miembros.setHorizontalHeaderLabels(["Nombre Completo", "Rol", "Correo Electrónico"])
        self.tabla_miembros.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.tabla_miembros.setSelectionMode(QAbstractItemView.SingleSelection)
        self.tabla_miembros.setEditTriggers(QAbstractItemView.NoEditTriggers)

        header = self.tabla_miembros.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.Stretch)
        header.setSectionResizeMode(1, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(2, QHeaderView.Stretch)

        # Conecta señales
        self.tabla_miembros.itemSelectionChanged.connect(self.on_fila_seleccionada)
        self.cb_filtro_depto.currentTextChanged.connect(self.callback_filtrar)
        self.btn_aceptar.clicked.connect(self._aceptar_actual)
        self.btn_actualizar.clicked.connect(self.abrir_dialogo_edicion)
        self.btn_eliminar.clicked.connect(self._eliminar_actual)
        self.btn_registrar.clicked.connect(self.abrir_dialogo_agregar_miembro)

        # Estado inicial: botones deshabilitados hasta seleccionar un miembro
        self._set_botones_habilitados(False)
        self.lbl_perfil.setText("Selecciona un miembro para ver su ficha")

    # =================================================================
    # MÉTODOS DE DATOS
    # =================================================================

    def llenar_combo_departamentos(self, lista_departamentos):
        self.cb_filtro_depto.blockSignals(True)
        self.cb_filtro_depto.clear()
        self.cb_filtro_depto.addItem("Todos")
        for depto in lista_departamentos:
            self.cb_filtro_depto.addItem(str(depto))
        self.cb_filtro_depto.blockSignals(False)

    def llenar_tabla_miembros(self, lista_miembros):
        self.tabla_miembros.blockSignals(True)
        self.tabla_miembros.setRowCount(0)
        for miembro in lista_miembros:
            row = self.tabla_miembros.rowCount()
            self.tabla_miembros.insertRow(row)

            item_nombre = QTableWidgetItem(str(miembro["nombre_completo"]))
            item_nombre.setData(Qt.UserRole, miembro["id"])

            self.tabla_miembros.setItem(row, 0, item_nombre)
            self.tabla_miembros.setItem(row, 1, QTableWidgetItem(str(miembro["rol"])))
            self.tabla_miembros.setItem(row, 2, QTableWidgetItem(str(miembro["email"])))
        self.tabla_miembros.blockSignals(False)
        self.mostrar_mensaje_vacio()

    def mostrar_panel_derecho(self, miembro_vo):
        self.miembro_actual_vo = miembro_vo
        self._set_botones_habilitados(True)

        # Bloquea el botón Aceptar si ya está aceptado
        self.btn_aceptar.setEnabled(miembro_vo.Aceptado != 1)

        # Bloquea eliminar si es Presidente y el operador no tiene rango
        rol_op = self._obtener_rol_operador()
        es_presidente = str(miembro_vo.Rol).strip().upper() == "PRESIDENTE"
        sin_permiso = rol_op in ["JEFE DEPARTAMENTO", "TESORERO", "SECRETARIO"]
        self.btn_eliminar.setEnabled(not (es_presidente and sin_permiso))

        # Actualiza el label de la ficha (definido en el .ui como lbl_perfil)
        estado = "✔ Aceptado" if miembro_vo.Aceptado == 1 else "⏳ Pendiente"
        self.lbl_perfil.setText(
            f"<b>{miembro_vo.Name} {miembro_vo.Surname}</b><br>"
            f"<b>Usuario:</b> {miembro_vo.NombreUsuario}<br>"
            f"<b>Rol:</b> {miembro_vo.Rol}<br>"
            f"<b>DNI:</b> {miembro_vo.DNI}<br>"
            f"<b>Teléfono:</b> {miembro_vo.Telefono}<br>"
            f"<b>Email:</b> {miembro_vo.Email}<br>"
            f"<b>Departamentos:</b> {getattr(miembro_vo, 'Departamento', 'Ninguno')}<br>"
            f"<b>Grupos:</b> {getattr(miembro_vo, 'Grupo', 'Ninguno')}<br>"
            f"<b>Estado:</b> {estado}"
        )
        self.lbl_perfil.setWordWrap(True)

    def mostrar_mensaje_vacio(self):
        self.miembro_actual_vo = None
        self._set_botones_habilitados(False)
        self.lbl_perfil.setText("Selecciona un miembro para ver su ficha")

    def _set_botones_habilitados(self, habilitado):
        self.btn_aceptar.setEnabled(habilitado)
        self.btn_actualizar.setEnabled(habilitado)
        self.btn_eliminar.setEnabled(habilitado)

    # =================================================================
    # ACCIONES
    # =================================================================

    def on_fila_seleccionada(self):
        item = self.tabla_miembros.item(self.tabla_miembros.currentRow(), 0)
        if item:
            usuario_id = item.data(Qt.UserRole)
            if usuario_id is not None:
                self.callback_seleccionar_miembro(int(usuario_id))

    def _aceptar_actual(self):
        if self.miembro_actual_vo:
            self.callback_aceptar(self.miembro_actual_vo.UsuarioID)

    def _eliminar_actual(self):
        if self.miembro_actual_vo:
            self.confirmar_eliminacion(self.miembro_actual_vo.UsuarioID)

    def abrir_dialogo_edicion(self):
        if not self.miembro_actual_vo:
            return
        from vistas.formulario_editar_vista import FormularioEditarDialog
        deptos, grupos = self.controller.obtener_listados_para_edicion()
        dialogo = FormularioEditarDialog(self, self.miembro_actual_vo, deptos, grupos, self._obtener_rol_operador())
        if dialogo.exec_() == QDialog.Accepted:
            datos = dialogo.obtener_datos()
            self.callback_actualizar(
                self.miembro_actual_vo.UsuarioID,
                datos["dni"], datos["nombre"], datos["apellido"],
                datos["telefono"], datos["email"], datos["rol"],
                datos["departamentos_lista"], datos["grupos_lista"]
            )

    def confirmar_eliminacion(self, usuario_id):
        rol_op = self._obtener_rol_operador()
        if self.miembro_actual_vo and str(self.miembro_actual_vo.Rol).strip().upper() == "PRESIDENTE" \
                and rol_op in ["JEFE DEPARTAMENTO", "TESORERO", "SECRETARIO"]:
            QMessageBox.critical(self, "Acceso Denegado", "No puedes eliminar al Presidente.")
            return
        resp = QMessageBox.question(self, "Confirmar Eliminación",
                                    "¿Estás seguro de eliminar a este miembro?\nEsta acción no se puede deshacer.",
                                    QMessageBox.Yes | QMessageBox.No)
        if resp == QMessageBox.Yes:
            self.callback_eliminar(usuario_id)

    def abrir_dialogo_agregar_miembro(self):
        from vistas.formulario_editar_vista import FormularioEditarDialog
        deptos, grupos = self.controller.obtener_listados_para_edicion()
        rol_op = self._obtener_rol_operador()
        dialogo = FormularioEditarDialog(self, None, deptos, grupos, rol_op)
        if dialogo.exec_() == QDialog.Accepted:
            datos = dialogo.obtener_datos()
            exito, mensaje = self.controller.procesar_agregar_miembro(rol_op, datos)
            if exito:
                QMessageBox.information(self, "Éxito", mensaje)
                self.callback_filtrar(self.obtener_filtro_actual())
            else:
                QMessageBox.critical(self, "Error al Registrar", mensaje)

    # =================================================================
    # AUXILIARES
    # =================================================================

    def obtener_filtro_actual(self):
        return self.cb_filtro_depto.currentText()

    def limpiar_detalle(self):
        self.mostrar_mensaje_vacio()

    def mostrar_mensaje_exito(self, mensaje):
        QMessageBox.information(self, "Operación Exitosa", mensaje)

    def mostrar_mensaje_error(self, mensaje):
        QMessageBox.critical(self, "Error de Operación", mensaje)

    def _obtener_rol_operador(self):
        if not hasattr(self, 'controller') or not self.controller:
            return "MIEMBRO"
        user = getattr(self.controller, 'usuario_logueado', None)
        if not user:
            return "MIEMBRO"
        if isinstance(user, dict):
            return str(user.get("Rol", user.get("rol", "MIEMBRO"))).strip().upper()
        return str(getattr(user, 'Rol', getattr(user, 'rol', 'MIEMBRO'))).strip().upper()