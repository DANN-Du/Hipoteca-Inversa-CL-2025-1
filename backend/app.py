import os
import sys
import datetime
from flask import Flask, request, jsonify, render_template, redirect
from flask_cors import CORS
from flasgger import Swagger

# Asegurar que src esté en el path de importaciones
sys.path.append(os.path.join(os.path.dirname(__file__), "src"))
sys.path.append(os.path.dirname(__file__))

from model.solicitante import Solicitante
from model.vivienda import Vivienda
from model import calculo
from model import excepciones
from controller.controlador_solicitante import ControladorSolicitante
from controller.controlador_vivienda import ControladorVivienda

app = Flask(__name__)
CORS(app)

# ============================================================================
# CONFIGURACIÓN DE SWAGGER (OPENAPI)
# ============================================================================
swagger_template = {
    "swagger": "2.0",
    "info": {
        "title": "Hipoteca Inversa CL - API REST & Swagger Documentation",
        "description": (
            "API RESTful para la simulación financiera de hipotecas inversas "
            "según normatividad colombiana (Banco de la República 2025), "
            "gestión de solicitantes (adultos mayores 65+) y registro de viviendas garantía.\n\n"
            "**Autores / Responsables:**\n"
            "- Juan Sebastian Pinilla Giraldo (jpinilla880@soyudemedellin.edu.co) - Desarrollador Líder\n"
            "- Daniel Duque (dduque642@soyudemedellin.edu.co) - Desarrollador\n"
        ),
        "version": "2.0.0",
        "contact": {
            "name": "Equipo Hipoteca Inversa CL",
            "email": "dduque642@soyudemedellin.edu.co"
        }
    },
    "basePath": "/",
    "schemes": ["http", "https"],
    "tags": [
        {"name": "General", "description": "Hola Mundo y chequeo de salud"},
        {"name": "Calculo", "description": "Simulación matemática de hipoteca inversa"},
        {"name": "Solicitantes", "description": "CRUD de adultos mayores solicitantes"},
        {"name": "Viviendas", "description": "CRUD de inmuebles en garantía"},
        {"name": "Pruebas", "description": "Flujo de prueba completo de integración"}
    ]
}

swagger_config = {
    "headers": [],
    "specs": [
        {
            "endpoint": "apispec_1",
            "route": "/apispec_1.json",
            "rule_filter": lambda rule: True,
            "model_filter": lambda tag: True,
        }
    ],
    "static_url_path": "/flasgger_static",
    "swagger_ui": True,
    "specs_route": "/apidocs/"
}

swagger = Swagger(app, template=swagger_template, config=swagger_config)


# ============================================================================
# ENDPOINTS GENERALES (HOLA MUNDO & SALUD)
# ============================================================================
@app.route("/api/v1/hello", methods=["GET"])
def hello_api():
    """Hola Mundo del Backend
    ---
    tags:
      - General
    summary: Retorna el mensaje Hola Mundo del Backend
    description: Verifica que el backend esté arriba y funcionando (requerimiento de entrega).
    responses:
      200:
        description: Mensaje de bienvenida y estado del servicio
        schema:
          type: object
          properties:
            mensaje:
              type: string
              example: ¡Hola Mundo desde el Backend de Hipoteca Inversa CL!
            version:
              type: string
              example: 2.0.0
            timestamp:
              type: string
              example: 2026-10-18T23:50:00Z
            estado:
              type: string
              example: online
    """
    return jsonify({
        "mensaje": "¡Hola Mundo desde el Backend de Hipoteca Inversa CL!",
        "proyecto": "Hipoteca Inversa CL - 2025-1",
        "version": "2.0.0",
        "estado": "online",
        "timestamp": datetime.datetime.now().isoformat()
    }), 200


