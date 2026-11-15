# ==============================================================================
# Script de Prueba End-to-End (E2E) en Minikube / Kubernetes
# Proyecto: Hipoteca Inversa CL - Demostración Técnica (D5 / D8)
# ==============================================================================
param(
    [string]$BaseUrl = ""
)

Write-Host "==================================================================" -ForegroundColor Cyan
Write-Host " 🧪 Iniciando Verificación End-to-End en Kubernetes (Minikube)" -ForegroundColor Cyan
Write-Host "==================================================================" -ForegroundColor Cyan

# 1. Determinar URL base
if (-not $BaseUrl) {
    try {
        $ip = minikube ip 2>$null
        if ($ip) {
            $BaseUrl = "http://${ip}:30080"
        }
    } catch {}
}

if (-not $BaseUrl) {
    $BaseUrl = "http://localhost:8080"
    Write-Host "ℹ️  Usando URL por defecto: $BaseUrl (asegúrese de haber hecho port-forward si no corre minikube service)" -ForegroundColor Yellow
} else {
    Write-Host "ℹ️  Conectando al servicio en: $BaseUrl" -ForegroundColor Green
}

$passed = 0
$total = 0

function Assert-Test {
    param(
        [string]$Name,
        [scriptblock]$Block
    )
    $script:total++
    Write-Host -NoNewline "[$script:total] $Name ... "
    try {
        & $Block
        Write-Host "PASSED (OK)" -ForegroundColor Green
        $script:passed++
    } catch {
        Write-Host "FAILED" -ForegroundColor Red
        Write-Host "      Detalle del error: $_" -ForegroundColor Red
    }
}

# TEST 1: Frontend Web HTTP 200
Assert-Test "Frontend Web accesible vía HTTP (UI Nginx)" {
    $res = Invoke-WebRequest -Uri "$BaseUrl/" -UseBasicParsing -TimeoutSec 10
    if ($res.StatusCode -ne 200) { throw "Código HTTP $($res.StatusCode)" }
    if ($res.Content -notmatch "Hipoteca Inversa CL") { throw "Contenido no coincide con la aplicación" }
}

# TEST 2: Backend Healthcheck (API y DB PostgreSQL)
Assert-Test "Backend Health Check (/api/v1/health)" {
    $res = Invoke-RestMethod -Uri "$BaseUrl/api/v1/health" -Method Get -TimeoutSec 10
    if ($res.estado_backend -ne "saludable") { throw "Backend no saludable: $($res.estado_backend)" }
    if ($res.base_de_datos -ne "conectado") { throw "Base de datos no conectada: $($res.base_de_datos)" }
}

# TEST 3: Endpoint Hola Mundo (/api/v1/hello)
Assert-Test "Backend Hola Mundo (/api/v1/hello)" {
    $res = Invoke-RestMethod -Uri "$BaseUrl/api/v1/hello" -Method Get -TimeoutSec 10
    if ($res.estado -ne "online") { throw "Estado no online" }
    if ($res.mensaje -notmatch "Hola Mundo") { throw "Mensaje de bienvenida ausente" }
}

# TEST 4: Swagger Documentation (/apidocs/ y /apispec_1.json)
Assert-Test "Documentación Swagger OpenAPI (/apidocs/ y /apispec_1.json)" {
    $resUi = Invoke-WebRequest -Uri "$BaseUrl/apidocs/" -UseBasicParsing -TimeoutSec 10
    if ($resUi.StatusCode -ne 200) { throw "Swagger UI no disponible" }
    $resSpec = Invoke-RestMethod -Uri "$BaseUrl/apispec_1.json" -Method Get -TimeoutSec 10
    if (-not $resSpec.paths."/api/v1/calculo") { throw "Endpoint /api/v1/calculo no documentado en OpenAPI" }
}

# TEST 5: Simulación Financiera con Parámetros Válidos (72 años / $300M COP)
Assert-Test "Cálculo Financiero de Hipoteca Inversa (Caso Válido: 72 años, $300M)" {
    $body = @{ edad = 72; valor_vivienda = 300000000.0 } | ConvertTo-Json
    $res = Invoke-RestMethod -Uri "$BaseUrl/api/v1/calculo" -Method Post -Body $body -ContentType "application/json" -TimeoutSec 10
    if ($res.porcentaje_financiado -ne 40) { throw "Porcentaje financiado incorrecto: $($res.porcentaje_financiado)" }
    if ($res.plazo_anios -ne 15) { throw "Plazo incorrecto: $($res.plazo_anios)" }
    if ($res.pago_mensual -le 0) { throw "Pago mensual inválido" }
    if ($res.intereses_totales -le 0) { throw "Intereses no calculados" }
    if ($res.saldo_final_proyectado -le $res.valor_financiado) { throw "Saldo final proyectado inconsistente" }
}

# TEST 6: Manejo Controlado de Error - Edad Menor a 65
Assert-Test "Manejo Controlado de Error (Edad < 65 años -> HTTP 400)" {
    $body = @{ edad = 55; valor_vivienda = 200000000.0 } | ConvertTo-Json
    try {
        $res = Invoke-WebRequest -Uri "$BaseUrl/api/v1/calculo" -Method Post -Body $body -ContentType "application/json" -TimeoutSec 10
        throw "La API debió rechazar la solicitud pero respondió HTTP $($res.StatusCode)"
    } catch [System.Net.WebException] {
        $resp = $_.Exception.Response
        if ($resp.StatusCode.value__ -ne 400) { throw "Se esperaba código 400, recibido: $($resp.StatusCode)" }
    }
}

# TEST 7: Manejo Controlado de Error - Valor de Vivienda Menor a $50M COP
Assert-Test "Manejo Controlado de Error (Valor < $50.000.000 COP -> HTTP 400)" {
    $body = @{ edad = 70; valor_vivienda = 25000000.0 } | ConvertTo-Json
    try {
        $res = Invoke-WebRequest -Uri "$BaseUrl/api/v1/calculo" -Method Post -Body $body -ContentType "application/json" -TimeoutSec 10
        throw "La API debió rechazar la solicitud pero respondió HTTP $($res.StatusCode)"
    } catch [System.Net.WebException] {
        $resp = $_.Exception.Response
        if ($resp.StatusCode.value__ -ne 400) { throw "Se esperaba código 400, recibido: $($resp.StatusCode)" }
    }
}

# TEST 8: Flujo Integral E2E de Comunicación (UI -> API -> PostgreSQL -> UI)
Assert-Test "Flujo E2E Completo Automatizado (/api/v1/flujo-prueba)" {
    $res = Invoke-RestMethod -Uri "$BaseUrl/api/v1/flujo-prueba" -Method Post -TimeoutSec 15
    if ($res.resultado -ne "EXITOSO") { throw "Flujo falló: $($res.mensaje)" }
    if ($res.pasos.Count -lt 4) { throw "Número de pasos verificados insuficiente" }
}

# Resumen
Write-Host "`n==================================================================" -ForegroundColor Cyan
Write-Host " 📊 RESUMEN DE PRUEBAS E2E: $passed / $total superadas" -ForegroundColor $(if ($passed -eq $total) { "Green" } else { "Red" })
Write-Host "==================================================================" -ForegroundColor Cyan

if ($passed -eq $total) {
    Write-Host "🎉 Todas las pruebas E2E en Kubernetes/Minikube pasaron con éxito (100%)." -ForegroundColor Green
    exit 0
} else {
    Write-Error "❌ Algunas pruebas fallaron ($($total - $passed) fallas)."
    exit 1
}
