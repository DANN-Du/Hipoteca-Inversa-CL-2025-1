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

# 3. Preparar Secret local (k8s/postgres-secret.yaml no se versiona en Git)
SECRET_FILE="k8s/postgres-secret.yaml"
if [ ! -f "$SECRET_FILE" ]; then
    echo "🔐 Creando $SECRET_FILE con una contraseña aleatoria (no se sube a Git)..."
    PASS=$(LC_ALL=C tr -dc 'A-Za-z0-9' </dev/urandom | head -c 24 || true)
    sed "s/CAMBIAR_ESTA_CONTRASENA/${PASS}/g" k8s/postgres-secret.example.yaml > "$SECRET_FILE"
    echo "✅ Secret local creado. Si ya tenía datos en el PVC con otra contraseña, edite $SECRET_FILE."
fi

# 4. Construir imágenes dentro de Minikube si aún no están (útil sin DockerHub)
if command -v minikube &> /dev/null; then
    for svc in backend frontend; do
        IMG="dduque642/hipoteca-inversa-${svc}:v2.0.0"
        if ! minikube image ls 2>/dev/null | grep -qF "$IMG"; then
            echo "🐳 Construyendo $IMG dentro de Minikube..."
            minikube image build -t "$IMG" "./$svc"
        fi
    done
fi

# 5. Aplicar manifiestos K8s
echo "⚙️  Aplicando manifiestos declarativos de Kubernetes (k8s/)..."
kubectl apply -k k8s/

# 6. Esperar rollout
echo "⏳ Esperando que los despliegues estén listos..."
for dep in postgres-deployment backend-deployment frontend-deployment; do
    if ! kubectl rollout status "deployment/$dep" -n hipoteca-inversa --timeout=300s; then
        echo "❌ $dep no quedó listo. Diagnóstico:"
        echo "   kubectl describe pod -l app=${dep%-deployment} -n hipoteca-inversa"
        kubectl get pods -n hipoteca-inversa
        exit 1
    fi
done

# 7. Estado general
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
