import os
import sys

# Agregar rutas relativas al PYTHONPATH
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))

try:
    from controller.controlador_solicitante import ControladorSolicitante
except ImportError:
    from src.controller.controlador_solicitante import ControladorSolicitante

try:
    from controller.controlador_vivienda import ControladorVivienda
except ImportError:
    from src.controller.controlador_vivienda import ControladorVivienda

# Alias en caso de ser invocado por nombre en minúsculas
controlador_solicitante = ControladorSolicitante

if __name__ == '__main__':
    print('Creando tablas solicitantes y viviendas (si no existen)...')
    ControladorSolicitante.crear_tabla()
    ControladorVivienda.crear_tabla()
    print('Listo.')
