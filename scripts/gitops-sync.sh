#!/usr/bin/env bash
# ==============================================================================
# Script de Reconciliación Declarativa GitOps (D6 - Bash)
# ==============================================================================
set -euo pipefail

echo "=================================================================="
echo " 🔄 Ciclo de Reconciliación Declarativa GitOps (D6)"
echo "=================================================================="

COMMIT_SHA=$(git rev-parse --short HEAD 2>/dev/null || echo "latest")
echo "1️⃣  Fuente de Verdad (Git): commit $COMMIT_SHA"

if [ ! -f k8s/postgres-secret.env ]; then
    echo "❌ Falta k8s/postgres-secret.env (no se versiona). Ejecute primero scripts/deploy-minikube.sh."
    exit 1
fi

echo "2️⃣  Detección de Desviación (kubectl diff):"
kubectl diff -k k8s/ || true

echo "3️⃣  Reconciliando estado deseado..."
kubectl apply -k k8s/

echo "✅ Trazabilidad completada: Git -> Manifiesto -> Pod."
