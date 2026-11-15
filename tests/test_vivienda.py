import unittest
import sys
from datetime import datetime
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "backend", "src")))

from model.vivienda import Vivienda
from controller.controlador_vivienda import ControladorVivienda
from model.solicitante import Solicitante
from controller.controlador_solicitante import ControladorSolicitante

class testDBvivienda (unittest.TestCase):
    
    # Test fixtures
    def setUpClass():
        """test fixtures: se ejecuta una vez al inicio de la prueba"""
        # Eliminar y crear tablas en el orden correcto (solicitantes primero por FK)
        ControladorSolicitante.eliminar_tabla()
        ControladorVivienda.eliminar_tabla()
        ControladorSolicitante.crear_tabla()
        ControladorVivienda.crear_tabla()

    @staticmethod
    def asegurar_propietario_existe(identificacion: str, nombre: str = None):
        """Inserta un solicitante si no existe (usa datos por defecto simples)."""
        if ControladorSolicitante.buscar_por_cedula(identificacion) is None:
            nombre = nombre or f"Propietario {identificacion}"
            s = Solicitante(
                nombre=nombre,
                identificacion=identificacion,
                fecha_nacimiento=datetime.strptime("1950-01-01", "%Y-%m-%d").date(),
                edad=75,
            )
            ControladorSolicitante.insertar(s)
        

    def test_insertar_y_buscar_direccion_1(self):
        """ Prueba que inserta una vivienda en la base de datos y luego la busca por su direccion """
        vivienda_prueba = Vivienda(ciudad="Medellín", 
            barrio="El Poblado",
            direccion="Calle 10 # 20-30", 
            identificacion_propietario="1022345678",
            valor=350000000)
        
        # Asegurar que el propietario existe para no violar la FK
        self.asegurar_propietario_existe(vivienda_prueba.identificacion_propietario)
        ControladorVivienda.insertar(vivienda_prueba)

        vivienda_encontrada = ControladorVivienda.buscar_por_direccion('Calle 10 # 20-30')

        self.assertTrue(vivienda_prueba.is_equal(vivienda_encontrada))

    def test_insertar_y_buscar_direccion_2(self):
        """ Prueba que inserta una vivienda en la base de datos y luego la busca por su direccion """
        vivienda_prueba = Vivienda(ciudad="Bogotá", 
            barrio="Chapinero",
            direccion="Carrera 15 # 85-45", 
            identificacion_propietario="1098765432",
            valor=450000000)
        
        self.asegurar_propietario_existe(vivienda_prueba.identificacion_propietario)
        ControladorVivienda.insertar(vivienda_prueba)

        vivienda_encontrada = ControladorVivienda.buscar_por_direccion('Carrera 15 # 85-45')

        self.assertTrue(vivienda_prueba.is_equal(vivienda_encontrada))
    
    def test_insertar_y_buscar_direccion_3(self):
        """ Prueba que inserta una vivienda en la base de datos y luego la busca por su direccion """
        vivienda_prueba = Vivienda(ciudad="Cali", 
            barrio="San Antonio",
            direccion="Avenida 4N # 22-10", 
            identificacion_propietario="1032145678",
            valor=300000000)
        
        self.asegurar_propietario_existe(vivienda_prueba.identificacion_propietario)
        ControladorVivienda.insertar(vivienda_prueba)

        vivienda_encontrada = ControladorVivienda.buscar_por_direccion('Avenida 4N # 22-10')

        self.assertTrue(vivienda_prueba.is_equal(vivienda_encontrada))
    
    def test_insertar_y_buscar_propietario_1(self):
        """ Prueba que inserta varias viviendas en la base de datos y luego las busca por la identificacion del propietario """
        vivienda1_prueba = Vivienda(ciudad="Medellín", 
            barrio="Laureles",
            direccion="Calle 33 # 70-15", 
            identificacion_propietario="1023344556",
            valor=280000000)
        
        vivienda2_prueba = Vivienda(ciudad="Medellín", 
            barrio="Laureles",
            direccion="Calle 45 # 80-20", 
            identificacion_propietario="1023344556",
            valor=320000000)
        
        # Asegurar propietario
        self.asegurar_propietario_existe(vivienda1_prueba.identificacion_propietario)
        ControladorVivienda.insertar(vivienda1_prueba)
        ControladorVivienda.insertar(vivienda2_prueba)

        viviendas_encontradas = ControladorVivienda.buscar_por_propietario('1023344556')

        self.assertEqual(2, len(viviendas_encontradas))
        self.assertTrue(vivienda1_prueba.is_equal(viviendas_encontradas[0]) or vivienda1_prueba.is_equal(viviendas_encontradas[1]))
        self.assertTrue(vivienda2_prueba.is_equal(viviendas_encontradas[0]) or vivienda2_prueba.is_equal(viviendas_encontradas[1]))

    def test_insertar_y_buscar_propietario_2(self):
        """ Prueba que inserta varias viviendas en la base de datos y luego las busca por la identificacion del propietario """
        vivienda1_prueba = Vivienda(ciudad="Bogotá", 
            barrio="Usaquén",
            direccion="Carrera 7 # 120-30", 
            identificacion_propietario="1078899001",
            valor=500000000)
        
        vivienda2_prueba = Vivienda(ciudad="Bogotá", 
            barrio="Usaquén",
            direccion="Calle 134 # 9-50", 
            identificacion_propietario="1078899001",
            valor=550000000)
        
        self.asegurar_propietario_existe(vivienda1_prueba.identificacion_propietario)
        ControladorVivienda.insertar(vivienda1_prueba)
        ControladorVivienda.insertar(vivienda2_prueba)

        viviendas_encontradas = ControladorVivienda.buscar_por_propietario('1078899001')

        self.assertEqual(2, len(viviendas_encontradas))
        self.assertTrue(vivienda1_prueba.is_equal(viviendas_encontradas[0]) or vivienda1_prueba.is_equal(viviendas_encontradas[1]))
        self.assertTrue(vivienda2_prueba.is_equal(viviendas_encontradas[0]) or vivienda2_prueba.is_equal(viviendas_encontradas[1]))

    def test_insertar_y_buscar_propietario_3(self):
        """ Prueba que inserta varias viviendas en la base de datos y luego las busca por la identificacion del propietario """
        vivienda1_prueba = Vivienda(ciudad="Cali", 
            barrio="Granada",
            direccion="Avenida 6N # 18-40", 
            identificacion_propietario="1066677889",
            valor=400000000)
        
        vivienda2_prueba = Vivienda(ciudad="Cali", 
            barrio="Granada",
            direccion="Calle 9 # 23-60", 
            identificacion_propietario="1066677889",
            valor=420000000)
        
        self.asegurar_propietario_existe(vivienda1_prueba.identificacion_propietario)
        ControladorVivienda.insertar(vivienda1_prueba)
        ControladorVivienda.insertar(vivienda2_prueba)

        viviendas_encontradas = ControladorVivienda.buscar_por_propietario('1066677889')

        self.assertEqual(2, len(viviendas_encontradas))
        self.assertTrue(vivienda1_prueba.is_equal(viviendas_encontradas[0]) or vivienda1_prueba.is_equal(viviendas_encontradas[1]))
        self.assertTrue(vivienda2_prueba.is_equal(viviendas_encontradas[0]) or vivienda2_prueba.is_equal(viviendas_encontradas[1]))

    def test_modificar_y_buscar_direccion_1(self):
        """ Prueba que modifica los datos de una vivienda en la base de datos y luego la busca por su direccion """
        vivienda_prueba = Vivienda(ciudad="Medellín", 
            barrio="Belen",
            direccion="Calle 20 # 50-10", 
            identificacion_propietario="1087654321",
            valor=290000000)
        
        self.asegurar_propietario_existe(vivienda_prueba.identificacion_propietario)
        ControladorVivienda.insertar(vivienda_prueba)

        # Modificar datos
        vivienda_prueba.barrio = "Belen Rosales"
        vivienda_prueba.valor = 300000000

        ControladorVivienda.modificar_datos(vivienda_prueba)

        vivienda_encontrada = ControladorVivienda.buscar_por_direccion('Calle 20 # 50-10')

        self.assertTrue(vivienda_prueba.is_equal(vivienda_encontrada))
    
    def test_modificar_y_buscar_direccion_2(self):
        """ Prueba que modifica los datos de una vivienda en la base de datos y luego la busca por su direccion """
        vivienda_prueba = Vivienda(ciudad="Bogotá", 
            barrio="Teusaquillo",
            direccion="Carrera 30 # 45-15", 
            identificacion_propietario="1054321987",
            valor=480000000)
        
        self.asegurar_propietario_existe(vivienda_prueba.identificacion_propietario)
        ControladorVivienda.insertar(vivienda_prueba)

        # Modificar datos
        vivienda_prueba.barrio = "Teusaquillo Norte"
        vivienda_prueba.valor = 490000000

        ControladorVivienda.modificar_datos(vivienda_prueba)

        vivienda_encontrada = ControladorVivienda.buscar_por_direccion('Carrera 30 # 45-15')

        self.assertTrue(vivienda_prueba.is_equal(vivienda_encontrada))

    def test_modificar_y_buscar_direccion_3(self):
        """ Prueba que modifica los datos de una vivienda en la base de datos y luego la busca por su direccion """
        vivienda_prueba = Vivienda(ciudad="Cali", 
            barrio="San Fernando",
            direccion="Avenida 3N # 12-25", 
            identificacion_propietario="1043219876",
            valor=310000000)
        
        self.asegurar_propietario_existe(vivienda_prueba.identificacion_propietario)
        ControladorVivienda.insertar(vivienda_prueba)

        # Modificar datos
        vivienda_prueba.barrio = "San Fernando Viejo"
        vivienda_prueba.valor = 320000000

        ControladorVivienda.modificar_datos(vivienda_prueba)

        vivienda_encontrada = ControladorVivienda.buscar_por_direccion('Avenida 3N # 12-25')

        self.assertTrue(vivienda_prueba.is_equal(vivienda_encontrada))

    def test_buscar_no_existente(self):
        """ Prueba que busca una vivienda que no existe en la base de datos """
        vivienda_encontrada = ControladorVivienda.buscar_por_direccion('Direccion Inexistente # 00-00')

        self.assertIsNone(vivienda_encontrada)

    def test_insertar_duplicado(self):
        """ Prueba que intenta insertar una vivienda con una direccion ya existente en la base de datos """
        vivienda_prueba = Vivienda(ciudad="Medellín", 
            barrio="Castropol",
            direccion="Calle 55 # 90-10", 
            identificacion_propietario="1034567890",
            valor=330000000)
        
        self.asegurar_propietario_existe(vivienda_prueba.identificacion_propietario)
        ControladorVivienda.insertar(vivienda_prueba)

        with self.assertRaises(Exception):
            # intentar insertar nuevamente la misma vivienda (debe fallar por PK/direccion única)
            ControladorVivienda.insertar(vivienda_prueba)

    def modificar_no_existente(self):
        """ Prueba que intenta modificar una vivienda que no existe en la base de datos """
        vivienda_prueba = Vivienda(ciudad="Bogotá", 
            barrio="Suba",
            direccion="Carrera 100 # 150-20", 
            identificacion_propietario="1023456789",
            valor=600000000)
        
        with self.assertRaises(ValueError):
            ControladorVivienda.modificar_datos(vivienda_prueba)
    
    def tearDownClass():
        """test fixtures: se ejecuta una vez al final de la prueba"""
        ControladorVivienda.eliminar_tabla()
    
if __name__ == '__main__':
    unittest.main()