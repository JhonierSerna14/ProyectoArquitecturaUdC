"""
Registro individual refactorizado con patrón Observer.

Este módulo implementa un registro que notifica cambios usando
el patrón Observer para desacoplar la lógica de la presentación.
"""

from typing import Any
from core.observer import Observable, EventType


class Register(Observable):
    """
    Registro individual que notifica cambios de estado.
    
    Utiliza el patrón Observer para notificar cuando su valor cambia,
    permitiendo que la interfaz gráfica se actualice automáticamente.
    """
    
    def __init__(self, name: str, initial_value: Any = 0):
        """
        Inicializa el registro con un nombre y valor inicial.
        
        Args:
            name: Nombre identificativo del registro
            initial_value: Valor inicial del registro
        """
        super().__init__()
        self._name = name
        self._value = initial_value
    
    @property
    def name(self) -> str:
        """Obtiene el nombre del registro."""
        return self._name
    
    @property
    def value(self) -> Any:
        """Obtiene el valor actual del registro."""
        return self._value
    
    def set_value(self, value: Any) -> None:
        """
        Establece un nuevo valor y notifica a los observadores.
        
        Args:
            value: Nuevo valor para el registro
        """
        old_value = self._value
        
        # Solo notificar si el valor realmente cambió
        if old_value != value:
            self._value = value
            
            # Notificar el cambio a todos los observadores
            self.notify_observers(
                EventType.REGISTER_VALUE_CHANGED,
                {
                    'register_name': self._name,
                    'old_value': old_value,
                    'new_value': value
                }
            )
        else:
            # Actualizar el valor sin notificar
            self._value = value
    
    def clear(self) -> None:
        """Limpia el registro estableciendo valor a 0."""
        self.set_value(0)
        self.notify_observers(
            EventType.REGISTER_CLEARED,
            {'register_name': self._name}
        )
    
    def __str__(self) -> str:
        """Representación string del registro."""
        return f"{self._name}: {self._value}"
    
    def __repr__(self) -> str:
        """Representación detallada del registro."""
        return f"Register(name='{self._name}', value={self._value})"