"""
Configuración de pruebas para el simulador de computadora.

Este módulo inicializa el entorno de pruebas y proporciona
fixtures comunes para todos los tests.
"""

import sys
import os

# Agregar el directorio raíz al path para imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))