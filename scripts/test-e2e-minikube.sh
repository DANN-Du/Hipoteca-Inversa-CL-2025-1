#!/usr/bin/env bash
# ==============================================================================
# Script de Prueba End-to-End (E2E) en Minikube / Kubernetes (Bash)
# Proyecto: Hipoteca Inversa CL - Demostración Técnica (D5 / D8)
# ==============================================================================
set -euo pipefail

BASE_URL="${1:-}"

if [ -z "$BASE_URL" ]; then
    if command -v minikube &> /dev/null; then
        MINIKUBE_IP=$(minikube ip 2>/dev/null || true)
        if [ -n "$MINIKUBE_IP" ]; then
            BASE_URL="http://${MINIKUBE_IP}:30080"
        fi
    fi
fi

BASE_URL="${BASE_URL:-http://localhost:8080}"

echo "=================================================================="
echo " 🧪 Verificación End-to-End en Kubernetes: $BASE_URL"
echo "=================================================================="

PASSED=0
TOTAL=0

assert_test() {
    local name="$1"
    local cmd="$2"
    TOTAL=$((TOTAL + 1))
    echo -n "[$TOTAL] $name ... "
    if eval "$cmd" > /dev/null 2>&1; then
        echo "PASSED (OK)"
        PASSED=$((PASSED + 1))
    else
        echo "FAILED"
    fi
}

assert_test "Frontend Web HTTP 200" "curl -sf --max-time 10 '$BASE_URL/' | grep -q 'Hipoteca Inversa CL'"
assert_test "Backend Healthcheck (/api/v1/health)" "curl -sf --max-time 10 '$BASE_URL/api/v1/health' | grep -q 'saludable'"
assert_test "Backend Hola Mundo (/api/v1/hello)" "curl -sf --max-time 10 '$BASE_URL/api/v1/hello' | grep -q 'online'"
assert_test "Swagger Documentation UI (/apidocs/)" "curl -sf --max-time 10 '$BASE_URL/apidocs/' | grep -qi 'swagger'"
assert_test "Cálculo Financiero Válido (72 años / $300M)" "curl -sf --max-time 10 -X POST -H 'Content-Type: application/json' -d '{\"edad\": 72, \"valor_vivienda\": 300000000}' '$BASE_URL/api/v1/calculo' | grep -q 'pago_mensual'"
assert_test "Error Controlado (Edad < 65)" "test \$(curl -s -o /dev/null -w '%{http_code}' -X POST -H 'Content-Type: application/json' -d '{\"edad\": 55, \"valor_vivienda\": 200000000}' '$BASE_URL/api/v1/calculo') -eq 400"
assert_test "Error Controlado (Valor < 50M)" "test \$(curl -s -o /dev/null -w '%{http_code}' -X POST -H 'Content-Type: application/json' -d '{\"edad\": 70, \"valor_vivienda\": 20000000}' '$BASE_URL/api/v1/calculo') -eq 400"
assert_test "Flujo Integral E2E (/api/v1/flujo-prueba)" "curl -sf --max-time 15 -X POST '$BASE_URL/api/v1/flujo-prueba' | grep -q 'EXITOSO'"

echo "=================================================================="
echo " 📊 Resumen: $PASSED / $TOTAL pruebas superadas"
echo "=================================================================="
if [ "$PASSED" -eq "$TOTAL" ]; then
    echo "🎉 100% Exitoso."
    exit 0
else
    echo "❌ Algunas pruebas fallaron."
    exit 1
fi
