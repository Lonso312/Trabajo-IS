from PyQt5.QtCore import QObject, pyqtSignal

class EventBus(QObject):
    _instancia = None
    
    grupos_actualizados = pyqtSignal()
    miembros_actualizados = pyqtSignal()

    @classmethod
    def get_instance(cls):
        """Método seguro para obtener la instancia Singleton en PyQt5"""
        if cls._instancia is None:
            cls._instancia = cls()
        return cls._instancia
