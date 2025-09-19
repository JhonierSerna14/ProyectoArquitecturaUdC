# Reportes del Proyecto

Esta carpeta almacena todos los reportes, métricas y resultados generados automáticamente por el proyecto.

## Estructura:

```
reports/
├── testing/          # Resultados de pruebas
│   ├── latest/       # Últimos resultados
│   ├── historical/   # Histórico de ejecuciones
│   ├── junit/        # Reportes JUnit XML
│   ├── html/         # Reportes HTML
│   └── README.md     # Documentación de testing
└── README.md        # Este archivo
```

## Generación automática:

### 🧪 Testing:
Los reportes de testing se generan con:
```bash
python scripts/testing/run_all_tests.py
```

**Formatos generados:**
- **JUnit XML**: Para integración CI/CD
- **HTML**: Reportes visuales
- **JSON**: Datos estructurados para análisis

## Métricas tracked:

### ✅ Pruebas:
- **Tasa de éxito/fallo** de pruebas
- **Tiempo de ejecución** por suite
- **Distribución por tipo** (unit, integration, functional)
- **Evolución temporal** de métricas

## Retención de datos:

### 📈 Histórico:
- **30 días**: Reportes detallados en `latest/`
- **6 meses**: Summaries en `historical/`
- **1 año**: Métricas agregadas
- **Permanente**: Hitos y releases importantes

### 🗂️ Organización:
```
reports/testing/historical/
├── 2024-12/           # Por mes
│   ├── week-01/       # Por semana
│   ├── week-02/
│   └── summary.json   # Resumen mensual
└── yearly-summary.json # Resumen anual
```

## Integración:

### 📊 Dashboards:
Los reportes están diseñados para integración con:
- **SonarQube** (calidad de código)
- **CodeClimate** (análisis estático)

### 🚀 CI/CD:
Formatos compatibles con:
- **GitHub Actions** (workflow status)
- **Jenkins** (build reports)
- **Azure DevOps** (test results)