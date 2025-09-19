"""
Módulo hardware del simulador de computadora.

Este módulo contiene todos los componentes de hardware
del simulador refactorizados con el patrón Observer.
"""

from .register import Register
from .register_bank import RegisterBank
from .alu import ALU
from .memory import Memory
from .control_unit import ControlUnit
from .wired_control_unit import WiredControlUnit

__all__ = [
    'Register',
    'RegisterBank',
    'ALU',
    'Memory',
    'ControlUnit',
    'WiredControlUnit'
]