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
    pass


class InvalidRegisterError(SimulatorError):
    """Excepción para acceso a registros inválidos."""
    pass


class InvalidMemoryAddressError(SimulatorError):
    """Excepción para direcciones de memoria inválidas."""
    pass


class ALUOperationError(SimulatorError):
    """Excepción para errores en operaciones de la ALU."""
    pass


class MemoryOverflowError(SimulatorError):
    """Excepción para desbordamiento de memoria."""
    pass


class RegisterNotFoundError(InvalidRegisterError):
    """Excepción para registros no encontrados."""
    pass


class OperandOutOfRangeError(ALUOperationError):
    """Excepción para operandos fuera del rango válido."""
    pass