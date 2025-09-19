"""
ALU refactorizada con patrón Observer.

Este módulo implementa la Unidad Aritmético-Lógica que notifica
cambios de estado y resultados de operaciones.
"""

from typing import Any, Dict
from core.observer import Observable, EventType
from core.exceptions import ALUOperationError, OperandOutOfRangeError


class ALU(Observable):
    """
    Unidad Aritmético-Lógica con capacidades de notificación.
    
    Ejecuta operaciones aritméticas y lógicas, manteniendo el registro
    PSW y notificando cambios de estado.
    """
    
    def __init__(self):
        """Inicializa la ALU con valor cero y flags del PSW."""
        super().__init__()
        self._value = 0
        self._psw = {
            'Z': 0,  # Zero flag
            'C': 0,  # Carry flag  
            'S': 0,  # Sign flag
            'O': 0   # Overflow flag
        }
    
    @property
    def value(self) -> int:
        """Obtiene el resultado de la última operación."""
        return self._value
    
    @property
    def psw(self) -> Dict[str, int]:
        """Obtiene el estado actual del PSW."""
        return self._psw.copy()
    
    def execute(self, opcode: str, operand1: int, operand2: int = None) -> int:
        """
        Ejecuta una operación y notifica el resultado.
        
        Args:
            opcode: Código de operación
            operand1: Primer operando
            operand2: Segundo operando (opcional)
            
        Returns:
            Resultado de la operación
            
        Raises:
            OperandOutOfRangeError: Si los operandos están fuera del rango
            ALUOperationError: Si la operación no es válida
        """
        # Validar rango de operandos
        self._validate_operands(operand1, operand2)
        
        # Resetear flags
        self._reset_flags()
        
        # Ejecutar operación
        old_value = self._value
        self._execute_operation(opcode, operand1, operand2)
        
        # Actualizar flags basados en el resultado
        self._update_flags()
        
        # Notificar operación ejecutada
        self.notify_observers(
            EventType.ALU_OPERATION_EXECUTED,
            {
                'opcode': opcode,
                'operand1': operand1,
                'operand2': operand2,
                'old_value': old_value,
                'new_value': self._value,
                'psw': self._psw.copy()
            }
        )
        
        # Notificar cambio de flags
        self.notify_observers(
            EventType.ALU_FLAGS_UPDATED,
            {'psw': self._psw.copy()}
        )
        
        return self._value
    
    def _validate_operands(self, operand1: int, operand2: int = None) -> None:
        """Valida que los operandos estén en el rango válido."""
        def is_valid_operand(operand):
            # Rango válido: [-16384, 16383] (16-bit signed integer range)
            return operand is None or (-16384 <= operand <= 16383)

        if not is_valid_operand(operand1) or not is_valid_operand(operand2):
            self._psw['O'] = 1
            raise OperandOutOfRangeError(f'Operands out of range [-16384, 16383]')
    
    def _reset_flags(self) -> None:
        """Resetea todos los flags del PSW."""
        for flag in self._psw:
            self._psw[flag] = 0
    
    def _execute_operation(self, opcode: str, operand1: int, operand2: int = None) -> None:
        """Ejecuta la operación específica."""
        opcode = opcode.upper()
        
        if opcode == 'ADD':
            self._value = operand1 + operand2
            self._psw['C'] = int(self._value > 0x3FFF)
            self._psw['O'] = int(self._detect_add_overflow(operand1, operand2))
            
        elif opcode == 'SUB':
            self._value = operand1 - operand2
            self._psw['C'] = int(operand1 < operand2)
            self._psw['O'] = int(self._detect_sub_overflow(operand1, operand2))
            
        elif opcode == 'MUL':
            self._value = operand1 * operand2
            self._psw['C'] = int(self._value > 0x3FFF)
            
        elif opcode == 'DIV':
            if operand2 == 0:
                # División por cero: retornar 0 y establecer flag Z
                self._value = 0
                self._psw['Z'] = 1
            else:
                self._value = operand1 // operand2
                
        elif opcode == 'AND':
            self._value = operand1 & operand2
            
        elif opcode == 'OR':
            self._value = operand1 | operand2
            
        elif opcode == 'NOT':
            self._value = ~operand2
            
        elif opcode == 'XOR':
            self._value = operand1 ^ operand2
            
        elif opcode == 'JP':
            self._value = operand1
            
        elif opcode == 'JPZ':
            self._value = operand1 if operand2 == 0 else None
            
        else:
            raise ALUOperationError(f"Unsupported operation: {opcode}")
    
    def _detect_add_overflow(self, operand1: int, operand2: int) -> bool:
        """Detecta overflow en suma."""
        return ((operand1 & 0x2000) == (operand2 & 0x2000)) and \
               ((self._value & 0x2000) != (operand1 & 0x2000))
    
    def _detect_sub_overflow(self, operand1: int, operand2: int) -> bool:
        """Detecta overflow en resta."""
        return ((operand1 & 0x2000) != (operand2 & 0x2000)) and \
               ((self._value & 0x2000) != (operand1 & 0x2000))
    
    def _update_flags(self) -> None:
        """Actualiza los flags basados en el resultado."""
        if self._value is not None:
            self._psw['Z'] = int(self._value == 0)
            self._psw['S'] = int(self._value < 0)
    
    def reset(self) -> None:
        """Resetea la ALU a su estado inicial."""
        old_value = self._value
        old_psw = self._psw.copy()
        
        self._value = 0
        self._reset_flags()
        
        self.notify_observers(
            EventType.SYSTEM_RESET,
            {
                'component': 'ALU',
                'old_value': old_value,
                'old_psw': old_psw
            }
        )
    
    def get_psw_string(self) -> str:
        """
        Obtiene una representación string del PSW.
        
        Returns:
            String formateado con los flags del PSW
        """
        return f"Z: {self._psw['Z']} C: {self._psw['C']} S: {self._psw['S']} O: {self._psw['O']}"
    
    # Convenience methods for backward compatibility with tests
    def add(self, operand1: int, operand2: int) -> int:
        """Suma dos operandos."""
        return self.execute('ADD', operand1, operand2)
    
    def subtract(self, operand1: int, operand2: int) -> int:
        """Resta dos operandos."""
        return self.execute('SUB', operand1, operand2)
    
    def multiply(self, operand1: int, operand2: int) -> int:
        """Multiplica dos operandos.""" 
        return self.execute('MUL', operand1, operand2)
    
    def divide(self, operand1: int, operand2: int) -> int:
        """Divide dos operandos."""
        return self.execute('DIV', operand1, operand2)
    
    def logical_and(self, operand1: int, operand2: int) -> int:
        """Operación AND lógica."""
        return self.execute('AND', operand1, operand2)
    
    def logical_or(self, operand1: int, operand2: int) -> int:
        """Operación OR lógica."""
        return self.execute('OR', operand1, operand2)
    
    def logical_not(self, operand: int) -> int:
        """Operación NOT lógica."""
        return self.execute('NOT', 0, operand)
    
    def logical_xor(self, operand1: int, operand2: int) -> int:
        """Operación XOR lógica."""
        return self.execute('XOR', operand1, operand2)