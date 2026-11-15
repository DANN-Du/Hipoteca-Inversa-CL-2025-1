#!/usr/bin/env bash
# ==============================================================================
# Script de Despliegue Automatizado en Minikube / Kubernetes (Bash)
# Proyecto: Hipoteca Inversa CL - Entrega Final DevOps
# ==============================================================================
set -euo pipefail

echo "=================================================================="
echo " 🚀 Iniciando Despliegue en Minikube: Hipoteca Inversa CL"
echo "=================================================================="

# 1. Verificar kubectl
if ! command -v kubectl &> /dev/null; then
    echo "❌ Error: kubectl no está instalado o no está en el PATH."
    exit 1
fi
echo "✅ kubectl detectado: $(kubectl version --client -o yaml | grep gitVersion || true)"

# 2. Verificar Minikube
if command -v minikube &> /dev/null; then
    echo "ℹ️  Estado de Minikube:"
    minikube status || true
    echo "📦 Habilitando addons en Minikube (ingress, metrics-server)..."
    minikube addons enable ingress 2>/dev/null || true
    minikube addons enable metrics-server 2>/dev/null || true
fi

# 3. Aplicar manifiestos K8s
echo "⚙️  Aplicando manifiestos declarativos de Kubernetes (k8s/)..."
kubectl apply -k k8s/

# 4. Esperar rollout
echo "⏳ Esperando que los despliegues estén listos..."
kubectl rollout status deployment/postgres-deployment -n hipoteca-inversa --timeout=120s
kubectl rollout status deployment/backend-deployment -n hipoteca-inversa --timeout=120s
kubectl rollout status deployment/frontend-deployment -n hipoteca-inversa --timeout=120s

# 5. Estado general
echo "=================================================================="
echo " 📊 Recursos en namespace 'hipoteca-inversa':"
echo "=================================================================="
kubectl get all,pvc,ingress -n hipoteca-inversa -o wide

echo "=================================================================="
echo " 🎉 Despliegue Completado con Éxito"
echo "=================================================================="
if command -v minikube &> /dev/null; then
    MINIKUBE_IP=$(minikube ip 2>/dev/null || true)
    if [ -n "$MINIKUBE_IP" ]; then
        echo "🌐 URL Frontend (NodePort): http://${MINIKUBE_IP}:30080"
        echo "📖 URL Swagger API:        http://${MINIKUBE_IP}:30080/apidocs/"
    fi
fi
echo "💡 Port-forward para acceso local:"
echo "   kubectl port-forward svc/frontend-service 8080:80 -n hipoteca-inversa"
