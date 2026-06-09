# archivo: controller/secretaria_controller.py

class SecretariaController:
    def __init__(self, secretaria_dao):
        self.secretaria_dao = secretaria_dao
        self.vista_secretaria = None