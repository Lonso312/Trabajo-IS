# archivo: vistas/menu_view.py
from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                             QLabel, QPushButton, QFrame, QInputDialog, 
                             QDialog, QFormLayout, QLineEdit, QTextEdit, 
                             QDialogButtonBox, QMessageBox)
from PyQt5.QtCore import Qt

# =================================================================
# UN RECUADRO CLICABLE (PANEL IZQUIERDO)
# =================================================================
class TarjetaClicable(QFrame):
    def __init__(self, id_entidad, titulo, sub_1, sub_2, callback_click, es_verde=False, parent=None):
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
        
        self.lbl_sub2 = QLabel(str(sub_2))
        self.lbl_sub2.setStyleSheet("font-size: 11px; border: none; background: transparent; color: inherit;")
        self.lbl_sub2.setAlignment(Qt.AlignRight)
        
        layout.addWidget(self.lbl_titulo)
        layout.addWidget(self.lbl_sub1)
        layout.addWidget(self.lbl_sub2)

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
        
        self.id_grupo_seleccionado = None  # Almacena el ID del grupo activo
        self.tarjetas_izquierda = []  
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle(f"SGA - Sistema de Gestión ({str(self.miembro.Rol)})")
        self.resize(1000, 650)
        self.setStyleSheet("background-color: #F8F9FA; font-family: 'Segoe UI', Arial;")

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(25, 20, 25, 25)

        # -------------------------------------------------------------
        # 1. BARRA SUPERIOR (Información del Usuario y Botón Logout)
        # -------------------------------------------------------------
        top_bar = QHBoxLayout()
        nombre_limpio = str(self.miembro.Name)
        rol_limpio = str(self.miembro.Rol)
        lbl_usuario = QLabel(f"{nombre_limpio} : {rol_limpio}")
        
        lbl_usuario.setStyleSheet("font-size: 15px; font-weight: bold; color: #333333;")
        top_bar.addWidget(lbl_usuario)
        
        top_bar.addStretch()  # Empuja los botones al extremo derecho
        
        # ----------------------------------------------------------------------
        # VALIDACIÓN VISUAL DEL ROL Y BOTONES DE GESTIÓN ADMINISTRATIVA
        # ----------------------------------------------------------------------
        rol_limpio_check = str(self.miembro.Rol).strip().upper() if self.miembro.Rol else "MIEMBRO"
        self.es_admin = rol_limpio_check in ["PRESIDENTE", "JEFE DEPARTAMENTO"]
        
        if rol_limpio_check in ["PRESIDENTE", "SECRETARIO", "TESORERO", "JEFE DEPARTAMENTO"]:
            self.btn_gestionar_miembros = QPushButton("Gestionar Miembros")
            self.btn_gestionar_miembros.setCursor(Qt.PointingHandCursor)
            self.btn_gestionar_miembros.setStyleSheet("""
                QPushButton {
                    background-color: #FFFFFF;
                    border: 2px solid #6B46C1;
                    border-radius: 10px;
                    padding: 5px 15px;
                    font-weight: bold;
                    color: #6B46C1;
                }
                QPushButton:hover {
                    background-color: #FAF5FF;
                    border-color: #553C9A;
                    color: #553C9A;
                }
            """)
            self.btn_gestionar_miembros.clicked.connect(self.callback_abrir_gestion)
            top_bar.addWidget(self.btn_gestionar_miembros)
            top_bar.addSpacing(10) 

        btn_logout = QPushButton("Cerrar Sesión")
        btn_logout.setCursor(Qt.PointingHandCursor)
        btn_logout.setStyleSheet("""
            QPushButton {
                background-color: #FFFFFF;
                border: 2px solid #000000;
                border-radius: 10px;
                padding: 5px 15px;
                font-weight: bold;
                color: #000000;
            }
            QPushButton:hover {
                background-color: #EFEFEF;
            }
        """)
        btn_logout.clicked.connect(self.callback_logout)
        top_bar.addWidget(btn_logout)
        
        main_layout.addLayout(top_bar)
        main_layout.addSpacing(15)

        # -------------------------------------------------------------
        # 2. CONTENIDO PRINCIPAL (Diseño de paneles izquierdo/derecho)
        # -------------------------------------------------------------
        content_layout = QHBoxLayout()
        
        # Panel Izquierdo (Contenedor vertical de tarjetas + Botón Crear Grupo)
        self.left_layout = QVBoxLayout()
        self.cargar_grupos_izquierdos()
        content_layout.addLayout(self.left_layout, stretch=2)  

        # Línea Divisora Central Estricta
        linea = QFrame()
        linea.setFrameShape(QFrame.VLine)
        linea.setStyleSheet("color: #A0A0A0; width: 2px; margin: 0px 15px;")
        content_layout.addWidget(linea)

        # Panel Derecho (Contenedor maestro de Tareas)
        right_container = QFrame()
        right_container.setStyleSheet("background-color: #FFFFFF; border: 2px solid #000000; border-radius: 5px;")
        self.right_layout = QVBoxLayout(right_container)
        self.right_layout.setContentsMargins(20, 20, 20, 20)
        
        content_layout.addWidget(right_container, stretch=3)  
        main_layout.addLayout(content_layout)

        # Mostrar mensaje de instrucciones iniciales al cargar la pantalla
        self.mostrar_mensaje_vacio()

    def cargar_grupos_izquierdos(self):
        """Vuelca dinámicamente las tarjetas reactivas de grupos en el menú izquierdo"""
        while self.left_layout.count():
            item = self.left_layout.takeAt(0)
            if item.widget(): 
                item.widget().deleteLater()

        self.tarjetas_izquierda.clear()

        if hasattr(self, 'es_admin') and self.es_admin:
            self.btn_crear_grupo = QPushButton("+ Crear Nuevo Grupo")
            self.btn_crear_grupo.setCursor(Qt.PointingHandCursor)
            self.btn_crear_grupo.setStyleSheet("""
                QPushButton {
                    background-color: #6B46C1;
                    border: 2px solid #000000;
                    border-radius: 5px;
                    padding: 8px;
                    font-weight: bold;
                    color: #FFFFFF;
                    margin-bottom: 10px;
                }
                QPushButton:hover {
                    background-color: #553C9A;
                }
            """)
            self.btn_crear_grupo.clicked.connect(self.abrir_dialogo_crear_grupo)
            self.left_layout.addWidget(self.btn_crear_grupo)

        # Iteración de mapeado para las tarjetas de grupos organizacionales
        for i, grupo in enumerate(self.lista_grupos):
            nombre_grupo = str(grupo['nombre'])
            cant_miembros = str(grupo['cantidad_miembros'])
            fecha_limite = str(grupo['fecha_limite'])
            
            tarjeta = TarjetaClicable(
                id_entidad=grupo['id'],
                titulo=nombre_grupo,
                sub_1=f"Miembros: {cant_miembros}",
                sub_2=f"Límite global: {fecha_limite}",
                callback_click=self.grupo_seleccionado,
                es_verde=False
            )
            
            # Si el grupo que estamos redibujando coincide con el seleccionado previamente, mantén el color verde activo
            if self.id_grupo_seleccionado and int(grupo['id']) == int(self.id_grupo_seleccionado):
                tarjeta.marcar_activa(True)

            self.left_layout.addWidget(tarjeta)
            self.tarjetas_izquierda.append(tarjeta)
        
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
        if id_grupo is None or tarjeta_pulsada is None:
            self.mostrar_mensaje_vacio()
            return

        self.id_grupo_seleccionado = int(id_grupo)

        # Conmutar estilos de las tarjetas izquierdas
        for tarjeta in self.tarjetas_izquierda:
            tarjeta.marcar_activa(activa=False)
        tarjeta_pulsada.marcar_activa(activa=True)

        # Vaciar el panel derecho de tareas antiguas
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

        # Solicitud de datos limpios a través del controlador
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
    def abrir_dialogo_crear_grupo(self):
        if not self.grupo_controller:
            QMessageBox.critical(self, "Error de Sistema", "El controlador de grupos no se encuentra vinculado.")
            return

        nombre, ok = QInputDialog.getText(self, "Nuevo Grupo Organizacional", "Introduce el nombre del grupo:")
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
        """
        Vuelve a consultar los grupos del usuario en la base de datos 
        y rellama a la función de renderizado para actualizar la interfaz.
        """
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