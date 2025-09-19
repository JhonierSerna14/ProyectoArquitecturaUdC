# Arquitectura MVC del Simulador de Computadora

## Descripción General

Este proyecto ha sido refactorizado para implementar una arquitectura **MVC (Model-View-Controller)** con **Observer Pattern**, mejorando significativamente la organización del código y la separación de responsabilidades.

## Estructura del Proyecto

```
ProyectoArquitecturaUdC-master/
├── main.py                      # Punto de entrada principal
├── core/                        # Núcleo del sistema
│   ├── __init__.py
│   ├── observer.py              # Patrón Observer
│   ├── exceptions.py            # Excepciones personalizadas
│   ├── instruction.py           # Representación de instrucciones
│   └── computer.py              # Modelo principal (MVC)
├── hardware/                    # Componentes de hardware refactorizados
│   ├── __init__.py
│   ├── register.py              # Registro individual
│   ├── register_bank.py         # Banco de registros
│   ├── alu.py                   # Unidad Aritmético-Lógica
│   ├── memory.py                # Sistema de memoria
│   ├── control_unit.py          # Unidad de control base
│   └── wired_control_unit.py    # Unidad de control cableada
├── gui/                         # Interfaz gráfica
│   ├── __init__.py
│   ├── simulator_view.py        # Vista del simulador (MVC)
│   └── simulator_controller.py  # Controlador (MVC)
├── utils/                       # Utilidades
│   ├── __init__.py
│   └── instruction_parser.py    # Parser de instrucciones
└── Class/                       # Implementación original (legacy)
    └── [archivos originales]
```

## Arquitectura MVC

### Modelo (Model)
- **Archivo**: `core/computer.py`
- **Responsabilidad**: Lógica de negocio del simulador
- **Funciones**:
  - Coordinar componentes de hardware
  - Gestionar estado del sistema
  - Ejecutar instrucciones
  - Notificar cambios a observadores

### Vista (View)
- **Archivo**: `gui/simulator_view.py`
- **Responsabilidad**: Interfaz gráfica de usuario
- **Funciones**:
  - Mostrar estado del sistema
  - Capturar entrada del usuario
  - Actualizar visualización
  - Observar cambios del modelo

### Controlador (Controller)
- **Archivo**: `gui/simulator_controller.py`
- **Responsabilidad**: Coordinar Modelo y Vista
- **Funciones**:
  - Procesar eventos de usuario
  - Actualizar el modelo
  - Gestionar flujo de ejecución
  - Manejar errores

## Patrón Observer

### Implementación
- **Observable**: `core/observer.py`
- **Beneficios**:
  - Desacoplamiento entre componentes
  - Comunicación asíncrona
  - Fácil extensibilidad
  - Mejor testabilidad

### Flujo de Comunicación
1. **Usuario** interactúa con la **Vista**
2. **Vista** notifica al **Controlador**
3. **Controlador** actualiza el **Modelo**
4. **Modelo** notifica cambios a observadores
5. **Vista** se actualiza automáticamente

## Mejoras Implementadas

### Organización del Código
- ✅ Separación clara de responsabilidades
- ✅ Módulos independientes y reutilizables
- ✅ Estructura de paquetes Python
- ✅ Documentación completa

### Patrones de Diseño
- ✅ MVC para separación de capas
- ✅ Observer para comunicación
- ✅ Strategy para diferentes tipos de instrucciones
- ✅ Factory para creación de componentes

### Manejo de Errores
- ✅ Excepciones personalizadas
- ✅ Validación de entrada
- ✅ Mensajes de error informativos
- ✅ Recuperación graceful

### Extensibilidad
- ✅ Fácil agregar nuevas instrucciones
- ✅ Componentes de hardware modulares
- ✅ Interfaces bien definidas
- ✅ Configuración flexible

## Cómo Ejecutar

```bash
# Navegar al directorio del proyecto
cd ProyectoArquitecturaUdC-master

# Ejecutar el simulador
python main.py
```

## Uso del Simulador

1. **Cargar Programa**: Escribir instrucciones en el área de texto
2. **Ejecutar**: Usar botones para ejecución completa o paso a paso
3. **Observar**: Ver cambios en registros, memoria y buses
4. **Resetear**: Limpiar el sistema para nuevo programa

## Ejemplo de Programa

```assembly
LOAD R1, 10      # Cargar valor 10 en R1
LOAD R2, 5       # Cargar valor 5 en R2
ADD R1, R2       # Sumar R1 + R2, resultado en R1
STORE R1, 100    # Guardar resultado en memoria[100]
HALT             # Detener ejecución
```

## Beneficios de la Refactorización

### Para Desarrolladores
- **Mantenibilidad**: Código más limpio y organizado
- **Testabilidad**: Componentes aislados fáciles de probar
- **Escalabilidad**: Fácil agregar nuevas funcionalidades
- **Legibilidad**: Estructura clara y documentada

### Para Usuarios
- **Estabilidad**: Mejor manejo de errores
- **Usabilidad**: Interfaz más responsive
- **Funcionalidad**: Más opciones de ejecución
- **Feedback**: Mejor información de estado

## Tecnologías Utilizadas

- **Python 3.8+**: Lenguaje principal
- **Tkinter**: Interfaz gráfica
- **Threading**: Ejecución asíncrona
- **Type Hints**: Tipado estático
- **Docstrings**: Documentación

## Próximas Mejoras

- [ ] Tests unitarios completos
- [ ] Serialización de estado
- [ ] Breakpoints en depuración
- [ ] Más tipos de instrucciones
- [ ] Modo de ejecución por tiempo
- [ ] Análisis de rendimiento
- [ ] Export/import de programas
- [ ] Temas visuales configurables

---

*Documentación actualizada para la versión 2.0 con arquitectura MVC*