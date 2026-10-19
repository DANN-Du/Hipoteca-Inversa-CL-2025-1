import sys 
sys.path.append("src")

from model import calculo, excepciones

def main():
    print("=== Calculadora Hipoteca Inversa ===")

    try:
        # Entradas
        edad = int(input("Ingrese la edad: "))
        valor_vivienda = float(input("Ingrese el valor de la vivienda: "))
        
        # Validaciones
        calculo.verificar_valor_vivienda(valor_vivienda)   # ✅ validación de vivienda
        porcentaje_financiado = calculo.calcular_porcentaje_financiado(edad)
        plazo_anios = calculo.calcular_plazo_financiacion(edad)

        # Cálculos
        pago_mensual = calculo.calcular_pago_mensual(porcentaje_financiado, valor_vivienda, plazo_anios)
        intereses_totales, saldo_final = calculo.calcular_intereses(
            pago_mensual,
            calculo.TASA_EFECTIVA_MENSUAL,
            plazo_anios
        )

        # Salidas
        print("\n--- Resultados ---")
        print(f"Porcentaje financiado: {porcentaje_financiado}%")
        print(f"Plazo en años: {plazo_anios}")
        print(f"Pago mensual: ${pago_mensual:,.2f}")
        print(f"Intereses Totales: ${intereses_totales:,.2f}")
        print(f"Saldo Final: ${saldo_final:,.2f}")

    except ValueError as e:
        print(f"Error: {e}")

    # Excepciones personalizadas
    except excepciones.ExcepcionPorEdadIncorrectaNegativa as e:
        print(f"Error: {e}")
    except excepciones.ExcepcionPorEdadIncorrectaMenorAMinimina as e:
        print(f"Error: {e}")
    except excepciones.ExcepcionPorEdadIncorrectaMayorAMaxima as e:
        print(f"Error: {e}")
    except excepciones.ExcepcionPorEdadIncorrectaDecimal as e:
        print(f"Error: {e}")
    except excepciones.ExcepcionPorEdadIncorrectaNoNumerica as e:
        print(f"Error: {e}")
    except excepciones.ExcepcionPorValorViviendaInvalido as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
