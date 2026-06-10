# archivo: vistas/formulario_editar_vista.py
import os
from PyQt5.QtWidgets import QDialog, QCheckBox, QVBoxLayout, QWidget
from PyQt5.QtCore import Qt
from PyQt5 import uic

UI_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "formulario_editar_vista.ui")

class FormularioEditarDialog(QDialog):
    def __init__(self, parent, miembro_vo, lista_departamentos, lista_grupos, rol_operador="PRESIDENTE"):
        super().__init__(parent)
        self.es_edicion = miembro_vo is not None

        # Carga el .ui — widgets: txt_dni, txt_nombre, txt_apellido, txt_telefono,
        # txt_correo, cb_grado, cb_rol, scroll_deptos, scroll_grupos,
        # layout_deptos_dinamicos, layout_grupos_dinamicos, buttons
        uic.loadUi(UI_PATH, self)

        self.setWindowTitle("Editar Miembro" if self.es_edicion else "Registrar Nuevo Miembro")
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowContextHelpButtonHint)

        # Rellena los campos básicos si es edición
        if miembro_vo:
            self.txt_dni.setText(str(getattr(miembro_vo, 'DNI', '') or ''))
            self.txt_nombre.setText(str(getattr(miembro_vo, 'Name', '') or ''))
            self.txt_apellido.setText(str(getattr(miembro_vo, 'Surname', '') or ''))
            self.txt_telefono.setText(str(getattr(miembro_vo, 'Telefono', '') or ''))
            self.txt_correo.setText(str(getattr(miembro_vo, 'Email', '') or ''))

        # Configura el ComboBox de roles según el rol del operador
        rol_actual = str(getattr(miembro_vo, 'Rol', 'MIEMBRO')).strip().upper() if miembro_vo else "MIEMBRO"
        rol_op = str(rol_operador).strip().upper()

        self.cb_rol.clear()
        if rol_op == "PRESIDENTE":
            self.cb_rol.addItems(["PRESIDENTE", "SECRETARIO", "TESORERO", "JEFE DEPARTAMENTO", "MIEMBRO"])
        elif rol_op == "JEFE DEPARTAMENTO":
            if rol_actual == "PRESIDENTE":
                self.cb_rol.addItems(["PRESIDENTE"])
                self.cb_rol.setEnabled(False)
            else:
                self.cb_rol.addItems(["SECRETARIO", "TESORERO", "JEFE DEPARTAMENTO", "MIEMBRO"])
        else:
            self.cb_rol.addItems([rol_actual])
            self.cb_rol.setEnabled(False)

        # Selecciona el rol actual en el combo
        idx = self.cb_rol.findText(rol_actual)
        if idx >= 0:
            self.cb_rol.setCurrentIndex(idx)

        # Rellena los checkboxes de departamentos dinámicamente en el scroll del .ui
        self.dict_check_deptos = {}
        deptos_actuales = []
        if miembro_vo:
            dep_str = str(getattr(miembro_vo, 'Departamento', ''))
            if dep_str and dep_str != "Ninguno":
                deptos_actuales = [d.strip() for d in dep_str.split(',')]

        widget_deptos = QWidget()
        layout_deptos = QVBoxLayout(widget_deptos)
        for depto in lista_departamentos:
            depto_str = str(depto).strip()
            cb = QCheckBox(depto_str)
            cb.setChecked(depto_str in deptos_actuales)
            layout_deptos.addWidget(cb)
            self.dict_check_deptos[depto_str] = cb
        self.scroll_deptos.setWidget(widget_deptos)

        # Rellena los checkboxes de grupos dinámicamente en el scroll del .ui
        self.dict_check_grupos = {}
        grupos_actuales = []
        if miembro_vo:
            grp_str = str(getattr(miembro_vo, 'Grupo', ''))
            if grp_str and grp_str != "Ninguno":
                grupos_actuales = [g.strip() for g in grp_str.split(',')]

        widget_grupos = QWidget()
        layout_grupos = QVBoxLayout(widget_grupos)
        for g in lista_grupos:
            nombre_grupo = g["nombre"] if isinstance(g, dict) and "nombre" in g else str(g)
            nombre_grupo = nombre_grupo.strip()
            cb = QCheckBox(nombre_grupo)
            cb.setChecked(nombre_grupo in grupos_actuales)
            layout_grupos.addWidget(cb)
            self.dict_check_grupos[nombre_grupo] = cb
        self.scroll_grupos.setWidget(widget_grupos)

        # Conecta los botones del QDialogButtonBox del .ui
        self.buttons.accepted.connect(self.accept)
        self.buttons.rejected.connect(self.reject)

    def obtener_datos(self):
        return {
            "dni":               self.txt_dni.text().strip(),
            "nombre":            self.txt_nombre.text().strip(),
            "apellido":          self.txt_apellido.text().strip(),
            "telefono":          self.txt_telefono.text().strip(),
            "email":             self.txt_correo.text().strip(),
            "rol":               self.cb_rol.currentText(),
            "departamentos_lista": [d for d, cb in self.dict_check_deptos.items() if cb.isChecked()],
            "grupos_lista":        [g for g, cb in self.dict_check_grupos.items() if cb.isChecked()]
        }