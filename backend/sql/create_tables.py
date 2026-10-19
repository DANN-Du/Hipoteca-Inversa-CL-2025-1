import sys
sys.path.append('src')

from controller.controlador_solicitante import controlador_solicitante
from controller.controlador_vivienda import ControladorVivienda

if __name__ == '__main__':
    print('Creando tablas solicitantes y viviendas (si no existen)...')
    controlador_solicitante.crear_tabla()
    ControladorVivienda.crear_tabla()
    print('Listo.')
