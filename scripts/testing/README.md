# Scripts de Testing

Esta carpeta contiene todos los scripts para ejecutar pruebas del proyecto.

## Scripts disponibles:

### Scripts principales:
- **`run_tests.py`** - Ejecuta las pruebas unitarias básicas
- **`run_all_tests.py`** - Ejecuta todas las pruebas del proyecto
- **`run_functional_tests.py`** - Ejecuta pruebas funcionales específicas
- **`run_master_analysis.py`** - Análisis maestro completo del sistema

## Uso:

```bash
# Pruebas básicas
python scripts/testing/run_tests.py

# Todas las pruebas
python scripts/testing/run_all_tests.py

# Análisis completo
python scripts/testing/run_master_analysis.py
```

## Configuración:

La configuración de pytest se encuentra en el archivo `pytest.ini` en la raíz del proyecto.
Los reportes se generan automáticamente en `reports/testing/`.