# ==============================================================================
# Script de Despliegue Automatizado en Minikube / Kubernetes
# Proyecto: Hipoteca Inversa CL - Entrega Final DevOps
# ==============================================================================

Write-Host "==================================================================" -ForegroundColor Cyan
Write-Host " 🚀 Iniciando Despliegue en Minikube: Hipoteca Inversa CL" -ForegroundColor Cyan
Write-Host "==================================================================" -ForegroundColor Cyan

# 1. Verificar kubectl
try {
    $kubectlVer = kubectl version --client 2>&1
    Write-Host "✅ kubectl detectado: $kubectlVer" -ForegroundColor Green
} catch {
    Write-Error "❌ kubectl no está instalado o en el PATH."
    exit 1
}

# 2. Verificar Minikube
try {
    $minikubeStatus = minikube status 2>&1
    Write-Host "ℹ️  Estado de Minikube:" -ForegroundColor Yellow
    Write-Host $minikubeStatus
} catch {
    Write-Warning "⚠️  Minikube no parece estar activo. Si no está corriendo, inícielo con: minikube start"
}

# 3. Habilitar Addons en Minikube (Ingress y Metrics-server)
Write-Host "`n📦 Habilitando addons recomendados en Minikube..." -ForegroundColor Yellow
try {
    minikube addons enable ingress 2>$null
    minikube addons enable metrics-server 2>$null
    Write-Host "✅ Addons verificados (ingress, metrics-server)." -ForegroundColor Green
} catch {
    Write-Host "ℹ️  Omitiendo addons si ya están configurados o en cluster remoto."
}

# 4. Aplicar manifiestos declarativos en Kubernetes (GitOps)
Write-Host "`n⚙️  Aplicando manifiestos declarativos (k8s/)..." -ForegroundColor Yellow
kubectl apply -k k8s/
if ($LASTEXITCODE -ne 0) {
    Write-Error "❌ Error al aplicar los manifiestos de Kubernetes."
    exit $LASTEXITCODE
}
Write-Host "✅ Manifiestos aplicados con éxito." -ForegroundColor Green

# 5. Esperar Rollout de Recursos
Write-Host "`n⏳ Esperando que los despliegues estén listos..." -ForegroundColor Yellow

Write-Host "-> Despliegue PostgreSQL..."
kubectl rollout status deployment/postgres-deployment -n hipoteca-inversa --timeout=120s

Write-Host "-> Despliegue Backend API..."
kubectl rollout status deployment/backend-deployment -n hipoteca-inversa --timeout=120s

Write-Host "-> Despliegue Frontend Web..."
kubectl rollout status deployment/frontend-deployment -n hipoteca-inversa --timeout=120s

# 6. Mostrar Estado del Cluster
Write-Host "`n==================================================================" -ForegroundColor Cyan
Write-Host " 📊 Estado de los Recursos en el Namespace 'hipoteca-inversa'" -ForegroundColor Cyan
Write-Host "==================================================================" -ForegroundColor Cyan
kubectl get all,pvc,ingress -n hipoteca-inversa -o wide

# 7. Obtener URL de acceso
Write-Host "`n==================================================================" -ForegroundColor Green
Write-Host " 🎉 Despliegue Finalizado Exitosamente" -ForegroundColor Green
Write-Host "==================================================================" -ForegroundColor Green

try {
    $minikubeIp = minikube ip 2>$null
    if ($minikubeIp) {
        Write-Host "🌐 Frontend Web (NodePort 30080): http://${minikubeIp}:30080" -ForegroundColor White
        Write-Host "🌐 Frontend Web (Minikube Service): minikube service frontend-service -n hipoteca-inversa" -ForegroundColor White
        Write-Host "📖 Documentación Swagger: http://${minikubeIp}:30080/apidocs/" -ForegroundColor White
    }
} catch {
    # Fallback genérico
}

Write-Host "`n💡 Comandos de Port-Forward para acceso local directo:" -ForegroundColor Cyan
Write-Host "   Frontend Web:  kubectl port-forward svc/frontend-service 8080:80 -n hipoteca-inversa (visitar http://localhost:8080)"
Write-Host "   Backend API:   kubectl port-forward svc/backend 5000:5000 -n hipoteca-inversa (visitar http://localhost:5000/apidocs/)"
Write-Host "   PostgreSQL BD: kubectl port-forward svc/postgres-service 5432:5432 -n hipoteca-inversa"
