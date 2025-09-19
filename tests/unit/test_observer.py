"""
Pruebas unitarias para el módulo observer.py

Aplicando técnicas de partición equivalente:
- Partición 1: Observadores válidos (objetos con método notify)
- Partición 2: Observadores inválidos (None, objetos sin notify)
- Partición 3: Operaciones con lista vacía
- Partición 4: Operaciones con múltiples observadores
"""

import unittest
from unittest.mock import Mock, MagicMock
import sys
import os

# Agregar path para imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from core.observer import Observable, Observer


class TestObserver(unittest.TestCase):
    """Pruebas para la clase Observer (base abstracta)."""
    
    def test_observer_is_abstract(self):
        """Verifica que Observer sea una clase abstracta."""
        with self.assertRaises(TypeError):
            Observer()


class TestObservable(unittest.TestCase):
    """Pruebas para la clase Observable usando partición equivalente."""
    
    def setUp(self):
        """Configuración común para todas las pruebas."""
        self.observable = Observable()
        self.mock_observer = Mock()
        self.mock_observer.update = Mock()
    
    # Partición 1: Observadores válidos
    def test_add_valid_observer(self):
        """Test añadir observador válido."""
        self.observable.add_observer(self.mock_observer)
        self.assertIn(self.mock_observer, self.observable._observers)
        self.assertEqual(len(self.observable._observers), 1)
    
    def test_add_multiple_valid_observers(self):
        """Test añadir múltiples observadores válidos."""
        observer2 = Mock()
        observer2.update = Mock()
        observer3 = Mock()
        observer3.update = Mock()
        
        self.observable.add_observer(self.mock_observer)
        self.observable.add_observer(observer2)
        self.observable.add_observer(observer3)
        
        self.assertEqual(len(self.observable._observers), 3)
        self.assertIn(self.mock_observer, self.observable._observers)
        self.assertIn(observer2, self.observable._observers)
        self.assertIn(observer3, self.observable._observers)
    
    def test_add_duplicate_observer(self):
        """Test añadir el mismo observador múltiples veces."""
        self.observable.add_observer(self.mock_observer)
        self.observable.add_observer(self.mock_observer)
        
        # No debe duplicarse
        self.assertEqual(len(self.observable._observers), 1)
    
    # Partición 2: Observadores inválidos
    def test_add_none_observer(self):
        """Test añadir observador None."""
        with self.assertRaises((AttributeError, TypeError)):
            self.observable.add_observer(None)
    
    def test_add_invalid_observer_without_notify(self):
        """Test añadir observador sin método notify."""
        invalid_observer = Mock()
        del invalid_observer.update  # Remover el método notify
        
        self.observable.add_observer(invalid_observer)
        # Debe fallar al intentar notificar
        with self.assertRaises(AttributeError):
            self.observable.notify_observers("test", "test")
    
    # Partición 3: Operaciones con lista vacía
    def test_remove_from_empty_list(self):
        """Test remover observador de lista vacía."""
        # No debe lanzar excepción
        self.observable.remove_observer(self.mock_observer)
        self.assertEqual(len(self.observable._observers), 0)
    
    def test_notify_empty_list(self):
        """Test notificar con lista vacía."""
        # No debe lanzar excepción
        self.observable.notify_observers("test", "test_message")
        self.assertEqual(len(self.observable._observers), 0)
    
    # Partición 4: Operaciones con múltiples observadores
    def test_remove_valid_observer(self):
        """Test remover observador válido."""
        self.observable.add_observer(self.mock_observer)
        self.observable.remove_observer(self.mock_observer)
        
        self.assertNotIn(self.mock_observer, self.observable._observers)
        self.assertEqual(len(self.observable._observers), 0)
    
    def test_remove_one_of_multiple_observers(self):
        """Test remover uno de múltiples observadores."""
        observer2 = Mock()
        observer2.update = Mock()
        
        self.observable.add_observer(self.mock_observer)
        self.observable.add_observer(observer2)
        
        self.observable.remove_observer(self.mock_observer)
        
        self.assertNotIn(self.mock_observer, self.observable._observers)
        self.assertIn(observer2, self.observable._observers)
        self.assertEqual(len(self.observable._observers), 1)
    
    def test_remove_nonexistent_observer(self):
        """Test remover observador que no existe."""
        observer2 = Mock()
        observer2.update = Mock()
        
        self.observable.add_observer(self.mock_observer)
        self.observable.remove_observer(observer2)  # No existe
        
        # La lista no debe cambiar
        self.assertIn(self.mock_observer, self.observable._observers)
        self.assertEqual(len(self.observable._observers), 1)
    
    def test_notify_multiple_observers(self):
        """Test notificar a múltiples observadores."""
        observer2 = Mock()
        observer2.update = Mock()
        observer3 = Mock()
        observer3.update = Mock()
        
        self.observable.add_observer(self.mock_observer)
        self.observable.add_observer(observer2)
        self.observable.add_observer(observer3)
        
        test_message = "test_notification"
        self.observable.notify_observers("test_event", test_message)
        
        # Verificar que todos fueron notificados
        self.mock_observer.update.assert_called_once_with(self.observable, "test_event", test_message)
        observer2.update.assert_called_once_with(self.observable, "test_event", test_message)
        observer3.update.assert_called_once_with(self.observable, "test_event", test_message)
    
    def test_notify_with_different_message_types(self):
        """Test notificar con diferentes tipos de mensaje."""
        self.observable.add_observer(self.mock_observer)
        
        # String
        self.observable.notify_observers("test", "string_message")
        self.mock_observer.update.assert_called_with(self.observable, "test", "string_message")
        
        # Dictionary
        dict_message = {"type": "update", "data": "test"}
        self.observable.notify_observers("test", dict_message)
        self.mock_observer.update.assert_called_with(self.observable, "test", dict_message)
        
        # None
        self.observable.notify_observers("test", None)
        self.mock_observer.update.assert_called_with(self.observable, "test", None)
    
    def test_observer_exception_handling(self):
        """Test manejo de excepciones en observadores."""
        failing_observer = Mock()
        failing_observer.update = Mock(side_effect=Exception("Observer failed"))
        
        working_observer = Mock()
        working_observer.update = Mock()
        
        self.observable.add_observer(failing_observer)
        self.observable.add_observer(working_observer)
        
        # No debe fallar aunque un observador lance excepción
        try:
            self.observable.notify_observers("test", "test")
        except Exception:
            self.fail("notify_observers no debe propagar excepciones de observadores")
        
        # El observador que funciona debe ser notificado
        working_observer.update.assert_called_once_with(self.observable, "test", "test")
    
    # Casos límite adicionales
    def test_observers_list_consistency(self):
        """Test consistencia de la lista de observadores."""
        # Verificar que la lista se inicializa correctamente
        self.assertIsInstance(self.observable._observers, list)
        self.assertEqual(len(self.observable._observers), 0)
    
    def test_massive_observers_addition(self):
        """Test añadir gran cantidad de observadores."""
        observers = []
        for i in range(100):
            observer = Mock()
            observer.update = Mock()
            observers.append(observer)
            self.observable.add_observer(observer)
        
        self.assertEqual(len(self.observable._observers), 100)
        
        # Notificar a todos
        self.observable.notify_observers("test", "mass_test")
        
        # Verificar que todos fueron notificados
        for observer in observers:
            observer.update.assert_called_once_with(self.observable, "test", "mass_test")


if __name__ == '__main__':
    unittest.main()