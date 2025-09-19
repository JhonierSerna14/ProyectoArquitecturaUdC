"""
Simulador de Computadora - Proyecto Final Arquitectura de Computadores

Este módulo principal inicializa y ejecuta el simulador de computadora con interfaz gráfica.
El simulador implementa los componentes básicos de una arquitectura de computadora:
- ALU (Unidad Aritmético-Lógica)
- Unidad de Control
- Memoria (instrucciones y datos)
- Banco de Registros
- Registros especiales (PC, MAR, IR, MBR, PSW)

Autor: Proyecto Universidad de Córdoba
Versión: 1.0
"""

import tkinter as tk
import sys
import os

from Class.ComputerSimulator import ComputerSimulator


def configure_tcl_tk_libraries():
    """
    Configura las librerías Tcl/Tk para resolver problemas de compatibilidad en Windows.
    
    Esta función es necesaria para Python 3.13+ en Windows, donde pueden existir
    conflictos con las rutas de las librerías Tcl/Tk.
    """
    if sys.platform != "win32":
        return
        
    # Rutas posibles donde pueden estar las librerías Tcl/Tk
    possible_paths = [
        os.path.dirname(os.path.dirname(sys.executable)),  # Python del sistema
    ]
    
    # Si estamos en un entorno virtual, buscar el Python original
    if hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix):
        possible_paths.append(sys.base_prefix)
    
    # Buscar y configurar las librerías Tcl/Tk
    for base_python in possible_paths:
        tcl_dir = os.path.join(base_python, 'tcl')
        tcl8_6_dir = os.path.join(tcl_dir, 'tcl8.6')
        tk8_6_dir = os.path.join(tcl_dir, 'tk8.6')
        
        if os.path.exists(tcl8_6_dir) and os.path.exists(tk8_6_dir):
            os.environ['TCL_LIBRARY'] = tcl8_6_dir
            os.environ['TK_LIBRARY'] = tk8_6_dir
            print(f"Configuradas librerías Tcl/Tk desde: {tcl_dir}")
            break


def main():
    """
    Función principal que inicializa y ejecuta el simulador de computadora.
    
    Configura la ventana principal de Tkinter y crea una instancia del
    simulador de computadora con las dimensiones apropiadas.
    """
    # Configurar librerías Tcl/Tk si es necesario
    configure_tcl_tk_libraries()
    
    # Crear y configurar la ventana principal
    root = tk.Tk()
    root.geometry("1300x750")
    root.title("Simulador de Computadora - UdC")
    
    # Inicializar el simulador
    app = ComputerSimulator(root)
    
    # Iniciar el bucle principal de la interfaz gráfica
    root.mainloop()


if __name__ == '__main__':
    main()
