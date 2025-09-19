# Reportes de Testing

Esta carpeta almacena todos los reportes y resultados de pruebas ejecutadas.

## Estructura:

```
reports/testing/
├── latest/          # Últimos resultados de pruebas
├── historical/      # Histórico de ejecuciones
├── junit/          # Reportes en formato JUnit XML
└── html/           # Reportes HTML interactivos
```

## Tipos de reportes:

### Resultados de pruebas:
- **Unitarias**: Resultados de pruebas de unidad
- **Integración**: Resultados de pruebas de integración
- **Funcionales**: Resultados de pruebas funcionales

### Métricas:
- **Tiempo de ejecución**: Duración de cada suite de pruebas
- **Tasa de éxito**: Porcentaje de pruebas pasadas
- **Tendencias**: Evolución temporal de las métricas

## Generación automática:

Los reportes se generan automáticamente con cada ejecución de:
- `scripts/testing/run_tests.py`
- `scripts/testing/run_all_tests.py`
- `scripts/testing/run_functional_tests.py`