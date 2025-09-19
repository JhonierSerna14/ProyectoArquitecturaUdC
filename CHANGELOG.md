# Changelog - Simulador de Computadora

## Versión 3.0 - Septiembre 2025 🚀

### ✨ Nuevas Características Principales

#### 🔢 Instrucciones de 3 Operandos
- **ANTES**: `ADD R1, R2` (R1 = R1 + R2)
- **AHORA**: `ADD R1, R2, R3` (R3 = R1 + R2)
- Aplicable a: ADD, SUB, MUL, DIV, AND, OR, XOR
- Beneficio: Mayor claridad y flexibilidad en programación

#### 💾 Memoria de 32 Bits
- **Configuración**: 32 posiciones totales
  - Posiciones 0-15: Área de instrucciones
  - Posiciones 16-31: Área de datos
- **Optimización**: Uso eficiente de memoria limitada
- **Validación**: Direcciones fuera de rango generan errores apropiados

#### 📥 Sintaxis LOAD Mejorada
- **Carga inmediata**: `LOAD R1, 100` (valor directo)
- **Carga desde memoria (dirección directa)**: `LOAD R1, *18`
- **Carga desde memoria (registro indirecto)**: `LOAD R1, *R2`
- **Distinción clara**: Entre valores inmediatos y direcciones de memoria

#### 🔄 Instrucción NOT Corregida
- **ANTES**: `NOT R1` (resultado en R1)
- **AHORA**: `NOT R1, R2` (NOT R1 → R2)
- **Consistencia**: Con el formato de 2 operandos estándar

### 🛡️ Mejoras de Seguridad y Robustez

#### ➗ División por Cero Segura
- **Comportamiento**: División por 0 retorna 0 (no excepción)
- **Flag Z**: Se establece automáticamente en 1
- **Beneficio**: Programas no se bloquean por error matemático

#### 🔍 Validación Mejorada
- **Rangos numéricos**: Validación de operandos ALU [-16384, 16383]
- **Direcciones memoria**: Solo direcciones válidas (16-31) para datos
- **Sintaxis**: Parser más robusto con mejor manejo de errores

### 🏗️ Mejoras Arquitectónicas

#### 👀 Patrón Observer Corregido
- **Método estándar**: `update()` en lugar de `notify()`
- **Comunicación**: Correcta entre Computer y componentes
- **Sincronización**: Estados actualizados en tiempo real

#### 🧮 ALU Mejorada
- **Propagación de errores**: Manejo correcto de excepciones
- **Operaciones lógicas**: NOT usa operand2 como fuente
- **Flags PSW**: Actualizados correctamente en todas las operaciones

### 📝 Documentación Actualizada

#### 📖 Ejemplos de Uso
- `examples/basic_arithmetic.txt`: Aritmética con 3 operandos
- `examples/complex_arithmetic.txt`: Operaciones complejas
- `examples/logical_operations.txt`: Operaciones lógicas mejoradas
- `examples/memory_operations.txt`: Uso de memoria de 32 bits
- `examples/control_flow.txt`: Control de flujo optimizado
- `examples/complete_demo.txt`: **NUEVO** - Demostración completa

#### 📚 Documentación
- `README.md`: Ejemplos actualizados con nueva sintaxis
- `docs/user-guide.md`: Guía completa de instrucciones
- Comentarios en código fuente actualizados

### 🧪 Calidad y Testing

#### ✅ Cobertura de Pruebas
- **191 pruebas** ejecutándose exitosamente
- **100% de aprobación** en toda la suite de tests
- Pruebas unitarias e integración actualizadas

#### 🔧 Correcciones de Bugs
1. **Parser de instrucciones**: Soporte completo para 3 operandos
2. **Resolución de operandos**: Manejo correcto de `*18` vs `*R1`
3. **Ejecución de instrucciones**: Pipeline fetch-decode-execute robusto
4. **Gestión de memoria**: Direcciones válidas y manejo de errores
5. **Comunicación MVC**: Observer pattern funcionando correctamente

### 🎯 Compatibilidad

#### ⬆️ Retrocompatibilidad
- Programas antiguos necesitan actualizarse a nueva sintaxis
- Migración requerida para:
  - Instrucciones aritméticas (2 → 3 operandos)
  - Direcciones de memoria (ajustar al rango 16-31)
  - Instrucción NOT (1 → 2 operandos)

#### 🔄 Migración Automática
- Ejemplos actualizados automáticamente
- Documentación de migración disponible
- Herramientas de testing verifican compatibilidad

---

## Versiones Anteriores

### Versión 2.0
- Arquitectura MVC implementada
- Patrón Observer básico
- Interfaz gráfica mejorada

### Versión 1.0
- Simulador básico funcional
- Instrucciones de 2 operandos
- Memoria simple

---

**Desarrollado por**: Equipo Universidad de Caldas  
**Fecha**: Septiembre 2025  
**Estado**: Producción ✅