"""
Pruebas de integración para el simulador de computadora MVC.

Estas pruebas verifican el funcionamiento completo del sistema
incluyendo la coordinación entre Model, View y Controller.
"""

import unittest
from unittest.mock import Mock, patch, MagicMock
import threading
import time
import sys
import os

# Agregar path para imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from core.computer import Computer
from core.instruction import Instruction, InstructionType
from core.exceptions import *


class TestComputerIntegration(unittest.TestCase):
    """Pruebas de integración para el sistema Computer completo."""
    
    def setUp(self):
        """Configuración común para todas las pruebas."""
        self.computer = Computer()
        self.mock_observer = Mock()
        self.mock_observer.update = Mock()  # Observer usa update, no notify
        self.computer.add_observer(self.mock_observer)
    
    def test_complete_program_execution(self):
        """Test ejecución completa de un programa simple."""
        program = [
            "LOAD R1, 10",
            "LOAD R2, 5",
            "ADD R1, R2, R3",
            "STORE R3, 20",
            "HALT"
        ]
        
        # Cargar programa
        success = self.computer.load_program(program)
        self.assertTrue(success)
        
        # Ejecutar programa completo
        steps = 0
        max_steps = 10  # Prevenir loops infinitos
        
        while (self.computer.pc_register.value < len(self.computer.loaded_program) and 
               steps < max_steps):
            has_more = self.computer.execute_next_instruction()
            steps += 1
            
            if not has_more:
                break
        
        # Verificar estado final
        # R1 debe tener 10, R2 debe tener 5, R3 debe tener 15
        self.assertEqual(self.computer.register_bank.get_register("R1").value, 10)
        self.assertEqual(self.computer.register_bank.get_register("R2").value, 5)
        self.assertEqual(self.computer.register_bank.get_register("R3").value, 15)
        
        # Memoria[100] debe tener 15
        self.assertEqual(self.computer.memory.read(20), 15)
    
    def test_arithmetic_operations_integration(self):
        """Test integración de operaciones aritméticas."""
        program = [
            "LOAD R1, 20",
            "LOAD R2, 8",
            "ADD R1, R2, R3",    # R3 = 28
            "SUB R1, R2, R4",    # R4 = 12
            "MUL R3, R4, R5",    # R5 = 28 * 12 = 336
            "DIV R5, R2, R6",    # R6 = 336 / 8 = 42
            "HALT"
        ]
        
        self.computer.load_program(program)
        
        # Ejecutar programa
        steps = 0
        while (self.computer.pc_register.value < len(self.computer.loaded_program) and 
               steps < 20):
            self.computer.execute_next_instruction()
            steps += 1
        
        # Verificar resultados
        self.assertEqual(self.computer.register_bank.get_register("R3").value, 28)
        self.assertEqual(self.computer.register_bank.get_register("R4").value, 12)
        self.assertEqual(self.computer.register_bank.get_register("R5").value, 336)
        self.assertEqual(self.computer.register_bank.get_register("R6").value, 42)
    
    def test_memory_operations_integration(self):
        """Test integración de operaciones de memoria."""
        program = [
            "LOAD R1, 100",      # Cargar 100 en R1
            "STORE R1, 18",      # Guardar R1 en memoria[18]
            "LOAD R2, 200",      # Cargar 200 en R2
            "STORE R2, 19",      # Guardar R2 en memoria[19]
            "LOAD R3, *18",      # Cargar memoria[18] en R3 (debería ser 100)
            "LOAD R4, *19",      # Cargar memoria[19] en R4 (debería ser 200)
            "HALT"
        ]
        
        self.computer.load_program(program)
        
        # Ejecutar programa
        steps = 0
        while (self.computer.pc_register.value < len(self.computer.loaded_program) and 
               steps < 15):
            self.computer.execute_next_instruction()
            steps += 1
        
        # Verificar que los datos se almacenaron y cargaron correctamente
        self.assertEqual(self.computer.memory.read(18), 100)
        self.assertEqual(self.computer.memory.read(19), 200)
        self.assertEqual(self.computer.register_bank.get_register("R3").value, 100)
        self.assertEqual(self.computer.register_bank.get_register("R4").value, 200)
    
    def test_logical_operations_integration(self):
        """Test integración de operaciones lógicas."""
        program = [
            "LOAD R1, 15",       # 1111 en binario
            "LOAD R2, 7",        # 0111 en binario
            "AND R1, R2, R3",    # R3 = 1111 & 0111 = 0111 = 7
            "OR R1, R2, R4",     # R4 = 1111 | 0111 = 1111 = 15
            "XOR R1, R2, R5",    # R5 = 1111 ^ 0111 = 1000 = 8
            "NOT R1, R6",        # R6 = ~1111 (depende de implementación)
            "HALT"
        ]
        
        self.computer.load_program(program)
        
        # Ejecutar programa
        steps = 0
        while (self.computer.pc_register.value < len(self.computer.loaded_program) and 
               steps < 15):
            self.computer.execute_next_instruction()
            steps += 1
        
        # Verificar resultados lógicos
        self.assertEqual(self.computer.register_bank.get_register("R3").value, 7)
        self.assertEqual(self.computer.register_bank.get_register("R4").value, 15)
        self.assertEqual(self.computer.register_bank.get_register("R5").value, 8)
        # R6 depende de la implementación del NOT
    
    def test_observer_notifications_during_execution(self):
        """Test que se generan notificaciones durante la ejecución."""
        program = [
            "LOAD R1, 42",
            "ADD R1, R1, R2",
            "HALT"
        ]
        
        self.computer.load_program(program)
        
        # Limpiar llamadas previas
        self.mock_observer.update.reset_mock()
        
        # Ejecutar una instrucción
        self.computer.execute_next_instruction()
        
        # Verificar que se generaron notificaciones
        self.assertTrue(self.mock_observer.update.called)
        self.assertGreater(self.mock_observer.update.call_count, 0)
    
    def test_pc_progression_during_execution(self):
        """Test que el PC progresa correctamente durante la ejecución."""
        program = [
            "LOAD R1, 1",
            "LOAD R2, 2",
            "LOAD R3, 3",
            "HALT"
        ]
        
        self.computer.load_program(program)
        
        # Verificar PC inicial
        self.assertEqual(self.computer.pc_register.value, 0)
        
        # Ejecutar primera instrucción
        self.computer.execute_next_instruction()
        self.assertEqual(self.computer.pc_register.value, 1)
        
        # Ejecutar segunda instrucción
        self.computer.execute_next_instruction()
        self.assertEqual(self.computer.pc_register.value, 2)
        
        # Ejecutar tercera instrucción
        self.computer.execute_next_instruction()
        self.assertEqual(self.computer.pc_register.value, 3)
    
    def test_error_handling_during_execution(self):
        """Test manejo de errores durante la ejecución."""
        program = [
            "LOAD R1, 10",
            "DIV R1, 0, R2",  # División por cero - debe retornar 0 y establecer flag Z
            "HALT"
        ]
        
        self.computer.load_program(program)
        
        # Primera instrucción debe ejecutarse bien
        self.computer.execute_next_instruction()
        self.assertEqual(self.computer._register_bank.get("R1"), 10)
        
        # Segunda instrucción debe ejecutarse sin error (división por cero retorna 0)
        self.computer.execute_next_instruction()
        self.assertEqual(self.computer._register_bank.get("R2"), 0)  # Resultado de DIV por 0
        self.assertEqual(self.computer._alu.psw['Z'], 1)  # Flag Z debe estar establecido
    
    def test_reset_functionality(self):
        """Test funcionalidad de reset del sistema."""
        program = [
            "LOAD R1, 99",
            "STORE R1, 25",
            "HALT"
        ]
        
        # Ejecutar programa
        self.computer.load_program(program)
        self.computer.execute_next_instruction()  # LOAD
        self.computer.execute_next_instruction()  # STORE
        
        # Verificar que hay datos
        self.assertEqual(self.computer.register_bank.get_register("R1").value, 99)
        self.assertEqual(self.computer.memory.read(25), 99)
        self.assertEqual(self.computer.pc_register.value, 2)
        
        # Reset
        self.computer.reset()
        
        # Verificar que todo está limpio
        self.assertEqual(self.computer.register_bank.get_register("R1").value, 0)
        self.assertEqual(self.computer.memory.read(25), 0)
        self.assertEqual(self.computer.pc_register.value, 0)
        self.assertEqual(len(self.computer.loaded_program), 0)
    
    def test_concurrent_observer_notifications(self):
        """Test notificaciones concurrentes a observadores."""
        observers = []
        for i in range(5):
            observer = Mock()
            observer.update = Mock()  # Observer usa update, no notify
            observers.append(observer)
            self.computer.add_observer(observer)
        
        program = ["LOAD R1, 123", "HALT"]
        self.computer.load_program(program)
        self.computer.execute_next_instruction()
        
        # Verificar que todos los observadores fueron notificados
        for observer in observers:
            self.assertTrue(observer.update.called)
    
    def test_memory_boundary_conditions(self):
        """Test condiciones límite de memoria."""
        # Test acceso a límites de memoria
        program = [
            f"LOAD R1, 999",
            f"STORE R1, {self.computer.memory.size - 1}",  # Última posición válida
            "HALT"
        ]
        
        self.computer.load_program(program)
        
        # Debe ejecutarse sin error
        self.computer.execute_next_instruction()  # LOAD
        self.computer.execute_next_instruction()  # STORE
        
        # Verificar que se almacenó
        self.assertEqual(
            self.computer.memory.read(self.computer.memory.size - 1), 
            999
        )
    
    def test_register_bank_integration(self):
        """Test integración completa del banco de registros."""
        program = []
        
        # Cargar valores en todos los registros disponibles
        for i in range(1, 10):  # R1 a R9
            program.append(f"LOAD R{i}, {i * 10}")
        
        program.append("HALT")
        
        self.computer.load_program(program)
        
        # Ejecutar todas las cargas
        for i in range(9):  # 9 instrucciones LOAD
            self.computer.execute_next_instruction()
        
        # Verificar que todos los registros tienen los valores correctos
        for i in range(1, 10):
            register_value = self.computer.register_bank.get_register(f"R{i}").value
            expected_value = i * 10
            self.assertEqual(register_value, expected_value)
    
    def test_complex_program_with_loops_simulation(self):
        """Test programa complejo que simula un bucle."""
        # Programa que suma números del 1 al 5
        program = [
            "LOAD R1, 0",      # Contador (sum)
            "LOAD R2, 1",      # Valor actual
            "LOAD R3, 5",      # Límite
            "ADD R1, R2, R1",  # sum += current
            "ADD R2, 1, R2",   # current += 1
            # En un simulador real habría JMP condicional aquí
            # Por simplicidad, repetimos las operaciones
            "ADD R1, R2, R1",  # sum += current (current=2)
            "ADD R2, 1, R2",   # current += 1 (current=3)
            "ADD R1, R2, R1",  # sum += current (current=3)
            "ADD R2, 1, R2",   # current += 1 (current=4)
            "ADD R1, R2, R1",  # sum += current (current=4)
            "ADD R2, 1, R2",   # current += 1 (current=5)
            "ADD R1, R2, R1",  # sum += current (current=5)
            "STORE R1, 30",    # Guardar resultado
            "HALT"
        ]
        
        self.computer.load_program(program)
        
        # Ejecutar programa completo
        steps = 0
        while (self.computer.pc_register.value < len(self.computer.loaded_program) and 
               steps < 30):
            self.computer.execute_next_instruction()
            steps += 1
        
        # Verificar resultado (1+2+3+4+5 = 15)
        final_sum = self.computer.memory.read(30)
        self.assertEqual(final_sum, 15)


