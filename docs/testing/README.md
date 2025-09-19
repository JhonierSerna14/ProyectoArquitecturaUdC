# Documentación de Testing v3.0

Esta carpeta contiene toda la documentación relacionada con las pruebas del proyecto.

## 🎯 Estado Actual
- **191 pruebas ejecutándose** con 100% de éxito
- **Cobertura completa** de nuevas características v3.0
- **Validación robusta** de instrucciones de 3 operandos, memoria 32-bits

## Archivos incluidos:

- `TESTING.md` - Documentación principal sobre el sistema de pruebas (actualizada v3.0)
- `RESUMEN_PRUEBAS.md` - Resumen ejecutivo de los resultados de pruebas (191 tests)

## ✨ Nuevas Características Testeadas:

### 🔢 Instrucciones de 3 Operandos
- Parser y validación sintáctica
- Ejecución correcta en Computer
- Operaciones: ADD, SUB, MUL, DIV, AND, OR, XOR

### 💾 Memoria de 32 Bits
- Separación instrucciones (0-15) y datos (16-31)
- Validación de direcciones
- Manejo de errores MemoryOverflowError

### 📥 LOAD Avanzado
- Sintaxis `*18` (dirección directa)
- Sintaxis `*R1` (registro indirecto)
- Distinción inmediato vs memoria

### ➗ División Segura
- División por cero retorna 0
- Flag Z establecido automáticamente
- Sin excepciones, ejecución continúa

## Estructura del sistema de testing:

Para ejecutar las pruebas, utiliza los scripts ubicados en `scripts/testing/`:
- Pruebas unitarias: `scripts/testing/run_tests.py`
- Todas las pruebas: `scripts/testing/run_all_tests.py` 
- Pruebas funcionales: `scripts/testing/run_functional_tests.py`

Los reportes se generan automáticamente en `reports/testing/`.

## 🧪 Metodología Aplicada:
- **Partición Equivalente**: Clases de entrada sistemáticas
- **Análisis de Cobertura**: Todas las rutas de código cubiertas
- **Pruebas de Integración**: Sistema completo MVC validado
- **Pruebas de Regresión**: Aseguran que cambios no rompen funcionalidad existente