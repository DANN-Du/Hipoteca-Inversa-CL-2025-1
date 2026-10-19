import os
import sys
import unittest
from unittest.mock import MagicMock, patch

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "backend", "src")))

from controller.controlador_solicitante import ControladorSolicitante
from controller.controlador_vivienda import ControladorVivienda

class TestSeguridadSQL(unittest.TestCase):

    @patch("controller.controlador_solicitante.ControladorSolicitante.obtener_cursor")
    def test_prevencion_sql_injection_solicitante(self, mock_obtener_cursor):
        """Verifica que buscar_por_cedula utiliza consultas parametrizadas (%s) y no concatenación de strings."""
        mock_cursor = MagicMock()
        mock_cursor.fetchone.return_value = None
        mock_obtener_cursor.return_value = mock_cursor

        payload_inyeccion = "' OR '1'='1' --"
        ControladorSolicitante.buscar_por_cedula(payload_inyeccion)

        # Verificar que se llamó execute con la consulta con %s y la tupla de parámetros
        mock_cursor.execute.assert_called_once()
        consulta_ejecutada, params = mock_cursor.execute.call_args[0]
        
        self.assertIn("%s", consulta_ejecutada)
        self.assertNotIn(payload_inyeccion, consulta_ejecutada)
        self.assertEqual(params, (payload_inyeccion,))

    @patch("controller.controlador_vivienda.ControladorVivienda.obtener_cursor")
    def test_prevencion_sql_injection_vivienda_direccion(self, mock_obtener_cursor):
        """Verifica que buscar_por_direccion utiliza consultas parametrizadas (%s)."""
        mock_cursor = MagicMock()
        mock_cursor.fetchone.return_value = None
        mock_obtener_cursor.return_value = mock_cursor

        payload_inyeccion = "Cra 10'; DROP TABLE viviendas; --"
        ControladorVivienda.buscar_por_direccion(payload_inyeccion)

        mock_cursor.execute.assert_called_once()
        consulta_ejecutada, params = mock_cursor.execute.call_args[0]

        self.assertIn("%s", consulta_ejecutada)
        self.assertNotIn(payload_inyeccion, consulta_ejecutada)
        self.assertEqual(params, (payload_inyeccion,))

    @patch("controller.controlador_vivienda.ControladorVivienda.obtener_cursor")
    def test_prevencion_sql_injection_vivienda_propietario(self, mock_obtener_cursor):
        """Verifica que buscar_por_propietario utiliza consultas parametrizadas (%s)."""
        mock_cursor = MagicMock()
        mock_cursor.fetchall.return_value = []
        mock_obtener_cursor.return_value = mock_cursor

        payload_inyeccion = "' UNION SELECT * FROM secret_table --"
        ControladorVivienda.buscar_por_propietario(payload_inyeccion)

        mock_cursor.execute.assert_called_once()
        consulta_ejecutada, params = mock_cursor.execute.call_args[0]

        self.assertIn("%s", consulta_ejecutada)
        self.assertNotIn(payload_inyeccion, consulta_ejecutada)
        self.assertEqual(params, (payload_inyeccion,))

if __name__ == "__main__":
    unittest.main()
