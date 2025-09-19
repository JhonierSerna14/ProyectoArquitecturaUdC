"""
Parser de instrucciones para el simulador.

Este módulo parsea y valida instrucciones del lenguaje ensamblador
del simulador.
"""

import re
from typing import Tuple, Optional
from core.instruction import Instruction, InstructionSet
from core.exceptions import InvalidInstructionError


class InstructionParser:
    """
    Parser que convierte strings en objetos Instruction validados.
    
    Valida la sintaxis y semántica de las instrucciones del simulador.
    """
    
    def __init__(self):
        """Inicializa el parser con patrones de expresiones regulares."""
        # Patrones para validar diferentes tipos de operandos
        self._register_pattern = re.compile(r'^R[1-9]$')
        self._immediate_pattern = re.compile(r'^-?\d+$')
        self._indirect_pattern = re.compile(r'^\*R[1-9]$')
        self._address_pattern = re.compile(r'^\d+$')
    
    def parse(self, instruction_str: str, address: int = 0) -> Instruction:
        """
        Parsea una instrucción desde string.
        
        Args:
            instruction_str: Instrucción como string
            address: Dirección de memoria (opcional)
            
        Returns:
            Objeto Instruction validado
            
        Raises:
            InvalidInstructionError: Si la instrucción es inválida
        """
        if not instruction_str or not instruction_str.strip():
            raise InvalidInstructionError("Empty instruction")
        
        # Limpiar y dividir la instrucción
        clean_instruction = instruction_str.strip()
        parts = clean_instruction.split(maxsplit=1)
        
        if not parts:
            raise InvalidInstructionError("No opcode found")
        
        opcode = parts[0].upper()
        
        # Validar opcode
        if not InstructionSet.is_valid_opcode(opcode):
            raise InvalidInstructionError(
                f"Invalid opcode '{opcode}'. Valid opcodes: {', '.join(sorted(InstructionSet.VALID_OPCODES))}"
            )
        
        # Parsear operandos
        operand1, operand2 = self._parse_operands(parts[1] if len(parts) > 1 else "", opcode)
        
        # Validar semántica de la instrucción
        self._validate_instruction_semantics(opcode, operand1, operand2)
        
        return Instruction(
            opcode=opcode,
            operand1=operand1,
            operand2=operand2,
            raw_instruction=clean_instruction,
            address=address
        )
    
    def _parse_operands(self, operands_str: str, opcode: str) -> Tuple[Optional[str], Optional[str]]:
        """
        Parsea los operandos de una instrucción.
        
        Args:
            operands_str: String con los operandos
            opcode: Código de operación
            
        Returns:
            Tupla con (operand1, operand2)
        """
        if not operands_str.strip():
            return None, None
        
        # Dividir operandos por coma
        operands = [op.strip() for op in operands_str.split(',')]
        
        operand1 = operands[0] if len(operands) > 0 and operands[0] else None
        operand2 = operands[1] if len(operands) > 1 and operands[1] else None
        
        # Validar formato de operandos
        if operand1:
            self._validate_operand_format(operand1, opcode, 1)
        if operand2:
            self._validate_operand_format(operand2, opcode, 2)
        
        return operand1, operand2
    
    def _validate_operand_format(self, operand: str, opcode: str, position: int) -> None:
        """
        Valida el formato de un operando específico.
        
        Args:
            operand: Operando a validar
            opcode: Código de operación
            position: Posición del operando (1 o 2)
            
        Raises:
            InvalidInstructionError: Si el formato es inválido
        """
        if not operand:
            return
        
        # Verificar si es un registro válido
        if self._register_pattern.match(operand):
            return
        
        # Verificar si es un valor inmediato válido
        if self._immediate_pattern.match(operand):
            value = int(operand)
            if not (-16384 <= value <= 16383):
                raise InvalidInstructionError(
                    f"Immediate value {value} out of range [-16384, 16383] in operand {position}"
                )
            return
        
        # Verificar si es direccionamiento indirecto válido
        if self._indirect_pattern.match(operand):
            return
        
        # Verificar si es una dirección válida (solo para ciertas instrucciones)
        if self._address_pattern.match(operand):
            address = int(operand)
            if not (0 <= address <= 31):  # Asumiendo memoria de 32 posiciones
                raise InvalidInstructionError(
                    f"Memory address {address} out of range [0, 31] in operand {position}"
                )
            return
        
        raise InvalidInstructionError(
            f"Invalid operand format '{operand}' in position {position}. "
            f"Expected: register (R1-R9), immediate value, indirect (*R1-*R9), or address (0-31)"
        )
    
    def _validate_instruction_semantics(self, opcode: str, operand1: Optional[str], operand2: Optional[str]) -> None:
        """
        Valida la semántica de la instrucción completa.
        
        Args:
            opcode: Código de operación
            operand1: Primer operando
            operand2: Segundo operando
            
        Raises:
            InvalidInstructionError: Si la semántica es inválida
        """
        # Validaciones específicas por tipo de instrucción
        if opcode in ['ADD', 'SUB', 'MUL', 'DIV', 'AND', 'OR', 'XOR']:
            self._validate_binary_arithmetic_instruction(opcode, operand1, operand2)
            
        elif opcode == 'NOT':
            self._validate_unary_instruction(opcode, operand1, operand2)
            
        elif opcode == 'LOAD':
            self._validate_load_instruction(operand1, operand2)
            
        elif opcode == 'STORE':
            self._validate_store_instruction(operand1, operand2)
            
        elif opcode == 'MOVE':
            self._validate_move_instruction(operand1, operand2)
            
        elif opcode == 'JP':
            self._validate_jump_instruction(operand1, operand2)
            
        elif opcode == 'JPZ':
            self._validate_conditional_jump_instruction(operand1, operand2)
    
    def _validate_binary_arithmetic_instruction(self, opcode: str, op1: Optional[str], op2: Optional[str]) -> None:
        """Valida instrucciones aritméticas binarias."""
        if not op1 or not op2:
            raise InvalidInstructionError(f"{opcode} requires two operands: {InstructionSet.get_instruction_format(opcode)}")
        
        if not self._register_pattern.match(op1):
            raise InvalidInstructionError(f"{opcode} first operand must be a register (R1-R9)")
        
        if not (self._register_pattern.match(op2) or self._immediate_pattern.match(op2)):
            raise InvalidInstructionError(f"{opcode} second operand must be a register or immediate value")
    
    def _validate_unary_instruction(self, opcode: str, op1: Optional[str], op2: Optional[str]) -> None:
        """Valida instrucciones unarias como NOT."""
        if not op1 or not op2:
            raise InvalidInstructionError(f"{opcode} requires two operands: {InstructionSet.get_instruction_format(opcode)}")
        
        if not self._register_pattern.match(op1):
            raise InvalidInstructionError(f"{opcode} first operand must be a register (R1-R9)")
        
        if not (self._register_pattern.match(op2) or self._immediate_pattern.match(op2)):
            raise InvalidInstructionError(f"{opcode} second operand must be a register or immediate value")
    
    def _validate_load_instruction(self, op1: Optional[str], op2: Optional[str]) -> None:
        """Valida instrucciones LOAD."""
        if not op1 or not op2:
            raise InvalidInstructionError("LOAD requires two operands: LOAD R1, value or LOAD R1, *R2")
        
        if not self._register_pattern.match(op1):
            raise InvalidInstructionError("LOAD first operand must be a register (R1-R9)")
        
        if not (self._immediate_pattern.match(op2) or self._indirect_pattern.match(op2)):
            raise InvalidInstructionError("LOAD second operand must be immediate value or indirect register (*R1-*R9)")
    
    def _validate_store_instruction(self, op1: Optional[str], op2: Optional[str]) -> None:
        """Valida instrucciones STORE."""
        if not op1 or not op2:
            raise InvalidInstructionError("STORE requires two operands: STORE R1, address")
        
        if not self._register_pattern.match(op1):
            raise InvalidInstructionError("STORE first operand must be a register (R1-R9)")
        
        if not (self._address_pattern.match(op2) or self._immediate_pattern.match(op2)):
            raise InvalidInstructionError("STORE second operand must be a memory address")
    
    def _validate_move_instruction(self, op1: Optional[str], op2: Optional[str]) -> None:
        """Valida instrucciones MOVE."""
        if not op1 or not op2:
            raise InvalidInstructionError("MOVE requires two operands: MOVE R1, R2")
        
        if not self._register_pattern.match(op1):
            raise InvalidInstructionError("MOVE first operand must be a register (R1-R9)")
        
        if not self._register_pattern.match(op2):
            raise InvalidInstructionError("MOVE second operand must be a register (R1-R9)")
    
    def _validate_jump_instruction(self, op1: Optional[str], op2: Optional[str]) -> None:
        """Valida instrucciones JP."""
        if not op1:
            raise InvalidInstructionError("JP requires one operand: JP address")
        
        if op2:
            raise InvalidInstructionError("JP takes only one operand")
        
        if not (self._address_pattern.match(op1) or self._immediate_pattern.match(op1)):
            raise InvalidInstructionError("JP operand must be a memory address")
    
    def _validate_conditional_jump_instruction(self, op1: Optional[str], op2: Optional[str]) -> None:
        """Valida instrucciones JPZ."""
        if not op1 or not op2:
            raise InvalidInstructionError("JPZ requires two operands: JPZ address, register")
        
        if not (self._address_pattern.match(op1) or self._immediate_pattern.match(op1)):
            raise InvalidInstructionError("JPZ first operand must be a memory address")
        
        if not self._register_pattern.match(op2):
            raise InvalidInstructionError("JPZ second operand must be a register (R1-R9)")
    
    def validate_program(self, program_lines: list) -> list:
        """
        Valida un programa completo.
        
        Args:
            program_lines: Lista de líneas del programa
            
        Returns:
            Lista de objetos Instruction validados
            
        Raises:
            InvalidInstructionError: Si alguna instrucción es inválida
        """
        instructions = []
        
        for line_num, line in enumerate(program_lines, 1):
            line = line.strip()
            if not line:  # Ignorar líneas vacías
                continue
            
            try:
                instruction = self.parse(line, line_num - 1)
                instructions.append(instruction)
            except InvalidInstructionError as e:
                raise InvalidInstructionError(f"Line {line_num}: {str(e)}")
        
        return instructions