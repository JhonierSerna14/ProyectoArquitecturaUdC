# Guía de Testing para el Simulador de Computadora

## Visión General

Este documento describe la estrategia de testing implementada para el simulador de computadora con arquitectura MVC. Se utilizan técnicas avanzadas de testing incluyendo **partición equivalente**, **análisis de cobertura** y **pruebas de integración**.

## Estructura de Testing

```
tests/
├── __init__.py                 # Configuración base
├── unit/                       # Pruebas unitarias
│   ├── test_observer.py        # Patrón Observer
│   ├── test_exceptions.py      # Excepciones personalizadas
│   ├── test_instruction.py     # Representación de instrucciones
│   ├── test_register.py        # Registros individuales
│   ├── test_alu.py            # Unidad Aritmético-Lógica
│   ├── test_memory.py         # Sistema de memoria
│   └── test_computer.py       # Modelo principal
├── integration/                # Pruebas de integración
│   └── test_full_system.py    # Sistema completo MVC
└── fixtures/                   # Datos de prueba
```

## Técnicas de Testing Aplicadas

### 1. Partición Equivalente

**Definición**: Técnica que divide el dominio de entrada en clases equivalentes donde todos los valores de una clase se comportan de manera similar.

#### Ejemplo: Registro de Valores
```python
# Partición 1: Valores válidos positivos
[1, 50, 255, 1000, 65535]

# Partición 2: Valor cero (caso límite)
[0]

# Partición 3: Valores negativos
[-1, -100, -999999]

# Partición 4: Valores extremos
[MAX_INT, MIN_INT]
```

#### Ejemplo: Operaciones ALU
```python
# Partición 1: Operaciones aritméticas válidas
ADD, SUB, MUL, DIV con operandos normales

# Partición 2: Casos límite
División por cero, overflow, underflow

# Partición 3: Operaciones lógicas
AND, OR, NOT, XOR con diferentes patrones de bits
```

### 2. Análisis de Calidad

**Objetivo**: Mantener alta calidad de código con pruebas exhaustivas.

#### Tipos de Validación:
- **Sintaxis**: Verificación de sintaxis correcta
- **Lógica**: Validación de comportamiento esperado
- **Edge Cases**: Casos límite identificados y probados
- **Integración**: Interacción entre componentes

### 3. Casos de Prueba por Módulo

#### Core Module (`core/`)

**Observer Pattern (`test_observer.py`)**:
- ✅ Adición/eliminación de observadores válidos
- ✅ Manejo de observadores inválidos (None, sin notify)
- ✅ Notificación a múltiples observadores
- ✅ Manejo de excepciones en observadores

**Exceptions (`test_exceptions.py`)**:
- ✅ Jerarquía de excepciones correcta
- ✅ Mensajes de error informativos
- ✅ Casos límite (mensajes vacíos, None)
- ✅ Excepciones específicas por tipo de error

**Instructions (`test_instruction.py`)**:
- ✅ Creación de instrucciones válidas por tipo
- ✅ Operandos opcionales y requeridos
- ✅ Representación string correcta
- ✅ Validación de tipos de instrucción

#### Hardware Module (`hardware/`)

**Register (`test_register.py`)**:
- ✅ Asignación/lectura de valores
- ✅ Notificación de cambios a observadores
- ✅ Valores límite (0, máximos, negativos)
- ✅ Inmutabilidad del nombre

**ALU (`test_alu.py`)**:
- ✅ Operaciones aritméticas (ADD, SUB, MUL, DIV)
- ✅ Operaciones lógicas (AND, OR, NOT, XOR)
- ✅ Manejo de errores (división por cero)
- ✅ Gestión de flags PSW (Zero, Sign, Carry)

#### Integration Tests (`integration/`)

**Sistema Completo (`test_full_system.py`)**:
- ✅ Ejecución de programas completos
- ✅ Coordinación entre componentes
- ✅ Progresión del PC
- ✅ Comunicación Observer entre MVC

## Ejecución de Pruebas

### Instalación de Dependencias
```bash
pip install -r requirements-test.txt
```

### Comandos de Testing

```bash
# Ejecutar todas las pruebas
pytest

# Ejecutar con cobertura
pytest --cov=core --cov=hardware --cov=gui --cov=utils

# Ejecutar solo pruebas unitarias
pytest tests/unit/ -v

# Ejecutar solo pruebas de integración
pytest tests/integration/ -v

# Generar reporte HTML de cobertura
pytest --cov-report=html

# Ejecutar pruebas específicas
pytest tests/unit/test_observer.py::TestObservable::test_add_valid_observer
```

### Marcadores de Pruebas

