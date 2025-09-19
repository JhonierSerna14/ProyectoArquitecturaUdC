"""
Vista principal del simulador usando arquitectura MVC.

Este módulo implementa la interfaz gráfica del simulador
separando la presentación de la lógica de negocio.
"""

import tkinter as tk
from tkinter import Canvas, Text, messagebox
from typing import Dict, Any, Optional
from core.observer import Observer, EventType


class SimulatorView(Observer):
    """
    Vista principal del simulador de computadora.
    
    Maneja toda la interfaz gráfica y recibe notificaciones
    del modelo usando el patrón Observer.
    """
    
    def __init__(self, root: tk.Tk):
        """
        Inicializa la vista del simulador.
        
        Args:
            root: Ventana principal de Tkinter
        """
        self.root = root
        
        # Referencias a elementos gráficos para actualización
        self._register_displays: Dict[str, int] = {}
        self._memory_text_id: Optional[int] = None
        self._control_signals_displays: Dict[str, int] = {}
        
        # Referencias a buses para animación
        self._bus_address_id: Optional[int] = None
        self._bus_data_id: Optional[int] = None
        self._bus_control_id: Optional[int] = None
        
        # Callback para comunicación con el controlador
        self._on_load_program_callback = None
        self._on_execute_program_callback = None
        self._on_step_execution_callback = None
        self._on_reset_callback = None
        
        # Configurar ventana y crear widgets
        self._setup_window()
        self._create_widgets()
        self._create_layout()
    
    def _setup_window(self) -> None:
        """Configura la ventana principal."""
        self.root.title("Simulador de Computadora - Arquitectura MVC")
        self.root.configure(bg="#2A629A")
        self.root.geometry("1300x750")
        self.root.resizable(True, True)
    
    def _create_widgets(self) -> None:
        """Crea todos los widgets de la interfaz."""
        # Canvas principal para la visualización
        self.canvas = Canvas(
            self.root, 
            width=1250, 
            height=500,
            bg="#2A829A", 
            highlightthickness=0
        )
        
        # Área de texto para instrucciones
        self.text_widget = Text(
            self.root, 
            height=5, 
            width=50, 
            bg="#D8BFD8", 
            fg="black", 
            font=("Arial", 12),
            wrap=tk.WORD
        )
        
        # Frame para botones
        button_frame = tk.Frame(self.root, bg="#2A629A")
        
        # Botones de control
        self.load_button = tk.Button(
            button_frame,
            text="Cargar Programa", 
            command=self._on_load_program,
            bg="#FF69B4", 
            fg="white", 
            font=("Arial", 12, "bold"),
            width=15
        )
        
        self.execute_button = tk.Button(
            button_frame,
            text="Ejecutar Todo", 
            command=self._on_execute_program,
            bg="#32CD32", 
            fg="white", 
            font=("Arial", 12, "bold"),
            width=15
        )
        
        self.step_button = tk.Button(
            button_frame,
            text="Paso a Paso", 
            command=self._on_step_execution,
            bg="#FFD700", 
            fg="black", 
            font=("Arial", 12, "bold"),
            width=15
        )
        
        self.reset_button = tk.Button(
            button_frame,
            text="Resetear", 
            command=self._on_reset,
            bg="#FF4500", 
            fg="white", 
            font=("Arial", 12, "bold"),
            width=15
        )
        
        # Label para estado del sistema
        self.status_label = tk.Label(
            self.root,
            text="Sistema Listo",
            bg="#2A629A",
            fg="white",
            font=("Arial", 10, "bold")
        )
        
        # Frame para información adicional
        self.info_frame = tk.Frame(self.root, bg="#2A629A")
        
        self.button_frame = button_frame
    
    def _create_layout(self) -> None:
        """Organiza los widgets en la ventana."""
        # Canvas principal
        self.canvas.pack(pady=10)
        
        # Área de texto
        tk.Label(
            self.root, 
            text="Programa (una instrucción por línea):", 
            bg="#2A629A", 
            fg="white", 
            font=("Arial", 12, "bold")
        ).pack()
        
        self.text_widget.pack(pady=5)
        
        # Botones
        self.button_frame.pack(pady=10)
        self.load_button.pack(side=tk.LEFT, padx=5)
        self.execute_button.pack(side=tk.LEFT, padx=5)
        self.step_button.pack(side=tk.LEFT, padx=5)
        self.reset_button.pack(side=tk.LEFT, padx=5)
        
        # Estado del sistema
        self.status_label.pack(pady=5)
        
        # Información adicional
        self.info_frame.pack(fill=tk.X, padx=10, pady=5)
        
        # Crear elementos gráficos en el canvas
        self._create_hardware_visualization()
    
    def _create_hardware_visualization(self) -> None:
        """Crea la visualización de los componentes de hardware."""
        # Registros especiales
        self._create_register_boxes()
        
        # Banco de registros
        self._create_register_bank_visualization()
        
        # Memoria
        self._create_memory_visualization()
        
        # Buses
        self._create_bus_visualization()
        
        # Señales de control
        self._create_control_signals_visualization()
        
        # ALU
        self._create_alu_visualization()
    
    def _create_register_boxes(self) -> None:
        """Crea las cajas de visualización para registros especiales."""
        # PC Register
        self.canvas.create_rectangle(170, 40, 250, 85, outline="white", width=2)
        self._register_displays["PC"] = self.canvas.create_text(
            210, 62, text="PC: 0", fill="white", font=("Arial", 12, "bold")
        )
        
        # MAR Register
        self.canvas.create_rectangle(70, 40, 150, 85, outline="white", width=2)
        self._register_displays["MAR"] = self.canvas.create_text(
            110, 62, text="MAR: 0", fill="white", font=("Arial", 12, "bold")
        )
        
        # IR Register
        self.canvas.create_rectangle(70, 105, 250, 165, outline="white", width=2)
        self._register_displays["IR"] = self.canvas.create_text(
            160, 135, text="IR: ", fill="white", font=("Arial", 12, "bold")
        )
        
        # MBR Register
        self.canvas.create_rectangle(70, 185, 250, 245, outline="white", width=2)
        self._register_displays["MBR"] = self.canvas.create_text(
            160, 215, text="MBR: 0", fill="white", font=("Arial", 12, "bold")
        )
        
        # ALU Result
        self.canvas.create_rectangle(70, 265, 250, 325, outline="white", width=2)
        self._register_displays["ALU"] = self.canvas.create_text(
            160, 295, text="ALU: 0", fill="white", font=("Arial", 12, "bold")
        )
        
        # PSW Register
        self.canvas.create_rectangle(70, 370, 430, 430, outline="white", width=2)
        self._register_displays["PSW"] = self.canvas.create_text(
            250, 400, text="PSW: Z: 0, C: 0, S: 0, O: 0", fill="white", font=("Arial", 12, "bold")
        )
    
    def _create_register_bank_visualization(self) -> None:
        """Crea la visualización del banco de registros."""
        self.canvas.create_rectangle(270, 40, 430, 350, outline="white", width=2)
        self.canvas.create_text(
            350, 25, text="Banco de Registros", fill="white", font=("Arial", 12, "bold")
        )
        
        # Crear displays para R1-R9
        for i in range(1, 10):
            y_pos = 60 + (i - 1) * 30
            reg_name = f"R{i}"
            self._register_displays[reg_name] = self.canvas.create_text(
                350, y_pos, text=f"{reg_name}: 0", fill="white", font=("Arial", 10, "bold")
            )
    
    def _create_memory_visualization(self) -> None:
        """Crea la visualización de la memoria."""
        # Rectángulo principal de memoria
        self.canvas.create_rectangle(630, 40, 990, 480, outline="white", width=2)
        
        # Línea divisoria entre instrucciones y datos
        self.canvas.create_line(810, 40, 810, 480, fill="white", width=2)
        
        # Títulos
        self.canvas.create_text(
            810, 20, text="Memoria Principal", fill="white", font=("Arial", 12, "bold")
        )
        self.canvas.create_text(
            720, 60, text="Instrucciones", fill="white", font=("Arial", 11, "bold")
        )
        self.canvas.create_text(
            900, 60, text="Datos", fill="white", font=("Arial", 11, "bold")
        )
        
        # Área de texto para mostrar contenido
        self._memory_text_id = self.canvas.create_text(
            650, 80, text="", fill="white", anchor="nw", font=("Arial", 10), width=150
        )
    
    def _create_bus_visualization(self) -> None:
        """Crea la visualización de los buses."""
        # Bus de direcciones
        self._bus_address_id = self.canvas.create_rectangle(
            450, 105, 600, 165, outline="white", width=2
        )
        self.canvas.create_text(
            525, 135, text="Bus de Direcciones", fill="white", font=("Arial", 10, "bold")
        )
        
        # Bus de datos
        self._bus_data_id = self.canvas.create_rectangle(
            450, 185, 600, 245, outline="white", width=2
        )
        self.canvas.create_text(
            525, 215, text="Bus de Datos", fill="white", font=("Arial", 10, "bold")
        )
        
        # Bus de control
        self._bus_control_id = self.canvas.create_rectangle(
            450, 265, 600, 325, outline="white", width=2
        )
        self.canvas.create_text(
            525, 295, text="Bus de Control", fill="white", font=("Arial", 10, "bold")
        )
    
    def _create_control_signals_visualization(self) -> None:
        """Crea la visualización de las señales de control."""
        signals = [
            'fetch', 'decode', 'execute', 'memory_read', 
            'memory_write', 'register_read', 'register_write', 'alu_operation'
        ]
        
        x_pos = 1050
        y_start = 60
        
        self.canvas.create_text(
            x_pos, 30, text="Señales de Control", fill="white", font=("Arial", 12, "bold")
        )
        
        for idx, signal in enumerate(signals):
            y_pos = y_start + idx * 30
            text_id = self.canvas.create_text(
                x_pos, y_pos, text=f"{signal}: Off", fill="red", 
                font=("Arial", 10, "bold"), anchor="w"
            )
            self._control_signals_displays[signal] = text_id
    
    def _create_alu_visualization(self) -> None:
        """Crea elementos adicionales para la ALU."""
        # Ya está incluido en los registros especiales
        pass
    
    def update(self, observable, event_type: str, data: Any = None) -> None:
        """
        Recibe notificaciones del modelo y actualiza la vista.
        
        Args:
            observable: Objeto que generó la notificación
            event_type: Tipo de evento
            data: Datos del evento
        """
        try:
            if event_type == EventType.REGISTER_VALUE_CHANGED:
                self._update_register_display(data)
                
            elif event_type == EventType.MEMORY_INSTRUCTION_LOADED:
                self._update_memory_display(data)
                
            elif event_type == EventType.ALU_OPERATION_EXECUTED:
                self._update_alu_display(data)
                
            elif event_type == EventType.ALU_FLAGS_UPDATED:
                self._update_psw_display(data)
                
            elif event_type == EventType.BUS_ADDRESS_ACTIVATED:
                self._animate_bus(self._bus_address_id, "blue")
                
            elif event_type == EventType.BUS_DATA_ACTIVATED:
                self._animate_bus(self._bus_data_id, "yellow")
                
            elif event_type == EventType.BUS_CONTROL_ACTIVATED:
                self._update_control_signals_display(data)
                self._animate_bus(self._bus_control_id, "green")
                
            elif event_type == EventType.SYSTEM_RESET:
                self._reset_all_displays()
                
            elif event_type == EventType.PROGRAM_LOADED:
                self._update_status(f"Programa cargado: {data['instruction_count']} instrucciones")
                
            elif event_type == EventType.EXECUTION_COMPLETED:
                self._update_status("Ejecución completada")
                
        except Exception as e:
            print(f"Error updating view: {e}")
    
    def _update_register_display(self, data: Dict[str, Any]) -> None:
        """Actualiza la visualización de un registro."""
        if 'data' in data and 'register_name' in data['data']:
            reg_name = data['data']['register_name']
            new_value = data['data']['new_value']
            
            if reg_name in self._register_displays:
                display_text = f"{reg_name}: {new_value}"
                self.canvas.itemconfig(
                    self._register_displays[reg_name], 
                    text=display_text
                )
    
    def _update_memory_display(self, data: Dict[str, Any]) -> None:
        """Actualiza la visualización de la memoria."""
        # Esta implementación se puede expandir para mostrar contenido específico
        pass
    
    def _update_alu_display(self, data: Dict[str, Any]) -> None:
        """Actualiza la visualización de la ALU."""
        if 'data' in data:
            alu_data = data['data']
            display_text = f"ALU: {alu_data.get('new_value', 0)}"
            if "ALU" in self._register_displays:
                self.canvas.itemconfig(
                    self._register_displays["ALU"], 
                    text=display_text
                )
    
    def _update_psw_display(self, data: Dict[str, Any]) -> None:
        """Actualiza la visualización del PSW."""
        if 'data' in data and 'psw' in data['data']:
            psw = data['data']['psw']
            psw_text = f"PSW: Z: {psw['Z']} C: {psw['C']} S: {psw['S']} O: {psw['O']}"
            if "PSW" in self._register_displays:
                self.canvas.itemconfig(
                    self._register_displays["PSW"], 
                    text=psw_text
                )
    
    def _update_control_signals_display(self, data: Dict[str, Any]) -> None:
        """Actualiza la visualización de señales de control."""
        if 'data' in data and 'new_signals' in data['data']:
            signals = data['data']['new_signals']
            
            for signal_name, signal_value in signals.items():
                if signal_name in self._control_signals_displays:
                    color = "green" if signal_value and signal_value != "Off" else "red"
                    text = f"{signal_name}: {'On' if signal_value and signal_value != 'Off' else 'Off'}"
                    
                    self.canvas.itemconfig(
                        self._control_signals_displays[signal_name],
                        text=text,
                        fill=color
                    )
    
    def _animate_bus(self, bus_id: int, color: str) -> None:
        """Anima un bus cambiando su color temporalmente."""
        if bus_id:
            self.canvas.itemconfig(bus_id, outline=color, width=3)
            self.root.after(500, lambda: self._reset_bus_color(bus_id))
    
    def _reset_bus_color(self, bus_id: int) -> None:
        """Resetea el color de un bus."""
        if bus_id:
            self.canvas.itemconfig(bus_id, outline="white", width=2)
    
    def _reset_all_displays(self) -> None:
        """Resetea todas las visualizaciones."""
        # Resetear registros
        for reg_name, display_id in self._register_displays.items():
            if reg_name.startswith('R'):
                self.canvas.itemconfig(display_id, text=f"{reg_name}: 0")
            elif reg_name == "PC":
                self.canvas.itemconfig(display_id, text="PC: 0")
            elif reg_name == "MAR":
                self.canvas.itemconfig(display_id, text="MAR: 0")
            elif reg_name == "IR":
                self.canvas.itemconfig(display_id, text="IR: ")
            elif reg_name == "MBR":
                self.canvas.itemconfig(display_id, text="MBR: 0")
            elif reg_name == "ALU":
                self.canvas.itemconfig(display_id, text="ALU: 0")
            elif reg_name == "PSW":
                self.canvas.itemconfig(display_id, text="PSW: Z: 0, C: 0, S: 0, O: 0")
        
        # Resetear señales de control
        for signal_name, display_id in self._control_signals_displays.items():
            self.canvas.itemconfig(display_id, text=f"{signal_name}: Off", fill="red")
        
        # Resetear memoria
        if self._memory_text_id:
            self.canvas.itemconfig(self._memory_text_id, text="")
        
        self._update_status("Sistema reseteado")
    
    def _update_status(self, message: str) -> None:
        """Actualiza el estado del sistema."""
        self.status_label.config(text=message)
    
    def get_program_text(self) -> str:
        """Obtiene el texto del programa ingresado."""
        return self.text_widget.get("1.0", tk.END).strip()
    
    def clear_program_text(self) -> None:
        """Limpia el área de texto del programa."""
        self.text_widget.delete("1.0", tk.END)
    
    def show_error(self, title: str, message: str) -> None:
        """Muestra un mensaje de error."""
        messagebox.showerror(title, message)
    
    def show_info(self, title: str, message: str) -> None:
        """Muestra un mensaje informativo."""
        messagebox.showinfo(title, message)
    
    # Métodos para configurar callbacks del controlador
    def set_load_program_callback(self, callback) -> None:
        """Configura el callback para cargar programa."""
        self._on_load_program_callback = callback
    
    def set_execute_program_callback(self, callback) -> None:
        """Configura el callback para ejecutar programa."""
        self._on_execute_program_callback = callback
    
    def set_step_execution_callback(self, callback) -> None:
        """Configura el callback para ejecución paso a paso."""
        self._on_step_execution_callback = callback
    
    def set_reset_callback(self, callback) -> None:
        """Configura el callback para resetear."""
        self._on_reset_callback = callback
    
    # Métodos de eventos internos
    def _on_load_program(self) -> None:
        """Maneja el evento de cargar programa."""
        if self._on_load_program_callback:
            self._on_load_program_callback()
    
    def _on_execute_program(self) -> None:
        """Maneja el evento de ejecutar programa."""
        if self._on_execute_program_callback:
            self._on_execute_program_callback()
    
    def _on_step_execution(self) -> None:
        """Maneja el evento de ejecución paso a paso."""
        if self._on_step_execution_callback:
            self._on_step_execution_callback()
    
    def _on_reset(self) -> None:
        """Maneja el evento de resetear."""
        if self._on_reset_callback:
            self._on_reset_callback()