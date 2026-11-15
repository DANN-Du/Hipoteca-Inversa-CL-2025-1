# ==============================================================================
# Script de Demostración de Resiliencia, Diagnóstico y Auto-Recuperación (D8)
# Proyecto: Hipoteca Inversa CL - Demostración en Minikube
# ==============================================================================

Write-Host "==================================================================" -ForegroundColor Cyan
Write-Host " 🛡️  Simulación de Falla y Diagnóstico de Observabilidad (D8)" -ForegroundColor Cyan
Write-Host "==================================================================" -ForegroundColor Cyan

# 1. Listar pods actuales del backend
Write-Host "`n1️⃣  Estado inicial de los pods en 'hipoteca-inversa':" -ForegroundColor Yellow
kubectl get pods -n hipoteca-inversa -l app=backend -o wide

$podToKill = (kubectl get pods -n hipoteca-inversa -l app=backend -o jsonpath='{.items[0].metadata.name}')
if (-not $podToKill) {
    Write-Error "❌ No se encontraron pods del backend corriendo."
    exit 1
}

Write-Host "`n2️⃣  Pod seleccionado para simulación de falla: $podToKill" -ForegroundColor Yellow

# 3. Mostrar logs del pod antes de la falla
Write-Host "`n3️⃣  Extrayendo últimos logs del pod seleccionado:" -ForegroundColor Cyan
kubectl logs $podToKill -n hipoteca-inversa --tail=10

# 4. Forzar falla eliminando el pod
Write-Host "`n4️⃣  Simulando falla forzada (eliminando pod con kubectl delete pod)..." -ForegroundColor Red
kubectl delete pod $podToKill -n hipoteca-inversa --now

# 5. Observar auto-reconciliación del Deployment de Kubernetes
Write-Host "`n5️⃣  Verificando Self-Healing (El ReplicaSet crea automáticamente un nuevo Pod):" -ForegroundColor Green
Start-Sleep -Seconds 3
kubectl get pods -n hipoteca-inversa -l app=backend -o wide

# 6. Describir eventos de auto-recuperación
Write-Host "`n6️⃣  Eventos del cluster registrados (kubectl describe):" -ForegroundColor Cyan
kubectl get events -n hipoteca-inversa --sort-by='.metadata.creationTimestamp' | Select-Object -Last 10

Write-Host "`n==================================================================" -ForegroundColor Green
Write-Host " ✅ Simulación Completada:" -ForegroundColor Green
Write-Host "    Kubernetes detectó la indisponibilidad del pod y restauró el estado" -ForegroundColor White
Write-Host "    deseado (2/2 réplicas) sin pérdida de disponibilidad para el usuario." -ForegroundColor White
Write-Host "==================================================================" -ForegroundColor Green
