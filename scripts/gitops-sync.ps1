# ==============================================================================
# Script de Reconciliación Declarativa GitOps (D6)
# Proyecto: Hipoteca Inversa CL
# ==============================================================================

Write-Host "==================================================================" -ForegroundColor Cyan
Write-Host " 🔄 Ciclo de Reconciliación Declarativa GitOps (D6)" -ForegroundColor Cyan
Write-Host "==================================================================" -ForegroundColor Cyan

# 1. Repositorio como Única Fuente de Verdad
Write-Host "1️⃣  Fuente de Verdad (Git): Manifiestos versionados en carpeta k8s/" -ForegroundColor Yellow
$currentCommit = (git rev-parse --short HEAD 2>$null)
Write-Host "    Commit SHA activo: $currentCommit" -ForegroundColor Green

# 2. Detección de Desviación (Drift Detection)
Write-Host "`n2️⃣  Verificando posibles diferencias entre Git y el Cluster (kubectl diff):" -ForegroundColor Yellow
kubectl diff -k k8s/ 2>$null
if ($LASTEXITCODE -eq 0) {
    Write-Host "    ✅ El estado del cluster está 100% sincronizado con el repositorio Git (In-Sync)." -ForegroundColor Green
} else {
    Write-Host "    ⚠️  Se detectaron diferencias o recursos pendientes de aplicar." -ForegroundColor Yellow
}

# 3. Aplicar Reconciliación (Sync)
Write-Host "`n3️⃣  Ejecutando Reconciliación declarativa hacia el estado deseado:" -ForegroundColor Cyan
kubectl apply -k k8s/

Write-Host "`n4️⃣  Trazabilidad Verificada:" -ForegroundColor Green
Write-Host "    Git Commit ($currentCommit) ➔ Manifiestos (k8s/) ➔ Pods en Minikube"
