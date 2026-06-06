# archivo: vistas/menu_view.py
from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QFrame
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
    def __init__(self, miembro, lista_grupos, callback_cargar_tareas, callback_logout):
        super().__init__()
        self.miembro = miembro
        self.lista_grupos = lista_grupos  
        self.callback_cargar_tareas = callback_cargar_tareas  
        self.callback_logout = callback_logout
        
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
        
        top_bar.addStretch()  # Empuja el botón al extremo derecho
        
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
        # 2. CONTENIDO PRINCIPAL 
        # -------------------------------------------------------------
        content_layout = QHBoxLayout()
        
        # Panel Izquierdo (Módulos / Grupos)
        self.left_layout = QVBoxLayout()
        self.cargar_grupos_izquierdos()
        content_layout.addLayout(self.left_layout, stretch=2)  

        # Línea Divisora Central Estricta
        linea = QFrame()
        linea.setFrameShape(QFrame.VLine)
        linea.setStyleSheet("color: #A0A0A0; width: 2px; margin: 0px 15px;")
        content_layout.addWidget(linea)

        # Panel Derecho
        right_container = QFrame()
        right_container.setStyleSheet("background-color: #FFFFFF; border: 2px solid #000000; border-radius: 5px;")
        self.right_layout = QVBoxLayout(right_container)
        self.right_layout.setContentsMargins(20, 20, 20, 20)
        
        content_layout.addWidget(right_container, stretch=3)  
        main_layout.addLayout(content_layout)


    def cargar_grupos_izquierdos(self):
        while self.left_layout.count():
            item = self.left_layout.takeAt(0)
            if item.widget(): 
                item.widget().deleteLater()

        self.tarjetas_izquierda.clear()

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
            self.left_layout.addWidget(tarjeta)
            self.tarjetas_izquierda.append(tarjeta)
        
        self.left_layout.addStretch()

    def mostrar_mensaje_vacio(self):
        """Limpia el panel derecho e introduce un texto de guía elegante"""
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
        """Manejador del Evento Clic: Actualiza colores de selección sin perder textos secundarios"""
        if id_grupo is None or tarjeta_pulsada is None:
            self.mostrar_mensaje_vacio()
            return

        # 1. Cambiar color de forma segura usando el método de la tarjeta
        for tarjeta in self.tarjetas_izquierda:
            tarjeta.marcar_activa(activa=False)
        
        tarjeta_pulsada.marcar_activa(activa=True)

        # 2. Limpieza total de todo lo que haya en el panel derecho
        while self.right_layout.count():
            item = self.right_layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()

        # 3. Solicitar la lista unificada combinada al controlador (main.py)
        elementos_derechos = self.callback_cargar_tareas(id_grupo)

        # 4. Dibujar dinámicamente cada elemento en la interfaz
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