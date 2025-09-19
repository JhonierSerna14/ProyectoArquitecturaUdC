"""
Pruebas unitarias para la clase Register - Versión Real.

Estas pruebas están adaptadas a la implementación real de Register.py
del módulo hardware que usa el patrón Observer.

Partición equivalente aplicada:
- Valores numéricos válidos: 0, positivos, negativos
- Valores límite: muy grandes, muy pequeños
- Funcionamiento del patrón Observer
"""

import unittest
from unittest.mock import Mock
import sys
import os

# Agregar el directorio padre al path para importar las clases
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from hardware.register import Register


class TestRegisterReal(unittest.TestCase):
    """Pruebas para la clase Register usando la implementación real."""
    
    def setUp(self):
        """Configura un registro para las pruebas."""
        pass  # No need for mock canvas with hardware Register
        
    def test_register_initialization(self):
        """Test la inicialización correcta del registro."""
        register = Register("TEST", 0)
        
        self.assertEqual(register.value, 0)
        self.assertEqual(register.name, "TEST")
        
    def test_set_value_positive(self):
        """Test establecer valores positivos."""
        register = Register("TEST", 0)
        
        # Partición: Valores positivos
        test_values = [1, 42, 1000, 999999]
        
        for value in test_values:
            with self.subTest(value=value):
                register.set_value(value)
                self.assertEqual(register.value, value)
                
    def test_set_value_negative(self):
        """Test establecer valores negativos."""
        register = Register("TEST", 0)
        
        # Partición: Valores negativos
        test_values = [-1, -42, -1000, -999999]
        
        for value in test_values:
            with self.subTest(value=value):
                register.set_value(value)
                self.assertEqual(register.value, value)
                
    def test_set_value_zero(self):
        """Test establecer valor cero."""
        register = Register("TEST", 0)
        
        register.set_value(0)
        self.assertEqual(register.value, 0)
        
    def test_set_value_updates_canvas(self):
        """Test que set_value notifica a los observadores."""
        register = Register("REG", 0)
        
        # Crear un observador mock
        mock_observer = Mock()
        register.add_observer(mock_observer)
        
        register.set_value(42)
        
        # Verifica que se notificó al observador con el método update
        mock_observer.update.assert_called_once()
        
    def test_multiple_value_changes(self):
        """Test múltiples cambios de valor."""
        register = Register("MULTI", 0)
        
        values = [10, -5, 0, 100, -200]
        
        for value in values:
            register.set_value(value)
            self.assertEqual(register.value, value)
            
    def test_value_persistence(self):
        """Test que el valor persiste hasta ser cambiado."""
        register = Register("PERSIST", 0)
        
        register.set_value(123)
        self.assertEqual(register.value, 123)
        
        # Simular otras operaciones
        _ = register.name
        
        # El valor debe seguir siendo el mismo
        self.assertEqual(register.value, 123)
        
    def test_large_values(self):
        """Test valores muy grandes."""
        register = Register("LARGE", 0)
        
        # Partición: Valores límite grandes
        large_values = [2**31-1, 2**32, 10**10]
        
        for value in large_values:
            with self.subTest(value=value):
                register.set_value(value)
                self.assertEqual(register.value, value)
                
    def test_register_string_representation(self):
        """Test representación string del registro."""
        register = Register("STRING_TEST", 42)
        
        # Test str()
        self.assertEqual(str(register), "STRING_TEST: 42")
        
        # Test repr()
        expected_repr = "Register(name='STRING_TEST', value=42)"
        self.assertEqual(repr(register), expected_repr)
        
    def test_clear_method(self):
        """Test método clear del registro."""
        register = Register("CLEAR_TEST", 100)
        
        # Verificar valor inicial
        self.assertEqual(register.value, 100)
        
        # Limpiar registro
        register.clear()
        
        # Verificar que se estableció a 0
        self.assertEqual(register.value, 0)


if __name__ == '__main__':
    unittest.main()