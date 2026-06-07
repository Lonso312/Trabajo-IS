# archivo: vistas/menu_view.py
from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                             QLabel, QPushButton, QFrame, QInputDialog, 
                             QDialog, QFormLayout, QLineEdit, QTextEdit, 
                             QDialogButtonBox, QMessageBox, QScrollArea, QComboBox) 
from PyQt5.QtCore import Qt

# =================================================================
# UN RECUADRO CLICABLE (PANEL IZQUIERDO)
# =================================================================
class TarjetaClicable(QFrame):
    def __init__(self, id_entidad, titulo, sub_1, callback_click, es_verde=False, parent=None):
        super().__init__(parent)
        self.id_entidad = id_entidad
        self.callback_click = callback_click
        
        self.estilo_blanco = "QFrame { background-color: #FFFFFF; border: 2px solid #000000; color: #000000; border-radius: 5px; }"
        self.estilo_verde = "QFrame { background-color: #2ECC71; border: 3px solid #000000; color: #FFFFFF; border-radius: 5px; }"
        
        if es_verde:
            self.setStyleSheet(self.estilo_verde)
        else:
            self.setStyleSheet(self.estilo_blanco)
            
        layout = QVBoxLayout(self)
        layout.setContentsMargins(15, 10, 15, 10)
        
        self.lbl_titulo = QLabel(str(titulo))
        self.lbl_titulo.setStyleSheet("font-weight: bold; font-size: 14px; border: none; background: transparent; color: inherit;")
        
        self.lbl_sub1 = QLabel(str(sub_1))
        self.lbl_sub1.setStyleSheet("font-size: 12px; border: none; background: transparent; color: inherit;")
        self.lbl_sub1.setAlignment(Qt.AlignRight)
        
        layout.addWidget(self.lbl_titulo)
        layout.addWidget(self.lbl_sub1)
        

    def mousePressEvent(self, event):
        """Detecta el clic del ratón y dispara el callback original"""
        if event.button() == Qt.LeftButton:
            self.callback_click(self.id_entidad, self)

    def marcar_activa(self, activa=True):
        """Cambia el color de la tarjeta de forma segura sin destruir su contenido"""
        if activa:
            self.setStyleSheet(self.estilo_verde)
        else:
            self.setStyleSheet(self.estilo_blanco)


