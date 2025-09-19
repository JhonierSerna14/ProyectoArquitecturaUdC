"""
Banco de Registros del simulador de computadora.

Este módulo implementa un conjunto de registros numerados (R1-R9)
que pueden ser accedidos y modificados durante la ejecución de programas.
"""

from Class.Register import Register


class RegisterBank:
    """
    Banco de registros que gestiona múltiples registros numerados.
    
    Proporciona una interfaz unificada para acceder y modificar
    los registros R1 através R9 utilizados en las instrucciones.
    
    Attributes:
        registers (dict): Diccionario de registros indexados por nombre
    """
    def __init__(self, canvas, x, y):
        """
        Inicializa el banco de registros con 9 registros (R1-R9).
        
        Args:
            canvas: Canvas de tkinter donde se mostrarán los registros
            x (int): Coordenada X base para posicionar los registros
            y (int): Coordenada Y base para posicionar los registros
        """
        # Crea una serie de registros numerados y los almacena en un diccionario.
        self.registers = {f'R{i}': Register(canvas, x, y + i * 30, f'R{i}') for i in range(1, 10)}

    def get(self, reg_name):
        """
        Obtiene el valor almacenado en un registro específico.
        
        Args:
            reg_name (str): Nombre del registro (ej: 'R1', 'R2', etc.)
            
        Returns:
            int: Valor almacenado en el registro
            
        Raises:
            KeyError: Si el registro especificado no existe
        """
        if reg_name not in self.registers:
            raise KeyError(f"Register {reg_name} not found")
        return self.registers[reg_name].value

    def set(self, reg_name, value):
        """
        Establece un valor en un registro específico.
        
        Args:
            reg_name (str): Nombre del registro (ej: 'R1', 'R2', etc.)
            value (int): Valor a almacenar en el registro
            
        Raises:
            KeyError: Si el registro especificado no existe
        """
        if reg_name not in self.registers:
            raise KeyError(f"Register {reg_name} not found")
        self.registers[reg_name].set_value(value)

    def clear_registers(self):
        """
        Limpia todos los registros estableciendo su valor a cero.
        """
        for register in self.registers.values():
            register.set_value(0)
