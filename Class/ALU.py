"""
Unidad Aritmético-Lógica (ALU) del simulador de computadora.

Este módulo implementa la ALU que realiza operaciones aritméticas y lógicas,
además de mantener los flags del registro de estado PSW.
"""


class ALU:
    """
    Unidad Aritmético-Lógica (ALU) que ejecuta operaciones aritméticas y lógicas.
    
    La ALU es responsable de:
    - Realizar operaciones aritméticas (ADD, SUB, MUL, DIV)
    - Realizar operaciones lógicas (AND, OR, NOT, XOR)
    - Manejar operaciones de salto (JP, JPZ)
    - Actualizar los flags del registro PSW (Program Status Word)
    
    Attributes:
        value (int): Resultado de la última operación ejecutada
        psw (dict): Registro de estado con flags Z, C, S, O
    """
    def __init__(self):
        """
        Inicializa la ALU con valor cero y flags del PSW en estado inicial.
        
        Los flags del PSW son:
        - Z (Zero): Se activa cuando el resultado es cero
        - C (Carry): Se activa en desbordamiento o acarreo
        - S (Sign): Se activa cuando el resultado es negativo
        - O (Overflow): Se activa en desbordamiento aritmético
        """
        self.value = 0
        self.psw = {
            'Z': 0,  # Zero flag
            'C': 0,  # Carry flag
            'S': 0,  # Sign(+/-) flag
            'O': 0  # Overflow flag
        }

    def execute(self, opcode, operand1, operand2):
        """
        Ejecuta una operación aritmética o lógica basada en el opcode.
        
        Args:
            opcode (str): Código de operación ('ADD', 'SUB', 'MUL', 'DIV', 
                         'AND', 'OR', 'NOT', 'XOR', 'JP', 'JPZ')
            operand1 (int): Primer operando para la operación
            operand2 (int): Segundo operando para la operación
            
        Raises:
            ValueError: Si los operandos están fuera del rango válido
            
        Note:
            El rango válido para operandos es [-16384, 16383] (15 bits + signo)
            Actualiza automáticamente los flags del PSW después de cada operación
        """
        if (operand1 > 0x3FFF or operand1 < -
           0x4000 or operand2 > 0x3FFF or operand2 < -0x4000):
            self.psw['O'] = 1
            raise ValueError('Operands out of range')
        else:
            if opcode == 'ADD':
                self.value = operand1 + operand2
                self.psw['C'] = int(self.value > 0x3FFF)
                self.psw['O'] = int(((operand1 & 0x2000) == (operand2 & 0x2000)) and (
                    (self.value & 0x2000) != (operand1 & 0x2000)))
            elif opcode == 'SUB':
                self.value = operand1 - operand2
                self.psw['C'] = int(operand1 < operand2)
                self.psw['O'] = int(((operand1 & 0x2000) != (operand2 & 0x2000)) and (
                    (self.value & 0x2000) != (operand1 & 0x2000)))
            elif opcode == 'MUL':
                self.value = operand1 * operand2
                self.psw['C'] = int(self.value > 0x3FFF)
            elif opcode == 'DIV':
                if operand2 == 0:
                    self.value = 0
                    self.psw['Z'] = 1
                else:
                    self.value = operand1 // operand2
            elif opcode == 'AND':
                self.value = operand1 & operand2
            elif opcode == 'OR':
                self.value = operand1 | operand2
            elif opcode == 'NOT':
                self.value = ~operand2
            elif opcode == 'XOR':
                self.value = operand1 ^ operand2
            elif opcode == 'JP':
                self.value = operand1
            elif opcode == 'JPZ':
                self.value = operand1 if operand2 == 0 else None

        # Actualiza los flags del PSW basados en el resultado
        self.psw['Z'] = int(self.value == 0)
        self.psw['S'] = int(self.value < 0)

    def get_psw(self):
        """
        Obtiene el estado actual del registro PSW.
        
        Returns:
            dict: Diccionario con los flags Z, C, S, O del PSW
        """
        return self.psw
