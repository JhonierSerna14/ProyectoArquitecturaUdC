# Ejemplos Paso a Paso

## 🎯 Objetivo
Aprender a programar el simulador con ejemplos detallados que muestran cada paso de ejecución.

## 📋 Ejemplo 1: Suma Básica con 3 Operandos

### Código
```assembly
LOAD R1, 15        # Línea 0
LOAD R2, 25        # Línea 1
ADD R1, R2, R3     # Línea 2
HALT               # Línea 3
```

### Ejecución Paso a Paso

#### Estado Inicial
- **PC**: 0 (apunta a la primera instrucción)
- **Registros**: Todos en 0
- **Memoria**: Vacía

#### Paso 1: LOAD R1, 15
- **FETCH**: Buscar instrucción en memoria[0]
- **DECODE**: Interpretar "LOAD R1, 15"
- **EXECUTE**: Cargar 15 en R1
- **Estado**: R1 = 15, PC = 1

#### Paso 2: LOAD R2, 25
- **FETCH**: Buscar instrucción en memoria[1]
- **DECODE**: Interpretar "LOAD R2, 25"
- **EXECUTE**: Cargar 25 en R2
- **Estado**: R1 = 15, R2 = 25, PC = 2

#### Paso 3: ADD R1, R2, R3
- **FETCH**: Buscar instrucción en memoria[2]
- **DECODE**: Interpretar "ADD R1, R2, R3"
- **EXECUTE**: 
  - ALU calcula R1 + R2 = 15 + 25 = 40
  - Resultado se guarda en R3
- **Estado**: R1 = 15, R2 = 25, R3 = 40, PC = 3

#### Paso 4: HALT
- **FETCH**: Buscar instrucción en memoria[3]
- **DECODE**: Interpretar "HALT"
- **EXECUTE**: Terminar programa
- **Estado Final**: R1 = 15, R2 = 25, R3 = 40, Programa terminado

---

## 📋 Ejemplo 2: Operaciones de Memoria

### Código
```assembly
LOAD R1, 100       # Línea 0: Cargar valor
STORE R1, 18       # Línea 1: Guardar en memoria
LOAD R2, 200       # Línea 2: Cargar otro valor
STORE R2, 19       # Línea 3: Guardar en memoria
LOAD R3, *18       # Línea 4: Cargar desde memoria
LOAD R4, *19       # Línea 5: Cargar desde memoria
ADD R3, R4, R5     # Línea 6: Sumar valores de memoria
HALT               # Línea 7: Terminar
```

### Ejecución Detallada

#### Pasos 0-1: Preparar primer valor
- **Después de línea 0**: R1 = 100
- **Después de línea 1**: memoria[18] = 100

#### Pasos 2-3: Preparar segundo valor
- **Después de línea 2**: R2 = 200
- **Después de línea 3**: memoria[19] = 200

#### Pasos 4-5: Recuperar valores de memoria
- **Línea 4 (LOAD R3, *18)**: 
  - Parser identifica "*18" como dirección directa
  - Se lee valor de memoria[18] = 100
  - R3 = 100
- **Línea 5 (LOAD R4, *19)**:
  - Se lee valor de memoria[19] = 200
  - R4 = 200

#### Paso 6: Operación aritmética
- **ADD R3, R4, R5**: 
  - ALU calcula 100 + 200 = 300
  - R5 = 300

### Estado Final
- **Registros**: R1=100, R2=200, R3=100, R4=200, R5=300
- **Memoria**: memoria[18]=100, memoria[19]=200

---

## 📋 Ejemplo 3: Direccionamiento Indirecto

### Código
```assembly
LOAD R1, 100       # Valor a almacenar
LOAD R2, 20        # Dirección donde almacenar
STORE R1, 20       # Guardar directamente
LOAD R3, *R2       # Cargar indirectamente
HALT
```

### Diferencias en Direccionamiento

#### Directo vs Indirecto
```assembly
# DIRECTO
LOAD R1, *20       # Lee memoria[20]

# INDIRECTO  
LOAD R2, 20        # R2 = 20 (la dirección)
LOAD R1, *R2       # Lee memoria[R2] = memoria[20]
```

#### Paso a Paso del Ejemplo
1. **R1 = 100** (valor a trabajar)
2. **R2 = 20** (dirección de memoria)
3. **memoria[20] = 100** (guardar valor)
4. **LOAD R3, *R2**: 
   - R2 contiene 20
   - Se lee memoria[20] = 100
   - R3 = 100

---

## 📋 Ejemplo 4: Programa con Bucle

### Código
```assembly
LOAD R1, 3         # Contador inicial (línea 0)
LOAD R2, 1         # Decremento (línea 1)
SUB R1, R2, R1     # R1 = R1 - 1 (línea 2)
JPZ 5, R1          # Si R1 = 0, saltar a línea 5 (línea 3)
JP 2               # Saltar de vuelta a línea 2 (línea 4)
HALT               # Fin del programa (línea 5)
```

### Ejecución del Bucle

#### Iteración 1
- **Estado inicial**: R1=3, R2=1, PC=0
- **Después línea 2**: R1=2 (3-1)
- **Línea 3**: R1 ≠ 0, no saltar
- **Línea 4**: JP 2, PC=2

#### Iteración 2
- **Línea 2**: R1=1 (2-1)
- **Línea 3**: R1 ≠ 0, no saltar
- **Línea 4**: JP 2, PC=2

#### Iteración 3
- **Línea 2**: R1=0 (1-1)
- **Línea 3**: R1 = 0, ¡saltar a línea 5!
- **Línea 5**: HALT

### Análisis del Bucle
- **Contador**: R1 va de 3 → 2 → 1 → 0
- **Iteraciones**: 3 veces
- **Condición de parada**: R1 = 0

---

## 📋 Ejemplo 5: División por Cero Segura

### Código
```assembly
LOAD R1, 10        # Dividendo
LOAD R2, 0         # Divisor (cero)
DIV R1, R2, R3     # División segura
HALT
```

### ¿Qué Sucede?
1. **R1 = 10**, **R2 = 0**
2. **DIV R1, R2, R3**: 
   - ALU detecta división por cero
   - No lanza error, establece R3 = 0
   - Flag Z = 1 (indica resultado cero)
3. **Programa continúa normalmente**

### Beneficio
- El programa no se bloquea
- Se puede verificar el flag Z para detectar división por cero
- Comportamiento predecible y seguro

---

## 🎯 Ejercicios Propuestos

### Ejercicio A: Calculadora Completa
Crea un programa que:
1. Cargue dos números en R1 y R2
2. Calcule suma, resta, multiplicación y división
3. Guarde cada resultado en memoria (posiciones 20-23)

### Ejercicio B: Búsqueda del Mayor
Compara tres números y encuentra el mayor usando saltos condicionales.

### Ejercicio C: Factorial Simple
Calcula 4! (factorial de 4) usando un bucle.

### Ejercicio D: Intercambio con Memoria
Intercambia los valores de R1 y R2 usando memoria[25] como variable temporal.

## 💡 Consejos de Programación

1. **Planifica antes de codificar**: Dibuja un diagrama de flujo
2. **Usa comentarios**: Documenta cada línea importante
3. **Prueba paso a paso**: Ejecuta línea por línea para entender
4. **Verifica flags**: Usa PSW para detectar condiciones especiales
5. **Organiza la memoria**: Usa posiciones específicas para datos específicos

## 🔗 Siguiente Paso
Una vez domines estos ejemplos, intenta los [ejercicios prácticos](exercises.md) para consolidar tu aprendizaje.