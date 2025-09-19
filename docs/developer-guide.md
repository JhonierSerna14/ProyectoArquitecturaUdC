# Guía del Desarrollador

Documentación técnica para desarrolladores que contribuyen al proyecto

## � Características Principales (v3.0)

### ✨ Nuevas Funcionalidades
- **Instrucciones de 3 operandos**: `ADD R1, R2, R3` (fuente1, fuente2, destino)
- **Memoria de 32 bits**: 16 instrucciones + 16 datos (0-15, 16-31)
- **Sintaxis LOAD avanzada**: `LOAD R1, *18` (dirección directa), `LOAD R1, *R2` (indirecto)
- **División por cero segura**: Retorna 0 y establece flag Z
- **Patrón Observer corregido**: Método `update()` estándar
- **Validación robusta**: Rangos y direcciones de memoria

## �🛠️ Setup del Entorno de Desarrollo

### Requisitos
- Python 3.8+
- Git
- IDE recomendado: VS Code

### Instalación para Desarrollo
```bash
# Clonar el repositorio
git clone https://github.com/JhonierSerna14/ProyectoArquitecturaUdC.git
cd ProyectoArquitecturaUdC

# Crear entorno virtual
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
# .venv\Scripts\activate   # Windows

# Instalar dependencias de desarrollo
pip install -r requirements-dev.txt
```

## 🏗️ Arquitectura del Código

### Patrón MVC Implementado
```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│     Model       │    │   Controller    │    │      View       │
│  (core/*)       │◄───┤ (gui/controller)│───►│   (gui/view)    │
│                 │    │                 │    │                 │
│ - Computer      │    │ - Event Handler │    │ - GUI Components│
│ - Components    │    │ - State Manager │    │ - Visualization │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

### Estructura de Módulos
- **`core/`**: Lógica de negocio
  - `computer.py`: Orquestador principal con soporte 3-operandos
  - `instruction.py`: Definición de instrucciones (HALT incluido)
  - `exceptions.py`: Manejo de errores personalizado
- **`hardware/`**: Componentes de hardware
  - `alu.py`: ALU con división segura y validación de rangos
  - `memory.py`: Memoria 32-bits con áreas separadas
  - `register_bank.py`: Banco de registros R1-R9
  - `control_unit.py`: Unidad de control con 3-operandos
- **`gui/`**: Interfaz gráfica (MVC)
- **`utils/`**: Utilidades y helpers
  - `instruction_parser.py`: Parser avanzado con validación
- **`tests/`**: Suite de pruebas (191 tests)
- **`examples/`**: Ejemplos actualizados con nueva sintaxis

## 🧪 Testing y Calidad

### Ejecutar Pruebas
```bash
# Todas las pruebas
python scripts/testing/run_all_tests.py

# Solo unitarias
python scripts/testing/run_tests.py

# Análisis de código
flake8 .
black --check .
mypy .
```

### Estándares de Calidad
- **Linting**: flake8 compliant
- **Formato**: black style
- **Type hints**: mypy compatible

## 📝 Convenciones de Código

### Estilo Python
```python
# Nombres de clases: PascalCase
class RegisterBank:
    pass

# Nombres de funciones: snake_case
def execute_instruction():
    pass

# Constantes: UPPER_CASE
MAX_REGISTERS = 9

# Variables privadas: _underscore
def _internal_method():
    pass
```

### Documentación
```python
def add_operation(self, operand1: int, operand2: int) -> int:
    """
    Ejecuta operación de suma en la ALU.
    
    Args:
        operand1: Primer operando
        operand2: Segundo operando
        
    Returns:
        Resultado de la suma
        
    Raises:
        Raises:
        ALUOperationError: Si hay error en la operación
    """

## 🎯 Instrucciones Soportadas

### Aritméticas (3 Operandos)
```python
# Formato: OPERACION fuente1, fuente2, destino
"ADD R1, R2, R3"    # R3 = R1 + R2
"SUB R4, R5, R6"    # R6 = R4 - R5
"MUL R7, R8, R9"    # R9 = R7 * R8
"DIV R1, R2, R3"    # R3 = R1 / R2 (división por 0 = 0)
```

### Lógicas (2-3 Operandos)
```python
"AND R1, R2, R3"    # R3 = R1 AND R2
"OR R1, R2, R3"     # R3 = R1 OR R2
"XOR R1, R2, R3"    # R3 = R1 XOR R2
"NOT R1, R2"        # R2 = NOT R1 (2 operandos)
```

### Memoria
```python
"LOAD R1, 100"      # Carga inmediata
"LOAD R1, *18"      # Carga desde memoria[18]
"LOAD R1, *R2"      # Carga indirecta desde memoria[R2]
"STORE R1, 18"      # Guarda R1 en memoria[18]
```

### Control
```python
"JP 5"              # Salto incondicional
"JPZ 0, R1"         # Salto si R1 = 0
"HALT"              # Terminar programa
```

## 🧠 Arquitectura de Memoria

### Distribución (32 bits total)
```
Direcciones 0-15:  Área de instrucciones
Direcciones 16-31: Área de datos
```

### Validaciones
- **Instrucciones**: Solo pueden escribirse en 0-15
- **Datos**: Solo pueden accederse en 16-31
- **Fuera de rango**: Genera `MemoryOverflowError`
    """
    pass
```

## 🔄 Workflow de Desarrollo

### 1. Crear Feature Branch
```bash
git checkout -b feature/nueva-funcionalidad
```

### 2. Desarrollo
- Escribir código siguiendo convenciones
- Añadir tests para nueva funcionalidad
- Actualizar documentación si es necesario

### 3. Testing
```bash
# Ejecutar pruebas localmente
python scripts/testing/run_all_tests.py

# Verificar calidad de código
flake8 .
black .
```

### 4. Commit y Push
```bash
git add .
git commit -m "feat: agregar nueva funcionalidad X"
git push origin feature/nueva-funcionalidad
```

### 5. Pull Request
- Crear PR con descripción clara
- Asegurar que todas las pruebas pasen
- Solicitar revisión de código

## 🏗️ Extensibilidad

### Agregar Nueva Instrucción
1. **Definir en `core/instruction.py`**
2. **Implementar en `hardware/alu.py`**
3. **Añadir parser en `utils/instruction_parser.py`**
4. **Crear tests en `tests/unit/`**

### Agregar Nuevo Componente
1. **Crear módulo en `hardware/`**
2. **Implementar interfaces apropiadas**
3. **Integrar con `core/computer.py`**
4. **Añadir visualización en `gui/`**

## 📊 Métricas y Monitoreo

### Métricas de Calidad
- **Cobertura de código**: >85%
- **Complejidad ciclomática**: <10 por función
- **Duplicación de código**: <3%
- **Deuda técnica**: Monitoreada semanalmente

### Herramientas de Análisis
- **pytest-cov**: Cobertura de código
- **flake8**: Linting
- **mypy**: Type checking
- **bandit**: Análisis de seguridad

## 🚀 Despliegue

### Build Local
```bash
# Generar distribución
python setup.py sdist bdist_wheel

# Verificar instalación
pip install dist/simulador-*.whl
```

### CI/CD Pipeline
- **Tests automáticos** en cada push
- **Análisis de calidad** en PRs
- **Build automático** en releases
- **Documentación** auto-generada

## 📚 Recursos Adicionales

- [API Reference](api-reference.md)
- [Arquitectura del Sistema](architecture.md)
- [Convenciones del Proyecto](CONVENTIONS.md)
- [Troubleshooting](troubleshooting.md)