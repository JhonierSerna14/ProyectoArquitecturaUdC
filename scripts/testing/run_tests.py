"""
Script para ejecutar todas las pruebas usando unittest (sin dependencias externas).

Este script ejecuta todas las pruebas unitarias y de integración
usando únicamente unittest que viene incluido con Python.
"""

import unittest
import sys
import os
from pathlib import Path
import subprocess


def discover_and_run_tests():
    """Descubre y ejecuta todas las pruebas."""
    print("=" * 60)
    print("🧪 EJECUTANDO PRUEBAS - SIMULADOR DE COMPUTADORA")
    print("=" * 60)
    
    # Agregar el directorio raíz al path
    project_root = Path(__file__).parent
    sys.path.insert(0, str(project_root))
    
    # Cambiar al directorio del proyecto
    os.chdir(project_root)
    
    # Descubrir pruebas
    loader = unittest.TestLoader()
    
    # Cargar pruebas unitarias
    print("\n🔍 Descubriendo pruebas unitarias...")
    try:
        unit_suite = loader.discover('tests/unit', pattern='test_*.py')
        unit_count = unit_suite.countTestCases()
        print(f"✅ Encontradas {unit_count} pruebas unitarias")
    except Exception as e:
        print(f"❌ Error cargando pruebas unitarias: {e}")
        unit_suite = unittest.TestSuite()
        unit_count = 0
    
    # Cargar pruebas de integración
    print("\n🔍 Descubriendo pruebas de integración...")
    try:
        integration_suite = loader.discover('tests/integration', pattern='test_*.py')
        integration_count = integration_suite.countTestCases()
        print(f"✅ Encontradas {integration_count} pruebas de integración")
    except Exception as e:
        print(f"❌ Error cargando pruebas de integración: {e}")
        integration_suite = unittest.TestSuite()
        integration_count = 0
    
    # Combinar todas las pruebas
    all_tests = unittest.TestSuite([unit_suite, integration_suite])
    total_tests = unit_count + integration_count
    
    print(f"\n📊 Total de pruebas a ejecutar: {total_tests}")
    
    if total_tests == 0:
        print("❌ No se encontraron pruebas para ejecutar")
        return False
    
    # Ejecutar pruebas
    print("\n" + "=" * 40)
    print("🚀 EJECUTANDO PRUEBAS")
    print("=" * 40)
    
    runner = unittest.TextTestRunner(verbosity=2, stream=sys.stdout)
    result = runner.run(all_tests)
    
    # Mostrar resumen
    print("\n" + "=" * 40)
    print("📊 RESUMEN DE RESULTADOS")
    print("=" * 40)
    
    print(f"Pruebas ejecutadas: {result.testsRun}")
    print(f"Pruebas exitosas: {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"Fallos: {len(result.failures)}")
    print(f"Errores: {len(result.errors)}")
    print(f"Saltadas: {len(result.skipped) if hasattr(result, 'skipped') else 0}")
    
    if result.failures:
        print(f"\n❌ FALLOS ENCONTRADOS:")
        for test, traceback in result.failures:
            print(f"  - {test}: {traceback.split('\\n')[-2] if traceback else 'Sin detalles'}")
    
    if result.errors:
        print(f"\n💥 ERRORES ENCONTRADOS:")
        for test, traceback in result.errors:
            print(f"  - {test}: {traceback.split('\\n')[-2] if traceback else 'Sin detalles'}")
    
    success_rate = ((result.testsRun - len(result.failures) - len(result.errors)) / result.testsRun * 100) if result.testsRun > 0 else 0
    print(f"\n🎯 Tasa de éxito: {success_rate:.1f}%")
    
    if success_rate >= 90:
        print("🎉 ¡Excelente! Tasa de éxito >= 90%")
    elif success_rate >= 80:
        print("👍 Buena tasa de éxito >= 80%")
    else:
        print("⚠️  Tasa de éxito baja, revisar fallos")
    
    return result.wasSuccessful()


def run_individual_test_file(test_file):
    """Ejecuta un archivo de prueba específico."""
    print(f"\n🧪 Ejecutando {test_file}...")
    
    try:
        # Importar y ejecutar el módulo de prueba específico
        spec = unittest.util.spec_from_file_location("test_module", test_file)
        test_module = unittest.util.module_from_spec(spec)
        spec.loader.exec_module(test_module)
        
        # Descubrir pruebas en el módulo
        loader = unittest.TestLoader()
        suite = loader.loadTestsFromModule(test_module)
        
        # Ejecutar pruebas
        runner = unittest.TextTestRunner(verbosity=1)
        result = runner.run(suite)
        
        return result.wasSuccessful()
        
    except Exception as e:
        print(f"❌ Error ejecutando {test_file}: {e}")
        return False


def check_test_files_manually():
    """Verifica manualmente qué módulos tienen pruebas."""
    print("\n" + "=" * 40)
    print("📋 VERIFICACIÓN MANUAL DE ARCHIVOS DE PRUEBA")
    print("=" * 40)
    
    # Módulos del proyecto
    modules_to_test = {
        'core/observer.py': 'tests/unit/test_observer.py',
        'core/exceptions.py': 'tests/unit/test_exceptions.py',
        'core/instruction.py': 'tests/unit/test_instruction.py',
        'hardware/register.py': 'tests/unit/test_register.py',
        'hardware/alu.py': 'tests/unit/test_alu.py',
    }
    
    test_report = []
    
    for module, test_file in modules_to_test.items():
        module_path = Path(module)
        test_path = Path(test_file)
        
        module_exists = module_path.exists()
        test_exists = test_path.exists()
        
        status = "✅" if module_exists and test_exists else "❌"
        test_report.append({
            'module': module,
            'test_file': test_file,
            'tested': module_exists and test_exists,
            'status': status
        })
        
        print(f"{status} {module} -> {test_file}")
    
    tested_count = sum(1 for report in test_report if report['tested'])
    total_count = len(test_report)
    test_percentage = (tested_count / total_count * 100) if total_count > 0 else 0
    
    print(f"\n📊 Archivos con pruebas: {tested_count}/{total_count} ({test_percentage:.1f}%)")
    
    return test_percentage


def main():
    """Función principal."""
    print("Simulador de Computadora - Test Runner")
    print("Usando unittest (sin dependencias externas)")
    
    # Verificar que estamos en el directorio correcto
    if not Path("pytest.ini").exists():
        print("❌ No se encontró pytest.ini. Ejecute desde el directorio raíz del proyecto.")
        return 1
    
    # Verificar archivos de prueba
    test_percentage = check_test_files_manually()
    
    # Ejecutar todas las pruebas
    all_tests_passed = discover_and_run_tests()
    
    # Recomendaciones finales
    print("\n" + "=" * 60)
    print("🎯 RECOMENDACIONES FINALES")
    print("=" * 60)
    
    if test_percentage < 80:
        print("📝 Agregar más archivos de prueba para módulos faltantes")
    
    if not all_tests_passed:
        print("🔧 Revisar y corregir pruebas que fallan")
    
    if all_tests_passed and test_percentage >= 80:
        print("🎉 ¡Sistema de pruebas en buen estado!")
        print("💡 Para mejorar:")
        print("   - Instalar pytest para funcionalidades avanzadas")
        print("   - Implementar CI/CD con GitHub Actions")
    
    print(f"\n📋 Ejecutar pruebas individuales:")
    print(f"   py -m unittest tests.unit.test_observer -v")
    print(f"   py -m unittest tests.unit.test_exceptions -v")
    print(f"   py -m unittest tests.unit.test_instruction -v")
    
    return 0 if all_tests_passed else 1


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)