@app.route("/api/v1/health", methods=["GET"])
def health_check():
    """Chequeo de Salud del Backend y Conexión a Base de Datos
    ---
    tags:
      - General
    summary: Verifica el estado del backend y la conexión con PostgreSQL
    description: Realiza un ping a la base de datos PostgreSQL para garantizar la comunicación.
    responses:
      200:
        description: Backend y base de datos funcionando correctamente
      503:
        description: Error al comunicarse con la base de datos
    """
    db_status = "desconectado"
    db_details = ""
    try:
        cursor = ControladorSolicitante.obtener_cursor()
        cursor.execute("SELECT 1;")
        cursor.fetchone()
        db_status = "conectado"
        db_details = "Conexión a PostgreSQL establecida exitosamente"
    except Exception as e:
        db_status = "error_conexion"
        db_details = str(e)

    status_code = 200 if db_status == "conectado" else 503
    return jsonify({
        "estado_backend": "saludable",
        "base_de_datos": db_status,
        "detalle_bd": db_details,
        "timestamp": datetime.datetime.now().isoformat()
    }), status_code


# ============================================================================
# ENDPOINT DE CÁLCULO DE HIPOTECA INVERSA
# ============================================================================
@app.route("/api/v1/calculo", methods=["POST"])
def calcular_hipoteca_api():
    """Calcular Hipoteca Inversa
    ---
    tags:
      - Calculo
    summary: Simula la hipoteca inversa según edad y valor de la vivienda
    description: Valida edad (65 a 114) y valor mínimo ($50,000,000 COP). Calcula porcentaje, plazo, cuota mensual, intereses y saldo final.
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          required:
            - edad
            - valor_vivienda
          properties:
            edad:
              type: integer
              example: 72
              description: Edad del solicitante en años (65 a 114)
            valor_vivienda:
              type: number
              example: 300000000
              description: Valor comercial del inmueble en COP (mínimo 50,000,000)
    responses:
      200:
        description: Cálculo completado exitosamente
      400:
        description: Datos inválidos de edad o valor de vivienda
    """
    data = request.get_json(silent=True) or request.args.to_dict()
    if not data:
        return jsonify({"error": "No se recibieron datos para el cálculo"}), 400

    try:
        edad = int(data.get("edad"))
    except (TypeError, ValueError):
        return jsonify({"error": "La edad debe ser un número entero válido"}), 400

    try:
        valor_vivienda = float(data.get("valor_vivienda"))
    except (TypeError, ValueError):
        return jsonify({"error": "El valor de la vivienda debe ser un número válido"}), 400

    # Validar edad y valor de vivienda
    try:
        calculo.verificar_edad(edad)
        calculo.verificar_valor_vivienda(valor_vivienda)
    except Exception as e:
        return jsonify({"error": str(e)}), 400

    porcentaje = calculo.calcular_porcentaje_financiado(edad)
    plazo = calculo.calcular_plazo_financiacion(edad)
    pago_mensual = calculo.calcular_pago_mensual(porcentaje, valor_vivienda, plazo)
    valor_financiado = calculo.calcular_valor_financiado(porcentaje, valor_vivienda)
    intereses, saldo_final = calculo.calcular_intereses(
        pago_mensual=pago_mensual,
        tasa_mensual=calculo.TASA_EFECTIVA_MENSUAL,
        plazo=plazo
    )

    return jsonify({
        "edad": edad,
        "valor_vivienda": valor_vivienda,
        "porcentaje_financiado": porcentaje,
        "plazo_anios": plazo,
        "plazo_meses": plazo * 12,
        "valor_financiado": valor_financiado,
        "pago_mensual": round(pago_mensual, 2),
        "intereses_totales": round(intereses, 2),
        "saldo_final_proyectado": round(saldo_final, 2),
        "tasa_efectiva_anual": "24.78%",
        "tasa_efectiva_mensual": f"{calculo.TASA_EFECTIVA_MENSUAL * 100:.2f}%"
    }), 200


