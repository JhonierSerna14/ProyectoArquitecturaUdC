"""
Memoria refactorizada con patrón Observer.

Este módulo implementa la memoria del sistema que gestiona
instrucciones y datos, notificando cambios de estado.
"""

from typing import Dict, List, Any, TYPE_CHECKING
from core.observer import Observable, EventType
from core.exceptions import InvalidMemoryAddressError, MemoryOverflowError

if TYPE_CHECKING:
    from hardware.register import Register


class Memory(Observable):
    """
    Memoria del sistema que gestiona instrucciones y datos.
    
    Divide la memoria en secciones de instrucciones y datos,
    notificando cambios usando el patrón Observer.
    """
    
    def __init__(self, size: int = 32):
        """
        Inicializa la memoria con el tamaño especificado.
        
        Args:
            size: Tamaño total de la memoria (default: 32)
        """
        super().__init__()
        self._size = size
        self._instruction_size = size // 2
        self._data_size = size // 2
        
        # Memoria de instrucciones (primera mitad)
        self._instruction_memory: List[str] = [''] * self._instruction_size
        
        # Memoria de datos (segunda mitad) - usando registros observables
        from hardware.register import Register
        self._data_memory: Dict[int, 'Register'] = {}
        for i in range(self._instruction_size, size):
            data_register = Register(f"MEM[{i}]")
            data_register.add_observer(self)
            self._data_memory[i] = data_register
    
    def update(self, observable: Observable, event_type: str, data: Any = None) -> None:
        """
        Recibe notificaciones de registros de datos y las propaga.
        
        Args:
            observable: El registro que cambió
            event_type: Tipo de evento
            data: Datos del evento
        """
        # Propagar eventos de memoria de datos
        if event_type == EventType.REGISTER_VALUE_CHANGED:
            self.notify_observers(
                EventType.MEMORY_DATA_STORED,
                data
            )
    
    @property
    def size(self) -> int:
        """Obtiene el tamaño total de la memoria."""
        return self._size
    
    @property
    def instruction_size(self) -> int:
        """Obtiene el tamaño de la memoria de instrucciones."""
        return self._instruction_size
    
    @property
    def data_size(self) -> int:
        """Obtiene el tamaño de la memoria de datos."""
        return self._data_size
    
    def load_instruction(self, address: int) -> str:
        """
        Carga una instrucción desde la memoria.
        
        Args:
            address: Dirección de memoria
            
        Returns:
            Instrucción en la dirección especificada
            
        Raises:
            InvalidMemoryAddressError: Si la dirección es inválida
        """
        if not self._is_valid_instruction_address(address):
            raise InvalidMemoryAddressError(
                f"Invalid instruction address: {address}. Valid range: 0-{self._instruction_size-1}"
            )
        
        instruction = self._instruction_memory[address]
        
        self.notify_observers(
            EventType.MEMORY_INSTRUCTION_LOADED,
            {
                'address': address,
                'instruction': instruction
            }
        )
        
        return instruction
    
    def store_instruction(self, address: int, instruction: str) -> None:
        """
        Almacena una instrucción en la memoria.
        
        Args:
            address: Dirección donde almacenar
            instruction: Instrucción a almacenar
            
        Raises:
            InvalidMemoryAddressError: Si la dirección es inválida
        """
        if not self._is_valid_instruction_address(address):
            raise InvalidMemoryAddressError(
                f"Invalid instruction address: {address}. Valid range: 0-{self._instruction_size-1}"
            )
        
        old_instruction = self._instruction_memory[address]
        self._instruction_memory[address] = instruction
        
        self.notify_observers(
            EventType.MEMORY_INSTRUCTION_LOADED,
            {
                'address': address,
                'old_instruction': old_instruction,
                'new_instruction': instruction
            }
        )
    
    def load_data(self, address: int) -> 'Register':
        """
        Carga un dato desde la memoria.
        
        Args:
            address: Dirección de memoria
            
        Returns:
            Registro con el dato
            
        Raises:
            InvalidMemoryAddressError: Si la dirección es inválida
        """
        if not self._is_valid_data_address(address):
            raise InvalidMemoryAddressError(
                f"Invalid data address: {address}. Valid range: {self._instruction_size}-{self._size-1}"
            )
        
        data_register = self._data_memory[address]
        
        self.notify_observers(
            EventType.MEMORY_DATA_LOADED,
            {
                'address': address,
                'value': data_register.value
            }
        )
        
        return data_register
    
    def read(self, address: int) -> int:
        """
        Lee el valor desde una dirección de memoria de datos.
        
        Args:
            address: Dirección de memoria
            
        Returns:
            Valor almacenado en la dirección
            
        Raises:
            InvalidMemoryAddressError: Si la dirección es inválida
        """
        return self.load_data(address).value
    
    def store_data(self, address: int, value: Any) -> None:
        """
        Almacena un dato en la memoria.
        
        Args:
            address: Dirección donde almacenar
            value: Valor a almacenar
            
        Raises:
            InvalidMemoryAddressError: Si la dirección es inválida
        """
        if not self._is_valid_data_address(address):
            raise InvalidMemoryAddressError(
                f"Invalid data address: {address}. Valid range: {self._instruction_size}-{self._size-1}"
            )
        
        self._data_memory[address].set_value(value)
    
    def clear_all(self) -> None:
        """Limpia toda la memoria."""
        # Limpiar instrucciones
        self._instruction_memory = [''] * self._instruction_size
        
        # Limpiar datos
        for data_register in self._data_memory.values():
            data_register.clear()
        
        self.notify_observers(
            EventType.MEMORY_CLEARED,
            {'message': 'All memory cleared'}
        )
    
    def get_instructions(self) -> List[str]:
        """
        Obtiene todas las instrucciones cargadas.
        
        Returns:
            Lista de instrucciones
        """
        return [instr for instr in self._instruction_memory if instr.strip()]
    
    def get_data_registers(self) -> Dict[int, 'Register']:
        """
        Obtiene todos los registros de datos.
        
        Returns:
            Diccionario de registros de datos
        """
        return self._data_memory.copy()
    
    def is_instruction_memory_full(self) -> bool:
        """
        Verifica si la memoria de instrucciones está llena.
        
        Returns:
            True si está llena
        """
        return len([instr for instr in self._instruction_memory if instr.strip()]) >= self._instruction_size
    
    def get_next_free_instruction_address(self) -> int:
        """
        Obtiene la siguiente dirección libre para instrucciones.
        
        Returns:
            Dirección libre o -1 si está llena
        """
        for i, instr in enumerate(self._instruction_memory):
            if not instr.strip():
                return i
        return -1
    
    def _is_valid_instruction_address(self, address: int) -> bool:
        """Valida si una dirección es válida para instrucciones."""
        return 0 <= address < self._instruction_size
    
    def _is_valid_data_address(self, address: int) -> bool:
        """Valida si una dirección es válida para datos."""
        return self._instruction_size <= address < self._size
    
    def get_memory_usage(self) -> Dict[str, Any]:
        """
        Obtiene información sobre el uso de memoria.
        
        Returns:
            Diccionario con estadísticas de uso
        """
        instructions_used = len([instr for instr in self._instruction_memory if instr.strip()])
        data_used = len([reg for reg in self._data_memory.values() if reg.value != 0])
        
        return {
            'total_size': self._size,
            'instruction_size': self._instruction_size,
            'data_size': self._data_size,
            'instructions_used': instructions_used,
            'data_used': data_used,
            'instruction_usage_percent': (instructions_used / self._instruction_size) * 100,
            'data_usage_percent': (data_used / self._data_size) * 100
        }