"""
Representación de instrucciones del simulador.

Este módulo define las clases para representar y manejar
instrucciones del lenguaje ensamblador del simulador.
"""

from dataclasses import dataclass
from typing import List, Optional
from core.exceptions import InvalidInstructionError


@dataclass
class Instruction:
    """
    Representa una instrucción del simulador.
    
    Attributes:
        opcode: Código de operación (ADD, SUB, LOAD, etc.)
        operand1: Primer operando (registro o valor)
        operand2: Segundo operando (registro, valor o None)
        raw_instruction: Instrucción original como string
        address: Dirección de memoria donde está la instrucción
    """
    opcode: str
    operand1: Optional[str] = None
    operand2: Optional[str] = None
    raw_instruction: str = ""
    address: int = 0
    
    def __post_init__(self):
        """Validación posterior a la inicialización."""
        if not self.opcode:
            raise InvalidInstructionError("Opcode cannot be empty")
        self.opcode = self.opcode.upper()
    
    def is_arithmetic_operation(self) -> bool:
        """Verifica si es una operación aritmética."""
        return self.opcode in ['ADD', 'SUB', 'MUL', 'DIV']
    
    def is_logical_operation(self) -> bool:
        """Verifica si es una operación lógica."""
        return self.opcode in ['AND', 'OR', 'NOT', 'XOR']
    
    def is_memory_operation(self) -> bool:
        """Verifica si es una operación de memoria."""
        return self.opcode in ['LOAD', 'STORE']
    
    def is_control_operation(self) -> bool:
        """Verifica si es una operación de control de flujo."""
        return self.opcode in ['JP', 'JPZ']
    
    def is_register_operation(self) -> bool:
        """Verifica si es una operación entre registros."""
        return self.opcode in ['MOVE']
    
    def requires_alu(self) -> bool:
        """Verifica si la instrucción requiere la ALU."""
        return (self.is_arithmetic_operation() or 
                self.is_logical_operation() or 
                self.is_control_operation())
    
    def __str__(self) -> str:
        """Representación string de la instrucción."""
        if self.operand2:
            return f"{self.opcode} {self.operand1}, {self.operand2}"
        elif self.operand1:
            return f"{self.opcode} {self.operand1}"
        else:
            return self.opcode


class InstructionSet:
    """
    Conjunto de instrucciones válidas del simulador.
    
    Esta clase define y valida las instrucciones soportadas
    por el simulador.
    """
    
    VALID_OPCODES = {
        # Operaciones aritméticas
        'ADD', 'SUB', 'MUL', 'DIV',
        # Operaciones lógicas
        'AND', 'OR', 'NOT', 'XOR',
        # Operaciones de memoria
        'LOAD', 'STORE',
        # Operaciones de registro
        'MOVE',
        # Operaciones de control
        'JP', 'JPZ'
    }
    
    @classmethod
    def is_valid_opcode(cls, opcode: str) -> bool:
        """
        Verifica si un opcode es válido.
        
        Args:
            opcode: Código de operación a validar
            
        Returns:
            True si el opcode es válido
        """
        return opcode.upper() in cls.VALID_OPCODES
    
    @classmethod
    def get_instruction_format(cls, opcode: str) -> str:
        """
        Obtiene el formato esperado para una instrucción.
        
        Args:
            opcode: Código de operación
            
        Returns:
            String describiendo el formato esperado
        """
        opcode = opcode.upper()
        
        formats = {
            'ADD': 'ADD R1, R2 - Suma R1 + R2, resultado en R1',
            'SUB': 'SUB R1, R2 - Resta R1 - R2, resultado en R1',
            'MUL': 'MUL R1, R2 - Multiplica R1 * R2, resultado en R1',
            'DIV': 'DIV R1, R2 - Divide R1 / R2, resultado en R1',
            'AND': 'AND R1, R2 - AND lógico entre R1 y R2',
            'OR': 'OR R1, R2 - OR lógico entre R1 y R2',
            'NOT': 'NOT R1, R2 - NOT lógico de R2, resultado en R1',
            'XOR': 'XOR R1, R2 - XOR lógico entre R1 y R2',
            'LOAD': 'LOAD R1, valor o LOAD R1, *R2 - Carga valor en R1',
            'STORE': 'STORE R1, dirección - Almacena R1 en dirección',
            'MOVE': 'MOVE R1, R2 - Copia valor de R2 a R1',
            'JP': 'JP dirección - Salto incondicional',
            'JPZ': 'JPZ dirección, R1 - Salto si R1 es cero'
        }
        
        return formats.get(opcode, f"Formato desconocido para {opcode}")
    
    @classmethod
    def get_all_formats(cls) -> List[str]:
        """
        Obtiene una lista de todos los formatos de instrucciones.
        
        Returns:
            Lista con todos los formatos disponibles
        """
        return [cls.get_instruction_format(opcode) for opcode in sorted(cls.VALID_OPCODES)]