# ============================================================================
# ENDPOINTS DE SOLICITANTES (CRUD)
# ============================================================================
@app.route("/api/v1/solicitantes", methods=["GET"])
def listar_solicitantes():
    """Listar Solicitantes
    ---
    tags:
      - Solicitantes
    summary: Retorna todos los solicitantes registrados en la BD
    responses:
      200:
        description: Lista de solicitantes
      500:
        description: Error al consultar la base de datos
    """
    try:
        solicitantes = ControladorSolicitante.listar_todos()
        return jsonify([s.to_dict() for s in solicitantes]), 200
    except Exception as e:
        return jsonify({"error": f"Error al consultar solicitantes: {str(e)}"}), 500


@app.route("/api/v1/solicitantes", methods=["POST"])
def crear_solicitante_api():
    """Registrar Solicitante
    ---
    tags:
      - Solicitantes
    summary: Crea un nuevo solicitante en la base de datos
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          required:
            - nombre
            - identificacion
            - fecha_nacimiento
            - edad
          properties:
            nombre:
              type: string
              example: Beatriz Elena Montoya
            identificacion:
              type: string
              example: "1022345678"
            fecha_nacimiento:
              type: string
              example: "1953-03-12"
            edad:
              type: integer
              example: 72
    responses:
      201:
        description: Solicitante registrado exitosamente
      400:
        description: Datos inválidos
      500:
        description: Error al insertar en la base de datos
    """
    data = request.get_json(silent=True) or request.form.to_dict()
    if not data:
        return jsonify({"error": "Cuerpo de solicitud requerido"}), 400

    nombre = data.get("nombre", "").strip()
    identificacion = str(data.get("identificacion", "")).strip()
    fecha_nacimiento = str(data.get("fecha_nacimiento", "")).strip()
    edad_val = data.get("edad")

    if not nombre or not identificacion or not fecha_nacimiento or edad_val is None:
        return jsonify({"error": "Todos los campos (nombre, identificacion, fecha_nacimiento, edad) son obligatorios"}), 400

    try:
        edad = int(edad_val)
    except ValueError:
        return jsonify({"error": "La edad debe ser un número entero"}), 400

    solicitante = Solicitante(
        nombre=nombre,
        identificacion=identificacion,
        fecha_nacimiento=fecha_nacimiento,
        edad=edad
    )

    try:
        ControladorSolicitante.insertar(solicitante)
        return jsonify({
            "mensaje": "Solicitante registrado exitosamente",
            "solicitante": solicitante.to_dict()
        }), 201
    except Exception as e:
        return jsonify({"error": f"Error al guardar solicitante: {str(e)}"}), 500


@app.route("/api/v1/solicitantes/<identificacion>", methods=["GET"])
def buscar_solicitante_api(identificacion):
    """Buscar Solicitante por Identificación
    ---
    tags:
      - Solicitantes
    summary: Obtiene los datos de un solicitante a partir de su cédula
    parameters:
      - in: path
        name: identificacion
        type: string
        required: true
        description: Cédula o número de identificación
    responses:
      200:
        description: Solicitante encontrado
      404:
        description: Solicitante no encontrado
    """
    try:
        solicitante = ControladorSolicitante.buscar_por_cedula(identificacion)
        if not solicitante:
            return jsonify({"error": f"No se encontró solicitante con identificación {identificacion}"}), 404
        return jsonify(solicitante.to_dict()), 200
    except Exception as e:
        return jsonify({"error": f"Error en la consulta: {str(e)}"}), 500


