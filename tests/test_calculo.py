import sys 
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "backend", "src")))

import unittest
from model import calculo
from model import excepciones

class TestHipotecaInversa(unittest.TestCase):
    # =========================
    # CASO 1
    # =========================
    def test_caso_1_porcentaje(self):
        # Entrada
        edad = 68
        # Cálculo
        resultado = calculo.calcular_porcentaje_financiado(edad)
        # Verificación
        self.assertEqual(resultado, 30)

    def test_caso_1_plazo(self):
        # Entrada
        edad = 68
        # Cálculo
        resultado = calculo.calcular_plazo_financiacion(edad)
        # Verificación
        self.assertEqual(resultado, 20)

    def test_caso_1_pago_mensual(self):
        # Entrada
        porcentaje_financiado = 30
        valor_vivienda = 500_000_000.0
        plazo = 20
        # Cálculo
        resultado = calculo.calcular_pago_mensual(porcentaje_financiado, valor_vivienda, plazo)
        # Verificación
        self.assertAlmostEqual(resultado, 625000.0, places=6)

    def test_caso_1_intereses(self):
        # Entrada
        edad = 68
        valor_vivienda = 500_000_000.0
        # Cálculo
        pf = calculo.calcular_porcentaje_financiado(edad)
        plazo = calculo.calcular_plazo_financiacion(edad)
        pago = calculo.calcular_pago_mensual(pf, valor_vivienda, plazo)
        intereses, _ = calculo.calcular_intereses(pago, calculo.TASA_EFECTIVA_MENSUAL, plazo)
        # Verificación
        self.assertAlmostEqual(intereses, 51708483.423720025, places=2)

    # =========================
    # CASO 2
    # =========================
    def test_caso_2_porcentaje(self):
        # Entrada
        edad = 70
        # Cálculo
        resultado = calculo.calcular_porcentaje_financiado(edad)
        # Verificación
        self.assertEqual(resultado, 40)

    def test_caso_2_plazo(self):
        # Entrada
        edad = 70
        # Cálculo
        resultado = calculo.calcular_plazo_financiacion(edad)
        # Verificación
        self.assertEqual(resultado, 15)

    def test_caso_2_pago_mensual(self):
        # Entrada
        porcentaje_financiado = 40
        valor_vivienda = 400_000_000.0
        plazo = 15
        # Cálculo
        resultado = calculo.calcular_pago_mensual(porcentaje_financiado, valor_vivienda, plazo)
        # Verificación
        self.assertAlmostEqual(resultado, 888888.8888888889, places=6)

    def test_caso_2_intereses(self):
        # Entrada
        edad = 70
        valor_vivienda = 400_000_000.0
        # Cálculo
        pf = calculo.calcular_porcentaje_financiado(edad)
        plazo = calculo.calcular_plazo_financiacion(edad)
        pago = calculo.calcular_pago_mensual(pf, valor_vivienda, plazo)
        intereses, _ = calculo.calcular_intereses(pago, calculo.TASA_EFECTIVA_MENSUAL, plazo)
        # Verificación
        self.assertAlmostEqual(intereses, 23716044.688623436, places=2)

    # =========================
    # CASO 3
    # =========================
    def test_caso_3_porcentaje(self):
        # Entrada
        edad = 80
        # Cálculo
        resultado = calculo.calcular_porcentaje_financiado(edad)
        # Verificación
        self.assertEqual(resultado, 55)

    def test_caso_3_plazo(self):
        # Entrada
        edad = 80
        # Cálculo
        resultado = calculo.calcular_plazo_financiacion(edad)
        # Verificación
        self.assertEqual(resultado, 5)

    def test_caso_3_pago_mensual(self):
        # Entrada
        porcentaje_financiado = 55
        valor_vivienda = 200_000_000.0
        plazo = 5
        # Cálculo
        resultado = calculo.calcular_pago_mensual(porcentaje_financiado, valor_vivienda, plazo)
        # Verificación
        self.assertAlmostEqual(resultado, 1833333.3333333333, places=6)

    def test_caso_3_intereses(self):
        # Entrada
        edad = 80
        valor_vivienda = 200_000_000.0
        # Cálculo
        pf = calculo.calcular_porcentaje_financiado(edad)
        plazo = calculo.calcular_plazo_financiacion(edad)
        pago = calculo.calcular_pago_mensual(pf, valor_vivienda, plazo)
        intereses, _ = calculo.calcular_intereses(pago, calculo.TASA_EFECTIVA_MENSUAL, plazo)
        # Verificación
        self.assertAlmostEqual(intereses, 3712493.966080846, places=2)

    # =========================
    # CASO 4
    # =========================
    def test_caso_4_porcentaje(self):
        # Entrada
        edad = 95
        # Cálculo
        resultado = calculo.calcular_porcentaje_financiado(edad)
        # Verificación
        self.assertEqual(resultado, 70)

    def test_caso_4_plazo(self):
        # Entrada
        edad = 95
        # Cálculo
        resultado = calculo.calcular_plazo_financiacion(edad)
        # Verificación
        self.assertEqual(resultado, 3)

    def test_caso_4_pago_mensual(self):
        # Entrada
        porcentaje_financiado = 70
        valor_vivienda = 10_000_000.0
        plazo = 3
        # Cálculo
        resultado = calculo.calcular_pago_mensual(porcentaje_financiado, valor_vivienda, plazo)
        # Verificación
        self.assertAlmostEqual(resultado, 194444.44444444444, places=6)

    def test_caso_4_intereses(self):
        # Entrada
        edad = 95
        valor_vivienda = 10_000_000.0
        # Cálculo
        pf = calculo.calcular_porcentaje_financiado(edad)
        plazo = calculo.calcular_plazo_financiacion(edad)
        pago = calculo.calcular_pago_mensual(pf, valor_vivienda, plazo)
        intereses, _ = calculo.calcular_intereses(pago, calculo.TASA_EFECTIVA_MENSUAL, plazo)
        # Verificación
        self.assertAlmostEqual(intereses, 183328.1798740009, places=2)

    # =========================
    # CASO 5
    # =========================
    def test_caso_5_porcentaje(self):
        # Entrada
        edad = 65
        # Cálculo
        resultado = calculo.calcular_porcentaje_financiado(edad)
        # Verificación
        self.assertEqual(resultado, 30)

    def test_caso_5_plazo(self):
        # Entrada
        edad = 65
        # Cálculo
        resultado = calculo.calcular_plazo_financiacion(edad)
        # Verificación
        self.assertEqual(resultado, 20)

    def test_caso_5_pago_mensual(self):
        # Entrada
        porcentaje_financiado = 30
        valor_vivienda = 2_000_000_000.0
        plazo = 20
        # Cálculo
        resultado = calculo.calcular_pago_mensual(porcentaje_financiado, valor_vivienda, plazo)
        # Verificación
        self.assertAlmostEqual(resultado, 2_500_000.0, places=6)

    def test_caso_5_intereses(self):
        # Entrada
        edad = 65
        valor_vivienda = 2_000_000_000.0
        # Cálculo
        pf = calculo.calcular_porcentaje_financiado(edad)
        plazo = calculo.calcular_plazo_financiacion(edad)
        pago = calculo.calcular_pago_mensual(pf, valor_vivienda, plazo)
        intereses, _ = calculo.calcular_intereses(pago, calculo.TASA_EFECTIVA_MENSUAL, plazo)
        # Verificación
        self.assertAlmostEqual(intereses, 206833933.6948801, places=2)


    # =========================
    # CASOS DE ERROR (4)
    # =========================
    def test_error_edad_menor_65(self):
        # Entrada
        edad = 62
        # Cálculo + Verificación
        with self.assertRaises(excepciones.ExcepcionPorEdadIncorrectaMenorAMinimina):
            _ = calculo.calcular_porcentaje_financiado(edad)

    def test_error_edad_negativa(self):
        # Entrada
        edad = -70
        # Cálculo + Verificación
        with self.assertRaises(excepciones.ExcepcionPorEdadIncorrectaNegativa):
            _ = calculo.calcular_porcentaje_financiado(edad)
            
    def test_error_valor_vivienda_cero(self):
        # Entrada
        porcentaje_financiado = 55
        valor_vivienda = 0
        plazo = 5
        # Cálculo + Verificación
        with self.assertRaises(ValueError):
            _ = calculo.calcular_pago_mensual(porcentaje_financiado, valor_vivienda, plazo)

    def test_error_valor_vivienda_negativo(self):
        # Entrada
        porcentaje_financiado = 70
        valor_vivienda = -80_000_000
        plazo = 3
        # Cálculo + Verificación
        with self.assertRaises(ValueError):
            _ = calculo.calcular_pago_mensual(porcentaje_financiado, valor_vivienda, plazo)


if __name__ == "__main__":
    unittest.main()
