
# archivo: controlador/secretaria_controller.py


class SecretariaController:
    def __init__(self, secretaria_service):
        self.service = secretaria_service
        self.vista_secretaria = None
        self.usuario_logueado = None  # inyectado por ControladorApp tras el login

    # ------------------------------------------------------------------
    # CONSULTA
    # ------------------------------------------------------------------
    def obtener_reuniones(self):
        """Devuelve la lista de reuniones para mostrar en la vista."""
        try:
            return self.service.obtener_reuniones()
        except Exception as e:
            print(f"[SecretariaController] Error obteniendo reuniones: {e}")
            return []

    # ------------------------------------------------------------------
    # CREACION
    # ------------------------------------------------------------------
    def procesar_crear_reunion(self, datos: dict):
        """
        Recibe los datos del formulario, obtiene el rol del usuario logueado
        y delega la validacion/creacion al servicio.
        Devuelve (True, mensaje) o (False, mensaje).
        """
        if not datos:
            return False, "No se recibieron datos para crear la reunion."

        rol_operador = self._obtener_rol_operador()

        try:
            return self.service.crear_reunion(datos, rol_operador)
        except ValueError as e:
            return False, f"Dato invalido: {str(e)}"
        except Exception as e:
            print(f"[SecretariaController] Error creando reunion: {e}")
            return False, f"Error inesperado al convocar la reunion: {str(e)}"

    # ------------------------------------------------------------------
    # CAMBIO DE ESTADO
    # ------------------------------------------------------------------
    def procesar_cambiar_estado(self, reunion_id, nuevo_estado):
        """
        Cambia el estado de una reunion (Celebrada / Cancelada), validando
        el rol del usuario logueado.
        Devuelve (True, mensaje) o (False, mensaje).
        """
        if reunion_id is None:
            return False, "No se especifico el ID de la reunion."

        rol_operador = self._obtener_rol_operador()

        try:
            return self.service.cambiar_estado_reunion(reunion_id, nuevo_estado, rol_operador)
        except ValueError as e:
            return False, f"Dato invalido: {str(e)}"
        except Exception as e:
            print(f"[SecretariaController] Error cambiando estado de reunion {reunion_id}: {e}")
            return False, f"Error inesperado al actualizar la reunion: {str(e)}"

    # ------------------------------------------------------------------
    # AUXILIARES
    # ------------------------------------------------------------------
    def _obtener_rol_operador(self):
        user = self.usuario_logueado
        if not user:
            return "MIEMBRO"
        if isinstance(user, dict):
            return str(user.get("Rol", user.get("rol", "MIEMBRO"))).strip().upper()
        return str(getattr(user, "Rol", getattr(user, "rol", "MIEMBRO"))).strip().upper()