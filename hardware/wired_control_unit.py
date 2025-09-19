"""
Unidad de Control Cableada refactorizada con patrón Observer.

Este módulo implementa la unidad de control cableada que genera
señales de control basadas en opcodes.
"""

from typing import Dict, Any
from core.observer import Observable, EventType


class WiredControlUnit(Observable):
    """
    Unidad de Control Cableada que genera señales de control.
    
    Genera las señales de control apropiadas para cada instrucción
    y notifica los cambios usando el patrón Observer.
    """
    
    def __init__(self):
        """Inicializa la unidad de control cableada."""
        super().__init__()
        self._control_signals: Dict[str, Any] = {}
    
    @property
    def control_signals(self) -> Dict[str, Any]:
        """Obtiene las señales de control actuales."""
        return self._control_signals.copy()
    
    def generate_control_signals(self, opcode: str) -> Dict[str, Any]:
        """
        Genera señales de control basadas en el opcode.
        
        Args:
            opcode: Código de operación de la instrucción
            
        Returns:
            Diccionario con las señales de control
        """
        old_signals = self._control_signals.copy()
        
        # Resetear señales a estado inicial
        self._control_signals = {
            'fetch': True,
            'decode': True,
            'execute': False,
            'memory_read': False,
            'memory_write': False,
            'register_read': False,
            'register_write': False,
            'alu_operation': None,
        }
        
        # Configurar señales según el opcode
        opcode = opcode.upper()
        
        if opcode in ['ADD', 'SUB', 'MUL', 'DIV', 'AND', 'OR', 'NOT', 'XOR']:
            self._configure_alu_operation(opcode)
            
        elif opcode == 'LOAD':
            self._configure_load_operation()
            
        elif opcode == 'STORE':
            self._configure_store_operation()
            
        elif opcode == 'MOVE':
            self._configure_move_operation()
            
        elif opcode in ['JP', 'JPZ']:
            self._configure_jump_operation(opcode)
        
        # Notificar cambio de señales
        self.notify_observers(
            EventType.BUS_CONTROL_ACTIVATED,
            {
                'old_signals': old_signals,
                'new_signals': self._control_signals.copy(),
                'opcode': opcode
            }
        )
        
        return self._control_signals.copy()
    
    def _configure_alu_operation(self, opcode: str) -> None:
        """Configura señales para operaciones de ALU."""
        self._control_signals.update({
            'execute': True,
            'alu_operation': opcode,
            'register_read': True,
            'register_write': True
        })
    
    def _configure_load_operation(self) -> None:
        """Configura señales para operación LOAD."""
        self._control_signals.update({
            'memory_read': True,
            'register_write': True
        })
    
    def _configure_store_operation(self) -> None:
        """Configura señales para operación STORE."""
        self._control_signals.update({
            'memory_write': True,
            'register_read': True
        })
    
    def _configure_move_operation(self) -> None:
        """Configura señales para operación MOVE."""
        self._control_signals.update({
            'register_read': True,
            'register_write': True
        })
    
    def _configure_jump_operation(self, opcode: str) -> None:
        """Configura señales para operaciones de salto."""
        self._control_signals.update({
            'execute': True,
            'alu_operation': opcode
        })
    
    def reset(self) -> None:
        """Resetea la unidad de control cableada."""
        old_signals = self._control_signals.copy()
        
        self._control_signals = {
            'fetch': False,
            'decode': False,
            'execute': False,
            'memory_read': False,
            'memory_write': False,
            'register_read': False,
            'register_write': False,
            'alu_operation': None,
        }
        
        self.notify_observers(
            EventType.SYSTEM_RESET,
            {
                'component': 'WiredControlUnit',
                'old_signals': old_signals,
                'new_signals': self._control_signals.copy()
            }
        )
    
    def get_signal_status(self, signal_name: str) -> Any:
        """
        Obtiene el estado de una señal específica.
        
        Args:
            signal_name: Nombre de la señal
            
        Returns:
            Estado de la señal o None si no existe
        """
        return self._control_signals.get(signal_name)
    
    def is_signal_active(self, signal_name: str) -> bool:
        """
        Verifica si una señal está activa.
        
        Args:
            signal_name: Nombre de la señal
            
        Returns:
            True si la señal está activa
        """
        signal = self._control_signals.get(signal_name)
        return signal is not None and signal is not False and signal != 0
    
    def get_active_signals(self) -> Dict[str, Any]:
        """
        Obtiene solo las señales que están activas.
        
        Returns:
            Diccionario con señales activas
        """
        return {
            name: value for name, value in self._control_signals.items()
            if self.is_signal_active(name)
        }
    
    def get_signal_summary(self) -> str:
        """
        Obtiene un resumen de las señales activas.
        
        Returns:
            String con resumen de señales activas
        """
        active_signals = self.get_active_signals()
        if not active_signals:
            return "No active signals"
        
        return ", ".join([
            f"{name}: {value}" for name, value in active_signals.items()
        ])