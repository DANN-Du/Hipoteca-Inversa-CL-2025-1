import os
import sys
import threading
import time
import pytest
from playwright.sync_api import sync_playwright, expect
from flask import send_from_directory

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "backend")))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "backend", "src")))

try:
    from backend.app import app
except ImportError:
    from app import app

# Configurar Flask para servir el frontend estático durante la prueba E2E
frontend_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "frontend", "src"))

@app.route("/e2e/<path:filename>")
def serve_e2e_frontend(filename):
    return send_from_directory(frontend_dir, filename)

@app.route("/e2e/")
def serve_e2e_index():
    return send_from_directory(frontend_dir, "index.html")

TEST_PORT = 5005
TEST_HOST = f"http://127.0.0.1:{TEST_PORT}"

_server_started = False

def start_test_server():
    global _server_started
    if not _server_started:
        thread = threading.Thread(
            target=lambda: app.run(host="127.0.0.1", port=TEST_PORT, debug=False, use_reloader=False),
            daemon=True
        )
        thread.start()
        _server_started = True
        time.sleep(1.5)  # Esperar a que el servidor esté listo

@pytest.fixture(scope="module")
def browser_context():
    start_test_server()
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context()
        yield context
        browser.close()

def _iniciar_sesion(page, usuario, password):
    page.click("#btnOpenLogin")
    page.fill("#loginUsuario", usuario)
    page.fill("#loginPassword", password)
    page.click("#btnSubmitLogin")

def test_e2e_carga_inicial_hola_mundo(browser_context):
    """Verifica la carga inicial en Simulador, pestaña Inicio y estado como Desarrollador."""
    page = browser_context.new_page()
    page.goto(f"{TEST_HOST}/e2e/")

    # Verificar título de la página
    expect(page).to_have_title("Hipoteca Inversa | Plataforma Financiera")

    # Al abrir sin sesión debe mostrarse Inicio primero y el botón de Iniciar sesión
    expect(page.locator("#tab-inicio")).to_be_visible()
    expect(page.locator("#btnOpenLogin")).to_be_visible()

    # Verificar pantalla de bienvenida en pestaña Inicio
    hero_title = page.locator(".hero-title")
    expect(hero_title).to_be_visible()
    expect(hero_title).to_contain_text("Bienvenido a tu Plataforma de Hipoteca Inversa")

    # Iniciar sesión como desarrollador para verificar estado del Frontend
    _iniciar_sesion(page, "dev", "Dev2025*")
    card_frontend = page.locator("#cardFrontend")
    expect(card_frontend).to_be_visible()
    expect(card_frontend).to_contain_text("Online · Puerto 80")
    page.close()

def test_e2e_simulador_calculo_exitoso(browser_context):
    """Verifica el flujo completo de cálculo desde el formulario frontend."""
    page = browser_context.new_page()
    page.goto(f"{TEST_HOST}/e2e/")

    # Cambiar a la pestaña de Simulador
    page.click("button[data-tab='tab-simulador']")

    # Llenar formulario con edad 72 y valor 300,000,000 COP
    page.fill("#calcEdad", "72")
    page.fill("#calcValor", "300000000")

    # Presionar botón de calcular
    page.click("#btnCalcular")

    # Esperar y verificar resultados
    resultados = page.locator("#calculoResultados")
    expect(resultados).to_be_visible(timeout=5000)

    # Verificar valores calculados
    expect(page.locator("#resPorcentaje")).to_contain_text("40%")
    expect(page.locator("#resPlazo")).to_contain_text("15 años")
    expect(page.locator("#resPagoMensual")).to_contain_text("$")
    expect(page.locator("#resIntereses")).to_contain_text("$")
    expect(page.locator("#resSaldoFinal")).to_contain_text("$")
    page.close()

def test_e2e_navegacion_pestanas(browser_context):
    """Verifica la navegación por roles (Asesor, Desarrollador y Administrador)."""
    page = browser_context.new_page()
    page.goto(f"{TEST_HOST}/e2e/")

    # Iniciar sesión como Asesor y navegar a Solicitantes y Viviendas
    _iniciar_sesion(page, "asesor", "Asesor2025*")
    page.click("button[data-tab='tab-solicitantes']")
    expect(page.locator("#tab-solicitantes h2").first).to_contain_text("Registrar Solicitante")
    expect(page.locator("#tablaSolicitantes")).to_be_visible()

    page.click("button[data-tab='tab-viviendas']")
    expect(page.locator("#tab-viviendas h2").first).to_contain_text("Registrar Vivienda en Garantía")
    expect(page.locator("#tablaViviendas")).to_be_visible()

    # Cerrar sesión e iniciar como Desarrollador para navegar a Flujo de Prueba
    page.click("#btnLogout")
    _iniciar_sesion(page, "dev", "Dev2025*")
    page.click("button[data-tab='tab-flujo-prueba']")
    expect(page.locator("#btnEjecutarFlujo")).to_be_visible()

    # Cerrar sesión e iniciar como Admin para verificar creación/eliminación de usuarios
    page.click("#btnLogout")
    _iniciar_sesion(page, "admin", "Admin2025*")
    expect(page.locator("#tab-admin")).to_be_visible()
    page.fill("#adminNombre", "Nuevo Asesor")
    page.fill("#adminUsuario", "nuevo.asesor")
    page.fill("#adminPassword", "Clave1234")
    page.select_option("#adminRol", "asesor")
    page.click("#formCrearUsuario button[type='submit']")
    expect(page.locator("#tbodyUsuariosAdmin")).to_contain_text("nuevo.asesor")
    page.close()
