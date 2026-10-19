import sys 
sys.path.append("src")
from model import excepciones

#Constantes
TASA_EFECTIVA_ANUAL = 0.2478 # Esta expresando en decimal (24.78 %)
TASA_EFECTIVA_MENSUAL = ((1+TASA_EFECTIVA_ANUAL)**(1/12))-1 # Resultado expresado en decimmal

def verificar_edad(edad: int):
    """
    Arroja la excepcion correspondiente al tipo de error por edad

    """
    if edad < 0:
        raise excepciones.ExcepcionPorEdadIncorrectaNegativa(edad)
    
    if edad < 65:
        raise excepciones.ExcepcionPorEdadIncorrectaMenorAMinimina(edad)
    
    if edad >= 115:
        raise excepciones.ExcepcionPorEdadIncorrectaMayorAMaxima(edad)
    
    if isinstance(edad, float):
        raise excepciones.ExcepcionPorEdadIncorrectaDecimal(edad)
    
    if not isinstance(edad, (int)):
        raise excepciones.ExcepcionPorEdadIncorrectaNoNumerica(edad)


def calcular_porcentaje_financiado(edad):
    #Calcula el porcentaje a financiar del total de la vivienda en funcion de la edad del interesado

    verificar_edad(edad)

    if edad >= 65 and edad < 70:
        return 30
    if edad >= 70 and edad < 80:
        return 40
    if edad >= 80 and edad < 85:
        return 55
    if edad >= 85 and edad <115:
        return 70

def calcular_plazo_financiacion(edad):
    #Calcula el plazo en años en el que el banco pagara las cuotas al usuario funcion de la edad del interesado

    verificar_edad(edad)

    if edad >= 65 and edad <70:
        return 20 
    if edad >= 70 and edad <75:
        return 15
    if edad >= 75 and edad <80:
        return 10
    if edad >= 80 and edad <85:
        return 5
    if edad >= 85 and edad <115:
        return 3

def calcular_pago_mensual(porcentaje_financiado, valor_vivienda, plazo):
    #Calcula el plazo en el que el banco pagara las cuotas al usuario funcion de la edad del interesado
    if valor_vivienda < 0:
        raise ValueError("El valor de la vivienda no puede ser negativo")
    if valor_vivienda == 0:
        raise ValueError("El valor de la vivienda no puede ser cero")
    if porcentaje_financiado <= 0:
        raise ValueError("El porcentaje financiado debe ser mayor que cero")
    # Se multiplica el plazo por 12 para pasarlo a meses.
    return (valor_vivienda * porcentaje_financiado / 100) / (plazo * 12)

def calcular_valor_financiado(porcentaje_financiado, valor_vivienda):
    #Calcula el valor de la hipoteca respecto al porcentaje fianciado
    valor_financiado = (porcentaje_financiado/100) * valor_vivienda
    return valor_financiado

def calcular_intereses(pago_mensual, tasa_mensual, plazo, saldo_inicial=0.0):
    #Calcula el interés total y el saldo final con dicho interes
    
    saldo = float(saldo_inicial)
    # Se multiplica el plazo por 12 para pasarlo a meses.
    for _ in range(plazo * 12):
        interes_mes = saldo * tasa_mensual
        saldo += interes_mes + pago_mensual

    interes_siguiente = saldo * tasa_mensual
    saldo_final = saldo + interes_siguiente
    return interes_siguiente, saldo_final

def verificar_valor_vivienda(valor_vivienda: float):
    if valor_vivienda < 50_000_000:
        raise excepciones.ExcepcionPorValorViviendaInvalido(valor_vivienda)
    return True
