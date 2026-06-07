<<<<<<< HEAD
# archivo: utils/event_bus.py
from PyQt5.QtCore import QObject, pyqtSignal

class EventBus(QObject):
    _instancia = None
    
    # Definimos los "eventos" que pueden ocurrir en la app
    grupos_actualizados = pyqtSignal()
    miembros_actualizados = pyqtSignal()

    @classmethod
    def get_instance(cls):
        """Método seguro para obtener la instancia Singleton en PyQt5"""
        if cls._instancia is None:
            cls._instancia = cls()
=======
# archivo: utils/event_bus.py
from PyQt5.QtCore import QObject, pyqtSignal

class EventBus(QObject):
    _instancia = None
    
    # Definimos los "eventos" que pueden ocurrir en la app
    grupos_actualizados = pyqtSignal()
    miembros_actualizados = pyqtSignal()

    @classmethod
    def get_instance(cls):
        """Método seguro para obtener la instancia Singleton en PyQt5"""
        if cls._instancia is None:
            cls._instancia = cls()
>>>>>>> 7d2097279427808e297d5ac03d7624f74165e601
        return cls._instancia