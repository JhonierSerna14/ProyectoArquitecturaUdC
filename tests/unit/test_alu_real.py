"""
Pruebas unitarias para la clase ALU - Versión Real.

Estas pruebas están adaptadas a la implementación real de ALU.py
usando partición equivalente para las operaciones aritméticas y lógicas.

Partición equivalente aplicada:
- Operaciones aritméticas: ADD, SUB, MUL, DIV
- Operaciones lógicas: AND, OR, NOT, XOR
- Operaciones de salto: JP, JPZ
- Valores válidos: [-16384, 16383] (rango de 15 bits + signo)
- Valores inválidos: fuera del rango válido
- Casos especiales: división por cero, flags PSW
"""

import unittest
import sys
import os

# Agregar el directorio padre al path para importar las clases
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from hardware.alu import ALU


class TestALUReal(unittest.TestCase):
    """Pruebas para la clase ALU usando la implementación real."""
    
    def setUp(self):
        """Configura una nueva ALU para cada prueba."""
        self.alu = ALU()
        
    def test_alu_initialization(self):
        """Test la inicialización correcta de la ALU."""
        self.assertEqual(self.alu.value, 0)
        self.assertEqual(self.alu.psw['Z'], 0)
        self.assertEqual(self.alu.psw['C'], 0)
        self.assertEqual(self.alu.psw['S'], 0)
        self.assertEqual(self.alu.psw['O'], 0)
        
    def test_get_psw(self):
        """Test obtener el estado del PSW."""
        psw = self.alu.psw
        self.assertIsInstance(psw, dict)
        self.assertIn('Z', psw)
        self.assertIn('C', psw)
        self.assertIn('S', psw)
        self.assertIn('O', psw)
        
    # === PRUEBAS DE OPERACIONES ARITMÉTICAS ===
        
    def test_add_operation(self):
        """Test operación ADD con partición equivalente."""
        # Partición 1: Valores positivos
        self.alu.execute('ADD', 10, 5)
        self.assertEqual(self.alu.value, 15)
        
        # Partición 2: Valores negativos
        self.alu.execute('ADD', -10, -5)
        self.assertEqual(self.alu.value, -15)
        
        # Partición 3: Mixtos
        self.alu.execute('ADD', 10, -5)
        self.assertEqual(self.alu.value, 5)
        
        # Partición 4: Resultado cero
        self.alu.execute('ADD', 5, -5)
        self.assertEqual(self.alu.value, 0)
        self.assertEqual(self.alu.psw['Z'], 1)  # Flag Z debe activarse
        
    def test_sub_operation(self):
        """Test operación SUB con partición equivalente."""
        # Partición 1: Resultado positivo
        self.alu.execute('SUB', 10, 5)
        self.assertEqual(self.alu.value, 5)
        
        # Partición 2: Resultado negativo
        self.alu.execute('SUB', 5, 10)
        self.assertEqual(self.alu.value, -5)
        
        # Partición 3: Resultado cero
        self.alu.execute('SUB', 10, 10)
        self.assertEqual(self.alu.value, 0)
        self.assertEqual(self.alu.psw['Z'], 1)
        
    def test_mul_operation(self):
        """Test operación MUL con partición equivalente."""
        # Partición 1: Números pequeños
        self.alu.execute('MUL', 5, 3)
        self.assertEqual(self.alu.value, 15)
        
        # Partición 2: Con cero
        self.alu.execute('MUL', 5, 0)
        self.assertEqual(self.alu.value, 0)
        self.assertEqual(self.alu.psw['Z'], 1)
        
        # Partición 3: Números negativos
        self.alu.execute('MUL', -5, 3)
        self.assertEqual(self.alu.value, -15)
        self.assertEqual(self.alu.psw['S'], 1)  # Flag S para negativo
        
    def test_div_operation(self):
        """Test operación DIV con partición equivalente."""
        # Partición 1: División normal
        self.alu.execute('DIV', 15, 3)
        self.assertEqual(self.alu.value, 5)
        
        # Partición 2: División por cero
        self.alu.execute('DIV', 10, 0)
        self.assertEqual(self.alu.value, 0)
        self.assertEqual(self.alu.psw['Z'], 1)
        
        # Partición 3: División con resto (división entera)
        self.alu.execute('DIV', 17, 5)
        self.assertEqual(self.alu.value, 3)  # 17 // 5 = 3
        
    # === PRUEBAS DE OPERACIONES LÓGICAS ===
        
    def test_and_operation(self):
        """Test operación AND con partición equivalente."""
        # Partición 1: Todos bits activados
        self.alu.execute('AND', 0xFF, 0xFF)
        self.assertEqual(self.alu.value, 0xFF)
        
        # Partición 2: Algunos bits activados
        self.alu.execute('AND', 0xF0, 0x0F)
        self.assertEqual(self.alu.value, 0)
        self.assertEqual(self.alu.psw['Z'], 1)
        
        # Partición 3: Resultado no cero
        self.alu.execute('AND', 0xFF, 0xAA)
        self.assertEqual(self.alu.value, 0xAA)
        
    def test_or_operation(self):
        """Test operación OR con partición equivalente."""
        # Partición 1: Con ceros
        self.alu.execute('OR', 0, 0)
        self.assertEqual(self.alu.value, 0)
        self.assertEqual(self.alu.psw['Z'], 1)
        
        # Partición 2: Combinación normal
        self.alu.execute('OR', 0xF0, 0x0F)
        self.assertEqual(self.alu.value, 0xFF)
        
    def test_not_operation(self):
        """Test operación NOT con partición equivalente."""
        # NOT usa solo operand2
        self.alu.execute('NOT', 0, 0)
        self.assertEqual(self.alu.value, ~0)
        
        self.alu.execute('NOT', 0, 0xFF)
        self.assertEqual(self.alu.value, ~0xFF)
        
    def test_xor_operation(self):
        """Test operación XOR con partición equivalente."""
        # Partición 1: Iguales (resultado 0)
        self.alu.execute('XOR', 0xFF, 0xFF)
        self.assertEqual(self.alu.value, 0)
        self.assertEqual(self.alu.psw['Z'], 1)
        
        # Partición 2: Diferentes
        self.alu.execute('XOR', 0xF0, 0x0F)
        self.assertEqual(self.alu.value, 0xFF)
        
    # === PRUEBAS DE OPERACIONES DE SALTO ===
        
    def test_jp_operation(self):
        """Test operación JP (jump)."""
        # JP simplemente asigna operand1 al valor
        self.alu.execute('JP', 100, 0)
        self.assertEqual(self.alu.value, 100)
        
    def test_jpz_operation(self):
        """Test operación JPZ (jump if zero)."""
        # Partición 1: operand2 es cero (salto)
        self.alu.execute('JPZ', 200, 0)
        self.assertEqual(self.alu.value, 200)
        
        # Partición 2: operand2 no es cero (no salto)
        self.alu.execute('JPZ', 300, 5)
        self.assertIsNone(self.alu.value)  # No salta, retorna None
        
        # Partición 3: Verificar flags PSW
        self.alu.execute('JPZ', 100, 0)  # Salta
        self.assertEqual(self.alu.psw['Z'], 0)  # 100 != 0, Z flag = 0
        
        self.alu.execute('JPZ', 0, 0)  # Salta a 0
        self.assertEqual(self.alu.psw['Z'], 1)  # 0 == 0, Z flag = 1
        
    # === PRUEBAS DE VALIDACIÓN DE RANGOS ===
        
    def test_valid_range_operations(self):
        """Test operaciones dentro del rango válido."""
        # Rango válido: [-16384, 16383] = [-0x4000, 0x3FFF]
        valid_values = [0, 1, -1, 16383, -16384, 100, -100]
        
        for val1 in [0, 100, -100]:
            for val2 in [0, 50, -50]:
                with self.subTest(val1=val1, val2=val2):
                    # No debe lanzar excepción
                    self.alu.execute('ADD', val1, val2)
                    
    def test_invalid_range_operations(self):
        """Test operaciones fuera del rango válido."""
        from core.exceptions import OperandOutOfRangeError
        
        # Valores fuera del rango válido
        invalid_values = [16384, -16385, 20000, -20000]
        
        for invalid_val in invalid_values:
            with self.subTest(invalid_val=invalid_val):
                with self.assertRaises(OperandOutOfRangeError) as context:
                    self.alu.execute('ADD', invalid_val, 0)
                self.assertIn('out of range', str(context.exception))
                
    # === PRUEBAS DE FLAGS PSW ===
        
    def test_zero_flag(self):
        """Test activación del flag Z (Zero)."""
        # Flag Z debe activarse cuando el resultado es 0
        self.alu.execute('SUB', 5, 5)
        self.assertEqual(self.alu.psw['Z'], 1)
        
        # Flag Z debe desactivarse cuando el resultado no es 0
        self.alu.execute('ADD', 1, 1)
        self.assertEqual(self.alu.psw['Z'], 0)
        
    def test_sign_flag(self):
        """Test activación del flag S (Sign)."""
        # Flag S debe activarse cuando el resultado es negativo
        self.alu.execute('SUB', 5, 10)
        self.assertEqual(self.alu.psw['S'], 1)
        
        # Flag S debe desactivarse cuando el resultado es positivo
        self.alu.execute('ADD', 10, 5)
        self.assertEqual(self.alu.psw['S'], 0)
        
    def test_carry_flag_add(self):
        """Test activación del flag C (Carry) en operaciones ADD."""
        # El flag C se activa cuando el resultado supera 0x3FFF en ADD
        # Usando valores que produzcan overflow
        self.alu.execute('ADD', 16383, 1)  # 0x3FFF + 1 = 0x4000
        self.assertEqual(self.alu.psw['C'], 1)
        
    def test_carry_flag_sub(self):
        """Test activación del flag C (Carry) en operaciones SUB."""
        # El flag C se activa cuando operand1 < operand2 en SUB
        self.alu.execute('SUB', 5, 10)
        self.assertEqual(self.alu.psw['C'], 1)
        
        self.alu.execute('SUB', 10, 5)
        self.assertEqual(self.alu.psw['C'], 0)
        
    def test_multiple_operations_sequence(self):
        """Test secuencia de múltiples operaciones."""
        # Secuencia realista de operaciones
        self.alu.execute('ADD', 10, 5)      # 15
        self.assertEqual(self.alu.value, 15)
        
        self.alu.execute('MUL', 3, 4)       # 12
        self.assertEqual(self.alu.value, 12)
        
        self.alu.execute('SUB', self.alu.value, 12)  # 0
        self.assertEqual(self.alu.value, 0)
        self.assertEqual(self.alu.psw['Z'], 1)


if __name__ == '__main__':
    unittest.main()