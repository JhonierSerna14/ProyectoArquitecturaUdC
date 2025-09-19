"""
Controlador del simulador usando arquitectura MVC.

Este módulo implementa el controlador que coordina
la comunicación entre el modelo y la vista.
"""

from typing import List
import threading
import time
from core.computer import Computer
from core.exceptions import *
from gui.simulator_view import SimulatorView


class SimulatorController:
    """
    Controlador del simulador de computadora.
    
    Coordina la comunicación entre el modelo (Computer) y
    la vista (SimulatorView) siguiendo el patrón MVC.
    """
    
    def __init__(self, view: SimulatorView, computer: Computer):
        """
        Inicializa el controlador.
        
        Args:
            view: Vista del simulador
            computer: Modelo del simulador
        """
        self._view = view
        self._computer = computer
        
        # Configurar observadores
        self._computer.add_observer(self._view)
        
        # Configurar callbacks de la vista
        self._setup_view_callbacks()
        
        # Estado del controlador
        self._is_executing = False
        self._execution_thread = None
    
    def _setup_view_callbacks(self) -> None:
        """Configura los callbacks de la vista."""
        self._view.set_load_program_callback(self.load_program)
        self._view.set_execute_program_callback(self.execute_program)
        self._view.set_step_execution_callback(self.step_execution)
        self._view.set_reset_callback(self.reset_system)
    
    def load_program(self) -> None:
        """
        Carga un programa desde la vista al modelo.
        """
        try:
            # Obtener el texto del programa desde la vista
            program_text = self._view.get_program_text()
            
            if not program_text.strip():
                self._view.show_error("Error", "Por favor ingrese un programa")
                return
            
            # Dividir en líneas
            program_lines = [line.strip() for line in program_text.split('\n') if line.strip()]
            
            if not program_lines:
                self._view.show_error("Error", "El programa no contiene instrucciones válidas")
                return
            
            # Cargar en el modelo
            success = self._computer.load_program(program_lines)
            
            if success:
                self._view.show_info("Éxito", f"Programa cargado exitosamente\\n{len(program_lines)} instrucciones")
            
        except MemoryOverflowError as e:
            self._view.show_error("Error de Memoria", str(e))
        except InvalidInstructionError as e:
            self._view.show_error("Error de Instrucción", str(e))
        except Exception as e:
            self._view.show_error("Error", f"Error inesperado: {str(e)}")
    
    def execute_program(self) -> None:
        """
        Ejecuta el programa completo en un hilo separado.
        """
        if self._is_executing:
            self._view.show_info("Información", "Ya hay una ejecución en curso")
            return
        
        if not self._computer.loaded_program:
            self._view.show_error("Error", "No hay programa cargado. Cargue un programa primero.")
            return
        
        try:
            self._is_executing = True
            
            # Ejecutar en hilo separado para no bloquear la GUI
            self._execution_thread = threading.Thread(
                target=self._execute_program_thread,
                daemon=True
            )
            self._execution_thread.start()
            
        except Exception as e:
            self._is_executing = False
            self._view.show_error("Error de Ejecución", str(e))
    
    def _execute_program_thread(self) -> None:
        """
        Ejecuta el programa en un hilo separado con animaciones.
        """
        try:
            # Resetear antes de ejecutar
            self._computer.reset()
            
            # Recargar el programa
            program_lines = [line.strip() for line in self._view.get_program_text().split('\n') if line.strip()]
            self._computer.load_program(program_lines)
            
            # Ejecutar paso a paso con delays para visualización
            while self._computer.pc_register.value < len(self._computer.loaded_program):
                if not self._is_executing:  # Permitir cancelación
                    break
                
                # Ejecutar siguiente instrucción
                self._computer.execute_next_instruction()
                
                # Delay para visualización
                time.sleep(1.5)  # 1.5 segundos entre instrucciones
            
            self._is_executing = False
            
        except Exception as e:
            self._is_executing = False
            # Capturar el error para usarlo en la lambda
            error_message = str(e)
            # Programar mostrar error en el hilo principal
            self._view.root.after(0, lambda: self._view.show_error("Error de Ejecución", error_message))
    
    def step_execution(self) -> None:
        """
        Ejecuta la siguiente instrucción paso a paso.
        """
        if self._is_executing:
            self._view.show_info("Información", "Hay una ejecución automática en curso")
            return
        
        if not self._computer.loaded_program:
            self._view.show_error("Error", "No hay programa cargado. Cargue un programa primero.")
            return
        
        try:
            # Verificar si hay más instrucciones
            if self._computer.pc_register.value >= len(self._computer.loaded_program):
                self._view.show_info("Información", "Ejecución completada. No hay más instrucciones.")
                return
            
            # Ejecutar siguiente instrucción
            has_more = self._computer.execute_next_instruction()
            
            if not has_more:
                self._view.show_info("Información", "Ejecución completada.")
            
        except SimulatorError as e:
            self._view.show_error("Error de Simulación", str(e))
        except Exception as e:
            self._view.show_error("Error", f"Error inesperado: {str(e)}")
    
    def reset_system(self) -> None:
        """
        Resetea el sistema completo.
        """
        try:
            # Detener ejecución si está en curso
            if self._is_executing:
                self._is_executing = False
                if self._execution_thread and self._execution_thread.is_alive():
                    self._execution_thread.join(timeout=1.0)
            
            # Resetear el modelo
            self._computer.reset()
            
            # Limpiar la vista
            self._view.clear_program_text()
            
            self._view.show_info("Información", "Sistema reseteado exitosamente")
            
        except Exception as e:
            self._view.show_error("Error", f"Error al resetear: {str(e)}")
    
    def stop_execution(self) -> None:
        """
        Detiene la ejecución automática.
        """
        if self._is_executing:
            self._is_executing = False
            self._computer.halt()
            
            if self._execution_thread and self._execution_thread.is_alive():
                self._execution_thread.join(timeout=2.0)
    
    def get_system_state(self) -> dict:
        """
        Obtiene el estado actual del sistema.
        
        Returns:
            Diccionario con el estado del sistema
        """
        return self._computer.get_system_state()
    
    def is_executing(self) -> bool:
        """
        Verifica si hay una ejecución en curso.
        
        Returns:
            True si está ejecutando
        """
        return self._is_executing
    
    def cleanup(self) -> None:
        """
        Limpia recursos del controlador.
        """
        self.stop_execution()
        
        # Remover observadores
        self._computer.remove_observer(self._view)