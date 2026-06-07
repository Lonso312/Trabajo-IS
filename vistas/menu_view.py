# archivo: vistas/menu_view.py
from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                             QLabel, QPushButton, QFrame, QInputDialog, 
                             QDialog, QFormLayout, QLineEdit, QTextEdit, 
                             QDialogButtonBox, QMessageBox, QScrollArea, QComboBox) 
from PyQt5.QtCore import Qt
from utils.event_bus import EventBus

class TarjetaClicable(QFrame):
    def __init__(self, id_entidad, titulo, sub_1, callback_click, es_verde=False, parent=None):
        super().__init__(parent)
        self.id_entidad = id_entidad
        self.callback_click = callback_click
        
        self.estilo_blanco = "QFrame { background-color: #FFFFFF; border: 2px solid #000000; color: #000000; border-radius: 5px; }"
        self.estilo_verde = "QFrame { background-color: #2ECC71; border: 3px solid #000000; color: #FFFFFF; border-radius: 5px; }"
        
        self.setStyleSheet(self.estilo_verde if es_verde else self.estilo_blanco)
            
        layout = QVBoxLayout(self)
        layout.setContentsMargins(15, 10, 15, 10)
        
        lbl_titulo = QLabel(str(titulo))
        lbl_titulo.setStyleSheet("font-weight: bold; font-size: 14px; border: none; background: transparent; color: inherit;")
        
        lbl_sub1 = QLabel(str(sub_1))
        lbl_sub1.setStyleSheet("font-size: 12px; border: none; background: transparent; color: inherit;")
        lbl_sub1.setAlignment(Qt.AlignRight)
        
        layout.addWidget(lbl_titulo)
        layout.addWidget(lbl_sub1)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.callback_click(self.id_entidad, self)

    def marcar_activa(self, activa=True):
        self.setStyleSheet(self.estilo_verde if activa else self.estilo_blanco)