@patch('tkinter.Tk')
@patch('tkinter.Canvas')
@patch('tkinter.Text')
@patch('tkinter.Frame')
@patch('tkinter.Button')
@patch('tkinter.Label')
@patch('tkinter.Scrollbar')
@patch('tkinter.messagebox.showerror')
class TestMVCIntegration(unittest.TestCase):
    """Pruebas de integración MVC (simuladas sin GUI real)."""
    
    def setUp(self):
        """Configuración para pruebas MVC."""
        pass
    
    def test_mvc_component_creation(self, mock_showerror, mock_scrollbar, mock_label, mock_button, mock_frame, mock_text, mock_canvas, mock_tk):
        """Test creación de componentes MVC."""
        # Configurar mock root con atributos necesarios
        mock_root = Mock()
        mock_root.tk = Mock()
        mock_root._last_child_ids = {}
        mock_tk.return_value = mock_root
        
        # Configurar mocks de widgets
        mock_frame_instance = Mock()
        mock_frame_instance.tk = mock_root.tk
        mock_frame.return_value = mock_frame_instance
        
        # Importar componentes MVC
        from core.computer import Computer
        from gui.simulator_view import SimulatorView
        from gui.simulator_controller import SimulatorController
        
        # Crear componentes
        computer = Computer()
        view = SimulatorView(mock_root)
        controller = SimulatorController(view, computer)
        
        # Verificar que se crearon correctamente
        self.assertIsNotNone(computer)
        self.assertIsNotNone(view)
        self.assertIsNotNone(controller)
    
    def test_controller_model_communication(self, mock_showerror, mock_scrollbar, mock_label, mock_button, mock_frame, mock_text, mock_canvas, mock_tk):
        """Test comunicación entre Controller y Model."""
        # Configurar mock root con atributos necesarios
        mock_root = Mock()
        mock_root.tk = Mock()
        mock_root._last_child_ids = {}
        mock_tk.return_value = mock_root
        
        # Configurar mocks de widgets
        mock_frame_instance = Mock()
        mock_frame_instance.tk = mock_root.tk
        mock_frame.return_value = mock_frame_instance
        
        from core.computer import Computer
        from gui.simulator_view import SimulatorView
        from gui.simulator_controller import SimulatorController
        
        computer = Computer()
        view = SimulatorView(mock_root)
        controller = SimulatorController(view, computer)
        
        # Mock del programa de texto
        view.get_program_text = Mock(return_value="LOAD R1, 42\nHALT")
        
        # Test cargar programa
        controller.load_program()
        
        # Verificar que el programa se cargó en el modelo
        self.assertTrue(len(computer.loaded_program) > 0)
    
    def test_observer_pattern_mvc_integration(self, mock_showerror, mock_scrollbar, mock_label, mock_button, mock_frame, mock_text, mock_canvas, mock_tk):
        """Test integración del patrón Observer en MVC."""
        # Configurar mock root con atributos necesarios
        mock_root = Mock()
        mock_root.tk = Mock()
        mock_root._last_child_ids = {}
        mock_tk.return_value = mock_root
        
        # Configurar mocks de widgets
        mock_frame_instance = Mock()
        mock_frame_instance.tk = mock_root.tk
        mock_frame.return_value = mock_frame_instance
        
        from core.computer import Computer
        from gui.simulator_view import SimulatorView
        from gui.simulator_controller import SimulatorController
        
        computer = Computer()
        view = SimulatorView(mock_root)
        controller = SimulatorController(view, computer)
        
        # Verificar que la vista es observadora del modelo
        self.assertIn(view, computer._observers)


if __name__ == '__main__':
    # Ejecutar pruebas de integración
    unittest.main()