@app.route("/api/v1/solicitantes/<identificacion>", methods=["PUT"])
def modificar_solicitante_api(identificacion):
    """Modificar Solicitante
    ---
    tags:
      - Solicitantes
    summary: Actualiza los datos de un solicitante existente
    parameters:
      - in: path
        name: identificacion
        type: string
        required: true
      - in: body
        name: body
        required: true
        schema:
          type: object
          properties:
            nombre:
              type: string
            fecha_nacimiento:
              type: string
            edad:
              type: integer
    responses:
      200:
        description: Solicitante actualizado exitosamente
      404:
        description: Solicitante no encontrado
    """
    data = request.get_json(silent=True) or request.form.to_dict()
    try:
        solicitante = Solicitante(
            nombre=data.get("nombre"),
            identificacion=identificacion,
            fecha_nacimiento=data.get("fecha_nacimiento"),
            edad=int(data.get("edad"))
        )
        ControladorSolicitante.modificar_datos(solicitante)
        return jsonify({"mensaje": "Solicitante actualizado exitosamente", "solicitante": solicitante.to_dict()}), 200
    except ValueError as ve:
        return jsonify({"error": str(ve)}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ============================================================================
# ENDPOINTS DE VIVIENDAS (CRUD)
# ============================================================================
@app.route("/api/v1/viviendas", methods=["GET"])
def listar_viviendas():
    """Listar Viviendas
    ---
    tags:
      - Viviendas
    summary: Retorna todas las viviendas registradas en garantía
    responses:
      200:
        description: Lista de viviendas
      500:
        description: Error al consultar viviendas
    """
    try:
        viviendas = ControladorVivienda.listar_todas()
        return jsonify([v.to_dict() for v in viviendas]), 200
    except Exception as e:
        return jsonify({"error": f"Error al consultar viviendas: {str(e)}"}), 500


@app.route("/api/v1/viviendas", methods=["POST"])
def crear_vivienda_api():
    """Registrar Vivienda en Garantía
    ---
    tags:
      - Viviendas
    summary: Registra un inmueble asociado al solicitante propietario
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          required:
            - ciudad
            - barrio
            - direccion
            - identificacion_propietario
            - valor
          properties:
            ciudad:
              type: string
              example: Medellín
            barrio:
              type: string
              example: El Poblado
            direccion:
              type: string
              example: Cra 43A # 1-50
            identificacion_propietario:
              type: string
              example: "1022345678"
            valor:
              type: number
              example: 350000000
    responses:
      201:
        description: Vivienda registrada exitosamente
      400:
        description: Datos inválidos o propietario inexistente
    """
    data = request.get_json(silent=True) or request.form.to_dict()
    if not data:
        return jsonify({"error": "Cuerpo de solicitud requerido"}), 400

    ciudad = data.get("ciudad", "").strip()
    barrio = data.get("barrio", "").strip()
    direccion = data.get("direccion", "").strip()
    identificacion_propietario = str(data.get("identificacion_propietario", "")).strip()
    valor_val = data.get("valor")

    if not ciudad or not barrio or not direccion or not identificacion_propietario or valor_val is None:
        return jsonify({"error": "Todos los campos de la vivienda son obligatorios"}), 400

    try:
        valor = float(valor_val)
        calculo.verificar_valor_vivienda(valor)
    except Exception as e:
        return jsonify({"error": str(e)}), 400

    vivienda = Vivienda(
        ciudad=ciudad,
        barrio=barrio,
        direccion=direccion,
        identificacion_propietario=identificacion_propietario,
        valor=valor
    )

    try:
        ControladorVivienda.insertar(vivienda)
        return jsonify({
            "mensaje": "Vivienda registrada exitosamente",
            "vivienda": vivienda.to_dict()
        }), 201
    except Exception as e:
        return jsonify({"error": f"Error al guardar vivienda (verifique que el propietario exista): {str(e)}"}), 400


@app.route("/api/v1/viviendas/<path:direccion>", methods=["GET"])
def buscar_vivienda_direccion(direccion):
    """Buscar Vivienda por Dirección
    ---
    tags:
      - Viviendas
    summary: Retorna los datos de una vivienda según su dirección única
    parameters:
      - in: path
        name: direccion
        type: string
        required: true
    responses:
      200:
        description: Vivienda encontrada
      404:
        description: Vivienda no encontrada
    """
    try:
        vivienda = ControladorVivienda.buscar_por_direccion(direccion)
        if not vivienda:
            return jsonify({"error": f"No se encontró vivienda con dirección {direccion}"}), 404
        return jsonify(vivienda.to_dict()), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/v1/viviendas/propietario/<identificacion>", methods=["GET"])
def buscar_viviendas_propietario(identificacion):
    """Buscar Viviendas por Cédula del Propietario
    ---
    tags:
      - Viviendas
    summary: Retorna la lista de viviendas pertenecientes a un solicitante
    parameters:
      - in: path
        name: identificacion
        type: string
        required: true
    responses:
      200:
        description: Lista de viviendas del propietario
    """
    try:
        viviendas = ControladorVivienda.buscar_por_propietario(identificacion)
        return jsonify([v.to_dict() for v in viviendas]), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ============================================================================
# FLUJO COMPLETO DE PRUEBA (FRONTEND <-> BACKEND <-> BD)
# ============================================================================
@app.route("/api/v1/flujo-prueba", methods=["POST"])
def ejecutar_flujo_prueba():
    """Ejecutar Flujo Completo de Prueba
    ---
    tags:
      - Pruebas
    summary: Ejecuta un flujo end-to-end de prueba entre componentes
    description: Inserta un solicitante y vivienda de prueba, ejecuta el cálculo financiero y verifica la persistencia en PostgreSQL.
    responses:
      200:
        description: Flujo de prueba completado exitosamente
      500:
        description: Falló algún paso del flujo de prueba
    """
    cedula_prueba = f"TEST{int(datetime.datetime.now().timestamp())}"
    direccion_prueba = f"Callejon de Prueba #{cedula_prueba[-4:]}"

    pasos = []
    try:
        # Paso 1: Crear solicitante de prueba
        solicitante_prueba = Solicitante(
            nombre="Usuario Prueba Automatizada",
            identificacion=cedula_prueba,
            fecha_nacimiento=datetime.date(1955, 6, 15),
            edad=71
        )
        ControladorSolicitante.insertar(solicitante_prueba)
        pasos.append({"paso": 1, "descripcion": "Crear Solicitante en BD", "estado": "OK", "identificacion": cedula_prueba})

        # Paso 2: Crear vivienda de prueba
        vivienda_prueba = Vivienda(
            ciudad="Medellín",
            barrio="Laureles",
            direccion=direccion_prueba,
            identificacion_propietario=cedula_prueba,
            valor=250000000.0
        )
        ControladorVivienda.insertar(vivienda_prueba)
        pasos.append({"paso": 2, "descripcion": "Crear Vivienda vinculada a Solicitante en BD", "estado": "OK", "direccion": direccion_prueba})

        # Paso 3: Consultar solicitante insertado
        encontrado = ControladorSolicitante.buscar_por_cedula(cedula_prueba)
        assert encontrado is not None, "El solicitante no fue encontrado tras inserción"
        pasos.append({"paso": 3, "descripcion": "Verificar lectura parametrizada de Solicitante", "estado": "OK"})

        # Paso 4: Calcular hipoteca
        porcentaje = calculo.calcular_porcentaje_financiado(71)
        plazo = calculo.calcular_plazo_financiacion(71)
        cuota = calculo.calcular_pago_mensual(porcentaje, 250000000.0, plazo)
        intereses, saldo = calculo.calcular_intereses(cuota, calculo.TASA_EFECTIVA_MENSUAL, plazo)
        pasos.append({
            "paso": 4,
            "descripcion": "Ejecución de cálculo matemático de hipoteca",
            "estado": "OK",
            "calculo": {
                "porcentaje": porcentaje,
                "plazo": plazo,
                "cuota_mensual": round(cuota, 2),
                "intereses": round(intereses, 2),
                "saldo_final": round(saldo, 2)
            }
        })

        return jsonify({
            "resultado": "EXITOSO",
            "mensaje": "Flujo de prueba completo ejecutado y verificado (Frontend <-> Backend <-> Base de Datos)",
            "pasos": pasos
        }), 200

    except Exception as e:
        return jsonify({
            "resultado": "FALLIDO",
            "mensaje": f"Error en la ejecución del flujo de prueba: {str(e)}",
            "pasos": pasos
        }), 500


@app.route("/api/v1/crear_tablas", methods=["POST", "GET"])
def api_crear_tablas():
    """Inicializar Tablas en la Base de Datos
    ---
    tags:
      - General
    summary: Crea las tablas solicitantes y viviendas en PostgreSQL si no existen
    responses:
      200:
        description: Tablas creadas exitosamente
    """
    try:
        ControladorSolicitante.crear_tabla()
        ControladorVivienda.crear_tabla()
        return jsonify({"mensaje": "Tablas solicitantes y viviendas creadas exitosamente"}), 200
    except Exception as e:
        return jsonify({"error": f"Error al crear tablas: {str(e)}"}), 500


# ============================================================================
# RUTAS WEB TRADICIONALES (RETROCOMPATIBILIDAD)
# ============================================================================
@app.route("/")
def home():
    try:
        return render_template("index.html")
    except Exception:
        return redirect("/apidocs/")


@app.route("/calculo")
def calculo_view():
    return render_template("calculo.html")


@app.route("/crear_solicitante")
def crear_solicitante_view():
    return render_template("crear_solicitante.html")


@app.route("/guardar_solicitante")
def guardar_solicitante():
    try:
        solicitante = Solicitante(
            nombre=request.args["nombre"],
            identificacion=request.args["identificacion"],
            fecha_nacimiento=request.args["fecha_nacimiento"],
            edad=int(request.args["edad"])
        )
        ControladorSolicitante.insertar(solicitante)
        return "Solicitante insertado exitosamente"
    except Exception as e:
        return f"Error al insertar solicitante: {e}", 400


@app.route("/buscar_solicitante")
def buscar_solicitante():
    identificacion = request.args.get("identificacion_buscada", "")
    solicitante_encontrado = ControladorSolicitante.buscar_por_cedula(identificacion)
    return render_template("solitante_buscado.html", solicitante=solicitante_encontrado)


@app.route("/calcular_hipoteca")
def calcular_hipoteca():
    try:
        edad = int(request.args["edad"])
        valor_vivienda = float(request.args["valor_vivienda"])

        porcentaje = calculo.calcular_porcentaje_financiado(edad)
        plazo = calculo.calcular_plazo_financiacion(edad)
        pago_mensual = calculo.calcular_pago_mensual(porcentaje, valor_vivienda, plazo)
        intereses, saldo_final = calculo.calcular_intereses(
            pago_mensual, calculo.TASA_EFECTIVA_MENSUAL, plazo
        )

        return (
            f"<h2>Resultado del cálculo</h2>"
            f"Edad: {edad} años<br>"
            f"Valor de la vivienda: ${valor_vivienda:,.0f} COP<br>"
            f"Porcentaje financiado: {porcentaje}%<br>"
            f"Plazo: {plazo} años ({plazo*12} meses)<br>"
            f"<b>Valor mensual recibido: ${pago_mensual:,.0f} COP</b><br>"
            f"Intereses proyectados: ${intereses:,.0f} COP<br>"
            f"Saldo final proyectado: ${saldo_final:,.0f} COP<br>"
            f"<br><a href='/calculo'>Volver a calcular</a> | <a href='/'>Inicio</a>"
        )
    except Exception as e:
        return f"<h3>Error en el cálculo:</h3><p>{e}</p><br><a href='/calculo'>Volver</a>", 400


@app.route("/crear_tablas")
def crear_tablas():
    try:
        ControladorSolicitante.crear_tabla()
        ControladorVivienda.crear_tabla()
        return "Tablas creadas exitosamente"
    except Exception as e:
        return f"Error al crear tablas: {e}", 500


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
