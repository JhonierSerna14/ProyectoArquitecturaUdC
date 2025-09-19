"""
Modelo principal del simulador de computadora usando arquitectura MVC.

Este módulo implementa la clase Computer que orquesta todos los
componentes del simulador y actúa como el modelo principal.
"""

from typing import List, Dict, Any, Optional
from core.observer import Observable, Observer, EventType
from core.instruction import Instruction
from core.exceptions import *
from hardware import *
from utils.instruction_parser import InstructionParser


class Computer(Observable, Observer):
    """
    Modelo principal del simulador de computadora.
    
    Orquesta todos los componentes de hardware y coordina
    la ejecución de programas siguiendo el patrón MVC.
    """
    
    def __init__(self, memory_size: int = 32):
        """
        Inicializa el simulador de computadora.
        
        Args:
            memory_size: Tamaño de la memoria (default: 32)
        """
        super().__init__()
        
        # Inicializar componentes de hardware
        self._memory = Memory(memory_size)
        self._alu = ALU()
        self._control_unit = ControlUnit()
        self._register_bank = RegisterBank()
        self._wired_control_unit = WiredControlUnit()
        
        # Registros especiales
        self._pc_register = Register("PC", 0)
        self._mar_register = Register("MAR", 0)
        self._ir_register = Register("IR", "")
        self._mbr_register = Register("MBR", 0)
        self._psw_register = Register("PSW", "Z: 0, C: 0, S: 0, O: 0")
        
        # Estado del sistema
        self._is_running = False
        self._is_halted = False
        self._execution_mode = "automatic"  # "automatic" o "step"
        self._loaded_program: List[str] = []
        
        # Parser de instrucciones
        self._parser = InstructionParser()
        
        # Configurar observadores
        self._setup_observers()
    
    def _setup_observers(self) -> None:
        """Configura los observadores para todos los componentes."""
        # Observar cambios en componentes de hardware
        self._memory.add_observer(self)
        self._alu.add_observer(self)
        self._control_unit.add_observer(self)
        self._register_bank.add_observer(self)
        self._wired_control_unit.add_observer(self)
        
        # Observar registros especiales
        self._pc_register.add_observer(self)
        self._mar_register.add_observer(self)
        self._ir_register.add_observer(self)
        self._mbr_register.add_observer(self)
        self._psw_register.add_observer(self)
    
    def update(self, observable: Observable, event_type: str, data: Any = None) -> None:
        """
        Recibe notificaciones de componentes y las propaga a los observadores.
        
        Args:
            observable: Componente que generó el evento
            event_type: Tipo de evento
            data: Datos del evento
        """
        # Procesar eventos específicos
        if event_type == EventType.ALU_FLAGS_UPDATED:
            self._update_psw_display(data['psw'])
        
        # Propagar todos los eventos a los observadores (GUI)
        self.notify_observers(event_type, {
            'source': observable.__class__.__name__,
            'data': data
        })
    
    def load_program(self, program_lines: List[str]) -> bool:
        """
        Carga un programa en la memoria.
        
        Args:
            program_lines: Lista de líneas del programa
            
        Returns:
            True si el programa se cargó exitosamente
            
        Raises:
            MemoryOverflowError: Si no hay suficiente memoria
            InvalidInstructionError: Si hay instrucciones inválidas
        """
        try:
            self.reset()
            
            # Validar que hay espacio en memoria
            if len(program_lines) > self._memory.instruction_size:
                raise MemoryOverflowError(
                    f"Program too large. Available: {self._memory.instruction_size}, Required: {len(program_lines)}"
                )
            
            # Cargar cada instrucción
            loaded_instructions = []
            for idx, line in enumerate(program_lines):
                line = line.strip()
                if line:  # Ignorar líneas vacías
                    # Validar instrucción
                    self._parser.parse(line)
                    
                    # Almacenar en memoria
                    self._memory.store_instruction(idx, line)
                    loaded_instructions.append(line)
            
            self._loaded_program = loaded_instructions
            
            # Notificar programa cargado
            self.notify_observers(
                EventType.PROGRAM_LOADED,
                {
                    'program': loaded_instructions,
                    'instruction_count': len(loaded_instructions)
                }
            )
            
            return True
            
        except Exception as e:
            raise InvalidInstructionError(f"Error loading program: {str(e)}")
    
    def execute_program(self) -> None:
        """Ejecuta el programa completo automáticamente."""
        if not self._loaded_program:
            raise InvalidInstructionError("No program loaded")
        
        self._execution_mode = "automatic"
        self._is_running = True
        self._is_halted = False
        
        try:
            while self._can_continue_execution():
                self._execute_single_cycle()
                
        except Exception as e:
            self._is_running = False
            raise SimulatorError(f"Execution error: {str(e)}")
        
        self._is_running = False
        self.notify_observers(
            EventType.EXECUTION_COMPLETED,
            {'mode': 'automatic'}
        )
    
    def execute_next_instruction(self) -> bool:
        """
        Ejecuta la siguiente instrucción en modo paso a paso.
        
        Returns:
            True si se ejecutó una instrucción, False si terminó
        """
        if not self._loaded_program:
            raise InvalidInstructionError("No program loaded")
        
        self._execution_mode = "step"
        
        if not self._can_continue_execution():
            return False
        
        try:
            self._execute_single_cycle()
            return True
            
        except Exception as e:
            self._is_running = False
            raise SimulatorError(f"Step execution error: {str(e)}")
    
    def _execute_single_cycle(self) -> None:
        """Ejecuta un ciclo completo fetch-decode-execute."""
        pc_value = self._pc_register.value
        
        # FETCH
        self._mar_register.set_value(pc_value)
        instruction_str = self._control_unit.fetch(self._memory, pc_value)
        self._mbr_register.set_value(instruction_str)
        self._ir_register.set_value(instruction_str)
        
        # DECODE
        opcode, operand1, operand2 = self._control_unit.decode()
        
        # Generar señales de control
        control_signals = self._wired_control_unit.generate_control_signals(opcode)
        
        # Preparar operandos
        resolved_operand1, resolved_operand2 = self._resolve_operands(operand1, operand2)
        
        # EXECUTE
        self._execute_instruction(opcode, operand1, operand2, resolved_operand1, resolved_operand2, control_signals)
        
        # Actualizar PC (si no fue modificado por salto)
        if opcode not in ['JP', 'JPZ'] or (opcode == 'JPZ' and resolved_operand2 != 0):
            self._pc_register.set_value(pc_value + 1)
        
        # Notificar finalización de ciclo
        self._control_unit.execute_completed()
    
    def _resolve_operands(self, operand1: str, operand2: str) -> tuple:
        """Resuelve los operandos a sus valores reales."""
        resolved_op1 = None
        resolved_op2 = None
        
        # Resolver operand1
        if operand1:
            if operand1.isdigit() or (operand1.startswith('-') and operand1[1:].isdigit()):
                resolved_op1 = int(operand1)
            elif self._register_bank.exists(operand1):
                resolved_op1 = self._register_bank.get(operand1)
        
        # Resolver operand2
        if operand2:
            if operand2.startswith('*'):
                # Direccionamiento indirecto
                address_register = operand2[1:]
                if self._register_bank.exists(address_register):
                    address = self._register_bank.get(address_register)
                    resolved_op2 = self._memory.load_data(address).value
                else:
                    raise InvalidRegisterError(f"Invalid register for indirect addressing: {address_register}")
            elif operand2.isdigit() or (operand2.startswith('-') and operand2[1:].isdigit()):
                resolved_op2 = int(operand2)
            elif self._register_bank.exists(operand2):
                resolved_op2 = self._register_bank.get(operand2)
        
        return resolved_op1, resolved_op2
    
    def _execute_instruction(self, opcode: str, op1: str, op2: str, 
                           resolved_op1: Any, resolved_op2: Any, 
                           control_signals: Dict[str, Any]) -> None:
        """Ejecuta una instrucción específica."""
        
        if control_signals.get('alu_operation'):
            # Operaciones que requieren ALU
            result = self._alu.execute(opcode, resolved_op1, resolved_op2)
            
            if opcode in ['ADD', 'SUB', 'MUL', 'DIV', 'AND', 'OR', 'NOT', 'XOR']:
                self._register_bank.set(op1, result)
                
        elif opcode == 'JP':
            # Salto incondicional
            self._pc_register.set_value(resolved_op1)
            
        elif opcode == 'JPZ':
            # Salto condicional
            if resolved_op2 == 0:
                self._pc_register.set_value(resolved_op1)
                
        elif opcode == 'LOAD':
            # Cargar datos
            if op2.startswith('*'):
                # Carga indirecta ya resuelta
                value = resolved_op2
            else:
                # Carga inmediata
                value = resolved_op2
                
            self._mbr_register.set_value(value)
            self._register_bank.set(op1, value)
            
        elif opcode == 'STORE':
            # Almacenar datos
            self._memory.store_data(resolved_op2, resolved_op1)
            
        elif opcode == 'MOVE':
            # Mover entre registros
            self._register_bank.set(op1, resolved_op2)
    
    def _update_psw_display(self, psw: Dict[str, int]) -> None:
        """Actualiza la visualización del PSW."""
        psw_text = f"Z: {psw['Z']} C: {psw['C']} S: {psw['S']} O: {psw['O']}"
        self._psw_register.set_value(psw_text)
    
    def _can_continue_execution(self) -> bool:
        """Verifica si la ejecución puede continuar."""
        return (not self._is_halted and 
                self._pc_register.value < len(self._loaded_program))
    
    def reset(self) -> None:
        """Resetea el simulador a su estado inicial."""
        # Resetear componentes
        self._memory.clear_all()
        self._alu.reset()
        self._control_unit.reset()
        self._register_bank.clear_all()
        self._wired_control_unit.reset()
        
        # Resetear registros especiales
        self._pc_register.set_value(0)
        self._mar_register.set_value(0)
        self._ir_register.set_value("")
        self._mbr_register.set_value(0)
        self._psw_register.set_value("Z: 0, C: 0, S: 0, O: 0")
        
        # Resetear estado
        self._is_running = False
        self._is_halted = False
        self._loaded_program.clear()
        
        # Notificar reset
        self.notify_observers(
            EventType.SYSTEM_RESET,
            {'component': 'Computer'}
        )
    
    def halt(self) -> None:
        """Detiene la ejecución del simulador."""
        self._is_halted = True
        self._is_running = False
    
    # Propiedades de solo lectura para acceso a componentes
    @property
    def memory(self) -> Memory:
        """Obtiene la memoria del sistema."""
        return self._memory
    
    @property
    def alu(self) -> ALU:
        """Obtiene la ALU."""
        return self._alu
    
    @property
    def register_bank(self) -> RegisterBank:
        """Obtiene el banco de registros."""
        return self._register_bank
    
    @property
    def pc_register(self) -> Register:
        """Obtiene el registro PC."""
        return self._pc_register
    
    @property
    def mar_register(self) -> Register:
        """Obtiene el registro MAR."""
        return self._mar_register
    
    @property
    def ir_register(self) -> Register:
        """Obtiene el registro IR."""
        return self._ir_register
    
    @property
    def mbr_register(self) -> Register:
        """Obtiene el registro MBR."""
        return self._mbr_register
    
    @property
    def psw_register(self) -> Register:
        """Obtiene el registro PSW."""
        return self._psw_register
    
    @property
    def is_running(self) -> bool:
        """Verifica si el simulador está ejecutando."""
        return self._is_running
    
    @property
    def loaded_program(self) -> List[str]:
        """Obtiene el programa cargado."""
        return self._loaded_program.copy()
    
    def get_system_state(self) -> Dict[str, Any]:
        """
        Obtiene el estado completo del sistema.
        
        Returns:
            Diccionario con el estado de todos los componentes
        """
        return {
            'pc': self._pc_register.value,
            'mar': self._mar_register.value,
            'ir': self._ir_register.value,
            'mbr': self._mbr_register.value,
            'psw': self._alu.psw,
            'alu_value': self._alu.value,
            'registers': {name: reg.value for name, reg in self._register_bank.get_all_registers().items()},
            'memory_usage': self._memory.get_memory_usage(),
            'is_running': self._is_running,
            'is_halted': self._is_halted,
            'execution_mode': self._execution_mode,
            'program_loaded': bool(self._loaded_program),
            'program_size': len(self._loaded_program)
        }