"""
Excepciones específicas del simulador de computadora.

Este módulo define excepciones personalizadas para diferentes
situaciones de error en el simulador.
"""


class SimulatorError(Exception):
    """Excepción base para errores del simulador."""
    pass


class InvalidInstructionError(SimulatorError):
    """Excepción para instrucciones inválidas o mal formateadas."""
    
    def __init__(self, instruction=None, line_number=None):
        self.instruction = instruction
        self.line_number = line_number
        
        if line_number is not None:
            message = f"Instrucción inválida '{instruction}' en línea {line_number}"
        elif instruction is not None:
            message = f"Instrucción inválida: {instruction}"
        else:
            message = "Instrucción inválida"
        
        super().__init__(message)


class InvalidRegisterError(SimulatorError):
    """Excepción para acceso a registros inválidos."""
    
    def __init__(self, *args):
        if len(args) == 2:
            # Both register_name and operation provided
            register_name, operation = args
            self.register_name = register_name
            self.operation = operation
            message = f"Error en registro {register_name} durante operación: {operation}"
        elif len(args) == 1:
            # Only register_name provided
            register_name = args[0]
            self.register_name = register_name
            self.operation = None
            message = f"Error en registro: {register_name}"
        else:
            # No arguments
            self.register_name = None
            self.operation = None
            message = "Error de registro inválido"
        
        super().__init__(message)


class InvalidMemoryAddressError(SimulatorError):
    """Excepción para direcciones de memoria inválidas."""
    pass


class ALUOperationError(SimulatorError):
    """Excepción para errores en operaciones de la ALU."""
    
    def __init__(self, operation=None, details=None):
        self.operation = operation
        self.details = details
        
        if operation and details:
            message = f"Error en ALU durante {operation}: {details}"
        elif operation:
            message = f"Error en ALU: {operation}"
        else:
            message = "Error en operación de ALU"
        
        super().__init__(message)


class MemoryOverflowError(SimulatorError):
    """Excepción para desbordamiento de memoria."""
    
    def __init__(self, address=None, max_size=None):
        self.address = address
        self.max_size = max_size
        
        if address is not None and max_size is not None:
            message = f"Dirección de memoria {address} fuera de rango (máximo: {max_size-1})"
        elif address is not None:
            message = f"Dirección de memoria fuera de rango: {address}"
        else:
            message = "Error de desbordamiento de memoria"
        
        super().__init__(message)


class RegisterNotFoundError(InvalidRegisterError):
    """Excepción para registros no encontrados."""
    pass


class OperandOutOfRangeError(ALUOperationError):
    """Excepción para operandos fuera del rango válido."""
    pass


# Aliases for backward compatibility
ALUError = ALUOperationError
RegisterError = InvalidRegisterError


class ControlUnitError(SimulatorError):
    """Excepción para errores en la Unidad de Control."""
    
    def __init__(self, phase=None, details=None):
        self.phase = phase
        self.details = details
        
        if phase and details:
            message = f"Error en Unidad de Control en fase {phase}: {details}"
        elif phase:
            message = f"Error en Unidad de Control: {phase}"
        else:
            message = "Error en Unidad de Control"
        
        super().__init__(message)