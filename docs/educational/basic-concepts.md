# Conceptos Básicos - Simulador de Computadora

## 🎯 Objetivo Educativo

Este simulador te permite entender cómo funciona una computadora a nivel básico, desde las operaciones más simples hasta programas completos.

## 🏗️ Componentes de una Computadora

### 1. 🧮 ALU (Unidad Aritmético-Lógica)
**¿Qué hace?** Realiza todas las operaciones matemáticas y lógicas.

**Operaciones que puede hacer:**
- **Aritméticas**: Suma, resta, multiplicación, división
- **Lógicas**: AND, OR, NOT, XOR
- **Comparaciones**: Establece flags (banderas) según el resultado

**Ejemplo práctico:**
```assembly
LOAD R1, 10        # Cargar 10 en registro R1
LOAD R2, 5         # Cargar 5 en registro R2
ADD R1, R2, R3     # R3 = R1 + R2 = 15
```

### 2. 💾 Memoria
**¿Qué hace?** Almacena tanto las instrucciones del programa como los datos.

**Organización en nuestro simulador:**
- **Posiciones 0-15**: Instrucciones del programa
- **Posiciones 16-31**: Datos del programa
- **Total**: 32 posiciones de memoria

**Ejemplo práctico:**
```assembly
LOAD R1, 100       # Cargar valor 100
STORE R1, 18       # Guardar en memoria posición 18
LOAD R2, *18       # Cargar desde memoria posición 18 a R2
```

### 3. 📋 Registros
**¿Qué son?** Pequeñas memorias muy rápidas dentro del procesador.

**Registros disponibles:**
- **R1 a R9**: Registros de propósito general
- **PC**: Contador de programa (indica qué instrucción ejecutar)
- **MAR**: Registro de dirección de memoria
- **MBR**: Registro buffer de memoria
- **IR**: Registro de instrucción
- **PSW**: Palabra de estado (flags Z, C, S, O)

### 4. 🎛️ Unidad de Control
**¿Qué hace?** Coordina todas las operaciones, como el director de una orquesta.

**Ciclo de ejecución:**
1. **FETCH**: Buscar la siguiente instrucción en memoria
2. **DECODE**: Interpretar qué operación realizar
3. **EXECUTE**: Ejecutar la operación

## 📝 Instrucciones Básicas

### 🔢 Carga de Datos
```assembly
LOAD R1, 50        # Cargar valor inmediato 50 en R1
LOAD R2, *20       # Cargar valor desde memoria[20] en R2
```

### ➕ Operaciones Aritméticas
```assembly
ADD R1, R2, R3     # R3 = R1 + R2
SUB R1, R2, R4     # R4 = R1 - R2
MUL R1, R2, R5     # R5 = R1 * R2
DIV R1, R2, R6     # R6 = R1 / R2
```

### 🔀 Operaciones Lógicas
```assembly
AND R1, R2, R3     # R3 = R1 AND R2 (operación bit a bit)
OR R1, R2, R4      # R4 = R1 OR R2
NOT R1, R5         # R5 = NOT R1 (invertir bits)
```

### 💾 Operaciones de Memoria
```assembly
STORE R1, 25       # Guardar R1 en memoria[25]
LOAD R2, *25       # Cargar desde memoria[25] a R2
```

### 🔄 Control de Flujo
```assembly
JP 5               # Saltar a instrucción 5
JPZ 0, R1          # Si R1 es 0, saltar a instrucción 0
HALT               # Terminar programa
```

## 🎮 Tu Primer Programa

### Programa: Sumar dos números
```assembly
LOAD R1, 15        # Cargar primer número
LOAD R2, 25        # Cargar segundo número
ADD R1, R2, R3     # Sumar y guardar resultado
HALT               # Terminar
```

**¿Qué pasa paso a paso?**
1. Se carga 15 en el registro R1
2. Se carga 25 en el registro R2
3. La ALU suma R1 + R2 y guarda 40 en R3
4. El programa termina

### Programa: Usar memoria
```assembly
LOAD R1, 100       # Cargar 100
STORE R1, 20       # Guardar en memoria[20]
LOAD R2, 200       # Cargar 200
STORE R2, 21       # Guardar en memoria[21]
LOAD R3, *20       # Cargar desde memoria[20] (100)
LOAD R4, *21       # Cargar desde memoria[21] (200)
ADD R3, R4, R5     # R5 = 100 + 200 = 300
HALT
```

## 🔍 Conceptos Importantes

### 1. Direccionamiento
- **Inmediato**: `LOAD R1, 50` (usar el valor 50 directamente)
- **Directo**: `LOAD R1, *20` (usar el valor que está en memoria[20])
- **Indirecto**: `LOAD R1, *R2` (usar memoria[valor_de_R2])

### 2. Flags del PSW
- **Z (Zero)**: Se activa cuando el resultado es 0
- **C (Carry)**: Se activa cuando hay acarreo
- **S (Sign)**: Se activa cuando el resultado es negativo
- **O (Overflow)**: Se activa cuando hay desbordamiento

### 3. División por Cero
En nuestro simulador, dividir por cero es seguro:
```assembly
LOAD R1, 10
LOAD R2, 0
DIV R1, R2, R3     # R3 = 0, Flag Z = 1
```

## 🎯 Ejercicios Propuestos

### Ejercicio 1: Calculadora básica
Escribe un programa que:
1. Cargue dos números en registros
2. Realice las 4 operaciones básicas
3. Guarde los resultados en memoria

### Ejercicio 2: Intercambio de valores
Intercambia los valores de dos registros usando memoria como auxiliar.

### Ejercicio 3: Contador
Crea un programa que cuente de 5 hacia 0 usando un bucle.

## 📚 Recursos Adicionales

- [Guía del Usuario](user-guide.md): Referencia completa de instrucciones
- [Ejemplos](../examples/): Programas de ejemplo listos para usar
- [Guía del Desarrollador](developer-guide.md): Para entender el código interno