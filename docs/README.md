# 📚 Índice de Documentación - Simulador de Computadora v3.0

## 🎯 Guías por Audiencia

### 👨‍🎓 Para Estudiantes
- **[📖 Conceptos Básicos](educational/basic-concepts.md)** - Introducción fundamental a la arquitectura de computadoras
- **[📝 Ejemplos Paso a Paso](educational/examples.md)** - Ejecuciones detalladas de programas
- **[🎮 Ejercicios Prácticos](educational/exercises.md)** - Desafíos progresivos para dominar el simulador
- **[📋 Guía del Usuario](user-guide.md)** - Referencia completa de instrucciones y sintaxis

### 👨‍💻 Para Desarrolladores
- **[🛠️ Guía del Desarrollador](developer-guide.md)** - Arquitectura técnica y convenciones de código
- **[🧪 Documentación de Testing](testing/TESTING.md)** - Estrategia de pruebas y metodología
- **[📊 Resumen de Pruebas](testing/RESUMEN_PRUEBAS.md)** - Estado actual: 191 pruebas (100% éxito)

### 📋 Para Profesores e Instructores
- **[🎓 Conceptos Básicos](educational/basic-concepts.md)** - Material didáctico estructurado
- **[📚 Ejemplos Educativos](educational/examples.md)** - Casos de estudio para clases
- **[✏️ Ejercicios con Soluciones](educational/exercises.md)** - Evaluaciones y actividades

---

## 🚀 Novedades Versión 3.0

### ✨ Características Principales
1. **Instrucciones de 3 Operandos**: `ADD R1, R2, R3` (fuente1, fuente2, destino)
2. **Memoria de 32 bits**: Separación clara entre instrucciones (0-15) y datos (16-31)
3. **LOAD Avanzado**: `*18` (directo), `*R1` (indirecto), `100` (inmediato)
4. **División Segura**: Por cero retorna 0, no excepción
5. **Observer Pattern**: Comunicación correcta entre componentes

### 📝 Documentación Actualizada
- ✅ **Todos los ejemplos** migrados a nueva sintaxis
- ✅ **Guías educativas** creadas desde cero
- ✅ **Ejercicios prácticos** con dificultad progresiva
- ✅ **Documentación técnica** actualizada
- ✅ **Testing documentation** con cobertura completa

---

## 📂 Estructura de Documentación

```
docs/
├── 📄 user-guide.md           # Guía completa del usuario
├── 📄 developer-guide.md      # Documentación técnica
├── 📂 educational/            # Material educativo
│   ├── basic-concepts.md      # Fundamentos de arquitectura
│   ├── examples.md            # Ejemplos paso a paso
│   └── exercises.md           # Ejercicios prácticos
├── 📂 testing/                # Documentación de pruebas
│   ├── README.md              # Índice de testing
│   ├── TESTING.md             # Metodología de pruebas
│   └── RESUMEN_PRUEBAS.md     # Estado actual (191 tests)
└── 📂 bugs/                   # Registro de bugs (archivado)
```

---

## 🎯 Rutas de Aprendizaje Sugeridas

### 🟢 Nivel Principiante
1. [Conceptos Básicos](educational/basic-concepts.md) - Entender componentes
2. [Ejemplos Básicos](educational/examples.md#ejemplo-1-suma-básica) - Primera ejecución
3. [Ejercicios Nivel Básico](educational/exercises.md#nivel-básico) - Práctica inicial
4. [Guía del Usuario](user-guide.md) - Referencia de instrucciones

### 🟡 Nivel Intermedio
1. [Ejemplos de Memoria](educational/examples.md#ejemplo-2-operaciones-de-memoria) - Direccionamiento
2. [Ejercicios Intermedios](educational/exercises.md#nivel-intermedio) - Bucles y control
3. [Operaciones Avanzadas](user-guide.md#operaciones-de-memoria) - LOAD avanzado
4. Crear programas propios

### 🔴 Nivel Avanzado
1. [Ejercicios Avanzados](educational/exercises.md#nivel-avanzado) - Algoritmos complejos
2. [Guía del Desarrollador](developer-guide.md) - Arquitectura interna
3. [Testing](testing/TESTING.md) - Contribuir con pruebas
4. Contribuir al proyecto

---

## 🔍 Búsqueda Rápida

### 📋 Instrucciones
- **Aritméticas**: `ADD R1, R2, R3`, `SUB`, `MUL`, `DIV` → [user-guide.md](user-guide.md#operaciones-aritméticas)
- **Lógicas**: `AND R1, R2, R3`, `OR`, `NOT R1, R2`, `XOR` → [user-guide.md](user-guide.md#operaciones-lógicas)
- **Memoria**: `LOAD R1, *18`, `STORE R1, 20` → [user-guide.md](user-guide.md#operaciones-de-memoria)
- **Control**: `JP 5`, `JPZ 0, R1`, `HALT` → [user-guide.md](user-guide.md#operaciones-de-control)

### 🎯 Conceptos
- **Memoria de 32 bits** → [basic-concepts.md](educational/basic-concepts.md#memoria)
- **Registros** → [basic-concepts.md](educational/basic-concepts.md#registros)
- **ALU** → [basic-concepts.md](educational/basic-concepts.md#alu)
- **Direccionamiento** → [basic-concepts.md](educational/basic-concepts.md#direccionamiento)

### 🧪 Ejercicios por Tema
- **Aritmética** → [exercises.md](educational/exercises.md#ejercicio-1-primera-calculadora)
- **Memoria** → [exercises.md](educational/exercises.md#ejercicio-2-almacén-de-datos)
- **Bucles** → [exercises.md](educational/exercises.md#ejercicio-4-contador-regresivo)
- **Algoritmos** → [exercises.md](educational/exercises.md#ejercicio-7-factorial-iterativo)

---

## 📞 Soporte y Contribuciones

### 🐛 Reportar Problemas
- Revisar [bugs/](bugs/) para problemas conocidos
- Crear issue en GitHub con descripción detallada
- Incluir código de ejemplo y comportamiento esperado

### 🤝 Contribuir
1. Fork del repositorio
2. Crear rama para nueva característica
3. Seguir [convenciones de código](developer-guide.md#convenciones-de-código)
4. Agregar pruebas para nueva funcionalidad
5. Actualizar documentación correspondiente
6. Crear Pull Request

### 📧 Contacto
- **Proyecto**: Universidad de Caldas
- **Repositorio**: [ProyectoArquitecturaUdC](https://github.com/JhonierSerna14/ProyectoArquitecturaUdC)
- **Versión**: 3.0 (Septiembre 2025)

---

## 🏆 Estado del Proyecto

- ✅ **Funcionalidad**: 100% operativa
- ✅ **Testing**: 191 pruebas pasando (100%)
- ✅ **Documentación**: Completa y actualizada
- ✅ **Ejemplos**: Todos migrados a v3.0
- ✅ **Material Educativo**: Creado desde cero
- ✅ **Calidad de Código**: Seguimiento de mejores prácticas

**¡El simulador está listo para uso educativo y desarrollo!** 🎉