# =================================================================
# VENTANA PRINCIPAL (PANEL DIVIDIDO)
# =================================================================
class MenuView(QMainWindow):
    def __init__(self, miembro, lista_grupos, callback_cargar_tareas, callback_abrir_gestion, callback_logout):
        super().__init__()
        self.miembro = miembro
        self.lista_grupos = lista_grupos  
        self.callback_cargar_tareas = callback_cargar_tareas  
        self.callback_abrir_gestion = callback_abrir_gestion
        self.callback_logout = callback_logout
        
        # Estas referencias se inyectarán desde main.py tras inicializar la vista
        self.grupo_controller = None
        self.tarea_controller = None
        self.bienes_controller = None  
        
        self.id_grupo_seleccionado = None  
        self.tarjetas_izquierda = []  
        self.init_ui()

    # archivo: vistas/menu_view.py

    def init_ui(self):
        self.setWindowTitle(f"SGA - Sistema de Gestión ({str(self.miembro.Rol)})")
        self.resize(1000, 650)
        self.setStyleSheet("background-color: #F8F9FA; font-family: 'Segoe UI', Arial;")

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(25, 20, 25, 25)

        # -------------------------------------------------------------
        # 1. BARRA SUPERIOR
        # -------------------------------------------------------------
        top_bar = QHBoxLayout()
        
        user_info_layout = QVBoxLayout()
        user_info_layout.setSpacing(4)
        
        nombre_limpio = str(self.miembro.Name)
        rol_limpio = str(self.miembro.Rol)
        lbl_usuario = QLabel(f"{nombre_limpio} : {rol_limpio}")
        lbl_usuario.setStyleSheet("font-size: 15px; font-weight: bold; color: #333333;")
        user_info_layout.addWidget(lbl_usuario)
        
        btn_cambiar_pass = QPushButton("Cambiar Contraseña")
        btn_cambiar_pass.setCursor(Qt.PointingHandCursor)
        btn_cambiar_pass.setStyleSheet("""
            QPushButton {
                background-color: #7F8C8D; color: white; font-weight: bold; font-size: 11px;
                padding: 3px 8px; border-radius: 4px; border: none;
            }
            QPushButton:hover { background-color: #95A5A6; }
        """)
        btn_cambiar_pass.clicked.connect(self.mostrar_dialogo_cambiar_pass)
        user_info_layout.addWidget(btn_cambiar_pass)
        
        top_bar.addLayout(user_info_layout)
        top_bar.addStretch()  
        
        # VALIDACIÓN VISUAL DEL ROL
        rol_limpio_check = str(self.miembro.Rol).strip().upper() if self.miembro.Rol else "MIEMBRO"
        self.es_admin = rol_limpio_check in ["PRESIDENTE", "JEFE DEPARTAMENTO"]
        self.es_tesorero = rol_limpio_check in ["TESORERO", "PRESIDENTE"] 
        if rol_limpio_check in ["PRESIDENTE", "SECRETARIO", "TESORERO", "JEFE DEPARTAMENTO"]:
            self.btn_gestionar_miembros = QPushButton("Gestionar Miembros")
            self.btn_gestionar_miembros.setCursor(Qt.PointingHandCursor)
            self.btn_gestionar_miembros.setStyleSheet("""
                QPushButton { background-color: #FFFFFF; border: 2px solid #6B46C1; border-radius: 10px; padding: 5px 15px; font-weight: bold; color: #6B46C1; }
                QPushButton:hover { background-color: #FAF5FF; border-color: #553C9A; color: #553C9A; }
            """)
            self.btn_gestionar_miembros.clicked.connect(self.callback_abrir_gestion)
            top_bar.addWidget(self.btn_gestionar_miembros)
            top_bar.addSpacing(10) 

        if rol_limpio_check in ["PRESIDENTE", "TESORERO", "JEFE DEPARTAMENTO"]:
            self.btn_bienes = QPushButton("Inventario")
            self.btn_bienes.setCursor(Qt.PointingHandCursor)
            self.btn_bienes.setStyleSheet("""
                QPushButton { background-color: #FFFFFF; border: 2px solid #2ECC71; border-radius: 10px; padding: 5px 15px; font-weight: bold; color: #2ECC71; }
                QPushButton:hover { background-color: #E8F8F5; border-color: #27AE60; color: #27AE60; }
            """)
            self.btn_bienes.clicked.connect(self.abrir_modulo_bienes)
            top_bar.addWidget(self.btn_bienes)
            top_bar.addSpacing(10)

        btn_logout = QPushButton("Cerrar Sesión")
        btn_logout.setCursor(Qt.PointingHandCursor)
        btn_logout.setStyleSheet("""
            QPushButton { background-color: #FFFFFF; border: 2px solid #000000; border-radius: 10px; padding: 5px 15px; font-weight: bold; color: #000000; }
            QPushButton:hover { background-color: #EFEFEF; }
        """)
        btn_logout.clicked.connect(self.callback_logout)
        top_bar.addWidget(btn_logout)
        
        main_layout.addLayout(top_bar)
        main_layout.addSpacing(15)

        # -------------------------------------------------------------
        # 2. CONTENIDO PRINCIPAL (Paneles izquierdo/derecho)
        # -------------------------------------------------------------
        content_layout = QHBoxLayout()
        
        # Área de scroll para el panel izquierdo
        self.scroll_izquierda = QScrollArea()
        self.scroll_izquierda.setWidgetResizable(True)
        self.scroll_izquierda.setStyleSheet("QScrollArea { border: none; background-color: transparent; }")
        
        self.widget_contenedor_izq = QWidget()
        self.widget_contenedor_izq.setStyleSheet("background-color: transparent;")
        self.left_layout = QVBoxLayout(self.widget_contenedor_izq)
        self.left_layout.setContentsMargins(0, 0, 5, 0)
        
        # Cargamos las tarjetas y la posible sección de tesorería
        self.cargar_grupos_izquierdos()
        
        self.scroll_izquierda.setWidget(self.widget_contenedor_izq)
        content_layout.addWidget(self.scroll_izquierda, stretch=2)  

        # Línea Divisora Central
        linea = QFrame()
        linea.setFrameShape(QFrame.VLine)
        linea.setStyleSheet("color: #A0A0A0; width: 2px; margin: 0px 15px;")
        content_layout.addWidget(linea)

        # Panel Derecho (Contenedor maestro de Tareas / Facturas)
        right_container = QFrame()
        right_container.setStyleSheet("background-color: #FFFFFF; border: 2px solid #000000; border-radius: 5px;")
        self.right_layout = QVBoxLayout(right_container)
        self.right_layout.setContentsMargins(20, 20, 20, 20)
        
        content_layout.addWidget(right_container, stretch=3)  
        main_layout.addLayout(content_layout)

        self.mostrar_mensaje_vacio()

    def cargar_grupos_izquierdos(self):
        """Vuelca dinámicamente las tarjetas reactivas de grupos y la sección de tesorería si aplica"""
        while self.left_layout.count():
            item = self.left_layout.takeAt(0)
            if item.widget(): 
                item.widget().deleteLater()

        self.tarjetas_izquierda.clear()

        # Título de sección Grupos
        lbl_seccion_grupos = QLabel("MIS GRUPOS")
        lbl_seccion_grupos.setStyleSheet("font-weight: bold; color: #555555; font-size: 11px; margin-bottom: 5px;")
        self.left_layout.addWidget(lbl_seccion_grupos)

        if hasattr(self, 'es_admin') and self.es_admin:
            self.btn_crear_grupo = QPushButton("+ Crear Nuevo Grupo")
            self.btn_crear_grupo.setCursor(Qt.PointingHandCursor)
            self.btn_crear_grupo.setStyleSheet("""
                QPushButton { background-color: #6B46C1; border: 2px solid #000000; border-radius: 5px; padding: 8px; font-weight: bold; color: #FFFFFF; margin-bottom: 10px; }
                QPushButton:hover { background-color: #553C9A; }
            """)
            self.btn_crear_grupo.clicked.connect(self.abrir_dialogo_crear_grupo)
            self.left_layout.addWidget(self.btn_crear_grupo)

        # Cargar grupos existentes
        for grupo in self.lista_grupos:
            nombre_grupo = str(grupo['nombre'])
            cant_miembros = str(grupo['cantidad_miembros'])
            
            tarjeta = TarjetaClicable(
                id_entidad=grupo['id'],
                titulo=nombre_grupo,
                sub_1=f"Miembros: {cant_miembros}",
                callback_click=self.grupo_seleccionado,
                es_verde=False
            )
            
            # Verificar si estaba seleccionado y no estamos en modo factura
            if self.id_grupo_seleccionado and int(grupo['id']) == int(self.id_grupo_seleccionado) and getattr(self, 'seccion_facturas_activa', False) == False:
                tarjeta.marcar_activa(True)

            self.left_layout.addWidget(tarjeta)
            self.tarjetas_izquierda.append(tarjeta)
        
        
        if hasattr(self, 'es_tesorero') and self.es_tesorero:
            self.left_layout.addSpacing(20)
            
            lbl_seccion_tesoreria = QLabel("TESORERÍA")
            lbl_seccion_tesoreria.setStyleSheet("font-weight: bold; color: #27AE60; font-size: 11px; margin-bottom: 5px;")
            self.left_layout.addWidget(lbl_seccion_tesoreria)
            
            # Usamos TarjetaClicable reutilizando el componente para mantener la estética uniforme
            self.tarjeta_facturas = TarjetaClicable(
                id_entidad=-99, # ID ficticio para identificar facturas
                titulo="Gestión de Facturas",
                sub_1="Crear y administrar",
                callback_click=self.abrir_seccion_facturas,
                es_verde=getattr(self, 'seccion_facturas_activa', False)
            )
            self.left_layout.addWidget(self.tarjeta_facturas)

        self.left_layout.addStretch()

    def mostrar_mensaje_vacio(self):
        """Limpia el panel derecho e introduce un texto de guía elegante"""
        self.id_grupo_seleccionado = None
        while self.right_layout.count():
            item = self.right_layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()
                
        lbl_vacio = QLabel("Selecciona un grupo del panel izquierdo para ver sus tareas y sesiones.")
        lbl_vacio.setStyleSheet("color: #888888; font-size: 14px; font-style: italic; font-weight: bold; border: none;")
        lbl_vacio.setAlignment(Qt.AlignCenter)
        self.right_layout.addWidget(lbl_vacio)

    def grupo_seleccionado(self, id_grupo, tarjeta_pulsada):
        """Manejador del Evento Clic: Actualiza colores de selección y renderiza las tareas"""
        self.seccion_facturas_activa = False
        if id_grupo is None or tarjeta_pulsada is None:
            self.mostrar_mensaje_vacio()
            return

        self.id_grupo_seleccionado = int(id_grupo)

        for tarjeta in self.tarjetas_izquierda:
            tarjeta.marcar_activa(activa=False)
        tarjeta_pulsada.marcar_activa(activa=True)

        while self.right_layout.count():
            item = self.right_layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()

        if self.es_admin:
            self.btn_crear_tarea = QPushButton("+ Asignar Tarea a este Grupo")
            self.btn_crear_tarea.setCursor(Qt.PointingHandCursor)
            self.btn_crear_tarea.setStyleSheet("""
                QPushButton {
                    background-color: #2ECC71;
                    border: 2px solid #000000;
                    border-radius: 5px;
                    padding: 8px;
                    font-weight: bold;
                    color: #FFFFFF;
                    margin-bottom: 12px;
                }
                QPushButton:hover {
                    background-color: #27AE60;
                }
            """)
            self.btn_crear_tarea.clicked.connect(self.abrir_dialogo_crear_tarea)
            self.right_layout.addWidget(self.btn_crear_tarea)

        elementos_derechos = self.callback_cargar_tareas(id_grupo)

        for elemento in elementos_derechos:
            self.crear_tarjeta_derecha(
                titulo=elemento['titulo'], 
                info_derecha=elemento['info_derecha'], 
                descripcion=elemento['descripcion']
            )
        
        self.right_layout.addStretch()

    def crear_tarjeta_derecha(self, titulo, info_derecha, descripcion):
        """Crea una tarjeta contenedora estilizada para el panel derecho (Tareas/Sesiones)"""
        frame = QFrame()
        frame.setStyleSheet("QFrame { background-color: #FFFFFF; border: 2px solid #000000; border-radius: 8px; }")
        
        layout_tarjeta = QVBoxLayout(frame)
        layout_tarjeta.setContentsMargins(15, 12, 15, 12)
        
        fila_superior = QHBoxLayout()
        
        lbl_titulo = QLabel(str(titulo))
        lbl_titulo.setStyleSheet("font-weight: bold; font-size: 14px; border: none;")
        
        lbl_info = QLabel(str(info_derecha))
        lbl_info.setStyleSheet("color: #666666; font-size: 12px; border: none;")
        
        fila_superior.addWidget(lbl_titulo)
        fila_superior.addStretch()
        fila_superior.addWidget(lbl_info)
        
        lbl_desc = QLabel(str(descripcion))
        lbl_desc.setStyleSheet("color: #444444; font-size: 13px; border: none; margin-top: 5px;")
        lbl_desc.setWordWrap(True)
        
        layout_tarjeta.addLayout(fila_superior)
        layout_tarjeta.addWidget(lbl_desc)
        
        self.right_layout.addWidget(frame)

    # =================================================================
    # VENTANAS MODALES EMERGENTES PARA LA ASIGNACIÓN DE CONTENIDO
    # =================================================================
    def mostrar_dialogo_cambiar_pass(self):
        """Muestra un diálogo modal para cambiar la contraseña del usuario actual."""
        dialogo = QDialog(self)
        dialogo.setWindowTitle("Seguridad - Cambiar Contraseña")
        dialogo.setMinimumWidth(360)
        dialogo.setWindowFlags(dialogo.windowFlags() & ~Qt.WindowContextHelpButtonHint)
        
        layout_modal = QVBoxLayout(dialogo)
        form = QFormLayout()
        
        txt_nueva_pass = QLineEdit()
        txt_nueva_pass.setEchoMode(QLineEdit.Password)
        txt_nueva_pass.setPlaceholderText("Mínimo 4 caracteres")
        
        txt_confirmar_pass = QLineEdit()
        txt_confirmar_pass.setEchoMode(QLineEdit.Password)
        txt_confirmar_pass.setPlaceholderText("Repita la nueva contraseña")
        
        form.addRow("Nueva Contraseña:", txt_nueva_pass)
        form.addRow("Confirmar Contraseña:", txt_confirmar_pass)
        layout_modal.addLayout(form)
        
        botones = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        botones.accepted.connect(dialogo.accept)
        botones.rejected.connect(dialogo.reject)
        layout_modal.addWidget(botones)
        
        if dialogo.exec_() == QDialog.Accepted:
            nueva_pass = txt_nueva_pass.text().strip()
            confirmar_pass = txt_confirmar_pass.text().strip()
            
            if len(nueva_pass) < 4:
                QMessageBox.warning(self, "Validación", "La contraseña es demasiado corta (mínimo 4 caracteres).")
                return
                
            if nueva_pass != confirmar_pass:
                QMessageBox.warning(self, "Validación", "Las contraseñas no coinciden. Inténtelo de nuevo.")
                return
            
            conexion_activa = None
            if hasattr(self, 'grupo_controller') and self.grupo_controller and self.grupo_controller.grupo_dao:
                conexion_activa = self.grupo_controller.grupo_dao.conexion
            elif hasattr(self, 'tarea_controller') and self.tarea_controller and self.tarea_controller.tarea_dao:
                conexion_activa = self.tarea_controller.tarea_dao.conexion
                
            if conexion_activa:
                from DAO.MiembroDAO import MiembroDAO
                dao_aux = MiembroDAO(conexion_activa)
                
                exito = dao_aux.actualizar_contrasena(self.miembro.NombreUsuario, nueva_pass)
                if exito:
                    QMessageBox.information(self, "Éxito", "Su contraseña ha sido actualizada correctamente.")
                else:
                    QMessageBox.critical(self, "Error", "No se pudo actualizar la contraseña (verifique el registro).")
            else:
                QMessageBox.critical(self, "Error de Sistema", "No se detectó una conexión activa con la base de datos.")

    def abrir_dialogo_crear_grupo(self):
        if not self.grupo_controller:
            QMessageBox.critical(self, "Error de Sistema", "El controlador de grupos no se encuentra vinculado.")
            return

        nombre, ok = QInputDialog.getText(
            self, 
            "Nuevo Grupo Organizacional", 
            "Introduce el nombre del grupo:",
            flags=self.windowFlags() & ~Qt.WindowContextHelpButtonHint
        )
        if ok and nombre.strip():
            nombre_limpio = str(nombre).strip()
            
            exito, mensaje = self.grupo_controller.procesar_crear_grupo(
                self.miembro.Rol, nombre_limpio, self.miembro.UsuarioID
            )
            
            if exito:
                QMessageBox.information(self, "Operación Completada", mensaje)
                self.lista_grupos = self.grupo_controller.obtener_grupos_usuario(
                    self.miembro.UsuarioID, self.miembro.Rol
                )
                self.cargar_grupos_izquierdos()
            else:
                QMessageBox.critical(self, "Error de Inserción", mensaje)

    def abrir_dialogo_crear_tarea(self):
        if not self.tarea_controller:
            QMessageBox.critical(self, "Error de Sistema", "El controlador de tareas no se encuentra vinculado.")
            return

        if self.id_grupo_seleccionado is None:
            QMessageBox.warning(self, "Atención", "Por favor, selecciona primero un grupo de trabajo.")
            return

        dialogo = QDialog(self)
        dialogo.setWindowTitle("Asignar Nueva Tarea Colectiva")
        dialogo.setMinimumWidth(400)
        layout_modal = QVBoxLayout(dialogo)
        
        form = QFormLayout()
        txt_titulo = QLineEdit()
        txt_desc = QTextEdit()
        txt_desc.setPlaceholderText("Introduce de forma detallada las metas de la tarea...")

        txt_fecha = QLineEdit()
        import datetime
        txt_fecha.setPlaceholderText("AAAA-MM-DD (Ej: " + datetime.date.today().strftime("%Y-%m-%d") + ")")
        
        form.addRow("Título de la Tarea:", txt_titulo)
        form.addRow("Descripción Extendida:", txt_desc)
        form.addRow("Fecha Límite (AAAA-MM-DD):", txt_fecha)
        layout_modal.addLayout(form)
        
        botones = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        botones.accepted.connect(dialogo.accept)
        botones.rejected.connect(dialogo.reject)
        layout_modal.addWidget(botones)
        
        if dialogo.exec_() == QDialog.Accepted:
            titulo = str(txt_titulo.text()).strip()
            descripcion = str(txt_desc.toPlainText()).strip()
            fecha_limite = str(txt_fecha.text()).strip()
            
            if not fecha_limite:
                fecha_limite = datetime.date.today().strftime("%Y-%m-%d")
            
            exito, mensaje = self.tarea_controller.procesar_crear_tarea(
                self.miembro.Rol, int(self.id_grupo_seleccionado), titulo, descripcion, fecha_limite
            )
            
            if exito:
                QMessageBox.information(self, "Éxito", mensaje)
                for tarjeta in self.tarjetas_izquierda:
                    if int(tarjeta.id_entidad) == int(self.id_grupo_seleccionado):
                        self.grupo_seleccionado(self.id_grupo_seleccionado, tarjeta)
                        break
            else:
                QMessageBox.critical(self, "Error en el Proceso", mensaje)

    def refrescar_grupos(self):
        if hasattr(self, 'grupo_controller') and self.grupo_controller:
            nuevos_grupos = self.grupo_controller.obtener_grupos_usuario(
                self.miembro.UsuarioID, self.miembro.Rol
            )
            self.lista_grupos = nuevos_grupos
            self.cargar_grupos_izquierdos()
            if self.id_grupo_seleccionado:
                for tarjeta in self.tarjetas_izquierda:
                    if int(tarjeta.id_entidad) == int(self.id_grupo_seleccionado):
                        self.grupo_seleccionado(self.id_grupo_seleccionado, tarjeta)
                        break

    def abrir_modulo_bienes(self):
        if hasattr(self, 'bienes_controller') and self.bienes_controller:
            self.bienes_controller.abrir_pantalla_bienes()
        else:
            QMessageBox.warning(
                self, 
                "Error de Inicialización", 
                "El módulo de bienes no se encuentra disponible o no posees los privilegios requeridos."
            )


    def abrir_seccion_facturas(self, id_entidad, tarjeta_pulsada):
        """Activa la vista de facturas en el panel derecho y desmarca los grupos"""
        self.seccion_facturas_activa = True
        self.id_grupo_seleccionado = None
        
        # Desmarcar tarjetas de grupos y marcar la de facturas
        for tarjeta in self.tarjetas_izquierda:
            tarjeta.marcar_activa(False)
        tarjeta_pulsada.marcar_activa(True)
        
        self.cargar_panel_facturas()

    def cargar_panel_facturas(self):
        """Limpia el panel derecho y renderiza las opciones y lista de facturas desde la BD"""
        while self.right_layout.count():
            item = self.right_layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()
                
        # Botón para Crear Factura
        self.btn_crear_factura = QPushButton("Registrar Nueva Factura")
        self.btn_crear_factura.setCursor(Qt.PointingHandCursor)
        self.btn_crear_factura.setStyleSheet("""
            QPushButton { background-color: #2ECC71; border: 2px solid #000000; border-radius: 5px; padding: 8px; font-weight: bold; color: #FFFFFF; margin-bottom: 12px; }
            QPushButton:hover { background-color: #27AE60; }
        """)
        self.btn_crear_factura.clicked.connect(self.abrir_dialogo_crear_factura)
        self.right_layout.addWidget(self.btn_crear_factura)
        
        # 🔌 LLAMADA REAL AL DAO: Obtener registros actualizados de la base de datos
        if hasattr(self, 'factura_dao') and self.factura_dao:
            lista_facturas = self.factura_dao.obtener_todas_las_facturas()
        else:
            lista_facturas = []
            
        for fac in lista_facturas:
            self.crear_tarjeta_factura(fac)
            
        self.right_layout.addStretch()

    def crear_tarjeta_factura(self, factura_dict):
        """Crea un contenedor para cada factura con un botón de edición incluido"""
        frame = QFrame()
        frame.setStyleSheet("QFrame { background-color: #FFFFFF; border: 2px solid #000000; border-radius: 8px; }")
        
        layout_tarjeta = QVBoxLayout(frame)
        layout_tarjeta.setContentsMargins(15, 12, 15, 12)
        
        fila_superior = QHBoxLayout()
        
        lbl_titulo = QLabel(str(factura_dict['concepto']))
        lbl_titulo.setStyleSheet("font-weight: bold; font-size: 14px; border: none;")
        
        lbl_info = QLabel(f"{factura_dict['monto']} | {factura_dict['fecha']}")
        lbl_info.setStyleSheet("color: #666666; font-size: 12px; border: none;")
        
        fila_superior.addWidget(lbl_titulo)
        fila_superior.addStretch()
        fila_superior.addWidget(lbl_info)
        
        fila_inferior = QHBoxLayout()
        lbl_estado = QLabel(f"Estado: {factura_dict['estado']}")
        lbl_estado.setStyleSheet(f"color: {'#2ECC71' if factura_dict['estado'] == 'Pagado' else '#E74C3C'}; font-weight: bold; border: none;")
        
        btn_editar = QPushButton("Editar")
        btn_editar.setCursor(Qt.PointingHandCursor)
        btn_editar.setFixedSize(60, 22)
        btn_editar.setStyleSheet("QPushButton { background-color: #F39C12; color: white; border-radius: 3px; font-size: 11px; font-weight: bold; border: none; } QPushButton:hover { background-color: #E67E22; }")
        # Pasamos el diccionario de la factura correspondiente al hacer clic
        btn_editar.clicked.connect(lambda checked, f=factura_dict: self.abrir_dialogo_editar_factura(f))
        
        fila_inferior.addWidget(lbl_estado)
        fila_inferior.addStretch()
        fila_inferior.addWidget(btn_editar)
        
        layout_tarjeta.addLayout(fila_superior)
        layout_tarjeta.addLayout(fila_inferior)
        
        self.right_layout.addWidget(frame)

    # =================================================================
    # MODALES FORMULARIOS DE FACTURAS (CREAR / EDITAR)
    # =================================================================
    def abrir_dialogo_crear_factura(self):
        dialogo = QDialog(self)
        dialogo.setWindowTitle("Registrar Nueva Factura")
        dialogo.setMinimumWidth(380)
        dialogo.setWindowFlags(dialogo.windowFlags() & ~Qt.WindowContextHelpButtonHint)
        
        layout_modal = QVBoxLayout(dialogo)
        form = QFormLayout()
        
        txt_concepto = QLineEdit()
        txt_monto = QLineEdit()
        txt_monto.setPlaceholderText("Ej: 120.50")
        
        cb_estado = QComboBox()
        cb_estado.addItems(["Pendiente", "Pagado"])
        
        form.addRow("Concepto / Detalle:", txt_concepto)
        form.addRow("Monto (€):", txt_monto)
        form.addRow("Estado del Pago:", cb_estado)
        layout_modal.addLayout(form)
        
        botones = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        botones.accepted.connect(dialogo.accept)
        botones.rejected.connect(dialogo.reject)
        layout_modal.addWidget(botones)
        
        if dialogo.exec_() == QDialog.Accepted:
            concepto = txt_concepto.text().strip()
            monto_str = txt_monto.text().strip()
            estado = cb_estado.currentText()
            
            if not concepto or not monto_str:
                QMessageBox.warning(self, "Validación", "Todos los campos son obligatorios.")
                return
            
            try:
                monto = float(monto_str)
            except ValueError:
                QMessageBox.warning(self, "Validación", "El monto ingresado debe ser un número válido.")
                return
            
            import datetime
            fecha_hoy = datetime.date.today().strftime("%Y-%m-%d")
            
            # 🔌 LLAMADA REAL AL DAO: Insertar registro
            if hasattr(self, 'factura_dao') and self.factura_dao:
                exito = self.factura_dao.insertar_factura(concepto, monto, fecha_hoy, estado)
                if exito:
                    QMessageBox.information(self, "Éxito", "Factura guardada correctamente en la Base de Datos.")
                    self.cargar_panel_facturas()
                else:
                    QMessageBox.critical(self, "Error", "No se pudo guardar la factura en la Base de Datos.")
            else:
                QMessageBox.critical(self, "Error de Sistema", "El DAO de facturas no está disponible.")


    def abrir_dialogo_editar_factura(self, factura_dict):
        dialogo = QDialog(self)
        dialogo.setWindowTitle(f"Editar Factura N° {factura_dict['id']}")
        dialogo.setMinimumWidth(380)
        dialogo.setWindowFlags(dialogo.windowFlags() & ~Qt.WindowContextHelpButtonHint)
        
        layout_modal = QVBoxLayout(dialogo)
        form = QFormLayout()
        
        txt_concepto = QLineEdit(factura_dict['concepto'])
        # Limpiamos los caracteres de moneda para el formulario
        monto_limpio = factura_dict['monto'].replace(" €", "").strip()
        txt_monto = QLineEdit(monto_limpio)
        
        cb_estado = QComboBox()
        cb_estado.addItems(["Pendiente", "Pagado"])
        cb_estado.setCurrentText(factura_dict['estado'])
        
        form.addRow("Concepto / Detalle:", txt_concepto)
        form.addRow("Monto (€):", txt_monto)
        form.addRow("Estado del Pago:", cb_estado)
        layout_modal.addLayout(form)
        
        botones = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        botones.accepted.connect(dialogo.accept)
        botones.rejected.connect(dialogo.reject)
        layout_modal.addWidget(botones)
        
        if dialogo.exec_() == QDialog.Accepted:
            concepto = txt_concepto.text().strip()
            monto_str = txt_monto.text().strip()
            estado = cb_estado.currentText()
            
            if not concepto or not monto_str:
                QMessageBox.warning(self, "Validación", "Los campos no pueden estar vacíos.")
                return
                
            try:
                monto = float(monto_str)
            except ValueError:
                QMessageBox.warning(self, "Validación", "El monto ingresado debe ser un número válido.")
                return
            
            # 🔌 LLAMADA REAL AL DAO: Actualizar el registro por su ID único
            if hasattr(self, 'factura_dao') and self.factura_dao:
                exito = self.factura_dao.actualizar_factura(factura_dict['id'], concepto, monto, estado)
                if exito:
                    QMessageBox.information(self, "Éxito", "Factura actualizada correctamente en la Base de Datos.")
                    self.cargar_panel_facturas()
                else:
                    QMessageBox.critical(self, "Error", "No se pudieron guardar los cambios en la Base de Datos.")
            else:
                QMessageBox.critical(self, "Error de Sistema", "El DAO de facturas no está disponible.")