```bash
# Ejecutar solo pruebas unitarias
pytest -m unit

# Ejecutar solo pruebas de integración
pytest -m integration

# Ejecutar pruebas lentas
pytest -m slow

# Ejecutar pruebas de GUI
pytest -m gui
```

## Métricas de Calidad

### Cobertura Objetivo por Módulo

| Módulo | Cobertura Mínima | Cobertura Objetivo |
|--------|------------------|-------------------|
| core/ | 90% | 95% |
| hardware/ | 85% | 92% |
| gui/ | 70% | 85% |
| utils/ | 90% | 95% |

### Estadísticas de Pruebas

- **Pruebas Unitarias**: 150+ test cases
- **Pruebas de Integración**: 20+ test cases
- **Particiones Equivalentes**: 40+ particiones identificadas
- **Casos Límite**: 60+ casos de borde
- **Tiempo de Ejecución**: <30 segundos

## Casos de Prueba por Partición Equivalente

### Registros
```python
# Partición 1: Valores válidos normales
test_set_valid_positive_value()
test_set_multiple_valid_values()

# Partición 2: Valores límite
test_set_zero_value()
test_set_maximum_16bit_value()

# Partición 3: Valores especiales
test_set_negative_value()
test_boundary_values()
```

### ALU Operations
```python
# Partición 1: Aritmética válida
test_add_positive_numbers()
test_subtract_positive_numbers()
test_multiply_positive_numbers()

# Partición 2: Casos límite
test_divide_by_zero_raises_error()
test_add_with_zero()

# Partición 3: Operaciones lógicas
test_and_operation()
test_or_operation()
test_xor_operation()
```

### Instrucciones
```python
# Partición 1: Instrucciones válidas por tipo
test_arithmetic_instructions()
test_memory_instructions()
test_control_instructions()

# Partición 2: Operandos
test_instruction_with_one_operand()
test_instruction_with_three_operands()

# Partición 3: Casos límite
test_instruction_with_zero_operand()
test_instruction_with_negative_operand()
```

## Automatización y CI/CD

### GitHub Actions (Futuro)
```yaml
name: Testing
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Setup Python
        uses: actions/setup-python@v2
        with:
          python-version: 3.8
      - name: Install dependencies
        run: pip install -r requirements-test.txt
      - name: Run tests
        run: pytest --cov --cov-fail-under=85
```

### Pre-commit Hooks
```bash
# Instalar pre-commit
pip install pre-commit

# Configurar hooks para ejecutar tests antes de commit
pre-commit install
```

## Análisis de Resultados

### Reporte de Pruebas
- **Terminal Output**: Muestra resultados detallados
- **XML Report**: Para integración con CI/CD

### Identificación de Problemas
```bash
# Ver detalles de pruebas fallidas
pytest -v

# Generar reporte detallado
python scripts/testing/run_tests.py
```

## Mejores Prácticas Implementadas

### 1. Nomenclatura Consistente
- `test_<functionality>_<scenario>()`
- Nombres descriptivos que explican el propósito

### 2. Estructura AAA (Arrange-Act-Assert)
```python
def test_add_positive_numbers(self):
    # Arrange
    alu = ALU()
    
    # Act
    result = alu.add(10, 5)
    
    # Assert
    self.assertEqual(result, 15)
```

### 3. Fixtures y Setup
- `setUp()` común para inicialización
- Mocks para dependencias externas
- Datos de prueba reutilizables

### 4. Aislamiento de Pruebas
- Cada test es independiente
- Sin dependencias entre tests
- Limpieza automática entre tests

## Debugging y Troubleshooting

### Ejecución de Tests Individuales
```bash
# Test específico con verbose
pytest tests/unit/test_alu.py::TestALU::test_add_positive_numbers -v -s

# Mostrar output completo
pytest --tb=long

# Parar en primer fallo
pytest -x
```

### Análisis de Fallos
```bash
# Mostrar traceback completo
pytest --tb=long

# Análisis detallado
python scripts/testing/run_all_tests.py
```

## Resultados Esperados

Al ejecutar la suite completa de pruebas, se debe obtener:

```
=================== test session starts ===================
platform win32 -- Python 3.13.7
collected 180 items

tests/unit/test_observer.py ............ [ 6%]
tests/unit/test_exceptions.py .......... [12%]
tests/unit/test_instruction.py ......... [18%]
tests/unit/test_register.py ............ [24%]
tests/unit/test_alu.py .................. [35%]
tests/integration/test_full_system.py ... [40%]

=================== 180 passed in 25.3s ===================
```

---

*Documentación de testing actualizada para versión 2.0 MVC*