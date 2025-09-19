"""
Módulo core del simulador de computadora.

Este módulo contiene las clases y funcionalidades centrales
del simulador, incluyendo el patrón Observer, excepciones
e instrucciones.
"""

from .observer import Observer, Observable, EventType
from .exceptions import *
from .instruction import Instruction, InstructionSet
from .computer import Computer

__all__ = [
    'Observer',
    'Observable', 
    'EventType',
    'Instruction',
    'InstructionSet',
    'Computer',
    'SimulatorError',
    'InvalidInstructionError',
    'InvalidRegisterError',
    'InvalidMemoryAddressError',
    'ALUOperationError',
    'MemoryOverflowError',
    'RegisterNotFoundError',
    'OperandOutOfRangeError'
]