"""
Banco de registros refactorizado con patrón Observer.

Este módulo implementa un banco de registros que gestiona
múltiples registros y notifica cambios de estado.
"""

from typing import Dict, Any
from hardware.register import Register
from core.observer import Observable, EventType
from core.exceptions import RegisterNotFoundError


class RegisterBank(Observable):
    """
    Banco de registros que gestiona múltiples registros numerados.
    
    Mantiene registros R1-R9 y notifica cambios usando el patrón Observer.
    """
    
    def __init__(self):
        """Inicializa el banco con registros R1-R9."""
        super().__init__()
        self._registers: Dict[str, Register] = {}
        
        # Crear registros R1 a R9
        for i in range(1, 10):
            reg_name = f'R{i}'
            register = Register(reg_name)
            # Propagar eventos del registro individual
            register.add_observer(self)
            self._registers[reg_name] = register
    
    def update(self, observable: Observable, event_type: str, data: Any = None) -> None:
        """
        Recibe notificaciones de registros individuales y las propaga.
        
        Args:
            observable: El registro que cambió
            event_type: Tipo de evento
            data: Datos del evento
        """
        # Propagar el evento a nuestros observadores
        self.notify_observers(event_type, data)
    
    def get(self, reg_name: str) -> Any:
        """
        Obtiene el valor de un registro específico.
        
        Args:
            reg_name: Nombre del registro (ej: 'R1', 'R2', etc.)
            
        Returns:
            Valor almacenado en el registro
            
        Raises:
            RegisterNotFoundError: Si el registro no existe
        """
        if reg_name not in self._registers:
            raise RegisterNotFoundError(f"Register {reg_name} not found")
        return self._registers[reg_name].value
    
    def set(self, reg_name: str, value: Any) -> None:
        """
        Establece un valor en un registro específico.
        
        Args:
            reg_name: Nombre del registro
            value: Valor a almacenar
            
        Raises:
            RegisterNotFoundError: Si el registro no existe
        """
        if reg_name not in self._registers:
            raise RegisterNotFoundError(f"Register {reg_name} not found")
        self._registers[reg_name].set_value(value)
    
    def get_register(self, reg_name: str) -> Register:
        """
        Obtiene la instancia completa de un registro.
        
        Args:
            reg_name: Nombre del registro
            
        Returns:
            Instancia del registro
            
        Raises:
            RegisterNotFoundError: Si el registro no existe
        """
        if reg_name not in self._registers:
            raise RegisterNotFoundError(f"Register {reg_name} not found")
        return self._registers[reg_name]
    
    def clear_all(self) -> None:
        """Limpia todos los registros."""
        for register in self._registers.values():
            register.clear()
        
        self.notify_observers(
            EventType.REGISTER_CLEARED,
            {'message': 'All registers cleared'}
        )
    
    def get_all_registers(self) -> Dict[str, Register]:
        """
        Obtiene todos los registros.
        
        Returns:
            Diccionario con todos los registros
        """
        return self._registers.copy()
    
    def exists(self, reg_name: str) -> bool:
        """
        Verifica si un registro existe.
        
        Args:
            reg_name: Nombre del registro
            
        Returns:
            True si el registro existe
        """
        return reg_name in self._registers
    
    def get_register_names(self) -> list:
        """
        Obtiene una lista de nombres de registros disponibles.
        
        Returns:
            Lista de nombres de registros
        """
        return list(self._registers.keys())
    
    def __str__(self) -> str:
        """Representación string del banco de registros."""
        reg_states = [str(reg) for reg in self._registers.values()]
        return f"RegisterBank({', '.join(reg_states)})"