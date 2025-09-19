# Guía del Desarrollador

Documentación técnica para desarrolladores que contribuyen al proyecto

## 🛠️ Setup del Entorno de Desarrollo

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
- **`hardware/`**: Componentes de hardware
- **`gui/`**: Interfaz gráfica (MVC)
- **`utils/`**: Utilidades y helpers
- **`tests/`**: Suite de pruebas

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
        OverflowException: Si el resultado excede el rango
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