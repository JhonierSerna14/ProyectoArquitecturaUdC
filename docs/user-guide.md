# Guía del Usuario

Bienvenido al Simulador de Computadora de la Universidad de Caldas

## 🎯 Introducción

Este simulador te permite entender cómo funciona una computadora a nivel de hardware, visualizando la ejecución de instrucciones paso a paso.

## 🚀 Inicio Rápido

### 1. Instalación
```bash
# Clonar el repositorio
git clone https://github.com/JhonierSerna14/ProyectoArquitecturaUdC.git
cd ProyectoArquitecturaUdC

# Instalar dependencias
pip install -r requirements.txt

# Ejecutar el simulador
python main.py
```

### 2. Primera Ejecución
1. **Escribir código**: Introduce instrucciones en el área de texto
2. **Cargar**: Presiona "Cargar Instrucciones"
3. **Ejecutar**: Usa "Comenzar" o "Paso a paso"
4. **Observar**: Ve cómo se actualizan los registros y memoria

## 📋 Conjunto de Instrucciones

### Operaciones Aritméticas
| Instrucción | Descripción | Ejemplo |
|-------------|-------------|---------|
| `ADD R1, R2` | Suma R1 + R2 → R1 | `ADD R1, R2` |
| `SUB R1, R2` | Resta R1 - R2 → R1 | `SUB R3, R4` |
| `MUL R1, R2` | Multiplica R1 × R2 → R1 | `MUL R1, R5` |
| `DIV R1, R2` | Divide R1 ÷ R2 → R1 | `DIV R2, R3` |

### Operaciones Aritméticas (3 Operandos)
| Instrucción | Descripción | Ejemplo |
|-------------|-------------|---------|
| `ADD R1, R2, R3` | R1 + R2 → R3 | `ADD R1, R2, R3` |
| `SUB R1, R2, R3` | R1 - R2 → R3 | `SUB R4, R5, R6` |
| `MUL R1, R2, R3` | R1 × R2 → R3 | `MUL R1, R2, R3` |
| `DIV R1, R2, R3` | R1 ÷ R2 → R3 | `DIV R7, R8, R9` |

> **Nota**: División por cero retorna 0 y establece el flag Z

### Operaciones Lógicas (3 Operandos)
| Instrucción | Descripción | Ejemplo |
|-------------|-------------|---------|
| `AND R1, R2, R3` | R1 AND R2 → R3 | `AND R1, R2, R3` |
| `OR R1, R2, R3` | R1 OR R2 → R3 | `OR R3, R4, R5` |
| `XOR R1, R2, R3` | R1 XOR R2 → R3 | `XOR R5, R6, R7` |
| `NOT R1, R2` | NOT R1 → R2 | `NOT R1, R2` |

### Operaciones de Memoria
| Instrucción | Descripción | Ejemplo |
|-------------|-------------|---------|
| `LOAD R1, valor` | Carga valor inmediato | `LOAD R1, 10` |
| `LOAD R1, *R2` | Carga desde memoria (indirecto) | `LOAD R1, *R2` |
| `LOAD R1, *16` | Carga desde dirección directa | `LOAD R1, *16` |
| `STORE R1, dir` | Almacena en memoria | `STORE R1, 18` |
| `MOVE R1, R2` | Copia R2 → R1 | `MOVE R1, R2` |

> **Memoria**: 32 posiciones total (0-15 instrucciones, 16-31 datos)

### Operaciones de Control
| Instrucción | Descripción | Ejemplo |
|-------------|-------------|---------|
| `JP dirección` | Salto incondicional | `JP 0` |
| `JPZ dir, R1` | Salto si R1 = 0 | `JPZ 5, R1` |
| `HALT` | Terminar programa | `HALT` |

## 💡 Ejemplos Prácticos

### Ejemplo 1: Aritmética con 3 Operandos
```assembly
LOAD R1, 15       # Cargar 15 en R1
LOAD R2, 25       # Cargar 25 en R2
ADD R1, R2, R3    # R3 = R1 + R2 = 40
SUB R1, R2, R4    # R4 = R1 - R2 = -10
MUL R1, R2, R5    # R5 = R1 * R2 = 375
DIV R5, R1, R6    # R6 = R5 / R1 = 25
```

### Ejemplo 2: Operaciones con Memoria (Memoria de 32 bits)
```assembly
LOAD R1, 100      # Cargar 100 en R1
STORE R1, 18      # Guardar R1 en dirección 18 (área de datos)
LOAD R2, *18      # Cargar desde dirección 18 a R2 (directo)
LOAD R3, 18       # Cargar dirección 18 en R3
LOAD R4, *R3      # Cargar desde memoria[R3] a R4 (indirecto)
ADD R1, R2, R5    # R5 = 100 + 100 = 200
```

### Ejemplo 3: Programa con Bucle y Control
```assembly
```assembly
LOAD R1, 5     # Contador inicial
LOAD R2, 1     # Decremento
SUB R1, R2     # Decrementar contador
JPZ 0, R1      # Si R1 = 0, saltar al inicio
```

## 🖥️ Interfaz Gráfica

### Componentes de la Interfaz
- **Editor de Código**: Área para escribir instrucciones
- **Registros**: Muestra R1-R9, PC, MAR, IR, MBR, PSW
- **Memoria**: Visualiza datos e instrucciones
- **Buses**: Representa transferencia de datos
- **Controles**: Botones para ejecución

### Modos de Ejecución
1. **Ejecución Completa**: Ejecuta todo el programa
2. **Paso a Paso**: Ejecuta una instrucción por vez
3. **Pausa/Continuar**: Control de ejecución

## 🔧 Troubleshooting

### Errores Comunes
- **Sintaxis incorrecta**: Verificar formato de instrucciones
- **Registros inválidos**: Usar R1-R9 únicamente
- **División por cero**: Verificar operandos
- **Direcciones fuera de rango**: Usar direcciones 0-31

### Soluciones
- Consultar la sintaxis en esta guía
- Usar el modo paso a paso para debugging
- Verificar el estado de los registros antes de cada operación

## 📚 Recursos Adicionales

- [Arquitectura del Sistema](architecture.md)
- [Ejemplos Avanzados](educational/examples.md)
- [Ejercicios Prácticos](educational/exercises.md)