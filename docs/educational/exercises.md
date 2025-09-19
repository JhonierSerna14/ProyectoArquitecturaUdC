# Ejercicios Prácticos

## 🎯 Objetivo
Consolidar el aprendizaje con ejercicios progresivos que cubren todos los aspectos del simulador.

---

## 🟢 Nivel Básico

### Ejercicio 1: Primera Calculadora
**Objetivo**: Dominar operaciones aritméticas básicas

**Enunciado**: 
Crea un programa que calcule: (15 + 25) × 2 - 10

**Plantilla**:
```assembly
# Tu código aquí
LOAD R1, ?
LOAD R2, ?
# ... completar
HALT
```

**Resultado esperado**: R final = 70

<details>
<summary>💡 Pista</summary>
Usa registros intermedios para almacenar resultados parciales.
</details>

<details>
<summary>✅ Solución</summary>

```assembly
LOAD R1, 15        # Primer número
LOAD R2, 25        # Segundo número
ADD R1, R2, R3     # R3 = 15 + 25 = 40
LOAD R4, 2         # Factor multiplicación
MUL R3, R4, R5     # R5 = 40 × 2 = 80
LOAD R6, 10        # Número a restar
SUB R5, R6, R7     # R7 = 80 - 10 = 70
HALT
```
</details>

---

### Ejercicio 2: Almacén de Datos
**Objetivo**: Practicar operaciones de memoria

**Enunciado**: 
1. Almacena los números 100, 200, 300 en memoria[20], [21], [22]
2. Cárgalos de vuelta en R1, R2, R3
3. Calcula su suma total

**Plantilla**:
```assembly
# Almacenar datos
LOAD R1, 100
STORE R1, ?
# ... completar

# Cargar datos
LOAD R1, *?
# ... completar

# Calcular suma
# ... completar
HALT
```

<details>
<summary>✅ Solución</summary>

```assembly
# Almacenar datos
LOAD R1, 100
STORE R1, 20
LOAD R2, 200
STORE R2, 21
LOAD R3, 300
STORE R3, 22

# Cargar datos de vuelta
LOAD R4, *20       # R4 = 100
LOAD R5, *21       # R5 = 200
LOAD R6, *22       # R6 = 300

# Calcular suma total
ADD R4, R5, R7     # R7 = 100 + 200 = 300
ADD R7, R6, R8     # R8 = 300 + 300 = 600
HALT
```
</details>

---

### Ejercicio 3: Lógica Binaria
**Objetivo**: Entender operaciones lógicas

**Enunciado**:
Dados dos números 12 (1100 binario) y 10 (1010 binario):
1. Calcula AND, OR, XOR
2. Calcula NOT de cada número original

**Plantilla**:
```assembly
LOAD R1, 12        # 1100
LOAD R2, 10        # 1010
# Completar operaciones lógicas
HALT
```

<details>
<summary>💡 Ayuda Binaria</summary>
- 12 = 1100
- 10 = 1010
- AND: 1100 & 1010 = 1000 = 8
- OR: 1100 | 1010 = 1110 = 14
- XOR: 1100 ^ 1010 = 0110 = 6
</details>

---

## 🟡 Nivel Intermedio

### Ejercicio 4: Contador Regresivo
**Objetivo**: Dominar bucles y saltos condicionales

**Enunciado**:
Crea un contador que vaya de 5 hasta 0, almacenando cada valor en memoria secuencial (posiciones 20-25).

**Algoritmo**:
1. Inicializar contador en 5
2. Guardar valor actual en memoria
3. Decrementar contador
4. Repetir hasta llegar a 0

**Plantilla**:
```assembly
LOAD R1, 5         # Contador inicial
LOAD R2, 20        # Dirección base de memoria
LOAD R3, 1         # Decremento

# Bucle principal
# Línea ?: STORE R1, ???
# Línea ?: SUB R1, R3, R1
# Línea ?: Actualizar dirección memoria
# Línea ?: JPZ ?, R1
# Línea ?: JP ?
HALT
```

<details>
<summary>✅ Solución</summary>

```assembly
LOAD R1, 5         # Contador (línea 0)
LOAD R2, 20        # Dirección base (línea 1)
LOAD R3, 1         # Decremento (línea 2)

# Bucle principal (línea 3)
STORE R1, *R2      # Guardar contador en memoria[R2] (línea 3)
SUB R1, R3, R1     # R1 = R1 - 1 (línea 4)
ADD R2, R3, R2     # R2 = R2 + 1 (siguiente posición) (línea 5)
JPZ 7, R1          # Si R1 = 0, terminar (línea 6)
JP 3               # Repetir bucle (línea 7)
HALT               # Fin (línea 8)

# Estado final de memoria:
# memoria[20] = 5, memoria[21] = 4, memoria[22] = 3
# memoria[23] = 2, memoria[24] = 1, memoria[25] = 0
```
</details>

---

### Ejercicio 5: Intercambio Inteligente
**Objetivo**: Manipulación avanzada de memoria

