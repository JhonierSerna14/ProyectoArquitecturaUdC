# Simulador de Computadora
### Universidad de Caldas - Arquitectura de Computadoras

> **Simulador educativo interactivo** que permite visualizar y entender el funcionamiento interno de una computadora a nivel de hardware.

---

## 🎯 ¿Qué es este proyecto?

Un simulador completo de arquitectura de computadora con **interfaz gráfica intuitiva** que implementa:
- **Componentes de hardware** reales (ALU, Memoria, Registros, Unidad de Control)
- **Ejecución paso a paso** de instrucciones
- **Visualización en tiempo real** de buses y transferencias de datos
- **Conjunto de instrucciones** educativo pero completo

## 🚀 Inicio Rápido

```bash
# 1. Clonar e instalar
git clone https://github.com/JhonierSerna14/ProyectoArquitecturaUdC.git
cd ProyectoArquitecturaUdC
pip install -r requirements.txt

# 2. Ejecutar
python main.py

# 3. Escribir código assembly y experimentar
LOAD R1, 10
LOAD R2, 5
ADD R1, R2
```

**🎓 Para estudiantes**: Comienza con la [Guía del Usuario](docs/user-guide.md)  
**👨‍💻 Para desarrolladores**: Ve a la [Guía del Desarrollador](docs/developer-guide.md)

---

## 📚 Características Principales

### 🖥️ Componentes Implementados
- **ALU**: Operaciones aritméticas y lógicas con flags PSW
- **Memoria**: Sistema de memoria unificado (32 posiciones)
- **Registros**: Banco de 9 registros + registros especiales
- **Unidad de Control**: Ciclo fetch-decode-execute completo

### 💻 Conjunto de Instrucciones
| Categoría | Instrucciones | Ejemplo |
|-----------|---------------|---------|
| **Aritméticas** | ADD, SUB, MUL, DIV | `ADD R1, R2` |
| **Lógicas** | AND, OR, NOT, XOR | `AND R1, R2` |
| **Memoria** | LOAD, STORE, MOVE | `LOAD R1, 10` |
| **Control** | JP, JPZ | `JPZ 0, R1` |

### 🎮 Modos de Ejecución
- **Ejecución completa**: Ejecuta todo el programa automáticamente
- **Paso a paso**: Control granular para análisis detallado
- **Depuración visual**: Observa cada cambio en tiempo real
---

## 📁 Estructura del Proyecto

<details>
<summary>🗂️ Ver estructura completa</summary>

```
ProyectoArquitecturaUdC/
│
├── 📄 main.py                    # Punto de entrada
├── 📄 requirements.txt           # Dependencias principales
├── 📄 requirements-dev.txt       # Herramientas de desarrollo
│
├── 📂 core/                      # Lógica de negocio
│   ├── computer.py               # Modelo principal (MVC)
│   ├── instruction.py            # Representación de instrucciones
│   └── exceptions.py             # Excepciones personalizadas
│
├── 📂 hardware/                  # Componentes de hardware
│   ├── alu.py                    # Unidad Aritmético-Lógica
│   ├── memory.py                 # Sistema de memoria
│   ├── register_bank.py          # Banco de registros
│   └── control_unit.py           # Unidad de control
│
├── 📂 gui/                       # Interfaz gráfica (MVC)
│   ├── simulator_view.py         # Vista del simulador
│   └── simulator_controller.py   # Controlador
│
├── 📂 tests/                     # Suite de pruebas (85%+ cobertura)
│   ├── unit/                     # 41 pruebas unitarias
│   └── integration/              # Pruebas de integración
│
├── 📂 scripts/                   # Herramientas de desarrollo
│   ├── testing/                  # Scripts de pruebas
│   └── analysis/                 # Análisis de código
│
├── 📂 docs/                      # Documentación completa
│   ├── user-guide.md             # Guía del usuario
│   ├── developer-guide.md        # Guía del desarrollador
│   └── installation.md           # Instalación detallada
│
└── 📂 examples/                  # Ejemplos educativos
    ├── basic_arithmetic.txt      # Operaciones básicas
    └── control_flow.txt          # Estructuras de control
```
</details>

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

---

## 🧪 Testing y Calidad de Código

### ✅ Métricas de Calidad
- **41 pruebas unitarias** - 100% de éxito
- **Cobertura >85%** - Objetivo de calidad alto
- **Metodología de partición equivalente** aplicada
- **Integración continua** con análisis automático

### 🔧 Ejecutar Pruebas
```bash
# Todas las pruebas
python scripts/testing/run_all_tests.py

# Solo pruebas unitarias
python scripts/testing/run_tests.py
```

### 📊 Reportes
- **Métricas detalladas**: Ver [documentación de testing](docs/testing/README.md)

---

## 🎓 Para Estudiantes

### 💡 Ejemplos Rápidos

**Suma básica:**
```assembly
LOAD R1, 15
LOAD R2, 25
ADD R1, R2      # R1 = 40
```

**Uso de memoria:**
```assembly
LOAD R1, 100
STORE R1, 16    # Guardar en memoria[16]
LOAD R2, *16    # Cargar desde memoria[16]
ADD R1, R2      # R1 = 200
```

**Bucle simple:**
```assembly
LOAD R1, 5      # Contador
LOAD R2, 1      # Decremento
SUB R1, R2      # R1 = R1 - 1
JPZ 0, R1       # Si R1 = 0, saltar al inicio
```

### 📖 Recursos Educativos
- [Conceptos Básicos](docs/educational/basic-concepts.md)
- [Ejemplos Paso a Paso](docs/educational/examples.md)
- [Ejercicios Prácticos](docs/educational/exercises.md)

---

## 👨‍� Para Desarrolladores

### 🛠️ Tecnologías Utilizadas
- **Python 3.8+** - Lenguaje principal
- **Tkinter** - Interfaz gráfica nativa
- **pytest** - Framework de testing
- **MVC Pattern** - Arquitectura del software

### 🏗️ Arquitectura
- **Patrón MVC** implementado completamente
- **Patrón Observer** para comunicación entre componentes
- **SOLID principles** aplicados
- **Clean Architecture** para mantenibilidad


**⭐ Si este proyecto te es útil, considera darle una estrella ⭐**

*Desarrollado con ❤️ para la comunidad educativa*

### 🐛 Tracking de Bugs

**Ver documentación completa**: 
- [Documentación de Testing](docs/testing/README.md)
- [Registro de Bugs](docs/bugs/BUGS_REGISTRO.md)


## 🎓 Propósito Educativo

Este simulador está diseñado para:
- Enseñar conceptos fundamentales de arquitectura de computadoras
- Visualizar el ciclo de ejecución de instrucciones
- Entender la interacción entre componentes de hardware
- Practicar programación en lenguaje ensamblador básico

## 📄 Licencia

Este proyecto es de uso educativo para la Universidad de Caldas.
