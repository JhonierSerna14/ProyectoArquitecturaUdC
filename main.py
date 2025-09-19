"""
Simulador de Computadora - Proyecto Final Arquitectura de Computadores

Este módulo principal inicializa y ejecuta el simulador de computadora con interfaz gráfica
usando arquitectura MVC. El simulador implementa los componentes básicos de una arquitectura 
de computadora:
- ALU (Unidad Aritmético-Lógica) con operaciones de 3 operandos
- Unidad de Control con soporte para instrucciones complejas  
- Memoria de 32 bits (16 instrucciones + 16 datos)
- Banco de Registros (R1-R9)
- Registros especiales (PC, MAR, IR, MBR, PSW)

CARACTERÍSTICAS PRINCIPALES:
✅ Instrucciones de 3 operandos: ADD R1, R2, R3 (src1, src2, dest)
✅ Carga inmediata vs memoria: LOAD R1, 10 vs LOAD R1, *18
✅ División por cero segura (retorna 0, establece flag Z)
✅ Sintaxis mejorada para NOT: NOT R1, R2 (fuente, destino)
✅ Direccionamiento indirecto: *R1 y *dirección
✅ Patrón Observer para comunicación entre componentes

Arquitectura: MVC (Model-View-Controller) + Observer Pattern

Autor: Proyecto Universidad de Caldas
Versión: 3.0 - Instrucciones 3-operandos + Memoria 32-bits
"""

import tkinter as tk
import sys
import os

# Agregar el directorio raíz al path para imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from core.computer import Computer
from gui.simulator_view import SimulatorView
from gui.simulator_controller import SimulatorController


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
    Función principal que inicializa y ejecuta el simulador usando arquitectura MVC.
    
    Crea los componentes del patrón MVC (Model-View-Controller) y 
    configura la comunicación entre ellos usando el patrón Observer.
    """
    # Configurar librerías Tcl/Tk si es necesario
    configure_tcl_tk_libraries()
    
    try:
        # Crear la ventana principal
        root = tk.Tk()
        root.title("Simulador de Computadora - UdC (MVC)")
        root.geometry("1300x750")
        
        # Configurar el cierre de la aplicación
        def on_closing():
            try:
                controller.cleanup()
            except:
                pass
            root.destroy()
        
        root.protocol("WM_DELETE_WINDOW", on_closing)
        
        # Crear componentes MVC
        print("Inicializando simulador con arquitectura MVC...")
        
        # Modelo: Computer
        computer = Computer()
        print("✓ Modelo (Computer) creado")
        
        # Vista: SimulatorView
        view = SimulatorView(root)
        print("✓ Vista (SimulatorView) creada")
        
        # Controlador: SimulatorController
        controller = SimulatorController(view, computer)
        print("✓ Controlador (SimulatorController) creado")
        
        print("\n=== Simulador de Computadora ===")
        print("Arquitectura: MVC + Observer Pattern")
        print("Estado: Listo para usar")
        print("=====================================\n")
        
        # Ejecutar la aplicación
        root.mainloop()
        
    except ImportError as e:
        print(f"Error de importación: {e}")
        print("Asegúrese de que todos los módulos están disponibles")
        return 1
    except Exception as e:
        print(f"Error inesperado: {e}")
        return 1
    
    return 0


if __name__ == '__main__':
    exit_code = main()
    sys.exit(exit_code)
