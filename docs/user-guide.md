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

### Operaciones Lógicas
| Instrucción | Descripción | Ejemplo |
|-------------|-------------|---------|
| `AND R1, R2` | R1 AND R2 → R1 | `AND R1, R2` |
| `OR R1, R2` | R1 OR R2 → R1 | `OR R3, R4` |
| `NOT R1, R2` | NOT R2 → R1 | `NOT R1, R2` |
| `XOR R1, R2` | R1 XOR R2 → R1 | `XOR R5, R6` |

### Operaciones de Memoria
| Instrucción | Descripción | Ejemplo |
|-------------|-------------|---------|
| `LOAD R1, valor` | Carga valor inmediato | `LOAD R1, 10` |
| `LOAD R1, *R2` | Carga desde memoria | `LOAD R1, *R2` |
| `STORE R1, dir` | Almacena en memoria | `STORE R1, 16` |
| `MOVE R1, R2` | Copia R2 → R1 | `MOVE R1, R2` |

### Operaciones de Control
| Instrucción | Descripción | Ejemplo |
|-------------|-------------|---------|
| `JP dirección` | Salto incondicional | `JP 0` |
| `JPZ dir, R1` | Salto si R1 = 0 | `JPZ 5, R1` |

## 💡 Ejemplos Prácticos

### Ejemplo 1: Suma Simple
```assembly
LOAD R1, 15    # Cargar 15 en R1
LOAD R2, 25    # Cargar 25 en R2
ADD R1, R2     # R1 = R1 + R2 (40)
```

### Ejemplo 2: Operaciones con Memoria
```assembly
LOAD R1, 100   # Cargar 100 en R1
STORE R1, 16   # Guardar R1 en dirección 16
LOAD R2, *16   # Cargar desde dirección 16 a R2
ADD R1, R2     # R1 = 100 + 100 = 200
```

### Ejemplo 3: Programa con Bucle
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