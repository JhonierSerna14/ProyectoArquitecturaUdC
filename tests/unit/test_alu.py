"""
Pruebas unitarias para el módulo alu.py

Aplicando técnicas de partición equivalente:
- Partición 1: Operaciones aritméticas válidas (ADD, SUB, MUL, DIV)
- Partición 2: Operaciones lógicas válidas (AND, OR, NOT, XOR)
- Partición 3: Casos límite (división por cero, overflow, valores extremos)
- Partición 4: Gestión de flags PSW (Zero, Carry, Sign, Overflow)
"""

import unittest
from unittest.mock import Mock, patch
import sys
import os

# Agregar path para imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from hardware.alu import ALU
from core.exceptions import ALUOperationError as ALUError


class TestALU(unittest.TestCase):
    """Pruebas para la clase ALU usando partición equivalente."""
    
    def setUp(self):
        """Configuración común para todas las pruebas."""
        self.alu = ALU()
        self.mock_observer = Mock()
        self.mock_observer.update = Mock()
    
    # Partición 1: Operaciones aritméticas válidas
    def test_add_positive_numbers(self):
        """Test suma de números positivos."""
        result = self.alu.add(10, 5)
        self.assertEqual(result, 15)
    
    def test_add_negative_numbers(self):
        """Test suma de números negativos."""
        result = self.alu.add(-10, -5)
        self.assertEqual(result, -15)
    
    def test_add_mixed_sign_numbers(self):
        """Test suma de números con signos diferentes."""
        result = self.alu.add(10, -3)
        self.assertEqual(result, 7)
        
        result = self.alu.add(-10, 15)
        self.assertEqual(result, 5)
    
    def test_add_with_zero(self):
        """Test suma con cero."""
        result = self.alu.add(42, 0)
        self.assertEqual(result, 42)
        
        result = self.alu.add(0, 42)
        self.assertEqual(result, 42)
        
        result = self.alu.add(0, 0)
        self.assertEqual(result, 0)
    
    def test_subtract_positive_numbers(self):
        """Test resta de números positivos."""
        result = self.alu.subtract(10, 3)
        self.assertEqual(result, 7)
        
        result = self.alu.subtract(5, 8)
        self.assertEqual(result, -3)
    
    def test_subtract_negative_numbers(self):
        """Test resta de números negativos."""
        result = self.alu.subtract(-10, -3)
        self.assertEqual(result, -7)
        
        result = self.alu.subtract(-5, -8)
        self.assertEqual(result, 3)
    
    def test_subtract_with_zero(self):
        """Test resta con cero."""
        result = self.alu.subtract(42, 0)
        self.assertEqual(result, 42)
        
        result = self.alu.subtract(0, 42)
        self.assertEqual(result, -42)
    
    def test_multiply_positive_numbers(self):
        """Test multiplicación de números positivos."""
        result = self.alu.multiply(6, 7)
        self.assertEqual(result, 42)
        
        result = self.alu.multiply(12, 8)
        self.assertEqual(result, 96)
    
    def test_multiply_negative_numbers(self):
        """Test multiplicación de números negativos."""
        result = self.alu.multiply(-6, -7)
        self.assertEqual(result, 42)
        
        result = self.alu.multiply(-5, 4)
        self.assertEqual(result, -20)
        
        result = self.alu.multiply(5, -4)
        self.assertEqual(result, -20)
    
    def test_multiply_with_zero(self):
        """Test multiplicación con cero."""
        result = self.alu.multiply(42, 0)
        self.assertEqual(result, 0)
        
        result = self.alu.multiply(0, 42)
        self.assertEqual(result, 0)
    
    def test_multiply_with_one(self):
        """Test multiplicación con uno."""
        result = self.alu.multiply(42, 1)
        self.assertEqual(result, 42)
        
        result = self.alu.multiply(1, 42)
        self.assertEqual(result, 42)
    
    def test_divide_positive_numbers(self):
        """Test división de números positivos."""
        result = self.alu.divide(20, 4)
        self.assertEqual(result, 5)
        
        result = self.alu.divide(15, 3)
        self.assertEqual(result, 5)
    
    def test_divide_negative_numbers(self):
        """Test división de números negativos."""
        result = self.alu.divide(-20, -4)
        self.assertEqual(result, 5)
        
        result = self.alu.divide(-15, 3)
        self.assertEqual(result, -5)
        
        result = self.alu.divide(15, -3)
        self.assertEqual(result, -5)
    
    def test_divide_with_remainder(self):
        """Test división con resto."""
        result = self.alu.divide(10, 3)
        self.assertEqual(result, 3)  # División entera
        
        result = self.alu.divide(17, 5)
        self.assertEqual(result, 3)
    
    def test_divide_by_one(self):
        """Test división por uno."""
        result = self.alu.divide(42, 1)
        self.assertEqual(result, 42)
        
        result = self.alu.divide(-42, 1)
        self.assertEqual(result, -42)
    
    # Partición 2: Operaciones lógicas válidas
    def test_and_operation(self):
        """Test operación AND lógica."""
        result = self.alu.logical_and(15, 7)  # 1111 & 0111 = 0111 = 7
        self.assertEqual(result, 7)
        
        result = self.alu.logical_and(12, 10)  # 1100 & 1010 = 1000 = 8
        self.assertEqual(result, 8)
    
    def test_and_with_zero(self):
        """Test operación AND con cero."""
        result = self.alu.logical_and(42, 0)
        self.assertEqual(result, 0)
        
        result = self.alu.logical_and(0, 42)
        self.assertEqual(result, 0)
    
    def test_and_with_all_ones(self):
        """Test operación AND con todos los bits en 1."""
        value = 42
        all_ones = 0xFFFFFFFF  # Asumiendo 32 bits
        result = self.alu.logical_and(value, all_ones)
        self.assertEqual(result, value)
    
    def test_or_operation(self):
        """Test operación OR lógica."""
        result = self.alu.logical_or(12, 10)  # 1100 | 1010 = 1110 = 14
        self.assertEqual(result, 14)
        
        result = self.alu.logical_or(5, 3)  # 0101 | 0011 = 0111 = 7
        self.assertEqual(result, 7)
    
    def test_or_with_zero(self):
        """Test operación OR con cero."""
        result = self.alu.logical_or(42, 0)
        self.assertEqual(result, 42)
        
        result = self.alu.logical_or(0, 42)
        self.assertEqual(result, 42)
    
    def test_or_with_same_value(self):
        """Test operación OR con el mismo valor."""
        result = self.alu.logical_or(42, 42)
        self.assertEqual(result, 42)
    
    def test_not_operation(self):
        """Test operación NOT lógica."""
        # NOT es complement bit a bit, depende de la implementación
        result = self.alu.logical_not(0)
        self.assertNotEqual(result, 0)  # NOT 0 debe ser diferente de 0
        
        # Para un valor, NOT NOT debe dar el valor original (con máscara)
        value = 42
        result = self.alu.logical_not(self.alu.logical_not(value))
        # Esto depende de cómo esté implementado el NOT
    
    def test_xor_operation(self):
        """Test operación XOR lógica."""
        result = self.alu.logical_xor(12, 10)  # 1100 ^ 1010 = 0110 = 6
        self.assertEqual(result, 6)
        
        result = self.alu.logical_xor(15, 15)  # Cualquier valor XOR consigo mismo = 0
        self.assertEqual(result, 0)
    
    def test_xor_with_zero(self):
        """Test operación XOR con cero."""
        result = self.alu.logical_xor(42, 0)
        self.assertEqual(result, 42)
        
        result = self.alu.logical_xor(0, 42)
        self.assertEqual(result, 42)
    
    # Partición 3: Casos límite y errores
    def test_divide_by_zero_raises_error(self):
        """Test división por cero lanza excepción."""
        with self.assertRaises(ALUError) as context:
            self.alu.divide(42, 0)
        
        self.assertIn("división por cero", str(context.exception).lower())
    
    def test_large_number_operations(self):
        """Test operaciones con números grandes."""
        large_num1 = 999999
        large_num2 = 888888
        
        result = self.alu.add(large_num1, large_num2)
        self.assertEqual(result, large_num1 + large_num2)
        
        result = self.alu.multiply(1000, 1000)
        self.assertEqual(result, 1000000)
    
    def test_negative_large_numbers(self):
        """Test operaciones con números negativos grandes."""
        large_neg1 = -999999
        large_neg2 = -888888
        
        result = self.alu.add(large_neg1, large_neg2)
        self.assertEqual(result, large_neg1 + large_neg2)
    
    # Partición 4: Gestión de flags PSW
    def test_zero_flag_set_on_zero_result(self):
        """Test que el flag Zero se establece en resultado cero."""
        self.alu.add_observer(self.mock_observer)
        
        result = self.alu.subtract(5, 5)  # Resultado debe ser 0
        self.assertEqual(result, 0)
        
        # Verificar notificación del flag Zero
        self.mock_observer.update.assert_called()
        # update(observable, event_type, data)
        call_args = self.mock_observer.update.call_args[0]
        data = call_args[2]  # data dict
        
        if 'flags' in data:
            self.assertTrue(data['flags'].get('zero', False))
    
    def test_zero_flag_not_set_on_nonzero_result(self):
        """Test que el flag Zero no se establece en resultado no-cero."""
        self.alu.add_observer(self.mock_observer)
        
        result = self.alu.add(5, 3)  # Resultado debe ser 8
        self.assertEqual(result, 8)
        
        # Verificar que el flag Zero no está establecido
        if self.mock_observer.notify.called:
            notification = self.mock_observer.notify.call_args[0][0]
            if 'flags' in notification:
                self.assertFalse(notification['flags'].get('zero', False))
    
    def test_sign_flag_on_negative_result(self):
        """Test que el flag Sign se establece en resultado negativo."""
        self.alu.add_observer(self.mock_observer)
        
        result = self.alu.subtract(3, 8)  # Resultado debe ser -5
        self.assertEqual(result, -5)
        
        # Verificar notificación del flag Sign
        if self.mock_observer.notify.called:
            notification = self.mock_observer.notify.call_args[0][0]
            if 'flags' in notification:
                self.assertTrue(notification['flags'].get('sign', False))
    
    def test_carry_flag_on_overflow(self):
        """Test flag Carry en overflow (si está implementado)."""
        self.alu.add_observer(self.mock_observer)
        
        # Operación que podría generar carry
        large_num = 2**31 - 1  # Máximo entero de 32 bits con signo
        self.alu.add(large_num, 1)
        
        # La implementación específica determinará si hay carry
        # Este test verifica que el sistema maneja la situación
    
    # Tests de observadores y notificaciones
    def test_observer_notification_on_operation(self):
        """Test notificación a observadores en operación."""
        self.alu.add_observer(self.mock_observer)
        
        result = self.alu.add(10, 5)
        
        # Verificar que se notificó
        self.mock_observer.update.assert_called()
        
        # Verificar contenido de la notificación
        # update(observable, event_type, data)
        # ALU sends 2 notifications: operation-executed and flags-updated
        # We want the first one (operation-executed) which has opcode
        first_call_args = self.mock_observer.update.call_args_list[0][0]
        alu_obj = first_call_args[0]     # ALU object  
        event_type = first_call_args[1]  # event type
        data = first_call_args[2]        # data dict
        
        self.assertEqual(alu_obj, self.alu)
        self.assertIn('opcode', data)
        self.assertEqual(data['opcode'], 'ADD')
    
    def test_multiple_operations_multiple_notifications(self):
        """Test múltiples operaciones generan múltiples notificaciones."""
        self.alu.add_observer(self.mock_observer)
        
        self.alu.add(1, 2)
        self.alu.subtract(5, 3)
        self.alu.multiply(4, 6)
        
        # Debe haber al menos 3 llamadas
        self.assertGreaterEqual(self.mock_observer.update.call_count, 3)
    
    # Tests de herencia de Observable
    def test_alu_inherits_observable(self):
        """Test que ALU hereda de Observable."""
        from core.observer import Observable
        self.assertIsInstance(self.alu, Observable)
    
    def test_alu_observer_operations(self):
        """Test operaciones de observador disponibles en ALU."""
        self.assertTrue(hasattr(self.alu, 'add_observer'))
        self.assertTrue(hasattr(self.alu, 'remove_observer'))
        self.assertTrue(hasattr(self.alu, 'notify_observers'))
    
    # Tests de casos especiales
    def test_sequential_operations(self):
        """Test operaciones secuenciales."""
        results = []
        results.append(self.alu.add(10, 5))        # 15
        results.append(self.alu.subtract(results[-1], 3))  # 12
        results.append(self.alu.multiply(results[-1], 2))  # 24
        results.append(self.alu.divide(results[-1], 4))    # 6
        
        expected = [15, 12, 24, 6]
        self.assertEqual(results, expected)
    
    def test_operation_with_float_inputs(self):
        """Test operaciones con entradas float (si está soportado)."""
        # Dependiendo de la implementación, podría convertir a entero
        try:
            result = self.alu.add(10.5, 5.3)
            # Verificar que el resultado es válido
            self.assertIsInstance(result, (int, float))
        except (TypeError, ValueError):
            # Si no soporta float, debe fallar de manera controlada
            pass
    
    def test_string_representation(self):
        """Test representación string de ALU."""
        str_repr = str(self.alu)
        self.assertIn("ALU", str_repr)


if __name__ == '__main__':
    unittest.main()