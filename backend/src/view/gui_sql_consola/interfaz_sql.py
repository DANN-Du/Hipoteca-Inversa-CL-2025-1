import sys
from datetime import datetime

sys.path.append("src")

from model.solicitante import Solicitante
from controller.controlador_solicitante import ControladorSolicitante
from model.vivienda import Vivienda
from controller.controlador_vivienda import ControladorVivienda

# Reglas mínimas
MIN_VALOR_VIVIENDA = 50_000_000
MIN_EDAD_SOLICITANTE = 65


def input_date(prompt: str):
    while True:
        s = input(prompt + " (YYYY-MM-DD): ")
        try:
            return datetime.strptime(s, "%Y-%m-%d").date()
        except Exception:
            print("Formato inválido. Intente de nuevo.")


def ensure_tables_exist():
    """Crea las tablas solicitantes y viviendas si no existen (usa controladores)."""
    try:
        ControladorSolicitante.crear_tabla()
    except Exception as e:
        print("Advertencia: no se pudo crear la tabla solicitantes automáticamente:", e)
    try:
        ControladorVivienda.crear_tabla()
    except Exception as e:
        print("Advertencia: no se pudo crear la tabla viviendas automáticamente:", e)


def insertar_solicitante():
    print("-- Insertar Solicitante --")
    nombre = input("Nombre: ")
    identificacion = input("Identificacion: ")
    fecha_nac = input_date("Fecha de nacimiento")
    edad = int(input("Edad: "))
    if edad < MIN_EDAD_SOLICITANTE:
        print(f"La edad mínima para solicitantes es {MIN_EDAD_SOLICITANTE}. Operación cancelada.")
        return
    s = Solicitante(nombre=nombre, identificacion=identificacion, fecha_nacimiento=fecha_nac, edad=edad)
    ControladorSolicitante.insertar(s)
    print("Solicitante insertado.")


def modificar_solicitante():
    print("-- Modificar Solicitante --")
    identificacion = input("Identificacion del solicitante a modificar: ")
    existente = ControladorSolicitante.buscar_por_cedula(identificacion)
    if existente is None:
        print("Solicitante no encontrado.")
        return
    nombre = input(f"Nombre [{existente.nombre}]: ") or existente.nombre
    fecha_nac = input(f"Fecha de nacimiento [{existente.fecha_nacimiento} - YYYY-MM-DD]: ")
    if fecha_nac.strip():
        fecha_nac = datetime.strptime(fecha_nac, "%Y-%m-%d").date()
    else:
        fecha_nac = existente.fecha_nacimiento
    edad = input(f"Edad [{existente.edad}]: ")
    edad = int(edad) if edad.strip() else existente.edad
    if edad < MIN_EDAD_SOLICITANTE:
        print(f"La edad mínima para solicitantes es {MIN_EDAD_SOLICITANTE}. Operación cancelada.")
        return
    s = Solicitante(nombre=nombre, identificacion=identificacion, fecha_nacimiento=fecha_nac, edad=edad)
    ControladorSolicitante.modificar_datos(s)
    print("Solicitante actualizado.")


def buscar_solicitante():
    print("-- Buscar Solicitante --")
    identificacion = input("Identificacion: ")
    encontrado = ControladorSolicitante.buscar_por_cedula(identificacion)
    if encontrado is None:
        print("No se encontró solicitante con esa identificacion.")
        return
    print(f"Nombre: {encontrado.nombre}")
    print(f"Identificacion: {encontrado.identificacion}")
    print(f"Fecha nacimiento: {encontrado.fecha_nacimiento}")
    print(f"Edad: {encontrado.edad}")


def insertar_vivienda():
    print("-- Insertar Vivienda --")
    ciudad = input("Ciudad: ")
    barrio = input("Barrio: ")
    direccion = input("Direccion: ")
    identificacion_propietario = input("Identificacion propietario: ")
    try:
        valor = int(input("Valor: "))
    except ValueError:
        print("Valor inválido. Operación cancelada.")
        return
    if valor < MIN_VALOR_VIVIENDA:
        print(f"El valor mínimo permitido es {MIN_VALOR_VIVIENDA:,}. Operación cancelada.")
        return

    # Asegurar que el propietario exista
    propietario = ControladorSolicitante.buscar_por_cedula(identificacion_propietario)
    if propietario is None:
        print("No existe un solicitante con esa identificacion.")
        crear = input("¿Desea crear el solicitante ahora? (s/n): ")
        if crear.lower() != 's':
            print("Operación cancelada.")
            return
        # Pedir datos mínimos para crear propietario
        nombre = input("Nombre del propietario: ")
        fecha_nac = input_date("Fecha de nacimiento")
        try:
            edad = int(input("Edad: "))
        except ValueError:
            print("Edad inválida. Operación cancelada.")
            return
        if edad < MIN_EDAD_SOLICITANTE:
            print(f"La edad mínima para solicitantes es {MIN_EDAD_SOLICITANTE}. Operación cancelada.")
            return
        nuevo = Solicitante(nombre=nombre, identificacion=identificacion_propietario, fecha_nacimiento=fecha_nac, edad=edad)
        ControladorSolicitante.insertar(nuevo)

    v = Vivienda(ciudad=ciudad, barrio=barrio, direccion=direccion, identificacion_propietario=identificacion_propietario, valor=valor)
    ControladorVivienda.insertar(v)
    print("Vivienda insertada.")


