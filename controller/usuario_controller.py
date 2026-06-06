class UsuarioController:
    def __init__(self, miembro_dao, departamento_dao):
        self.miembro_dao = miembro_dao
        self.departamento_dao = departamento_dao 
        self.vista_gestion = None

    def abrir_pantalla_gestion(self, parent_view=None):
        from vistas.gestion_miembros_view import GestionMiembrosView
        
        self.vista_gestion = GestionMiembrosView(
            callback_filtrar=self.filtrar_miembros,
            callback_seleccionar_miembro=self.cargar_detalle_miembro
        )
        todos_los_miembros = self.miembro_dao.obtener_miembros_para_gestion()
        self.vista_gestion.llenar_tabla_miembros(todos_los_miembros)
        
        departamentos_bd = self.departamento_dao.obtener_todos_los_tipos()
        self.vista_gestion.llenar_combo_departamentos(departamentos_bd)
        
        self.vista_gestion.show()

    def filtrar_miembros(self, tipo_departamento):
        """Se ejecuta automáticamente cuando cambias el ComboBox"""
        miembros_filtrados = self.miembro_dao.obtener_miembros_para_gestion(tipo_departamento)
        self.vista_gestion.llenar_tabla_miembros(miembros_filtrados)

    def cargar_detalle_miembro(self, usuario_id):
        miembro_vo = self.miembro_dao.buscar_por_id(usuario_id)
        if miembro_vo:
            self.vista_gestion.mostrar_panel_derecho(miembro_vo)