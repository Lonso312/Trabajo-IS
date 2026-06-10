from modelo.vo.BienVO import BienVO

class BienesService:
    def __init__(self, bienes_dao):
        self.bienes_dao = bienes_dao

    def verificar_acceso(self, rol):
        if rol not in ['PRESIDENTE', 'TESORERO', 'JEFE DEPARTAMENTO']:
            return False, "Solo Tesoreros o Presidentes pueden gestionar los bienes."
        return True, ""

    def obtener_bienes(self):
        return self.bienes_dao.obtener_bienes_para_gestion()

    def obtener_bien(self, bien_id):
        return self.bienes_dao.buscar_por_id(bien_id)

    def añadir_bien(self, datos):
        nuevo_bien = BienVO(
            tipo=datos['tipo'],
            precio=float(datos['precio']),
            cantidad=int(datos['cantidad'])
        )
        return self.bienes_dao.crear(nuevo_bien)

    def actualizar_bien(self, bien_id, datos):
        return self.bienes_dao.actualizar_bien(
            bien_id, datos['tipo'],
            float(datos['precio']),
            int(datos['cantidad'])
        )

    def eliminar_bien(self, bien_id):
        return self.bienes_dao.eliminar_bien(bien_id)