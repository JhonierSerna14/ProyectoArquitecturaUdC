"""
Unidad de Control refactorizada con patrón Observer.

Este módulo implementa la unidad de control que coordina
el ciclo fetch-decode-execute y notifica cambios de estado.
"""

from typing import Tuple, Optional
from core.observer import Observable, EventType
from core.instruction import Instruction
from core.exceptions import InvalidInstructionError
from hardware.memory import Memory
from utils.instruction_parser import InstructionParser


class ControlUnit(Observable):
    """
    Unidad de Control que coordina el ciclo de ejecución.
    
    Maneja el ciclo fetch-decode-execute y notifica cada fase
    usando el patrón Observer.
    """
    
    def __init__(self):
        """Inicializa la unidad de control."""
        super().__init__()
        self._instruction_register: Optional[Instruction] = None
        self._current_pc = 0
        self._parser = InstructionParser()
    
    @property
    def instruction_register(self) -> Optional[Instruction]:
        """Obtiene la instrucción actualmente cargada."""
        return self._instruction_register
    
    @property
    def current_pc(self) -> int:
        """Obtiene el valor actual del PC."""
        return self._current_pc
    
    def fetch(self, memory: Memory, pc: int) -> str:
        """
        Realiza la fase de fetch del ciclo de instrucción.
        
        Args:
            memory: Memoria del sistema
            pc: Valor del program counter
            
        Returns:
            Instrucción cargada como string
            
        Raises:
            InvalidInstructionError: Si no se encuentra instrucción
        """
        self._current_pc = pc
        
        try:
            instruction_str = memory.load_instruction(pc)
            
            if not instruction_str.strip():
                raise InvalidInstructionError(f"No instruction found at PC address {pc}")
            
            # Crear objeto Instruction
            self._instruction_register = self._create_instruction(instruction_str, pc)
            
            self.notify_observers(
                EventType.INSTRUCTION_FETCHED,
                {
                    'pc': pc,
                    'instruction': instruction_str,
                    'instruction_obj': self._instruction_register
                }
            )
            
            return instruction_str
            
        except Exception as e:
            raise InvalidInstructionError(f"Error fetching instruction at address {pc}: {str(e)}")
    
    def decode(self) -> Tuple[str, str, str, str]:
        """
        Realiza la fase de decode del ciclo de instrucción.
        
        Returns:
            Tupla con (opcode, operand1, operand2, operand3)
            
        Raises:
            InvalidInstructionError: Si no hay instrucción cargada
        """
        if not self._instruction_register:
            raise InvalidInstructionError("No instruction loaded in the instruction register")
        
        instruction = self._instruction_register
        
        self.notify_observers(
            EventType.INSTRUCTION_DECODED,
            {
                'opcode': instruction.type,
                'operand1': instruction.operand1,
                'operand2': instruction.operand2,
                'operand3': instruction.operand3,
                'instruction_obj': instruction
            }
        )
        
        return (
            instruction.type.value if hasattr(instruction.type, 'value') else str(instruction.type),
            instruction.operand1 or '',
            instruction.operand2 or '',
            instruction.operand3 or ''
        )
    
    def execute_completed(self, result: any = None) -> None:
        """
        Notifica que la fase de ejecución ha completado.
        
        Args:
            result: Resultado de la ejecución (opcional)
        """
        self.notify_observers(
            EventType.INSTRUCTION_EXECUTED,
            {
                'instruction': self._instruction_register,
                'result': result,
                'pc': self._current_pc
            }
        )
    
    def reset(self) -> None:
        """Resetea la unidad de control."""
        old_instruction = self._instruction_register
        old_pc = self._current_pc
        
        self._instruction_register = None
        self._current_pc = 0
        
        self.notify_observers(
            EventType.SYSTEM_RESET,
            {
                'component': 'ControlUnit',
                'old_instruction': old_instruction,
                'old_pc': old_pc
            }
        )
    
    def _create_instruction(self, instruction_str: str, address: int) -> Instruction:
        """
        Crea un objeto Instruction a partir de un string.
        
        Args:
            instruction_str: Instrucción como string
            address: Dirección de memoria
            
        Returns:
            Objeto Instruction
            
        Raises:
            InvalidInstructionError: Si la instrucción es inválida
        """
        try:
            # Usar el parser oficial para obtener la instrucción parseada
            instruction = self._parser.parse(instruction_str, address)
            return instruction
            
        except Exception as e:
            raise InvalidInstructionError(f"Invalid instruction format '{instruction_str}': {str(e)}")
    
    def get_current_instruction_info(self) -> dict:
        """
        Obtiene información sobre la instrucción actual.
        
        Returns:
            Diccionario con información de la instrucción
        """
        if not self._instruction_register:
            return {'status': 'No instruction loaded'}
        
        instruction = self._instruction_register
        return {
            'opcode': instruction.opcode,
            'operand1': instruction.operand1,
            'operand2': instruction.operand2,
            'raw_instruction': instruction.raw_instruction,
            'address': instruction.address,
            'requires_alu': instruction.requires_alu(),
            'is_arithmetic': instruction.is_arithmetic_operation(),
            'is_logical': instruction.is_logical_operation(),
            'is_memory': instruction.is_memory_operation(),
            'is_control': instruction.is_control_operation()
        }