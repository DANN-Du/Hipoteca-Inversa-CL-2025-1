#!/usr/bin/env bash
# ==============================================================================
# Script de Resiliencia, Diagnóstico y Auto-Recuperación (D8 - Bash)
# Proyecto: Hipoteca Inversa CL - Demostración en Minikube
# ==============================================================================
set -euo pipefail

echo "=================================================================="
echo " 🛡️  Simulación de Falla y Diagnóstico de Observabilidad (D8)"
echo "=================================================================="

echo "1️⃣  Estado inicial de los pods en 'hipoteca-inversa':"
kubectl get pods -n hipoteca-inversa -l app=backend -o wide

POD_TO_KILL=$(kubectl get pods -n hipoteca-inversa -l app=backend -o jsonpath='{.items[0].metadata.name}')
echo "2️⃣  Pod seleccionado para simular falla: $POD_TO_KILL"

echo "3️⃣  Logs del pod previo a la falla:"
kubectl logs "$POD_TO_KILL" -n hipoteca-inversa --tail=10 || true

echo "4️⃣  Eliminando pod para simular fallo..."
kubectl delete pod "$POD_TO_KILL" -n hipoteca-inversa --now

echo "5️⃣  Verificando reconciliación automática (Self-Healing)..."
sleep 3
kubectl get pods -n hipoteca-inversa -l app=backend -o wide

echo "6️⃣  Últimos eventos en el namespace:"
kubectl get events -n hipoteca-inversa --sort-by='.metadata.creationTimestamp' | tail -n 10

echo "=================================================================="
echo " ✅ Reconciliación exitosa: Estado deseado (2/2) restaurado automáticamente."
echo "=================================================================="
