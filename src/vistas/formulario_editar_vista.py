# archivo: vistas/formulario_editar_vista.py
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QFormLayout, QLineEdit, QComboBox, QDialogButtonBox, QCheckBox, QScrollArea, QWidget
from PyQt5.QtCore import Qt

class FormularioEditarDialog(QDialog):
    def __init__(self, parent, miembro_vo, lista_departamentos, lista_grupos, rol_operador="PRESIDENTE"):
        super().__init__(parent)
        self.es_edicion = miembro_vo is not None
        self.setWindowTitle("Editar Miembro" if self.es_edicion else "Registrar Nuevo Miembro")
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowContextHelpButtonHint)
        self.setMinimumWidth(450)
        self.setMinimumHeight(550)
        
        layout = QVBoxLayout(self)
        form_layout = QFormLayout()

        dni_val = str(getattr(miembro_vo, 'DNI', '')) if getattr(miembro_vo, 'DNI', '') is not None else ""
        nombre_val = str(getattr(miembro_vo, 'Name', '')) if getattr(miembro_vo, 'Name', '') is not None else ""
        apellido_val = str(getattr(miembro_vo, 'Surname', '')) if getattr(miembro_vo, 'Surname', '') is not None else ""
        telefono_val = str(getattr(miembro_vo, 'Telefono', '')) if getattr(miembro_vo, 'Telefono', '') is not None else ""
        email_val = str(getattr(miembro_vo, 'Email', '')) if getattr(miembro_vo, 'Email', '') is not None else ""

        self.txt_dni = QLineEdit(dni_val)
        self.txt_nombre = QLineEdit(nombre_val)
        self.txt_apellido = QLineEdit(apellido_val)
        self.txt_telefono = QLineEdit(telefono_val)
        self.txt_email = QLineEdit(email_val)
        
        self.combo_rol = QComboBox()
        rol_actual = str(getattr(miembro_vo, 'Rol', 'MIEMBRO')).strip().upper() if miembro_vo else "MIEMBRO"
        
        
        rol_op_limpio = str(rol_operador).strip().upper()
        
        if rol_op_limpio == "PRESIDENTE":
            self.combo_rol.addItems(["PRESIDENTE", "SECRETARIO", "TESORERO", "JEFE DEPARTAMENTO", "MIEMBRO"])
            
        elif rol_op_limpio == "JEFE DEPARTAMENTO":
            if rol_actual == "PRESIDENTE":
                self.combo_rol.addItems(["PRESIDENTE"])
                self.combo_rol.setEnabled(False) 
            else:
                self.combo_rol.addItems(["SECRETARIO", "TESORERO", "JEFE DEPARTAMENTO", "MIEMBRO"])
                
        else:
            self.combo_rol.addItems([rol_actual])
            self.combo_rol.setEnabled(False)

        # Campos básicos agregados al layout
        form_layout.addRow("DNI / Identificación:", self.txt_dni)
        form_layout.addRow("Nombre:", self.txt_nombre)
        form_layout.addRow("Apellidos:", self.txt_apellido)
        form_layout.addRow("Teléfono:", self.txt_telefono)
        form_layout.addRow("Correo Electrónico:", self.txt_email)
        form_layout.addRow("Rol en Sistema:", self.combo_rol)

        self.dict_check_deptos = {}
        widget_deptos = QWidget()
        layout_deptos = QVBoxLayout(widget_deptos)
        
        deptos_actuales_str = str(getattr(miembro_vo, 'Departamento', ''))
        deptos_actuales = [d.strip() for d in deptos_actuales_str.split(',')] if deptos_actuales_str and deptos_actuales_str != "Ninguno" else []

        for depto in lista_departamentos:
            depto_str = str(depto).strip()
            cb = QCheckBox(depto_str)
            if depto_str in deptos_actuales:
                cb.setChecked(True)
            layout_deptos.addWidget(cb)
            self.dict_check_deptos[depto_str] = cb

        scroll_deptos = QScrollArea()
        scroll_deptos.setWidgetResizable(True)
        scroll_deptos.setWidget(widget_deptos)
        scroll_deptos.setFixedHeight(120)
        form_layout.addRow("Departamentos:", scroll_deptos)

        self.dict_check_grupos = {}
        widget_grupos = QWidget()
        layout_grupos = QVBoxLayout(widget_grupos)
        
        grupos_actuales_str = str(getattr(miembro_vo, 'Grupo', ''))
        grupos_actuales = [g.strip() for g in grupos_actuales_str.split(',')] if grupos_actuales_str and grupos_actuales_str != "Ninguno" else []

        for g in lista_grupos:
            if isinstance(g, dict) and "nombre" in g:
                nombre_crudo = g["nombre"]
            else:
                nombre_crudo = g

            nombre_grupo = str(nombre_crudo).strip()
            
            cb = QCheckBox(nombre_grupo)
            if nombre_grupo in grupos_actuales:
                cb.setChecked(True)
            layout_grupos.addWidget(cb)
            self.dict_check_grupos[nombre_grupo] = cb

        scroll_grupos = QScrollArea()
        scroll_grupos.setWidgetResizable(True)
        scroll_grupos.setWidget(widget_grupos)
        scroll_grupos.setFixedHeight(120)
        form_layout.addRow("Grupos de Trabajo:", scroll_grupos)

        layout.addLayout(form_layout)

        # Botones de Aceptar / Cancelar
        self.buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        self.buttons.accepted.connect(self.accept)
        self.buttons.rejected.connect(self.reject)
        layout.addWidget(self.buttons)

    def obtener_datos(self):
        """Retorna las listas de elementos seleccionados por el usuario"""
        deptos_seleccionados = [depto for depto, cb in self.dict_check_deptos.items() if cb.isChecked()]
        grupos_seleccionados = [grupo for grupo, cb in self.dict_check_grupos.items() if cb.isChecked()]
        
        return {
            "dni": self.txt_dni.text().strip(),
            "nombre": self.txt_nombre.text().strip(),
            "apellido": self.txt_apellido.text().strip(),
            "telefono": self.txt_telefono.text().strip(),
            "email": self.txt_email.text().strip(),
            "rol": self.combo_rol.currentText(),
            "departamentos_lista": deptos_seleccionados,
            "grupos_lista": grupos_seleccionados
        }