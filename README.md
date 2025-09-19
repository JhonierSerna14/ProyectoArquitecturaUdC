# Simulador de Computadora - Universidad de Córdoba

Un simulador educativo de arquitectura de computadora con interfaz gráfica desarrollado en Python usando Tkinter. Este proyecto implementa los componentes fundamentales de una computadora y permite visualizar el ciclo de ejecución de instrucciones.

## 🎯 Características

- **Interfaz Gráfica Intuitiva**: Visualización en tiempo real de todos los componentes
- **Arquitectura Completa**: Implementación de ALU, Memoria, Registros y Unidad de Control
- **Ejecución Paso a Paso**: Posibilidad de ejecutar instrucciones una por una para análisis detallado
- **Visualización de Buses**: Representación gráfica de los buses de datos, direcciones y control
- **Registro PSW**: Monitoreo de flags de estado (Zero, Carry, Sign, Overflow)

## 🏗️ Arquitectura del Sistema

### Componentes Principales

1. **ALU (Unidad Aritmético-Lógica)**
   - Operaciones aritméticas: ADD, SUB, MUL, DIV
   - Operaciones lógicas: AND, OR, NOT, XOR
   - Manejo de flags PSW

2. **Memoria**
   - Separación entre memoria de instrucciones y datos
   - 32 posiciones de memoria (16 para instrucciones, 16 para datos)
   - Carga y almacenamiento de datos

3. **Banco de Registros**
   - 9 registros de propósito general (R1-R9)
   - Registros especiales: PC, MAR, IR, MBR, PSW

4. **Unidad de Control**
   - Ciclo fetch-decode-execute
   - Generación de señales de control
   - Coordinación de todos los componentes

## 🚀 Instalación y Uso

### Requisitos

- Python 3.8 o superior
- Tkinter (incluido con Python)

### Ejecución

```bash
# Clonar el repositorio
git clone https://github.com/usuario/ProyectoArquitecturaUdC.git
cd ProyectoArquitecturaUdC

# Ejecutar el simulador
python main.py
```

## 📝 Conjunto de Instrucciones

### Operaciones Aritméticas
- `ADD R1, R2` - Suma R1 + R2, resultado en R1
- `SUB R1, R2` - Resta R1 - R2, resultado en R1
- `MUL R1, R2` - Multiplica R1 * R2, resultado en R1
- `DIV R1, R2` - Divide R1 / R2, resultado en R1

### Operaciones Lógicas
- `AND R1, R2` - AND lógico entre R1 y R2
- `OR R1, R2` - OR lógico entre R1 y R2
- `NOT R1, R2` - NOT lógico de R2, resultado en R1
- `XOR R1, R2` - XOR lógico entre R1 y R2

### Operaciones de Memoria
- `LOAD R1, valor` - Carga un valor inmediato en R1
- `LOAD R1, *R2` - Carga el valor de la dirección en R2 hacia R1
- `STORE R1, dirección` - Almacena R1 en la dirección especificada
- `MOVE R1, R2` - Copia el valor de R2 a R1

### Operaciones de Control
- `JP dirección` - Salto incondicional a la dirección
- `JPZ dirección, R1` - Salto condicional si R1 es cero

## 💡 Ejemplos de Uso

### Ejemplo 1: Suma Básica
```assembly
LOAD R1, 10
LOAD R2, 5
ADD R1, R2
```
**Resultado**: R1 contendrá 15

### Ejemplo 2: Cálculo con Memoria
```assembly
LOAD R1, 20
LOAD R2, 16
STORE R1, 16
LOAD R3, *R2
ADD R1, R3
```
**Resultado**: R1 contendrá 40

### Ejemplo 3: Operaciones Lógicas
```assembly
LOAD R1, 12
LOAD R2, 8
AND R1, R2
OR R1, R2
```

### Ejemplo 4: Programa con Salto
```assembly
LOAD R1, 0
LOAD R2, 1
ADD R1, R2
JPZ 0, R1
```

## 🎮 Modo de Uso de la Interfaz

1. **Cargar Instrucciones**: Escribe las instrucciones en el área de texto
2. **Ejecutar Todo**: Presiona "Comenzar" para ejecutar todas las instrucciones
3. **Paso a Paso**: 
   - Presiona "Cargar Instrucciones" para cargar sin ejecutar
   - Usa "Paso a paso" para ejecutar una instrucción a la vez
4. **Visualización**: Observa cómo se actualizan los registros, memoria y buses

## 📁 Estructura del Proyecto

```
ProyectoArquitecturaUdC/
├── main.py                    # Archivo principal de ejecución
├── README.md                  # Documentación del proyecto
├── .gitignore                # Archivos a ignorar por Git
├── examples/                  # Ejemplos de programas
│   ├── basic_arithmetic.txt
│   ├── memory_operations.txt
│   ├── logical_operations.txt
│   └── control_flow.txt
└── Class/                     # Clases del simulador
    ├── ALU.py                # Unidad Aritmético-Lógica
    ├── ComputerSimulator.py  # Simulador principal
    ├── ControlUnit.py        # Unidad de Control
    ├── Memory.py             # Gestión de memoria
    ├── Register.py           # Registro individual
    ├── RegisterBank.py       # Banco de registros
    └── WiredControlUnit.py   # Unidad de control cableada
```

## 🎓 Propósito Educativo

Este simulador está diseñado para:
- Enseñar conceptos fundamentales de arquitectura de computadoras
- Visualizar el ciclo de ejecución de instrucciones
- Entender la interacción entre componentes de hardware
- Practicar programación en lenguaje ensamblador básico

## 👥 Contribución

Las contribuciones son bienvenidas. Por favor:
1. Haz fork del proyecto
2. Crea una rama para tu característica (`git checkout -b feature/AmazingFeature`)
3. Confirma tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Haz push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## 📄 Licencia

Este proyecto es de uso educativo para la Universidad de Córdoba.

## ✨ Créditos

Proyecto desarrollado como parte del curso de Arquitectura de Computadores en la Universidad de Córdoba.

---

**Universidad de Córdoba** - Programa de Ingeniería de Sistemas
