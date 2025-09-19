"""
Pruebas unitarias para el módulo exceptions.py

Aplicando técnicas de partición equivalente:
- Partición 1: Mensajes de error válidos (string no vacío)
- Partición 2: Mensajes de error vacíos o None
- Partición 3: Jerarquía de excepciones correcta
- Partición 4: Atributos adicionales de excepciones específicas
"""

import unittest
import sys
import os

# Agregar path para imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from core.exceptions import (
    SimulatorError,
    InvalidInstructionError,
    InvalidRegisterError,
    InvalidMemoryAddressError,
    ALUOperationError,
    MemoryOverflowError,
    ALUError,
    RegisterError,
    ControlUnitError
)


class TestSimulatorError(unittest.TestCase):
    """Pruebas para la excepción base SimulatorError."""
    
    def test_simulator_error_inheritance(self):
        """Verifica que SimulatorError herede de Exception."""
        self.assertTrue(issubclass(SimulatorError, Exception))
    
    def test_simulator_error_with_message(self):
        """Test crear excepción con mensaje válido."""
        message = "Error en el simulador"
        error = SimulatorError(message)
        
        self.assertEqual(str(error), message)
        self.assertIsInstance(error, Exception)
        self.assertIsInstance(error, SimulatorError)
    
    def test_simulator_error_empty_message(self):
        """Test crear excepción con mensaje vacío."""
        error = SimulatorError("")
        self.assertEqual(str(error), "")
    
    def test_simulator_error_none_message(self):
        """Test crear excepción con mensaje None."""
        error = SimulatorError(None)
        self.assertEqual(str(error), "None")
    
    def test_simulator_error_no_message(self):
        """Test crear excepción sin mensaje."""
        error = SimulatorError()
        self.assertEqual(str(error), "")


class TestInvalidInstructionError(unittest.TestCase):
    """Pruebas para InvalidInstructionError usando partición equivalente."""
    
    def test_inheritance(self):
        """Verifica herencia correcta."""
        self.assertTrue(issubclass(InvalidInstructionError, SimulatorError))
        self.assertTrue(issubclass(InvalidInstructionError, Exception))
    
    def test_valid_instruction_and_line(self):
        """Test con instrucción y línea válidas."""
        instruction = "INVALID_OP"
        line_number = 5
        error = InvalidInstructionError(instruction, line_number)
        
        expected_message = f"Instrucción inválida '{instruction}' en línea {line_number}"
        self.assertEqual(str(error), expected_message)
    
    def test_only_instruction(self):
        """Test solo con instrucción."""
        instruction = "BAD_INSTRUCTION"
        error = InvalidInstructionError(instruction)
        
        expected_message = f"Instrucción inválida: {instruction}"
        self.assertEqual(str(error), expected_message)
    
    def test_empty_instruction(self):
        """Test con instrucción vacía."""
        error = InvalidInstructionError("", 1)
        expected_message = "Instrucción inválida '' en línea 1"
        self.assertEqual(str(error), expected_message)
    
    def test_none_instruction(self):
        """Test con instrucción None."""
        error = InvalidInstructionError(None, 2)
        expected_message = "Instrucción inválida 'None' en línea 2"
        self.assertEqual(str(error), expected_message)
    
    def test_zero_line_number(self):
        """Test con número de línea cero."""
        error = InvalidInstructionError("TEST", 0)
        expected_message = "Instrucción inválida 'TEST' en línea 0"
        self.assertEqual(str(error), expected_message)
    
    def test_negative_line_number(self):
        """Test con número de línea negativo."""
        error = InvalidInstructionError("TEST", -1)
        expected_message = "Instrucción inválida 'TEST' en línea -1"
        self.assertEqual(str(error), expected_message)


class TestMemoryOverflowError(unittest.TestCase):
    """Pruebas para MemoryOverflowError."""
    
    def test_inheritance(self):
        """Verifica herencia correcta."""
        self.assertTrue(issubclass(MemoryOverflowError, SimulatorError))
    
    def test_with_address_and_size(self):
        """Test con dirección y tamaño válidos."""
        address = 100
        max_size = 50
        error = MemoryOverflowError(address, max_size)
        
        expected_message = f"Dirección de memoria {address} fuera de rango (máximo: {max_size-1})"
        self.assertEqual(str(error), expected_message)
    
    def test_only_address(self):
        """Test solo con dirección."""
        address = 200
        error = MemoryOverflowError(address)
        
        expected_message = f"Dirección de memoria fuera de rango: {address}"
        self.assertEqual(str(error), expected_message)
    
    def test_zero_address(self):
        """Test con dirección cero."""
        error = MemoryOverflowError(0, 10)
        expected_message = "Dirección de memoria 0 fuera de rango (máximo: 9)"
        self.assertEqual(str(error), expected_message)
    
    def test_negative_address(self):
        """Test con dirección negativa."""
        error = MemoryOverflowError(-5, 10)
        expected_message = "Dirección de memoria -5 fuera de rango (máximo: 9)"
        self.assertEqual(str(error), expected_message)
    
    def test_edge_case_max_size_zero(self):
        """Test caso límite con tamaño máximo cero."""
        error = MemoryOverflowError(1, 0)
        expected_message = "Dirección de memoria 1 fuera de rango (máximo: -1)"
        self.assertEqual(str(error), expected_message)


