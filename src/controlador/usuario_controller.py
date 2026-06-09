# archivo: controller/usuario_controller.py

class UsuarioController:
    def __init__(self, miembro_dao, departamento_dao, grupo_dao):
        self.miembro_dao = miembro_dao
        self.departamento_dao = departamento_dao 
        self.grupo_dao = grupo_dao  
        self.vista_gestion = None
        self.usuario_logueado = None

    def abrir_pantalla_gestion(self, parent_view=None):
        from vistas.gestion_miembros_view import GestionMiembrosView
        
        self.vista_gestion = GestionMiembrosView(
            callback_filtrar=self.filtrar_miembros,
            callback_seleccionar_miembro=self.cargar_detalle_miembro,
            callback_aceptar=self.procesar_aceptar_miembro,
            callback_eliminar=self.procesar_eliminar_miembro,
            callback_actualizar=self.procesar_actualizar_miembro,
            controller=self  
        )
        todos_los_miembros = self.miembro_dao.obtener_miembros_para_gestion()
        self.vista_gestion.llenar_tabla_miembros(todos_los_miembros)
        
        departamentos_bd = self.departamento_dao.obtener_todos_los_tipos()
        self.vista_gestion.llenar_combo_departamentos(departamentos_bd)
        
        self.vista_gestion.show()

    def filtrar_miembros(self, tipo_departamento):
        """Filtra la lista de miembros según el departamento"""
        miembros_filtrados = self.miembro_dao.obtener_miembros_para_gestion(tipo_departamento)
        self.vista_gestion.llenar_tabla_miembros(miembros_filtrados)

    def cargar_detalle_miembro(self, usuario_id):
        """Carga el Value Object (VO) detallado de un miembro desde la BD y redibuja la derecha"""
        miembro_completo = self.miembro_dao.buscar_por_id(usuario_id)
        if miembro_completo:
            self.vista_gestion.mostrar_panel_derecho(miembro_completo)
        else:
            self.vista_gestion.mostrar_mensaje_error("No se pudo cargar la información detallada del miembro.")

    def _refrescar_tabla_con_filtro_actual(self):
        """Helper para refrescar la tabla usando el filtro activo de la UI"""
        if self.vista_gestion:
            filtro_actual = self.vista_gestion.obtener_filtro_actual()
            self.filtrar_miembros(filtro_actual)

    # =================================================================
    # MÉTODOS AUXILIARES PARA PASAR DATOS A LA VISTA
    # =================================================================
    def obtener_listados_para_edicion(self, miembro_vo):
        """Devuelve los catálogos completos de la organización disponibles para asignar"""
        cat_departamentos = self.departamento_dao.obtener_todos_los_tipos()
        cat_grupos = self.miembro_dao.conexion.cursor()
        
        cat_grupos.execute("SELECT Name FROM Grupos ORDER BY Name ASC")
        filas = cat_grupos.fetchall()
        lista_grupos_limpios = [str(f[0]).strip() for f in filas if f[0]]
        cat_grupos.close()
        
        return cat_departamentos, lista_grupos_limpios

    # =================================================================
    # PROCESADORES DE ACCIONES 
    # =================================================================

    def procesar_aceptar_miembro(self, usuario_id):
        if self.miembro_dao.aceptar_miembro(usuario_id):
            self.vista_gestion.mostrar_mensaje_exito("El miembro ha sido aceptado en el sistema correctamente.")
            self._refrescar_tabla_con_filtro_actual()
            self.cargar_detalle_miembro(usuario_id)
        else:
            self.vista_gestion.mostrar_mensaje_error("No se pudo cambiar el estado del miembro en la base de datos.")

    def procesar_eliminar_miembro(self, usuario_id):
        if self.miembro_dao.eliminar_miembro(usuario_id):
            self.vista_gestion.mostrar_mensaje_exito("El miembro ha sido eliminado permanentemente.")
            self._refrescar_tabla_con_filtro_actual()
            self.vista_gestion.limpiar_detalle() 
        else:
            self.vista_gestion.mostrar_mensaje_error("Error al intentar eliminar el registro.")

    def procesar_actualizar_miembro(self, usuario_id, dni, nombre, apellido, telefono, email, rol, lista_deptos, lista_grupos):
        exito_base = self.miembro_dao.actualizar_miembro(usuario_id, dni, nombre, apellido, telefono, email, rol)
        
        if exito_base:
            self.miembro_dao.limpiar_departamentos_usuario(usuario_id)
            for nombre_depto in lista_deptos:
                self.miembro_dao.vincular_a_departamento(usuario_id, nombre_depto)
                
            self.miembro_dao.limpiar_grupos_usuario(usuario_id)
            for nombre_grupo in lista_grupos:
                self.miembro_dao.vincular_a_grupo(usuario_id, nombre_grupo)

            self.vista_gestion.mostrar_mensaje_exito("Miembro y todas sus asignaciones múltiples actualizadas correctamente.")

            self._refrescar_tabla_con_filtro_actual()
            self.cargar_detalle_miembro(usuario_id) 
        else:
            self.vista_gestion.mostrar_mensaje_error("No se pudieron guardar los cambios básicos en la base de datos.")

    def procesar_agregar_miembro(self, rol_operador, datos):
        """Valida permisos del administrador y procesa el alta del nuevo miembro en ambas tablas"""
        rol_op = str(rol_operador).strip().upper()
        if rol_op not in ["PRESIDENTE", "JEFE DEPARTAMENTO"]:
            return False, "No tienes privilegios para registrar nuevos miembros."
            
        # Validaciones de campos obligatorios
        if not datos.get("dni") or not datos.get("nombre") or not datos.get("apellido"):
            return False, "El DNI, Nombre y Apellidos son campos obligatorios."
            

        primera_letra = datos['nombre'][0].lower() if datos['nombre'] else 'u'
        primer_apellido = datos['apellido'].split()[0].lower() if datos['apellido'] else 'usuario'
        nombre_usuario = f"{primera_letra}{primer_apellido}"
        

        usuario_id = self.miembro_dao.insertar_miembro_completo(
            dni=datos["dni"],
            nombre=datos["nombre"],
            apellido=datos["apellido"],
            telefono=datos["telefono"],
            email=datos["email"],
            rol=datos["rol"],
            usuario_nombre=nombre_usuario,
            password="12345" 
        )
        
        if usuario_id:
            for nombre_depto in datos.get("departamentos_lista", []):
                self.miembro_dao.vincular_a_departamento(usuario_id, nombre_depto)
                
            for nombre_grupo in datos.get("grupos_lista", []):
                self.miembro_dao.vincular_a_grupo(usuario_id, nombre_grupo)
                
            return True, f"El miembro '{datos['nombre']} {datos['apellido']}' ha sido pre-registrado con el usuario '{nombre_usuario}'."
        
        return False, "No se pudo completar el registro. Verifique que el DNI o el Nombre de Usuario no estén duplicados."