**Enunciado**:
Intercambia los contenidos de memoria[20] y memoria[21] sin usar registros directamente (solo como auxiliares temporales).

**Condiciones iniciales**:
- memoria[20] = 100
- memoria[21] = 200

**Resultado esperado**:
- memoria[20] = 200
- memoria[21] = 100

<details>
<summary>💡 Pista</summary>
Necesitarás una posición de memoria temporal, como memoria[22].
</details>

---

## 🔴 Nivel Avanzado

### Ejercicio 6: Búsqueda del Máximo
**Objetivo**: Algoritmos de comparación

**Enunciado**:
Dados tres números almacenados en memoria[20], [21], [22], encuentra el mayor y guárdalo en memoria[25].

**Algoritmo sugerido**:
1. Cargar primeros dos números
2. Compararlos usando resta
3. Guardar el mayor temporalmente
4. Comparar con el tercero
5. Guardar el resultado final

**Datos de prueba**:
- memoria[20] = 150
- memoria[21] = 89
- memoria[22] = 203

**Resultado esperado**: memoria[25] = 203

---

### Ejercicio 7: Factorial Iterativo
**Objetivo**: Algoritmos matemáticos complejos

**Enunciado**:
Calcula 5! (factorial de 5 = 5×4×3×2×1 = 120) usando un bucle.

**Algoritmo**:
1. Inicializar resultado = 1
2. Inicializar contador = 5
3. Multiplicar resultado × contador
4. Decrementar contador
5. Repetir hasta contador = 0

**Plantilla**:
```assembly
LOAD R1, 1         # Resultado (acumulador)
LOAD R2, 5         # Contador
LOAD R3, 1         # Decremento

# Bucle de multiplicación
# ??? (multiplicar R1 × R2)
# ??? (decrementar R2)
# ??? (verificar si R2 = 0)
# ??? (repetir o terminar)
HALT
```

---

### Ejercicio 8: División por Restas Sucesivas
**Objetivo**: Implementar división sin usar DIV

**Enunciado**:
Divide 20 entre 3 contando cuántas veces puedes restar 3 de 20 antes de que el resultado sea menor que 3.

**Algoritmo**:
1. Dividendo = 20, divisor = 3, cociente = 0
2. Mientras dividendo ≥ divisor:
   - Restar divisor del dividendo
   - Incrementar cociente
3. El cociente es el resultado de la división

**Resultado esperado**: 
- Cociente = 6 (20 ÷ 3 = 6 resto 2)
- Resto = 2

---

## 🏆 Desafío Maestro

### Ejercicio 9: Ordenamiento Burbuja Simplificado
**Objetivo**: Algoritmo de ordenamiento

**Enunciado**:
Ordena tres números almacenados en memoria[20], [21], [22] de menor a mayor.

**Datos de prueba**:
- memoria[20] = 50
- memoria[21] = 30  
- memoria[22] = 40

**Resultado esperado**:
- memoria[20] = 30
- memoria[21] = 40
- memoria[22] = 50

**Pistas**:
- Compara pares de números usando resta
- Intercambia si están en orden incorrecto
- Repite el proceso para asegurar orden completo

---

## 📊 Sistema de Evaluación

### 🟢 Básico (Ejercicios 1-3)
- ✅ **Objetivo**: Sintaxis y operaciones fundamentales
- ✅ **Criterios**: Código funciona y produce resultado correcto
- ✅ **Tiempo sugerido**: 30 minutos por ejercicio

### 🟡 Intermedio (Ejercicios 4-5)
- ✅ **Objetivo**: Bucles, memoria y lógica de control
- ✅ **Criterios**: Algoritmo eficiente y uso correcto de memoria
- ✅ **Tiempo sugerido**: 45 minutos por ejercicio

### 🔴 Avanzado (Ejercicios 6-8)
- ✅ **Objetivo**: Algoritmos complejos y optimización
- ✅ **Criterios**: Solución elegante y manejo de casos edge
- ✅ **Tiempo sugerido**: 60 minutos por ejercicio

### 🏆 Maestro (Ejercicio 9)
- ✅ **Objetivo**: Dominio completo del simulador
- ✅ **Criterios**: Implementación correcta de algoritmo complejo
- ✅ **Tiempo sugerido**: 90 minutos

---

## 🔗 Recursos de Apoyo

- [Conceptos Básicos](basic-concepts.md): Repasa fundamentos
- [Ejemplos Paso a Paso](examples.md): Ve ejecuciones detalladas
- [Guía del Usuario](../user-guide.md): Referencia de instrucciones
- [Ejemplos de Código](../../examples/): Programas completos funcionando

## 🎯 Siguientes Pasos

¡Felicitaciones por completar los ejercicios! Ahora estás listo para:
1. **Crear tus propios programas** con algoritmos originales
2. **Optimizar código** para usar menos instrucciones
3. **Experimentar** con casos edge y situaciones especiales
4. **Contribuir** al proyecto con nuevos ejemplos o mejoras