class TestRegisterError(unittest.TestCase):
    """Pruebas para RegisterError."""
    
    def test_inheritance(self):
        """Verifica herencia correcta."""
        self.assertTrue(issubclass(RegisterError, SimulatorError))
    
    def test_with_register_name_and_operation(self):
        """Test con nombre de registro y operación."""
        register_name = "R1"
        operation = "read"
        error = RegisterError(register_name, operation)
        
        expected_message = f"Error en registro {register_name} durante operación: {operation}"
        self.assertEqual(str(error), expected_message)
    
    def test_only_register_name(self):
        """Test solo con nombre de registro."""
        register_name = "PC"
        error = RegisterError(register_name)
        
        expected_message = f"Error en registro: {register_name}"
        self.assertEqual(str(error), expected_message)
    
    def test_empty_register_name(self):
        """Test con nombre de registro vacío."""
        error = RegisterError("", "write")
        expected_message = "Error en registro  durante operación: write"
        self.assertEqual(str(error), expected_message)
    
    def test_none_values(self):
        """Test con valores None."""
        error = RegisterError(None, None)
        expected_message = "Error en registro None durante operación: None"
        self.assertEqual(str(error), expected_message)


class TestALUError(unittest.TestCase):
    """Pruebas para ALUError."""
    
    def test_inheritance(self):
        """Verifica herencia correcta."""
        self.assertTrue(issubclass(ALUError, SimulatorError))
    
    def test_with_operation_and_details(self):
        """Test con operación y detalles."""
        operation = "ADD"
        details = "Division by zero"
        error = ALUError(operation, details)
        
        expected_message = f"Error en ALU durante {operation}: {details}"
        self.assertEqual(str(error), expected_message)
    
    def test_only_operation(self):
        """Test solo con operación."""
        operation = "SUB"
        error = ALUError(operation)
        
        expected_message = f"Error en ALU: {operation}"
        self.assertEqual(str(error), expected_message)
    
    def test_division_by_zero_scenario(self):
        """Test escenario específico de división por cero."""
        error = ALUError("DIV", "División por cero")
        expected_message = "Error en ALU durante DIV: División por cero"
        self.assertEqual(str(error), expected_message)
    
    def test_overflow_scenario(self):
        """Test escenario de overflow."""
        error = ALUError("MUL", "Resultado excede capacidad de registro")
        expected_message = "Error en ALU durante MUL: Resultado excede capacidad de registro"
        self.assertEqual(str(error), expected_message)


class TestControlUnitError(unittest.TestCase):
    """Pruebas para ControlUnitError."""
    
    def test_inheritance(self):
        """Verifica herencia correcta."""
        self.assertTrue(issubclass(ControlUnitError, SimulatorError))
    
    def test_with_phase_and_details(self):
        """Test con fase y detalles."""
        phase = "FETCH"
        details = "No se puede acceder a memoria"
        error = ControlUnitError(phase, details)
        
        expected_message = f"Error en Unidad de Control en fase {phase}: {details}"
        self.assertEqual(str(error), expected_message)
    
    def test_only_phase(self):
        """Test solo con fase."""
        phase = "DECODE"
        error = ControlUnitError(phase)
        
        expected_message = f"Error en Unidad de Control: {phase}"
        self.assertEqual(str(error), expected_message)
    
    def test_fetch_phase_error(self):
        """Test error específico en fase FETCH."""
        error = ControlUnitError("FETCH", "PC fuera de rango")
        expected_message = "Error en Unidad de Control en fase FETCH: PC fuera de rango"
        self.assertEqual(str(error), expected_message)
    
    def test_execute_phase_error(self):
        """Test error específico en fase EXECUTE."""
        error = ControlUnitError("EXECUTE", "Instrucción no implementada")
        expected_message = "Error en Unidad de Control en fase EXECUTE: Instrucción no implementada"
        self.assertEqual(str(error), expected_message)


class TestExceptionHierarchy(unittest.TestCase):
    """Pruebas para verificar la jerarquía de excepciones."""
    
    def test_all_inherit_from_simulator_error(self):
        """Verifica que todas las excepciones hereden de SimulatorError."""
        exceptions = [
            InvalidInstructionError,
            MemoryOverflowError,
            RegisterError,
            ALUError,
            ControlUnitError
        ]
        
        for exc_class in exceptions:
            with self.subTest(exception=exc_class.__name__):
                self.assertTrue(issubclass(exc_class, SimulatorError))
    
    def test_all_inherit_from_base_exception(self):
        """Verifica que todas hereden de Exception."""
        exceptions = [
            SimulatorError,
            InvalidInstructionError,
            MemoryOverflowError,
            RegisterError,
            ALUError,
            ControlUnitError
        ]
        
        for exc_class in exceptions:
            with self.subTest(exception=exc_class.__name__):
                self.assertTrue(issubclass(exc_class, Exception))
    
    def test_exception_raising_and_catching(self):
        """Test levantar y capturar excepciones."""
        # Test captura específica
        with self.assertRaises(InvalidInstructionError):
            raise InvalidInstructionError("TEST")
        
        # Test captura por clase base
        with self.assertRaises(SimulatorError):
            raise MemoryOverflowError(100, 50)
        
        # Test captura por Exception
        with self.assertRaises(Exception):
            raise ALUError("DIV", "División por cero")


if __name__ == '__main__':
    unittest.main()