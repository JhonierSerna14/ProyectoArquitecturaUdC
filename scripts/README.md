# Scripts del Proyecto

Esta carpeta contiene todos los scripts automatizados del proyecto organizados por funcionalidad.

## Estructura:

```
scripts/
├── testing/          # Scripts de ejecución de pruebas
│   ├── run_tests.py           # Pruebas unitarias básicas
│   ├── run_all_tests.py       # Todas las pruebas
│   ├── run_functional_tests.py # Pruebas funcionales
│   ├── run_master_analysis.py # Análisis completo
│   └── README.md             # Documentación de scripts
├── analysis/         # Scripts de análisis de código
│   └── README.md             # Documentación de análisis
└── README.md        # Este archivo
```

## Uso rápido:

### 🧪 Ejecutar pruebas:
```bash
# Desde la raíz del proyecto:
python scripts/testing/run_tests.py          # Pruebas unitarias
python scripts/testing/run_all_tests.py      # Todas las pruebas
```

### 📊 Análisis:
```bash
# No hay scripts de análisis disponibles actualmente
```

## Características:

### ✨ Automatización completa:
- **Instalación automática** de dependencias
- **Detección de errores** y manejo graceful
- **Reportes detallados** de resultados
- **Logging estructurado** de ejecución

### 📈 Métricas y reportes:
- Generación automática en `reports/`
- Formatos múltiples (HTML, XML, texto)
- Histórico de ejecuciones
- Métricas de tendencias

### 🔧 Configuración:
- Variables de entorno detectadas automáticamente
- Rutas relativas para portabilidad
- Configuración centralizada en `pytest.ini`
- Soporte multi-plataforma

## Integración:

### CI/CD:
Los scripts están diseñados para integración con:
- **GitHub Actions**
- **Jenkins**
- **GitLab CI**
- **Azure DevOps**

### IDEs:
Configuración incluida para:
- **VS Code** (tasks.json)
- **PyCharm** (run configurations)
- **Vim/Neovim** (makefiles)