import os
import sys
import unittest
import json

# Agregar rutas necesarias al PYTHONPATH
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "backend")))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "backend", "src")))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))

from backend.app import app

class TestApiEndpoints(unittest.TestCase):

    def setUp(self):
        self.app = app
        self.app.testing = True
        self.client = self.app.test_client()

    def test_hello_endpoint(self):
        """Prueba que el endpoint Hola Mundo responde 200 con el mensaje correcto."""
        response = self.client.get("/api/v1/hello")
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn("mensaje", data)
        self.assertIn("Hola Mundo", data["mensaje"])
        self.assertEqual(data["estado"], "online")

    def test_health_endpoint(self):
        """Prueba que el endpoint de salud responde con el estado del backend."""
        response = self.client.get("/api/v1/health")
        # Puede responder 200 (si BD está conectada) o 503 (si no hay BD local en ejecución)
        self.assertIn(response.status_code, [200, 503])
        data = json.loads(response.data)
        self.assertIn("estado_backend", data)
        self.assertEqual(data["estado_backend"], "saludable")

    def test_swagger_ui_available(self):
        """Prueba que la documentación interactiva Swagger (OpenAPI) está disponible."""
        response = self.client.get("/apidocs/")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"swagger", response.data.lower())

    def test_swagger_apispec_json(self):
        """Prueba que la especificación OpenAPI en JSON contiene los endpoints documentados."""
        response = self.client.get("/apispec_1.json")
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn("swagger", data)
        self.assertIn("paths", data)
        self.assertIn("/api/v1/calculo", data["paths"])
        self.assertIn("/api/v1/solicitantes", data["paths"])
        self.assertIn("/api/v1/viviendas", data["paths"])

    def test_calculo_exitoso(self):
        """Prueba cálculo financiero con valores válidos (edad 72, valor 300M)."""
        payload = {"edad": 72, "valor_vivienda": 300000000.0}
        response = self.client.post(
            "/api/v1/calculo",
            data=json.dumps(payload),
            content_type="application/json"
        )
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data["porcentaje_financiado"], 40)
        self.assertEqual(data["plazo_anios"], 15)
        self.assertAlmostEqual(data["pago_mensual"], (300000000.0 * 0.40) / (15 * 12), places=1)
        self.assertGreater(data["intereses_totales"], 0)
        self.assertGreater(data["saldo_final_proyectado"], data["valor_financiado"])

    def test_calculo_edad_menor_invalida(self):
        """Prueba que el cálculo rechaza edad menor a 65 años con código 400."""
        payload = {"edad": 58, "valor_vivienda": 200000000.0}
        response = self.client.post(
            "/api/v1/calculo",
            data=json.dumps(payload),
            content_type="application/json"
        )
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertIn("error", data)
        self.assertIn("65", data["error"])

    def test_calculo_edad_mayor_invalida(self):
        """Prueba que el cálculo rechaza edad mayor o igual a 115 años con código 400."""
        payload = {"edad": 116, "valor_vivienda": 200000000.0}
        response = self.client.post(
            "/api/v1/calculo",
            data=json.dumps(payload),
            content_type="application/json"
        )
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertIn("error", data)

    def test_calculo_valor_vivienda_menor_minimo(self):
        """Prueba que el cálculo rechaza valor de vivienda inferior a $50,000,000 COP."""
        payload = {"edad": 70, "valor_vivienda": 40000000.0}
        response = self.client.post(
            "/api/v1/calculo",
            data=json.dumps(payload),
            content_type="application/json"
        )
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertIn("error", data)
        self.assertIn("50,000,000", data["error"])

    def test_crear_solicitante_validacion_datos_incompletos(self):
        """Prueba validación de error 400 si faltan campos obligatorios."""
        payload = {"nombre": "Juan Pérez"}
        response = self.client.post(
            "/api/v1/solicitantes",
            data=json.dumps(payload),
            content_type="application/json"
        )
        self.assertEqual(response.status_code, 400)

    def test_crear_vivienda_validacion_datos_incompletos(self):
        """Prueba validación de error 400 si faltan campos de la vivienda."""
        payload = {"ciudad": "Medellín"}
        response = self.client.post(
            "/api/v1/viviendas",
            data=json.dumps(payload),
            content_type="application/json"
        )
        self.assertEqual(response.status_code, 400)

if __name__ == "__main__":
    unittest.main()