class MenuView(QMainWindow):
    def __init__(self, miembro, lista_grupos, callback_cargar_tareas, callback_abrir_gestion, callback_logout):
        super().__init__()
        self.miembro = miembro
        self.lista_grupos = lista_grupos  
        self.callback_cargar_tareas = callback_cargar_tareas  
        self.callback_abrir_gestion = callback_abrir_gestion
        self.callback_logout = callback_logout
        
        self.grupo_controller = None
        self.tarea_controller = None
        self.bienes_controller = None  
        
        self.id_grupo_seleccionado = None  
        self.seccion_facturas_activa = False
        self.seccion_solicitudes_activa = False
        self.seccion_secretaria_activa = False # 👈 Nuevo estado
        self.tarjetas_izquierda = []  
        
        EventBus.get_instance().grupos_actualizados.connect(self.refrescar_grupos)
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle(f"SGA - Sistema de Gestión ({str(self.miembro.Rol)})")
        self.resize(1000, 650)
        self.setStyleSheet("background-color: #F8F9FA; font-family: 'Segoe UI', Arial;")

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(25, 20, 25, 25)

        # --- BARRA SUPERIOR ---
        top_bar = QHBoxLayout()
        user_info_layout = QVBoxLayout()
        user_info_layout.setSpacing(4)
        
        lbl_usuario = QLabel(f"{self.miembro.Name} : {self.miembro.Rol}")
        lbl_usuario.setStyleSheet("font-size: 15px; font-weight: bold; color: #333333;")
        user_info_layout.addWidget(lbl_usuario)
        
        btn_cambiar_pass = QPushButton("Cambiar Contraseña")
        btn_cambiar_pass.setCursor(Qt.PointingHandCursor)
        btn_cambiar_pass.setStyleSheet("QPushButton { background-color: #7F8C8D; color: white; font-weight: bold; font-size: 11px; padding: 3px 8px; border-radius: 4px; border: none; } QPushButton:hover { background-color: #95A5A6; }")
        btn_cambiar_pass.clicked.connect(self.mostrar_dialogo_cambiar_pass)
        user_info_layout.addWidget(btn_cambiar_pass)
        
        top_bar.addLayout(user_info_layout)
        top_bar.addStretch()  
        
        # --- VALIDACIÓN ROLES ---
        rol_limpio = str(self.miembro.Rol).strip().upper() if self.miembro.Rol else "MIEMBRO"
        self.es_admin = rol_limpio in ["PRESIDENTE", "JEFE DEPARTAMENTO"]
        self.es_tesorero = rol_limpio in ["TESORERO", "PRESIDENTE"]

        if self.es_admin:
            btn_solicitar_mat = QPushButton("Solicitar Materiales")
            btn_solicitar_mat.setCursor(Qt.PointingHandCursor)
            btn_solicitar_mat.setStyleSheet("QPushButton { background-color: #FFFFFF; border: 2px solid #E67E22; border-radius: 10px; padding: 5px 15px; font-weight: bold; color: #E67E22; } QPushButton:hover { background-color: #FDF2E9; border-color: #D35400; color: #D35400; }")
            btn_solicitar_mat.clicked.connect(self.abrir_dialogo_solicitar_materiales)
            top_bar.addWidget(btn_solicitar_mat)
            top_bar.addSpacing(10)
        
        if rol_limpio in ["PRESIDENTE", "SECRETARIO", "TESORERO", "JEFE DEPARTAMENTO"]:
            btn_gestionar_miembros = QPushButton("Gestionar Miembros")
            btn_gestionar_miembros.setCursor(Qt.PointingHandCursor)
            btn_gestionar_miembros.setStyleSheet("QPushButton { background-color: #FFFFFF; border: 2px solid #6B46C1; border-radius: 10px; padding: 5px 15px; font-weight: bold; color: #6B46C1; } QPushButton:hover { background-color: #FAF5FF; border-color: #553C9A; color: #553C9A; }")
            btn_gestionar_miembros.clicked.connect(self.callback_abrir_gestion)
            top_bar.addWidget(btn_gestionar_miembros)
            top_bar.addSpacing(10) 

        if rol_limpio in ["PRESIDENTE", "TESORERO", "JEFE DEPARTAMENTO"]:
            btn_bienes = QPushButton("Inventario")
            btn_bienes.setCursor(Qt.PointingHandCursor)
            btn_bienes.setStyleSheet("QPushButton { background-color: #FFFFFF; border: 2px solid #2ECC71; border-radius: 10px; padding: 5px 15px; font-weight: bold; color: #2ECC71; } QPushButton:hover { background-color: #E8F8F5; border-color: #27AE60; color: #27AE60; }")
            btn_bienes.clicked.connect(self.abrir_modulo_bienes)
            top_bar.addWidget(btn_bienes)
            top_bar.addSpacing(10)

        btn_logout = QPushButton("Cerrar Sesión")
        btn_logout.setCursor(Qt.PointingHandCursor)
        btn_logout.setStyleSheet("QPushButton { background-color: #FFFFFF; border: 2px solid #000000; border-radius: 10px; padding: 5px 15px; font-weight: bold; color: #000000; } QPushButton:hover { background-color: #EFEFEF; }")
        btn_logout.clicked.connect(self.callback_logout)
        top_bar.addWidget(btn_logout)
        
        main_layout.addLayout(top_bar)
        main_layout.addSpacing(15)

        # --- CONTENIDO PRINCIPAL ---
        content_layout = QHBoxLayout()
        
        # Panel Izquierdo
        self.scroll_izquierda = QScrollArea()
        self.scroll_izquierda.setWidgetResizable(True)
        self.scroll_izquierda.setStyleSheet("QScrollArea { border: none; background-color: transparent; }")
        
        self.widget_contenedor_izq = QWidget()
        self.widget_contenedor_izq.setStyleSheet("background-color: transparent;")
        self.left_layout = QVBoxLayout(self.widget_contenedor_izq)
        self.left_layout.setContentsMargins(0, 0, 5, 0)
        
        self.cargar_grupos_izquierdos()
        
        self.scroll_izquierda.setWidget(self.widget_contenedor_izq)
        content_layout.addWidget(self.scroll_izquierda, stretch=2)  

        # Línea Divisora
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

        self.mostrar_mensaje_vacio()

    # =================================================================
    # GESTIÓN PANEL IZQUIERDO Y UTILIDADES
    # =================================================================
    def cargar_grupos_izquierdos(self):
        while self.left_layout.count():
            item = self.left_layout.takeAt(0)
            if item.widget(): item.widget().deleteLater()

        self.tarjetas_izquierda.clear()

        lbl_seccion_grupos = QLabel("MIS GRUPOS")
        lbl_seccion_grupos.setStyleSheet("font-weight: bold; color: #555555; font-size: 11px; margin-bottom: 5px;")
        self.left_layout.addWidget(lbl_seccion_grupos)

        if self.es_admin:
            btn_crear_grupo = QPushButton("+ Crear Nuevo Grupo")
            btn_crear_grupo.setCursor(Qt.PointingHandCursor)
            btn_crear_grupo.setStyleSheet("QPushButton { background-color: #6B46C1; border: 2px solid #000000; border-radius: 5px; padding: 8px; font-weight: bold; color: #FFFFFF; margin-bottom: 10px; } QPushButton:hover { background-color: #553C9A; }")
            btn_crear_grupo.clicked.connect(self.abrir_dialogo_crear_grupo)
            self.left_layout.addWidget(btn_crear_grupo)

        for grupo in self.lista_grupos:
            es_activa = (self.id_grupo_seleccionado == grupo['id'] and not self.seccion_facturas_activa and not self.seccion_solicitudes_activa and not self.seccion_secretaria_activa)
            tarjeta = TarjetaClicable(
                id_entidad=grupo['id'],
                titulo=grupo['nombre'],
                sub_1=f"Miembros: {grupo['cantidad_miembros']}",
                callback_click=self.grupo_seleccionado,
                es_verde=es_activa
            )
            self.left_layout.addWidget(tarjeta)
            self.tarjetas_izquierda.append(tarjeta)
        
        rol_limpio = str(self.miembro.Rol).strip().upper() if self.miembro.Rol else "MIEMBRO"
        
        if self.es_tesorero:
            self.left_layout.addSpacing(20)
            lbl_seccion_tesoreria = QLabel("TESORERÍA")
            lbl_seccion_tesoreria.setStyleSheet("font-weight: bold; color: #27AE60; font-size: 11px; margin-bottom: 5px;")
            self.left_layout.addWidget(lbl_seccion_tesoreria)
            
            self.tarjeta_facturas = TarjetaClicable(-99, "Gestión de Facturas", "Crear y administrar", self.abrir_seccion_facturas, self.seccion_facturas_activa)
            self.left_layout.addWidget(self.tarjeta_facturas)
            
            self.tarjeta_solicitudes = TarjetaClicable(-100, "Validar Materiales", "Peticiones de Jefes", self.abrir_seccion_solicitudes, self.seccion_solicitudes_activa)
            self.left_layout.addWidget(self.tarjeta_solicitudes)

        # 📋 NUEVA SECCIÓN: SECRETARÍA
        if rol_limpio in ["SECRETARIO", "JEFE DEPARTAMENTO", "TESORERO", "PRESIDENTE"]:
            self.left_layout.addSpacing(20)
            lbl_seccion_secretaria = QLabel("SECRETARÍA")
            lbl_seccion_secretaria.setStyleSheet("font-weight: bold; color: #3498DB; font-size: 11px; margin-bottom: 5px;")
            self.left_layout.addWidget(lbl_seccion_secretaria)
            
            self.tarjeta_secretaria = TarjetaClicable(-101, "Reuniones y Actas", "Control de asambleas", self.abrir_seccion_secretaria, self.seccion_secretaria_activa)
            self.left_layout.addWidget(self.tarjeta_secretaria)

        self.left_layout.addStretch()

    def desmarcar_todas_las_tarjetas(self):
        """Limpia cualquier selección visual en el panel izquierdo"""
        for tarjeta in self.tarjetas_izquierda:
            tarjeta.marcar_activa(False)
        if hasattr(self, 'tarjeta_facturas'): self.tarjeta_facturas.marcar_activa(False)
        if hasattr(self, 'tarjeta_solicitudes'): self.tarjeta_solicitudes.marcar_activa(False)
        if hasattr(self, 'tarjeta_secretaria'): self.tarjeta_secretaria.marcar_activa(False)

    def limpiar_panel_derecho(self):
        """Elimina todos los widgets del panel derecho dinámicamente"""
        while self.right_layout.count():
            item = self.right_layout.takeAt(0)
            if item.widget(): item.widget().deleteLater()

    # =================================================================
    # GESTIÓN PANEL DERECHO: GRUPOS / TAREAS
    # =================================================================
    def mostrar_mensaje_vacio(self):
        self.id_grupo_seleccionado = None
        self.limpiar_panel_derecho()
        lbl_vacio = QLabel("Selecciona un elemento del panel izquierdo para ver sus detalles.")
        lbl_vacio.setStyleSheet("color: #888888; font-size: 14px; font-style: italic; font-weight: bold;")
        lbl_vacio.setAlignment(Qt.AlignCenter)
        self.right_layout.addWidget(lbl_vacio)

    def grupo_seleccionado(self, id_grupo, tarjeta_pulsada):
        self.id_grupo_seleccionado = id_grupo
        self.seccion_facturas_activa = False
        self.seccion_solicitudes_activa = False 
        self.seccion_secretaria_activa = False

        self.desmarcar_todas_las_tarjetas()
        tarjeta_pulsada.marcar_activa(True)
        self.cargar_panel_derecho_grupo()

    def cargar_panel_derecho_grupo(self):
        self.limpiar_panel_derecho()

        if self.es_admin:
            btn_crear_tarea = QPushButton("+ Asignar Tarea a este Grupo")
            btn_crear_tarea.setCursor(Qt.PointingHandCursor)
            btn_crear_tarea.setStyleSheet("QPushButton { background-color: #2ECC71; border: 2px solid #000000; border-radius: 5px; padding: 8px; font-weight: bold; color: #FFFFFF; margin-bottom: 12px; } QPushButton:hover { background-color: #27AE60; }")
            btn_crear_tarea.clicked.connect(self.abrir_dialogo_crear_tarea)
            self.right_layout.addWidget(btn_crear_tarea)

        elementos_derechos = self.callback_cargar_tareas(self.id_grupo_seleccionado)
        for elemento in elementos_derechos:
            self.crear_tarjeta_derecha(elemento['titulo'], elemento['info_derecha'], elemento['descripcion'])
        
        self.right_layout.addStretch()

    def crear_tarjeta_derecha(self, titulo, info_derecha, descripcion):
        frame = QFrame()
        frame.setStyleSheet("QFrame { background-color: #FFFFFF; border: 2px solid #000000; border-radius: 8px; }")
        layout = QVBoxLayout(frame)
        layout.setContentsMargins(15, 12, 15, 12)
        
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
        
        layout.addLayout(fila_superior)
        layout.addWidget(lbl_desc)
        self.right_layout.addWidget(frame)

    # =================================================================
    # GESTIÓN PANEL DERECHO: FACTURAS Y SOLICITUDES
    # =================================================================
    def abrir_seccion_facturas(self, id_entidad, tarjeta_pulsada):
        self.seccion_facturas_activa = True
        self.seccion_solicitudes_activa = False
        self.seccion_secretaria_activa = False
        self.id_grupo_seleccionado = None

        self.desmarcar_todas_las_tarjetas()
        tarjeta_pulsada.marcar_activa(True)
        self.cargar_panel_facturas()

    def cargar_panel_facturas(self):
        self.limpiar_panel_derecho()
        
        btn_crear_factura = QPushButton("+ Registrar Nueva Factura")
        btn_crear_factura.setCursor(Qt.PointingHandCursor)
        btn_crear_factura.setStyleSheet("QPushButton { background-color: #2ECC71; border: 2px solid #000000; border-radius: 5px; padding: 8px; font-weight: bold; color: #FFFFFF; margin-bottom: 12px; } QPushButton:hover { background-color: #27AE60; }")
        btn_crear_factura.clicked.connect(self.abrir_dialogo_crear_factura)
        self.right_layout.addWidget(btn_crear_factura)
        
        lista_facturas = self.factura_dao.obtener_todas_las_facturas() if hasattr(self, 'factura_dao') and self.factura_dao else []
        for fac in lista_facturas:
            self.crear_tarjeta_factura(fac)
            
        self.right_layout.addStretch()

    def crear_tarjeta_factura(self, factura_dict):
        frame = QFrame()
        frame.setStyleSheet("QFrame { background-color: #FFFFFF; border: 2px solid #000000; border-radius: 8px; }")
        layout = QVBoxLayout(frame)
        layout.setContentsMargins(15, 12, 15, 12)
        
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
        btn_editar.clicked.connect(lambda checked, f=factura_dict: self.abrir_dialogo_editar_factura(f))
        
        fila_inferior.addWidget(lbl_estado)
        fila_inferior.addStretch()
        fila_inferior.addWidget(btn_editar)
        
        layout.addLayout(fila_superior)
        layout.addLayout(fila_inferior)
        self.right_layout.addWidget(frame)

    def abrir_seccion_solicitudes(self, id_entidad, tarjeta_pulsada):
        self.seccion_facturas_activa = False
        self.seccion_solicitudes_activa = True
        self.seccion_secretaria_activa = False
        self.id_grupo_seleccionado = None
        
        self.desmarcar_todas_las_tarjetas()
        tarjeta_pulsada.marcar_activa(True)
        self.cargar_panel_solicitudes()

    def cargar_panel_solicitudes(self):
        self.limpiar_panel_derecho()
            
        lbl_titulo = QLabel("📦 SOLICITUDES DE MATERIALES PENDIENTES")
        lbl_titulo.setStyleSheet("font-weight: bold; font-size: 14px; color: #2C3E50; margin-bottom: 10px; border:none;")
        self.right_layout.addWidget(lbl_titulo)
        
        lista_solicitudes = self.solicitud_dao.obtener_solicitudes_pendientes() if hasattr(self, 'solicitud_dao') and self.solicitud_dao else []
            
        if not lista_solicitudes:
            lbl_vacio = QLabel("No hay solicitudes de materiales pendientes de aprobación.")
            lbl_vacio.setStyleSheet("color: #7F8C8D; font-style: italic; border: none; margin-top: 10px;")
            self.right_layout.addWidget(lbl_vacio)
        else:
            for sol in lista_solicitudes:
                self.crear_tarjeta_solicitud_visual(sol)
                
        self.right_layout.addStretch()

    def crear_tarjeta_solicitud_visual(self, sol_dict):
        frame = QFrame()
        frame.setStyleSheet("QFrame { background-color: #FFFFFF; border: 2px solid #000000; border-radius: 8px; }")
        layout = QVBoxLayout(frame)
        layout.setContentsMargins(15, 12, 15, 12)
        
        fila_superior = QHBoxLayout()
        lbl_material = QLabel(f"📦 {sol_dict['concepto']} (Cant: {sol_dict['cantidad']})")
        lbl_material.setStyleSheet("font-weight: bold; font-size: 13px; border: none;")
        lbl_solicitante = QLabel(f"Por: {sol_dict['solicitante']}")
        lbl_solicitante.setStyleSheet("color: #7F8C8D; font-size: 11px; border: none;")
        
        fila_superior.addWidget(lbl_material)
        fila_superior.addStretch()
        fila_superior.addWidget(lbl_solicitante)
        
        fila_botones = QHBoxLayout()
        fila_botones.addStretch()
        
        btn_aceptar = QPushButton("Aceptar")
        btn_aceptar.setFixedSize(75, 24)
        btn_aceptar.setStyleSheet("QPushButton { background-color: #2ECC71; color: white; border-radius: 4px; font-weight: bold; border:none; } QPushButton:hover { background-color: #27AE60; }")
        btn_aceptar.clicked.connect(lambda checked, s_id=sol_dict['id']: self.procesar_respuesta_solicitud(s_id, "Aprobado"))
        
        btn_rechazar = QPushButton("Rechazar")
        btn_rechazar.setFixedSize(75, 24)
        btn_rechazar.setStyleSheet("QPushButton { background-color: #E74C3C; color: white; border-radius: 4px; font-weight: bold; border:none; } QPushButton:hover { background-color: #C0392B; }")
        btn_rechazar.clicked.connect(lambda checked, s_id=sol_dict['id']: self.procesar_respuesta_solicitud(s_id, "Rechazado"))
        
        fila_botones.addWidget(btn_aceptar)
        fila_botones.addSpacing(8)
        fila_botones.addWidget(btn_rechazar)
        
        layout.addLayout(fila_superior)
        layout.addLayout(fila_botones)
        self.right_layout.addWidget(frame)

    def procesar_respuesta_solicitud(self, solicitud_id, nuevo_estado):
        # ERROR CORREGIDO: solicitun_id cambiado por solicitud_id
        if hasattr(self, 'solicitud_dao') and self.solicitud_dao:
            if self.solicitud_dao.cambiar_estado_solicitud(solicitud_id=solicitud_id, nuevo_estado=nuevo_estado):
                QMessageBox.information(self, "Decisión Registrada", f"La solicitud ha sido marcada como: {nuevo_estado}")
                self.cargar_panel_solicitudes()
            else:
                QMessageBox.critical(self, "Error", "No se pudo actualizar el estado de la solicitud.")

    # =================================================================
    # NUEVO MÓDULO: SECRETARÍA Y REUNIONES
    # =================================================================
    def abrir_seccion_secretaria(self, id_entidad, tarjeta_pulsada):
        self.seccion_facturas_activa = False
        self.seccion_solicitudes_activa = False
        self.seccion_secretaria_activa = True
        self.id_grupo_seleccionado = None
        
        self.desmarcar_todas_las_tarjetas()
        tarjeta_pulsada.marcar_activa(True)
        self.cargar_panel_secretaria()

    def cargar_panel_secretaria(self):
        self.limpiar_panel_derecho()
        
        lbl_titulo = QLabel("MÓDULO DE SECRETARÍA - REUNIONES")
        lbl_titulo.setStyleSheet("font-weight: bold; font-size: 14px; color: #2C3E50; margin-bottom: 10px; border:none;")
        self.right_layout.addWidget(lbl_titulo)
        
        rol_limpio = str(self.miembro.Rol).strip().upper() if self.miembro.Rol else "MIEMBRO"
        
        # Solo el Secretario puede programar nuevas
        if rol_limpio == "SECRETARIO":
            btn_crear_reunion = QPushButton("Convocar Nueva Reunión")
            btn_crear_reunion.setCursor(Qt.PointingHandCursor)
            btn_crear_reunion.setStyleSheet("QPushButton { background-color: #3498DB; border: 2px solid #000000; border-radius: 5px; padding: 8px; font-weight: bold; color: #FFFFFF; margin-bottom: 12px; } QPushButton:hover { background-color: #2980B9; }")
            btn_crear_reunion.clicked.connect(self.mostrar_dialogo_crear_reunion)
            self.right_layout.addWidget(btn_crear_reunion)

        lista_reuniones = self.secretaria_dao.obtener_reuniones_secretaria() if hasattr(self, 'secretaria_dao') and self.secretaria_dao else []
        
        if not lista_reuniones:
            lbl_vacio = QLabel("No hay reuniones programadas actualmente.")
            lbl_vacio.setStyleSheet("color: #7F8C8D; font-style: italic; border: none; margin-top: 10px;")
            self.right_layout.addWidget(lbl_vacio)
        else:
            for reu in lista_reuniones:
                self.crear_tarjeta_reunion(reu)
                
        self.right_layout.addStretch()

    def crear_tarjeta_reunion(self, reu):
        frame = QFrame()
        frame.setStyleSheet("QFrame { background-color: #FFFFFF; border: 2px solid #000000; border-radius: 8px; }")
        layout = QVBoxLayout(frame)
        layout.setContentsMargins(15, 12, 15, 12)
        
        fila_superior = QHBoxLayout()
        lbl_titulo = QLabel(f"{reu['titulo']}")
        lbl_titulo.setStyleSheet("font-weight: bold; font-size: 14px; border: none;")
        
        lbl_info = QLabel(f"{reu['lugar']} | {reu['fecha']} {reu['hora']}")
        lbl_info.setStyleSheet("color: #666666; font-size: 12px; border: none;")
        
        fila_superior.addWidget(lbl_titulo)
        fila_superior.addStretch()
        fila_superior.addWidget(lbl_info)
        
        fila_inferior = QHBoxLayout()
        
        lbl_estado = QLabel(reu['estado'].upper())
        if reu['estado'] == 'Programada':
            lbl_estado.setStyleSheet("color: #3498DB; font-weight: bold; border: none;")
        elif reu['estado'] == 'Celebrada':
            lbl_estado.setStyleSheet("color: #2ECC71; font-weight: bold; border: none;")
        else:
            lbl_estado.setStyleSheet("color: #E74C3C; font-weight: bold; border: none;")
        
        fila_inferior.addWidget(lbl_estado)
        fila_inferior.addStretch()
        
        rol_limpio = str(self.miembro.Rol).strip().upper() if self.miembro.Rol else "MIEMBRO"
        if rol_limpio in ["SECRETARIO", "PRESIDENTE"] and reu['estado'] == 'Programada':
            btn_celebrada = QPushButton("Celebrada")
            btn_celebrada.setCursor(Qt.PointingHandCursor)
            btn_celebrada.setFixedSize(75, 24)
            btn_celebrada.setStyleSheet("QPushButton { background-color: #2ECC71; color: white; border-radius: 4px; font-weight: bold; border:none; } QPushButton:hover { background-color: #27AE60; }")
            btn_celebrada.clicked.connect(lambda checked, r_id=reu['id']: self.cambiar_estado_reunion(r_id, "Celebrada"))
            
            btn_cancelar = QPushButton("Cancelar")
            btn_cancelar.setCursor(Qt.PointingHandCursor)
            btn_cancelar.setFixedSize(75, 24)
            btn_cancelar.setStyleSheet("QPushButton { background-color: #E74C3C; color: white; border-radius: 4px; font-weight: bold; border:none; } QPushButton:hover { background-color: #C0392B; }")
            btn_cancelar.clicked.connect(lambda checked, r_id=reu['id']: self.cambiar_estado_reunion(r_id, "Cancelada"))
            
            fila_inferior.addWidget(btn_celebrada)
            fila_inferior.addSpacing(8)
            fila_inferior.addWidget(btn_cancelar)
            
        layout.addLayout(fila_superior)
        layout.addLayout(fila_inferior)
        self.right_layout.addWidget(frame)

    def cambiar_estado_reunion(self, reunion_id, nuevo_estado):
        if hasattr(self, 'secretaria_dao') and self.secretaria_dao:
            if self.secretaria_dao.actualizar_estado_reunion(reunion_id, nuevo_estado):
                self.cargar_panel_secretaria()

    def mostrar_dialogo_crear_reunion(self):
        dialogo = QDialog(self)
        dialogo.setWindowTitle("Convocar Nueva Reunión")
        layout = QFormLayout(dialogo)
        
        import datetime
        txt_titulo = QLineEdit()
        txt_fecha = QLineEdit()
        txt_fecha.setPlaceholderText(datetime.date.today().strftime("%Y-%m-%d"))
        txt_hora = QLineEdit()
        txt_hora.setPlaceholderText("Ej: 10:30")
        txt_lugar = QLineEdit()
        
        layout.addRow("Título/Motivo:", txt_titulo)
        layout.addRow("Fecha (YYYY-MM-DD):", txt_fecha)
        layout.addRow("Hora:", txt_hora)
        layout.addRow("Lugar:", txt_lugar)
        
        botones = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        botones.accepted.connect(dialogo.accept)
        botones.rejected.connect(dialogo.reject)
        layout.addWidget(botones)
        
        if dialogo.exec_() == QDialog.Accepted:
            titulo = txt_titulo.text().strip()
            fecha = txt_fecha.text().strip() or datetime.date.today().strftime("%Y-%m-%d")
            hora = txt_hora.text().strip()
            lugar = txt_lugar.text().strip()
            
            if titulo and fecha and hora and lugar:
                if self.secretaria_dao.registrar_reunion(titulo, fecha, hora, lugar):
                    QMessageBox.information(self, "Éxito", "Reunión convocada correctamente.")
                    self.cargar_panel_secretaria()
                else:
                    QMessageBox.critical(self, "Error", "No se pudo registrar en la base de datos.")
            else:
                QMessageBox.warning(self, "Campos Vacíos", "Todos los campos son obligatorios.")

    # =================================================================
    # VENTANAS MODALES GLOBALES
    # =================================================================
    def mostrar_dialogo_cambiar_pass(self):
        dialogo = QDialog(self)
        dialogo.setWindowTitle("Cambiar Contraseña")
        layout = QFormLayout(dialogo)
        
        txt_pass = QLineEdit(); txt_pass.setEchoMode(QLineEdit.Password)
        txt_conf = QLineEdit(); txt_conf.setEchoMode(QLineEdit.Password)
        
        layout.addRow("Nueva:", txt_pass)
        layout.addRow("Confirmar:", txt_conf)
        
        botones = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        botones.accepted.connect(dialogo.accept)
        botones.rejected.connect(dialogo.reject)
        layout.addWidget(botones)
        
        if dialogo.exec_() == QDialog.Accepted:
            if txt_pass.text() != txt_conf.text():
                return QMessageBox.warning(self, "Error", "Las contraseñas no coinciden.")
            
            from DAO.MiembroDAO import MiembroDAO
            conexion_activa = self.grupo_controller.grupo_dao.conexion if hasattr(self, 'grupo_controller') and self.grupo_controller else None
            
            if conexion_activa:
                dao = MiembroDAO(conexion_activa)
                if dao.actualizar_contrasena(self.miembro.NombreUsuario, txt_pass.text().strip()):
                    QMessageBox.information(self, "Éxito", "Contraseña actualizada.")
                else:
                    QMessageBox.critical(self, "Error", "Fallo al actualizar en BD.")

    def abrir_dialogo_solicitar_materiales(self):
        dialogo = QDialog(self)
        dialogo.setWindowTitle("Solicitar Materiales")
        layout = QFormLayout(dialogo)
        
        txt_mat = QLineEdit()
        txt_cant = QLineEdit()
        
        layout.addRow("Material:", txt_mat)
        layout.addRow("Cantidad:", txt_cant)
        
        botones = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        botones.accepted.connect(dialogo.accept)
        botones.rejected.connect(dialogo.reject)
        layout.addWidget(botones)
        
        if dialogo.exec_() == QDialog.Accepted:
            try:
                cant = int(txt_cant.text().strip())
                if hasattr(self, 'solicitud_dao') and self.solicitud_dao:
                    self.solicitud_dao.registrar_solicitud(txt_mat.text().strip(), cant, self.miembro.Name)
                    QMessageBox.information(self, "Éxito", "Solicitud enviada a Tesorería.")
            except ValueError:
                QMessageBox.warning(self, "Error", "La cantidad debe ser un número.")

    def abrir_dialogo_crear_grupo(self):
        nombre, ok = QInputDialog.getText(self, "Nuevo Grupo", "Nombre del grupo:")
        if ok and nombre.strip() and self.grupo_controller:
            exito, msg = self.grupo_controller.procesar_crear_grupo(self.miembro.Rol, nombre.strip(), self.miembro.UsuarioID)
            if exito:
                self.refrescar_grupos()
            else:
                QMessageBox.critical(self, "Error", msg)

    def abrir_dialogo_crear_tarea(self):
        dialogo = QDialog(self)
        dialogo.setWindowTitle("Asignar Tarea")
        layout = QFormLayout(dialogo)
        
        txt_titulo = QLineEdit()
        txt_desc = QTextEdit()
        txt_fecha = QLineEdit()
        import datetime
        txt_fecha.setPlaceholderText(datetime.date.today().strftime("%Y-%m-%d"))
        
        layout.addRow("Título:", txt_titulo)
        layout.addRow("Descripción:", txt_desc)
        layout.addRow("Fecha Límite:", txt_fecha)
        
        botones = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        botones.accepted.connect(dialogo.accept)
        botones.rejected.connect(dialogo.reject)
        layout.addWidget(botones)
        
        if dialogo.exec_() == QDialog.Accepted:
            fecha = txt_fecha.text().strip() or datetime.date.today().strftime("%Y-%m-%d")
            exito, msg = self.tarea_controller.procesar_crear_tarea(self.miembro.Rol, self.id_grupo_seleccionado, txt_titulo.text().strip(), txt_desc.toPlainText().strip(), fecha)
            if exito:
                self.cargar_panel_derecho_grupo()
            else:
                QMessageBox.critical(self, "Error", msg)

    def abrir_dialogo_crear_factura(self):
        dialogo = QDialog(self)
        dialogo.setWindowTitle("Nueva Factura")
        layout = QFormLayout(dialogo)
        
        txt_concepto = QLineEdit()
        txt_monto = QLineEdit()
        cb_estado = QComboBox()
        cb_estado.addItems(["Pendiente", "Pagado"])
        
        layout.addRow("Concepto:", txt_concepto)
        layout.addRow("Monto:", txt_monto)
        layout.addRow("Estado:", cb_estado)
        
        botones = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        botones.accepted.connect(dialogo.accept)
        botones.rejected.connect(dialogo.reject)
        layout.addWidget(botones)
        
        if dialogo.exec_() == QDialog.Accepted:
            try:
                monto = float(txt_monto.text().strip())
                import datetime
                if hasattr(self, 'factura_dao') and self.factura_dao:
                    self.factura_dao.insertar_factura(txt_concepto.text().strip(), monto, datetime.date.today().strftime("%Y-%m-%d"), cb_estado.currentText())
                    self.cargar_panel_facturas()
            except ValueError:
                QMessageBox.warning(self, "Error", "Monto inválido.")

    def abrir_dialogo_editar_factura(self, factura_dict):
        dialogo = QDialog(self)
        dialogo.setWindowTitle("Editar Factura")
        layout = QFormLayout(dialogo)
        
        txt_concepto = QLineEdit(factura_dict['concepto'])
        txt_monto = QLineEdit(factura_dict['monto'].replace(" €", "").strip())
        cb_estado = QComboBox()
        cb_estado.addItems(["Pendiente", "Pagado"])
        cb_estado.setCurrentText(factura_dict['estado'])
        
        layout.addRow("Concepto:", txt_concepto)
        layout.addRow("Monto:", txt_monto)
        layout.addRow("Estado:", cb_estado)
        
        botones = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        botones.accepted.connect(dialogo.accept)
        botones.rejected.connect(dialogo.reject)
        layout.addWidget(botones)
        
        if dialogo.exec_() == QDialog.Accepted:
            try:
                monto = float(txt_monto.text().strip())
                if hasattr(self, 'factura_dao') and self.factura_dao:
                    self.factura_dao.actualizar_factura(factura_dict['id'], txt_concepto.text().strip(), monto, cb_estado.currentText())
                    self.cargar_panel_facturas()
            except ValueError:
                QMessageBox.warning(self, "Error", "Monto inválido.")

    def refrescar_grupos(self):
        if hasattr(self, 'grupo_controller') and self.grupo_controller:
            self.lista_grupos = self.grupo_controller.obtener_grupos_usuario(self.miembro.UsuarioID, self.miembro.Rol)
            self.cargar_grupos_izquierdos()

    def abrir_modulo_bienes(self):
        if hasattr(self, 'bienes_controller') and self.bienes_controller:
            self.bienes_controller.abrir_pantalla_bienes()