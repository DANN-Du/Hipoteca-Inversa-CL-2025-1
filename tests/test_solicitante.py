import unittest
import sys
from datetime import datetime
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "backend", "src")))

from model.solicitante import Solicitante
from controller.controlador_solicitante import ControladorSolicitante

class testDBsolicitante (unittest.TestCase):

    # Test fixtures
    def setUpClass():
        """test fixtures: se ejecuta una vez al inicio de la prueba"""
        ControladorSolicitante.eliminar_tabla()
        ControladorSolicitante.crear_tabla()
        

    def test_insertar_y_buscar_1(self):
        """ Prueba que inserta un solicitante en la base de datos y luego lo busca por su cedula """
        solicitante_prueba = Solicitante(nombre="Beatriz Elena Montoya", 
            identificacion="1022345678",
            fecha_nacimiento= datetime.strptime("1953-03-12", "%Y-%m-%d").date(), 
            edad=72)
        
        ControladorSolicitante.insertar(solicitante_prueba)

        solicitante_encontrado = ControladorSolicitante.buscar_por_cedula('1022345678')

        self.assertTrue(solicitante_prueba.is_equal(solicitante_encontrado))

    def test_insertar_y_buscar_2(self):
        """ Prueba que inserta un solicitante en la base de datos y luego lo busca por su cedula """
        solicitante_prueba = Solicitante(nombre="Carlos Andrés Ramírez", 
            identificacion="1098765432",
            fecha_nacimiento= datetime.strptime("1965-07-25", "%Y-%m-%d").date(), 
            edad=65)
        
        ControladorSolicitante.insertar(solicitante_prueba)

        solicitante_encontrado = ControladorSolicitante.buscar_por_cedula('1098765432')

        self.assertTrue(solicitante_prueba.is_equal(solicitante_encontrado))
    
    def test_insertar_y_buscar_3(self):
        """ Prueba que inserta un solicitante en la base de datos y luego lo busca por su cedula """
        solicitante_prueba = Solicitante(nombre="Luis Fernando Gómez", 
            identificacion="1032145678",
            fecha_nacimiento= datetime.strptime("1980-05-15", "%Y-%m-%d").date(), 
            edad=43)
        
        ControladorSolicitante.insertar(solicitante_prueba)

        solicitante_encontrado = ControladorSolicitante.buscar_por_cedula('1032145678')

        self.assertTrue(solicitante_prueba.is_equal(solicitante_encontrado))

    def test_modificar_y_buscar_1(self):
        """ Prueba que modifica los datos de un solicitante en la base de datos y luego lo busca por su cedula """
        solicitante_prueba = Solicitante(nombre="Ana María López", 
            identificacion="1034567890",
            fecha_nacimiento= datetime.strptime("1970-11-30", "%Y-%m-%d").date(), 
            edad=70)
        
        ControladorSolicitante.insertar(solicitante_prueba)

        # Modificar datos
        solicitante_prueba.nombre = "Ana M. López"
        solicitante_prueba.edad = 71

        ControladorSolicitante.modificar_datos(solicitante_prueba)

        solicitante_encontrado = ControladorSolicitante.buscar_por_cedula('1034567890')

        self.assertTrue(solicitante_prueba.is_equal(solicitante_encontrado))
    
    def test_modificar_y_buscar_2(self):
        """ Prueba que modifica los datos de un solicitante en la base de datos y luego lo busca por su cedula """
        solicitante_prueba = Solicitante(nombre="Jorge Luis Hernández", 
            identificacion="1045678901",
            fecha_nacimiento= datetime.strptime("1960-02-20", "%Y-%m-%d").date(), 
            edad=68)
        
        ControladorSolicitante.insertar(solicitante_prueba)

        # Modificar datos
        solicitante_prueba.nombre = "Jorge L. Hernández"
        solicitante_prueba.edad = 69

        ControladorSolicitante.modificar_datos(solicitante_prueba)

        solicitante_encontrado = ControladorSolicitante.buscar_por_cedula('1045678901')

        self.assertTrue(solicitante_prueba.is_equal(solicitante_encontrado))

    def test_modificar_y_buscar_3(self):
        """ Prueba que modifica los datos de un solicitante en la base de datos y luego lo busca por su cedula """
        solicitante_prueba = Solicitante(nombre="María Fernanda Castillo", 
            identificacion="1056789012",
            fecha_nacimiento= datetime.strptime("1975-09-10", "%Y-%m-%d").date(), 
            edad=85)
        
        ControladorSolicitante.insertar(solicitante_prueba)

        # Modificar datos
        solicitante_prueba.nombre = "María F. Castillo"
        solicitante_prueba.edad = 86

        ControladorSolicitante.modificar_datos(solicitante_prueba)

        solicitante_encontrado = ControladorSolicitante.buscar_por_cedula('1056789012')

        self.assertTrue(solicitante_prueba.is_equal(solicitante_encontrado))

    def test_buscar_no_existente(self):
        """ Prueba que busca un solicitante que no existe en la base de datos """
        solicitante_encontrado = ControladorSolicitante.buscar_por_cedula('9999999999')
        self.assertIsNone(solicitante_encontrado)

    def test_insertar_duplicado(self):
        """ Prueba que intenta insertar un solicitante con una cedula que ya existe en la base de datos """
        solicitante_prueba = Solicitante(nombre="Pedro Pablo Díaz", 
            identificacion="1067890123",
            fecha_nacimiento= datetime.strptime("1985-12-05", "%Y-%m-%d").date(), 
            edad=69)
        
        ControladorSolicitante.insertar(solicitante_prueba)

        with self.assertRaises(Exception):
            ControladorSolicitante.insertar(solicitante_prueba)

    def test_modificar_no_existente(self):
        """ Prueba que intenta modificar un solicitante que no existe en la base de datos """
        solicitante_prueba = Solicitante(nombre="Laura Isabel Moreno", 
            identificacion="1078901234",
            fecha_nacimiento= datetime.strptime("1990-08-22", "%Y-%m-%d").date(), 
            edad=72)
        
        with self.assertRaises(Exception):
            ControladorSolicitante.modificar_datos(solicitante_prueba)
    
    def tearDownClass():
        """test fixtures: se ejecuta una vez al final de la prueba"""
        ControladorSolicitante.eliminar_tabla()

if __name__ == '__main__':
    unittest.main()
