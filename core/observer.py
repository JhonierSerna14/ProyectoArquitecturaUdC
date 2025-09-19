"""
Patrón Observer para la comunicación entre componentes del simulador.

Este módulo implementa las clases base Observable y Observer que permiten
la comunicación desacoplada entre los componentes de hardware y la interfaz gráfica.
"""

from abc import ABC, abstractmethod
from typing import Any, List


class Observer(ABC):
    """
    Interfaz abstracta para observadores en el patrón Observer.
    
    Los observadores reciben notificaciones cuando el estado de un
    objeto observable cambia.
    """
    
    @abstractmethod
    def update(self, observable: 'Observable', event_type: str, data: Any = None) -> None:
        """
        Método llamado cuando el objeto observable notifica un cambio.
        
        Args:
            observable: El objeto que generó la notificación
            event_type: Tipo de evento que ocurrió
            data: Datos adicionales sobre el evento
        """
        pass


class Observable:
    """
    Clase base para objetos observables en el patrón Observer.
    
    Los objetos observables mantienen una lista de observadores y
    los notifican cuando su estado cambia.
    """
    
    def __init__(self):
        """Inicializa la lista de observadores."""
        self._observers: List[Observer] = []
    
    def add_observer(self, observer: Observer) -> None:
        """
        Agrega un observador a la lista de notificaciones.
        
        Args:
            observer: El observador a agregar
        """
        if observer not in self._observers:
            self._observers.append(observer)
    
    def remove_observer(self, observer: Observer) -> None:
        """
        Remueve un observador de la lista de notificaciones.
        
        Args:
            observer: El observador a remover
        """
        if observer in self._observers:
            self._observers.remove(observer)
    
    def notify_observers(self, event_type: str, data: Any = None) -> None:
        """
        Notifica a todos los observadores sobre un cambio de estado.
        
        Args:
            event_type: Tipo de evento que ocurrió
            data: Datos adicionales sobre el evento
        """
        for observer in self._observers:
            observer.update(self, event_type, data)
    
    def clear_observers(self) -> None:
        """Remueve todos los observadores."""
        self._observers.clear()


class EventType:
    """
    Constantes para los tipos de eventos del simulador.
    
    Esta clase centraliza todos los tipos de eventos que pueden
    ser notificados en el sistema.
    """
    
    # Eventos de registros
    REGISTER_VALUE_CHANGED = "register_value_changed"
    REGISTER_CLEARED = "register_cleared"
    
    # Eventos de memoria
    MEMORY_INSTRUCTION_LOADED = "memory_instruction_loaded"
    MEMORY_DATA_STORED = "memory_data_stored"
    MEMORY_DATA_LOADED = "memory_data_loaded"
    MEMORY_CLEARED = "memory_cleared"
    
    # Eventos de ALU
    ALU_OPERATION_EXECUTED = "alu_operation_executed"
    ALU_FLAGS_UPDATED = "alu_flags_updated"
    
    # Eventos de unidad de control
    INSTRUCTION_FETCHED = "instruction_fetched"
    INSTRUCTION_DECODED = "instruction_decoded"
    INSTRUCTION_EXECUTED = "instruction_executed"
    
    # Eventos de buses
    BUS_ADDRESS_ACTIVATED = "bus_address_activated"
    BUS_DATA_ACTIVATED = "bus_data_activated"
    BUS_CONTROL_ACTIVATED = "bus_control_activated"
    
    # Eventos del sistema
    SYSTEM_RESET = "system_reset"
    PROGRAM_LOADED = "program_loaded"
    EXECUTION_COMPLETED = "execution_completed"