def modificar_vivienda():
    print("-- Modificar Vivienda --")
    direccion = input("Direccion de la vivienda a modificar: ")
    existente = ControladorVivienda.buscar_por_direccion(direccion)
    if existente is None:
        print("Vivienda no encontrada.")
        return
    ciudad = input(f"Ciudad [{existente.ciudad}]: ") or existente.ciudad
    barrio = input(f"Barrio [{existente.barrio}]: ") or existente.barrio
    identificacion_propietario = input(f"Identificacion propietario [{existente.identificacion_propietario}]: ") or existente.identificacion_propietario
    valor = input(f"Valor [{existente.valor}]: ")
    valor = int(valor) if valor.strip() else existente.valor
    if valor < MIN_VALOR_VIVIENDA:
        print(f"El valor mínimo permitido es {MIN_VALOR_VIVIENDA:,}. Operación cancelada.")
        return
    # Asegurar propietario
    propietario = ControladorSolicitante.buscar_por_cedula(identificacion_propietario)
    if propietario is None:
        print("No existe un solicitante con esa identificacion.")
        crear = input("¿Desea crear el solicitante ahora? (s/n): ")
        if crear.lower() != 's':
            print("Operación cancelada.")
            return
        nombre = input("Nombre del propietario: ")
        fecha_nac = input_date("Fecha de nacimiento")
        try:
            edad = int(input("Edad: "))
        except ValueError:
            print("Edad inválida. Operación cancelada.")
            return
        if edad < MIN_EDAD_SOLICITANTE:
            print(f"La edad mínima para solicitantes es {MIN_EDAD_SOLICITANTE}. Operación cancelada.")
            return
        nuevo = Solicitante(nombre=nombre, identificacion=identificacion_propietario, fecha_nacimiento=fecha_nac, edad=edad)
        ControladorSolicitante.insertar(nuevo)
    v = Vivienda(ciudad=ciudad, barrio=barrio, direccion=direccion, identificacion_propietario=identificacion_propietario, valor=valor)
    ControladorVivienda.modificar_datos(v)
    print("Vivienda actualizada.")


def buscar_vivienda():
    print("-- Buscar Vivienda --")
    direccion = input("Direccion: ")
    encontrado = ControladorVivienda.buscar_por_direccion(direccion)
    if encontrado is None:
        print("No se encontró vivienda con esa direccion.")
        return
    print(f"Ciudad: {encontrado.ciudad}")
    print(f"Barrio: {encontrado.barrio}")
    print(f"Direccion: {encontrado.direccion}")
    print(f"Identificacion propietario: {encontrado.identificacion_propietario}")
    print(f"Valor: {encontrado.valor}")


def main_menu():
    # Intentar crear tablas si no existen
    ensure_tables_exist()
    while True:
        print("\n--- Interfaz SQL Consola ---")
        print("1) Solicitante - Insertar")
        print("2) Solicitante - Modificar")
        print("3) Solicitante - Buscar")
        print("4) Vivienda - Insertar")
        print("5) Vivienda - Modificar")
        print("6) Vivienda - Buscar")
        print("0) Salir")
        opt = input("Seleccione una opción: ")
        try:
            if opt == "1":
                insertar_solicitante()
            elif opt == "2":
                modificar_solicitante()
            elif opt == "3":
                buscar_solicitante()
            elif opt == "4":
                insertar_vivienda()
            elif opt == "5":
                modificar_vivienda()
            elif opt == "6":
                buscar_vivienda()
            elif opt == "0":
                print("Saliendo...")
                break
            else:
                print("Opción inválida")
        except Exception as e:
            print(f"Ocurrió un error: {e}")


if __name__ == "__main__":
    main_menu()
