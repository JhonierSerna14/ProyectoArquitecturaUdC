"""
Pruebas unitarias para el módulo instruction.py

Aplicando técnicas de partición equivalente:
- Partición 1: Instrucciones válidas con diferentes tipos (LOAD, STORE, ADD, etc.)
- Partición 2: Instrucciones inválidas (formato incorrecto, operandos incorrectos)
- Partición 3: Casos límite (valores máximos, mínimos, operandos opcionales)
- Partición 4: Tipos de instrucciones (aritméticas, memoria, control)
"""

import unittest
import sys
import os

# Agregar path para imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from core.instruction import Instruction, InstructionType


class TestInstructionType(unittest.TestCase):
    """Pruebas para el enum InstructionType."""
    
    def test_instruction_types_exist(self):
        """Verifica que todos los tipos de instrucción existen."""
        expected_types = [
            'LOAD', 'STORE', 'ADD', 'SUB', 'MUL', 'DIV',
            'AND', 'OR', 'NOT', 'XOR', 'JMP', 'JZ', 'JNZ', 'HALT'
        ]
        
        for inst_type in expected_types:
            with self.subTest(instruction_type=inst_type):
                self.assertTrue(hasattr(InstructionType, inst_type))
    
    def test_instruction_type_values(self):
        """Verifica los valores de los tipos de instrucción."""
        self.assertEqual(InstructionType.LOAD.value, "LOAD")
        self.assertEqual(InstructionType.STORE.value, "STORE")
        self.assertEqual(InstructionType.ADD.value, "ADD")
        self.assertEqual(InstructionType.HALT.value, "HALT")


