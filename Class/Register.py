"""
Registro individual del simulador de computadora.

Este módulo implementa un registro que puede almacenar un valor
y mostrarlo en la interfaz gráfica.
"""


class Register:
    """
    Representa un registro individual en la computadora simulada.
    
    Cada registro tiene un nombre identificativo, almacena un valor
    y se muestra visualmente en el canvas de la interfaz gráfica.
    
    Attributes:
        value: Valor actual almacenado en el registro
        canvas: Canvas de tkinter donde se muestra el registro
        x, y: Coordenadas de posición en el canvas
        name: Nombre identificativo del registro
        text_id: ID del texto en el canvas para actualización
    """
    def __init__(self, canvas, x, y, name):
        """
        Inicializa un registro con su posición y representación visual.
        
        Args:
            canvas: Canvas de tkinter donde se mostrará el registro
            x (int): Coordenada X de posición en el canvas
            y (int): Coordenada Y de posición en el canvas
            name (str): Nombre identificativo del registro
        """
        self.value = 0
        self.canvas = canvas
        self.x = x
        self.y = y
        self.name = name
        # Crea un texto en el lienzo para representar el valor del registro.
        self.text_id = canvas.create_text(x + 50, y + 15, text=f"{name}: {self.value}", fill="white",
                                          font=("Arial", 12, "bold"))

    def set_value(self, value):
        """
        Establece un nuevo valor en el registro y actualiza la visualización.
        
        Args:
            value: Nuevo valor a almacenar en el registro
        """
        self.value = value
        self.canvas.itemconfig(self.text_id, text=f"{self.name}: {self.value}")
