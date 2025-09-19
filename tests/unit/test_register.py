"""
Pruebas unitarias para el módulo register.py

Aplicando técnicas de partición equivalente:
- Partición 1: Valores válidos (enteros dentro del rango)
- Partición 2: Valores límite (0, valores máximos/mínimos)
- Partición 3: Valores inválidos (negativos, fuera de rango)
- Partición 4: Operaciones con observadores
"""

import unittest
from unittest.mock import Mock
import sys
import os

# Agregar path para imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from hardware.register import Register
from core.exceptions import InvalidRegisterError


class TestRegister(unittest.TestCase):
    """Pruebas para la clase Register usando partición equivalente."""
    
    def setUp(self):
        """Configuración común para todas las pruebas."""
        self.register_name = "R1"
        self.register = Register(self.register_name)
        self.mock_observer = Mock()
        self.mock_observer.update = Mock()
    
    # Partición 1: Valores válidos
    def test_register_creation_with_valid_name(self):
        """Test creación de registro con nombre válido."""
        register = Register("PC")
        self.assertEqual(register.name, "PC")
        self.assertEqual(register.value, 0)  # Valor inicial por defecto
    
    def test_register_creation_with_initial_value(self):
        """Test creación de registro con valor inicial."""
        initial_value = 42
        register = Register("MAR", initial_value)
        self.assertEqual(register.name, "MAR")
        self.assertEqual(register.value, initial_value)
    
    def test_set_valid_positive_value(self):
        """Test asignar valor positivo válido."""
        test_value = 100
        self.register.set_value(test_value)
        self.assertEqual(self.register.value, test_value)
    
    def test_set_multiple_valid_values(self):
        """Test asignar múltiples valores válidos."""
        test_values = [1, 50, 255, 1000, 65535]
        
        for value in test_values:
            with self.subTest(value=value):
                self.register.set_value(value)
                self.assertEqual(self.register.value, value)
    
    def test_get_value_after_set(self):
        """Test obtener valor después de asignarlo."""
        test_value = 777
        self.register.set_value(test_value)
        retrieved_value = self.register.value
        self.assertEqual(retrieved_value, test_value)
    
    # Partición 2: Valores límite
    def test_set_zero_value(self):
        """Test asignar valor cero."""
        self.register.set_value(0)
        self.assertEqual(self.register.value, 0)
    
    def test_set_maximum_16bit_value(self):
        """Test asignar valor máximo de 16 bits."""
        max_value = 65535  # 2^16 - 1
        self.register.set_value(max_value)
        self.assertEqual(self.register.value, max_value)
    
    def test_set_maximum_32bit_value(self):
        """Test asignar valor máximo de 32 bits."""
        max_value = 2147483647  # 2^31 - 1
        self.register.set_value(max_value)
        self.assertEqual(self.register.value, max_value)
    
    def test_boundary_values(self):
        """Test valores límite específicos."""
        boundary_values = [0, 1, 255, 256, 65535, 65536]
        
        for value in boundary_values:
            with self.subTest(value=value):
                self.register.set_value(value)
                self.assertEqual(self.register.value, value)
    
    # Partición 3: Valores inválidos (según diseño, pueden ser válidos)
    def test_set_negative_value(self):
        """Test asignar valor negativo."""
        # En algunos diseños, valores negativos podrían ser válidos
        negative_value = -10
        self.register.set_value(negative_value)
        self.assertEqual(self.register.value, negative_value)
    
    def test_set_large_negative_value(self):
        """Test asignar valor negativo grande."""
        large_negative = -999999
        self.register.set_value(large_negative)
        self.assertEqual(self.register.value, large_negative)
    
    def test_set_very_large_positive_value(self):
        """Test asignar valor positivo muy grande."""
        very_large_value = 999999999
        self.register.set_value(very_large_value)
        self.assertEqual(self.register.value, very_large_value)
    
    # Partición 4: Operaciones con observadores
    def test_observer_notification_on_value_change(self):
        """Test notificación a observadores al cambiar valor."""
        self.register.add_observer(self.mock_observer)
        
        new_value = 42
        self.register.set_value(new_value)
        
        # Verificar que el observador fue notificado
        self.mock_observer.update.assert_called()

        # Verificar que se pasó la información correcta
        # update(observable, event_type, data)
        call_args = self.mock_observer.update.call_args[0]
        register_obj = call_args[0]  # the register object
        event_type = call_args[1]    # event type
        data = call_args[2]          # data dict
        
        self.assertEqual(register_obj, self.register)
        self.assertIn('register_name', data)
        self.assertEqual(data['register_name'], self.register_name)
        self.assertEqual(data['new_value'], new_value)
    
    def test_multiple_observers_notification(self):
        """Test notificación a múltiples observadores."""
        observer2 = Mock()
        observer2.update = Mock()
        observer3 = Mock()
        observer3.update = Mock()
        
        self.register.add_observer(self.mock_observer)
        self.register.add_observer(observer2)
        self.register.add_observer(observer3)
        
        self.register.set_value(123)
        
        # Verificar que todos los observadores fueron notificados
        self.mock_observer.update.assert_called_once()
        observer2.update.assert_called_once()
        observer3.update.assert_called_once()
    
    def test_no_notification_when_same_value(self):
        """Test que no se notifica cuando se asigna el mismo valor."""
        initial_value = 50
        self.register.set_value(initial_value)
        
        self.register.add_observer(self.mock_observer)
        self.mock_observer.update.reset_mock()  # Limpiar llamadas anteriores
        
        # Asignar el mismo valor
        self.register.set_value(initial_value)
        
        # No debe haber notificación
        self.mock_observer.update.assert_not_called()
    
    def test_notification_content_format(self):
        """Test formato del contenido de notificación."""
        self.register.add_observer(self.mock_observer)
        
        test_value = 888
        self.register.set_value(test_value)
        
        # Obtener los argumentos pasados a update
        call_args = self.mock_observer.update.call_args[0]
        register_obj = call_args[0]  # the register object
        event_type = call_args[1]    # event type
        data = call_args[2]          # data dict
        
        # Verificar estructura de la notificación
        self.assertIsInstance(data, dict)
        self.assertIn('register_name', data)
        self.assertIn('new_value', data)
        self.assertEqual(data['new_value'], test_value)
        self.assertEqual(data['register_name'], self.register_name)
    
    # Tests de propiedades del registro
    def test_register_name_immutable(self):
        """Test que el nombre del registro es inmutable."""
        original_name = self.register.name
        
        # Intentar cambiar el nombre (no debe ser posible)
        with self.assertRaises(AttributeError):
            self.register.name = "NewName"
        
        # Verificar que el nombre no cambió
        self.assertEqual(self.register.name, original_name)
    
    def test_register_string_representation(self):
        """Test representación string del registro."""
        self.register.set_value(456)
        str_repr = str(self.register)
        
        self.assertIn(self.register_name, str_repr)
        self.assertIn("456", str_repr)
    
    def test_register_repr_representation(self):
        """Test representación repr del registro."""
        self.register.set_value(789)
        repr_str = repr(self.register)
        
        self.assertIn("Register", repr_str)
        self.assertIn(self.register_name, repr_str)
        self.assertIn("789", repr_str)
    
    # Tests de casos especiales
    def test_register_with_empty_name(self):
        """Test crear registro con nombre vacío."""
        register = Register("")
        self.assertEqual(register.name, "")
        self.assertEqual(register.value, 0)
    
    def test_register_with_special_character_name(self):
        """Test crear registro con caracteres especiales en el nombre."""
        special_names = ["R-1", "R_1", "REG#1", "R.1"]
        
        for name in special_names:
            with self.subTest(name=name):
                register = Register(name)
                self.assertEqual(register.name, name)
    
    def test_register_with_long_name(self):
        """Test crear registro con nombre largo."""
        long_name = "Very_Long_Register_Name_That_Exceeds_Normal_Length"
        register = Register(long_name)
        self.assertEqual(register.name, long_name)
    
    # Tests de concurrencia y estado
    def test_sequential_value_changes(self):
        """Test cambios secuenciales de valor."""
        values = [0, 10, 20, 15, 5, 100, 0]
        
        for value in values:
            with self.subTest(value=value):
                self.register.set_value(value)
                self.assertEqual(self.register.value, value)
    
    def test_rapid_value_changes_with_observer(self):
        """Test cambios rápidos de valor con observador."""
        self.register.add_observer(self.mock_observer)
        
        values = list(range(10, 100, 10))  # [10, 20, 30, ..., 90] - skip 0 since register starts with 0
        
        for value in values:
            self.register.set_value(value)
        
        # Verificar que se llamó update para cada cambio
        self.assertEqual(self.mock_observer.update.call_count, len(values))
    
    # Tests de herencia de Observable
    def test_register_inherits_observable(self):
        """Test que Register hereda de Observable."""
        from core.observer import Observable
        self.assertIsInstance(self.register, Observable)
    
    def test_observer_operations_inherited(self):
        """Test que las operaciones de Observable están disponibles."""
        # Debe tener métodos de Observable
        self.assertTrue(hasattr(self.register, 'add_observer'))
        self.assertTrue(hasattr(self.register, 'remove_observer'))
        self.assertTrue(hasattr(self.register, 'notify_observers'))
    
    def test_remove_observer_functionality(self):
        """Test funcionalidad de remover observador."""
        self.register.add_observer(self.mock_observer)
        self.register.set_value(100)  # Debe notificar
        
        self.mock_observer.update.assert_called_once()
        self.mock_observer.update.reset_mock()
        
        # Remover observador
        self.register.remove_observer(self.mock_observer)
        self.register.set_value(200)  # No debe notificar
        
        self.mock_observer.update.assert_not_called()


if __name__ == '__main__':
    unittest.main()