class TestInstruction(unittest.TestCase):
    """Pruebas para la clase Instruction usando partición equivalente."""
    
    # Partición 1: Instrucciones válidas
    def test_load_instruction_valid(self):
        """Test instrucción LOAD válida."""
        instruction = Instruction(InstructionType.LOAD, "R1", 100)
        
        self.assertEqual(instruction.type, InstructionType.LOAD)
        self.assertEqual(instruction.operand1, "R1")
        self.assertEqual(instruction.operand2, 100)
        self.assertIsNone(instruction.operand3)
    
    def test_store_instruction_valid(self):
        """Test instrucción STORE válida."""
        instruction = Instruction(InstructionType.STORE, "R2", 200)
        
        self.assertEqual(instruction.type, InstructionType.STORE)
        self.assertEqual(instruction.operand1, "R2")
        self.assertEqual(instruction.operand2, 200)
    
    def test_add_instruction_valid(self):
        """Test instrucción ADD válida con tres operandos."""
        instruction = Instruction(InstructionType.ADD, "R1", "R2", "R3")
        
        self.assertEqual(instruction.type, InstructionType.ADD)
        self.assertEqual(instruction.operand1, "R1")
        self.assertEqual(instruction.operand2, "R2")
        self.assertEqual(instruction.operand3, "R3")
    
    def test_sub_instruction_valid(self):
        """Test instrucción SUB válida."""
        instruction = Instruction(InstructionType.SUB, "R4", "R5", "R6")
        
        self.assertEqual(instruction.type, InstructionType.SUB)
        self.assertEqual(instruction.operand1, "R4")
        self.assertEqual(instruction.operand2, "R5")
        self.assertEqual(instruction.operand3, "R6")
    
    def test_halt_instruction_valid(self):
        """Test instrucción HALT válida sin operandos."""
        instruction = Instruction(InstructionType.HALT)
        
        self.assertEqual(instruction.type, InstructionType.HALT)
        self.assertIsNone(instruction.operand1)
        self.assertIsNone(instruction.operand2)
        self.assertIsNone(instruction.operand3)
    
    def test_jmp_instruction_valid(self):
        """Test instrucción JMP válida."""
        instruction = Instruction(InstructionType.JMP, 50)
        
        self.assertEqual(instruction.type, InstructionType.JMP)
        self.assertEqual(instruction.operand1, 50)
        self.assertIsNone(instruction.operand2)
        self.assertIsNone(instruction.operand3)
    
    # Partición 2: Diferentes tipos de operandos
    def test_instruction_with_string_operands(self):
        """Test instrucción con operandos string."""
        instruction = Instruction(InstructionType.ADD, "R1", "R2", "R3")
        
        self.assertIsInstance(instruction.operand1, str)
        self.assertIsInstance(instruction.operand2, str)
        self.assertIsInstance(instruction.operand3, str)
    
    def test_instruction_with_integer_operands(self):
        """Test instrucción con operandos enteros."""
        instruction = Instruction(InstructionType.LOAD, "R1", 42)
        
        self.assertIsInstance(instruction.operand1, str)
        self.assertIsInstance(instruction.operand2, int)
    
    def test_instruction_with_mixed_operands(self):
        """Test instrucción con operandos mixtos."""
        instruction = Instruction(InstructionType.STORE, "R7", 999)
        
        self.assertEqual(instruction.operand1, "R7")
        self.assertEqual(instruction.operand2, 999)
    
    # Partición 3: Casos límite
    def test_instruction_with_zero_operand(self):
        """Test instrucción con operando cero."""
        instruction = Instruction(InstructionType.LOAD, "R1", 0)
        
        self.assertEqual(instruction.operand2, 0)
    
    def test_instruction_with_negative_operand(self):
        """Test instrucción con operando negativo."""
        instruction = Instruction(InstructionType.JMP, -1)
        
        self.assertEqual(instruction.operand1, -1)
    
    def test_instruction_with_large_operand(self):
        """Test instrucción con operando grande."""
        large_value = 999999
        instruction = Instruction(InstructionType.STORE, "R1", large_value)
        
        self.assertEqual(instruction.operand2, large_value)
    
    def test_instruction_with_empty_string_operand(self):
        """Test instrucción con operando string vacío."""
        instruction = Instruction(InstructionType.ADD, "", "R2", "R3")
        
        self.assertEqual(instruction.operand1, "")
    
    # Partición 4: Operandos opcionales
    def test_instruction_with_one_operand(self):
        """Test instrucción con un operando."""
        instruction = Instruction(InstructionType.NOT, "R1")
        
        self.assertEqual(instruction.operand1, "R1")
        self.assertIsNone(instruction.operand2)
        self.assertIsNone(instruction.operand3)
    
    def test_instruction_with_two_operands(self):
        """Test instrucción con dos operandos."""
        instruction = Instruction(InstructionType.LOAD, "R1", 50)
        
        self.assertEqual(instruction.operand1, "R1")
        self.assertEqual(instruction.operand2, 50)
        self.assertIsNone(instruction.operand3)
    
    def test_instruction_with_three_operands(self):
        """Test instrucción con tres operandos."""
        instruction = Instruction(InstructionType.MUL, "R1", "R2", "R3")
        
        self.assertEqual(instruction.operand1, "R1")
        self.assertEqual(instruction.operand2, "R2")
        self.assertEqual(instruction.operand3, "R3")
    
    def test_instruction_with_none_operands(self):
        """Test instrucción con operandos None explícitos."""
        instruction = Instruction(InstructionType.HALT, None, None, None)
        
        self.assertIsNone(instruction.operand1)
        self.assertIsNone(instruction.operand2)
        self.assertIsNone(instruction.operand3)
    
    # Tests para representación string
    def test_instruction_str_representation(self):
        """Test representación string de instrucción."""
        instruction = Instruction(InstructionType.ADD, "R1", "R2", "R3")
        str_repr = str(instruction)
        
        self.assertIn("ADD", str_repr)
        self.assertIn("R1", str_repr)
        self.assertIn("R2", str_repr)
        self.assertIn("R3", str_repr)
    
    def test_instruction_str_with_none_operands(self):
        """Test representación string con operandos None."""
        instruction = Instruction(InstructionType.HALT)
        str_repr = str(instruction)
        
        self.assertIn("HALT", str_repr)
        # No debe incluir 'None' para operandos no especificados
        self.assertNotIn("None", str_repr)
    
    def test_instruction_str_with_partial_operands(self):
        """Test representación string con operandos parciales."""
        instruction = Instruction(InstructionType.JMP, 100)
        str_repr = str(instruction)
        
        self.assertIn("JMP", str_repr)
        self.assertIn("100", str_repr)
    
    # Tests para comparación e igualdad
    def test_instruction_equality_same_values(self):
        """Test igualdad entre instrucciones con mismos valores."""
        inst1 = Instruction(InstructionType.ADD, "R1", "R2", "R3")
        inst2 = Instruction(InstructionType.ADD, "R1", "R2", "R3")
        
        self.assertEqual(inst1.type, inst2.type)
        self.assertEqual(inst1.operand1, inst2.operand1)
        self.assertEqual(inst1.operand2, inst2.operand2)
        self.assertEqual(inst1.operand3, inst2.operand3)
    
    def test_instruction_inequality_different_types(self):
        """Test desigualdad entre instrucciones de diferente tipo."""
        inst1 = Instruction(InstructionType.ADD, "R1", "R2", "R3")
        inst2 = Instruction(InstructionType.SUB, "R1", "R2", "R3")
        
        self.assertNotEqual(inst1.type, inst2.type)
    
    def test_instruction_inequality_different_operands(self):
        """Test desigualdad entre instrucciones con diferentes operandos."""
        inst1 = Instruction(InstructionType.LOAD, "R1", 100)
        inst2 = Instruction(InstructionType.LOAD, "R1", 200)
        
        self.assertNotEqual(inst1.operand2, inst2.operand2)
    
    # Tests para validación de tipos
    def test_instruction_type_validation(self):
        """Test validación del tipo de instrucción."""
        # Debe aceptar tipos válidos de InstructionType
        for inst_type in InstructionType:
            with self.subTest(instruction_type=inst_type):
                instruction = Instruction(inst_type)
                self.assertEqual(instruction.type, inst_type)
    
    # Tests de casos especiales por tipo de instrucción
    def test_arithmetic_instructions(self):
        """Test instrucciones aritméticas."""
        arithmetic_types = [
            InstructionType.ADD, InstructionType.SUB,
            InstructionType.MUL, InstructionType.DIV
        ]
        
        for inst_type in arithmetic_types:
            with self.subTest(instruction_type=inst_type):
                instruction = Instruction(inst_type, "R1", "R2", "R3")
                self.assertEqual(instruction.type, inst_type)
    
    def test_logical_instructions(self):
        """Test instrucciones lógicas."""
        logical_types = [
            InstructionType.AND, InstructionType.OR,
            InstructionType.NOT, InstructionType.XOR
        ]
        
        for inst_type in logical_types:
            with self.subTest(instruction_type=inst_type):
                if inst_type == InstructionType.NOT:
                    instruction = Instruction(inst_type, "R1", "R2")
                else:
                    instruction = Instruction(inst_type, "R1", "R2", "R3")
                self.assertEqual(instruction.type, inst_type)
    
    def test_memory_instructions(self):
        """Test instrucciones de memoria."""
        memory_types = [InstructionType.LOAD, InstructionType.STORE]
        
        for inst_type in memory_types:
            with self.subTest(instruction_type=inst_type):
                instruction = Instruction(inst_type, "R1", 100)
                self.assertEqual(instruction.type, inst_type)
    
    def test_control_instructions(self):
        """Test instrucciones de control."""
        control_types = [
            InstructionType.JMP, InstructionType.JZ,
            InstructionType.JNZ, InstructionType.HALT
        ]
        
        for inst_type in control_types:
            with self.subTest(instruction_type=inst_type):
                if inst_type == InstructionType.HALT:
                    instruction = Instruction(inst_type)
                else:
                    instruction = Instruction(inst_type, 100)
                self.assertEqual(instruction.type, inst_type)


if __name__ == '__main__':
    unittest.main()