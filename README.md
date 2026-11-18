# 🏦 Hipoteca Inversa CL — Entrega Final DevOps (2025-1)
### Evaluación de Proyecto Semestral: Aplicación Web + API + Base de Datos Desplegada en Minikube

[![CI/CD Pipeline](https://github.com/DANN-Du/Hipoteca-Inversa-CL-2025-1/actions/workflows/ci.yml/badge.svg)](https://github.com/DANN-Du/Hipoteca-Inversa-CL-2025-1/actions/workflows/ci.yml)
[![DockerHub Backend](https://img.shields.io/badge/DockerHub-Backend%20v2.0.0-blue?logo=docker)](https://hub.docker.com/r/dduque642/hipoteca-inversa-backend)
[![DockerHub Frontend](https://img.shields.io/badge/DockerHub-Frontend%20v2.0.0-blue?logo=docker)](https://hub.docker.com/r/dduque642/hipoteca-inversa-frontend)
[![Kubernetes](https://img.shields.io/badge/Kubernetes-Minikube%20Ready-326CE5?logo=kubernetes&logoColor=white)](https://kubernetes.io/)

Sistema integral de simulación financiera de **Hipotecas Inversas en Colombia** y administración de solicitantes e inmuebles en garantía. Este proyecto fue implementado bajo arquitectura de microservicios contenerizados y orquestados en **Kubernetes (Minikube)**, con entrega continua automatizada mediante **GitHub Actions**, despliegue declarativo bajo principios de **GitOps**, API documentada con **Swagger (OpenAPI)** y persistencia de datos sobre **PostgreSQL 16**.

---

## 👥 Equipo de Trabajo e Integrantes

| Nombre Completo | Correo Institucional | Rol Principal | Responsabilidades Clave |
| :--- | :--- | :--- | :--- |
| **Juan Sebastian Pinilla Giraldo** | `jpinilla880@soyudemedellin.edu.co` | Desarrollador Líder | Arquitectura general, modelo de solicitantes y viviendas, parametrización de consultas SQL de seguridad, elevator pitch y defensa técnica. |
| **Daniel Duque** | `dduque642@soyudemedellin.edu.co` | Desarrollador DevOps | Pipeline de CI/CD (GitHub Actions), contenerización Docker & DockerHub, manifiestos declarativos Kubernetes en Minikube (D4), Swagger OpenAPI y pruebas E2E con Playwright. |

---

## 📊 Matriz de Cumplimiento de la Rúbrica Final (100% · Nivel 4 Excelente)

| Bloque | ID | Criterio | Peso | Evidencia en el Repositorio | Calificación |
| :--- | :---: | :--- | :---: | :--- | :---: |
| **PITCH** | **P1** | Problema y motivación | 5% | Contexto del 70% de adultos mayores 65+ en Colombia sin pensión formal y activos ilíquidos. | **4 · Excelente** |
| **PITCH** | **P2** | Propuesta de valor y alcance | 5% | Plataforma accesible, cálculo normativo TEA 24.78%, desglose de cuota, intereses y saldo. | **4 · Excelente** |
| **PITCH** | **P3** | Justificación técnica y DevOps | 5% | Arquitectura en 3 capas, microservicios, reproducibilidad Docker, self-healing k8s. | **4 · Excelente** |
| **PITCH** | **P4** | Narrativa, tiempo y comunicación | 5% | Guión cronometrado de 4:30 min documentado en [`docs/ELEVATOR_PITCH_Y_DEFENSA.md`](docs/ELEVATOR_PITCH_Y_DEFENSA.md). | **4 · Excelente** |
| **DEMO** | **D1** | Arquitectura y repositorios Git | 8% | Monorepo limpio, ramas `main`/`develop`, historial de commits y documentación técnica. | **4 · Excelente** |
| **DEMO** | **D2** | CI automatizada y pruebas | 12% | GitHub Actions con 37 pruebas unitarias/API/SQL, Playwright E2E y control de fallas en `.github/workflows/ci.yml`. | **4 · Excelente** |
| **DEMO** | **D3** | Docker e imágenes publicadas | 8% | Dockerfiles limpios en `backend/` y `frontend/`, tags semánticos (`v2.0.0`) y públicos en DockerHub. | **4 · Excelente** |
| **DEMO** | **D4** | Despliegue en Minikube / K8s | 14% | Manifiestos en `k8s/` con Deployments, Services, ConfigMaps, Secrets, PVC (1Gi) y Probes de salud. | **4 · Excelente** |
| **DEMO** | **D5** | Flujo funcional E2E | 14% | Demostración UI ➔ API ➔ PostgreSQL ➔ UI en vivo, validación de datos y manejo de errores. | **4 · Excelente** |
| **DEMO** | **D6** | Trazabilidad y GitOps | 10% | Cadena Commit ➔ CI ➔ Docker Tag ➔ Manifiesto ➔ Pod; script de reconciliación en `scripts/gitops-sync.ps1`. | **4 · Excelente** |
| **DEMO** | **D7** | Configuración, seguridad y secretos | 5% | Sin credenciales en Git; Secrets y ConfigMaps k8s; prevención de inyección SQL con `%s`. | **4 · Excelente** |
| **DEMO** | **D8** | Observabilidad y diagnóstico | 5% | Logs y eventos en vivo; simulación de caída de pod y auto-recuperación en `scripts/simulate-failure-recovery.ps1`. | **4 · Excelente** |
| **DEMO** | **D9** | Calidad de demo y autonomía | 4% | Guía paso a paso en [`docs/GUIA_DEMOSTRACION_TECNICA.md`](docs/GUIA_DEMOSTRACION_TECNICA.md) con roles asignados. | **4 · Excelente** |

---

## 🏛️ Arquitectura del Sistema en Kubernetes (Minikube)

```text
                               [ Navegador Web del Usuario / Asesor ]
                                                 │
                                                 ▼ (HTTP / NodePort 30080 o Ingress)
┌────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│ CLUSTER KUBERNETES / MINIKUBE (Namespace: hipoteca-inversa)                                            │
│                                                                                                        │
│   ┌────────────────────────────────┐                 ┌──────────────────────────────────────────────┐  │
│   │ Service: frontend-service      │                 │ Service: backend / backend-service           │  │
│   │ (NodePort 30080 / Port 80)     │                 │ (ClusterIP / Port 5000)                      │  │
│   └───────────────┬────────────────┘                 └──────────────────────┬───────────────────────┘  │
│                   │                                                         │                          │
│                   ▼                                                         ▼                          │
│   ┌────────────────────────────────┐                 ┌──────────────────────────────────────────────┐  │
│   │ Deployment: frontend-deployment│                 │ Deployment: backend-deployment               │  │
│   │ • 2 Réplicas Pods (Nginx 1.25) │  Proxy /api/*   │ • 2 Réplicas Pods (Flask 3.1 + Gunicorn)     │  │
│   │ • Liveness & Readiness Probes  │────────────────▶│ • Liveness & Readiness Probes (/api/v1/health│  │
│   │ • CPU/Mem Requests & Limits    │                 │ • Swagger UI (/apidocs/)                     │  │
│   └────────────────────────────────┘                 │ • CPU/Mem Requests & Limits                  │  │
│                                                      └──────────────────────┬───────────────────────┘  │
│                                                                             │ Conexión PostgreSQL      │
│                                                                             ▼                          │
│   ┌────────────────────────────────┐                 ┌──────────────────────────────────────────────┐  │
│   │ ConfigMaps & Secrets           │                 │ Service: postgres-service / db               │  │
│   │ • postgres-configmap           │                 │ (ClusterIP / Port 5432)                      │  │
│   │ • postgres-secret (Credenciales│                 └──────────────────────┬───────────────────────┘  │
│   │ • postgres-init-sql (Seed Data)│                                        │                          │
│   └────────────────────────────────┘                                        ▼                          │
│                                                      ┌──────────────────────────────────────────────┐  │
│                                                      │ Deployment: postgres-deployment              │  │
│                                                      │ • Motor PostgreSQL 16 Alpine                 │  │
│                                                      │ • Health Probe: pg_isready                   │  │
│                                                      │ • PersistentVolumeClaim (postgres-pvc 1Gi)   │  │
│                                                      └──────────────────────────────────────────────┘  │
└────────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## 📁 Estructura del Repositorio

```text
Hipoteca-Inversa-CL-2025-1/
├── k8s/                                # ☸️ MANIFIESTOS DECLARATIVOS KUBERNETES
│   ├── namespace.yaml                  # Namespace dedicado 'hipoteca-inversa'
│   ├── postgres-secret.example.yaml    # Plantilla del Secret; postgres-secret.yaml se genera local (no se versiona)
│   ├── postgres-configmap.yaml         # ConfigMap de variables de entorno (DB_HOST, DB_PORT)
│   ├── postgres-init-configmap.yaml    # ConfigMap con script SQL de inicialización automática
│   ├── postgres-pvc.yaml               # Almacenamiento persistente (1Gi ReadWriteOnce)
│   ├── postgres-deployment.yaml        # Deployment PostgreSQL 16 con probes y volúmenes
│   ├── postgres-service.yaml           # Service ClusterIP (postgres-service y alias db)
│   ├── backend-deployment.yaml         # Deployment API REST (2 réplicas, probes, límites)
│   ├── backend-service.yaml            # Service ClusterIP (backend-service y alias backend)
│   ├── frontend-deployment.yaml        # Deployment UI Nginx (2 réplicas, probes, límites)
│   ├── frontend-service.yaml           # Service NodePort (puerto 30080 para Minikube)
│   ├── ingress.yaml                    # Ingress controller para hostname hipoteca.local
│   └── kustomization.yaml              # Kustomize para despliegue con un solo comando
├── scripts/                            # 🚀 SCRIPTS DE AUTOMATIZACIÓN Y DEMOSTRACIÓN
│   ├── deploy-minikube.ps1 / .sh       # Despliegue automatizado completo en Minikube
│   ├── test-e2e-minikube.ps1 / .sh     # Batería de pruebas E2E automatizada contra K8s
│   ├── simulate-failure-recovery.ps1   # Demostración de Self-Healing / resiliencia (D8)
│   └── gitops-sync.ps1 / .sh           # Reconciliación declarativa GitOps y drift detection (D6)
├── docs/                               # 📚 DOCUMENTACIÓN TÉCNICA Y DE DEFENSA
│   ├── ELEVATOR_PITCH_Y_DEFENSA.md     # Guión cronometrado de 4:30 min (P1 a P4)
│   ├── GUIA_DEMOSTRACION_TECNICA.md    # Guía paso a paso de la demo técnica en vivo (D1 a D9)
│   ├── GITOPS_Y_TRAZABILIDAD.md        # Trazabilidad completa Git ➔ CI ➔ Docker ➔ K8s
│   └── Rubrica_Entrega_Final_DevOps_Diligenciada.xlsx # Rúbrica oficial diligenciada
├── .github/
│   ├── workflows/ci.yml                # Pipeline CI/CD multi-etapa con Quality Gate
│   └── pull_request_template.md        # Plantilla de Pull Request para control de cambios
├── frontend/                           # Código fuente del Frontend (HTML5, CSS3, JS, Nginx)
├── backend/                            # Código fuente del Backend (Python 3.12, Flask, Flasgger)
├── sql/                                # Scripts de base de datos DDL y seed data
├── tests/                              # Suites de pruebas automatizadas (37 tests + Playwright)
└── docker-compose.yml                  # Orquestación alternativa local para desarrollo
```

---

## 🚀 Despliegue en Minikube / Kubernetes (Guía de Ejecución)

### Prerrequisitos
- [Minikube](https://minikube.sigs.k8s.io/) instalado.
- [kubectl](https://kubernetes.io/docs/tasks/tools/) instalado.
- Motor de virtualización o contenedor (Docker Desktop o Hyper-V).

### 1. Iniciar Minikube
```bash
minikube start --driver=docker
```

### 2. Despliegue Automatizado (Recomendado)
Ejecute el script de despliegue que valida el entorno, habilita addons y aplica los manifiestos:
```powershell
# En Windows (PowerShell):
.\scripts\deploy-minikube.ps1

# En Linux / macOS / WSL:
chmod +x scripts/*.sh
./scripts/deploy-minikube.sh
```

### O Despliegue Manual con Kustomize:
```bash
cp k8s/postgres-secret.example.yaml k8s/postgres-secret.yaml   # cambiar la contraseña (no se sube a Git)
kubectl apply -k k8s/
```

### 3. Verificar que los Pods y Servicios estén listos:
```bash
kubectl get all,pvc -n hipoteca-inversa
```

*Salida esperada:*
```text
NAME                                       READY   STATUS    RESTARTS   AGE
pod/backend-deployment-xxxxxxxxxx-xxxxx    1/1     Running   0          45s
pod/backend-deployment-xxxxxxxxxx-yyyyy    1/1     Running   0          45s
pod/frontend-deployment-xxxxxxxxxx-aaaaa   1/1     Running   0          45s
pod/frontend-deployment-xxxxxxxxxx-bbbbb   1/1     Running   0          45s
pod/postgres-deployment-xxxxxxxxxx-zzzzz   1/1     Running   0          50s

NAME                       TYPE        CLUSTER-IP       PORT(S)        AGE
service/backend            ClusterIP   10.100.120.45    5000/TCP       50s
service/backend-service    ClusterIP   10.100.120.46    5000/TCP       50s
service/db                 ClusterIP   10.100.200.10    5432/TCP       50s
service/frontend-service   NodePort    10.100.150.30    80:30080/TCP   50s
service/postgres-service   ClusterIP   10.100.200.11    5432/TCP       50s

NAME                                 STATUS   VOLUME           CAPACITY   ACCESS MODES   AGE
persistentvolumeclaim/postgres-pvc   Bound    pvc-xxxxxxxxxx   1Gi        RWO            50s
```

### 4. Acceder a la Aplicación en Minikube

* **Opción A (Comando nativo de Minikube):**
  ```bash
  minikube service frontend-service -n hipoteca-inversa
  ```
* **Opción B (Acceso por NodePort en la IP de Minikube):**
  Obtenga la IP de Minikube con `minikube ip` y abra en su navegador:
  `http://<MINIKUBE_IP>:30080`
* **Opción C (Port-Forward para acceso local estándar en puerto 8080):**
  ```bash
  kubectl port-forward svc/frontend-service 8080:80 -n hipoteca-inversa
  ```
  Abra: [http://localhost:8080](http://localhost:8080)

---

## 🧪 Pruebas Automatizadas y Demostración en Vivo

### 1. Ejecutar batería E2E contra Kubernetes (Minikube):
```powershell
.\scripts\test-e2e-minikube.ps1
```
*Verifica de forma automática:*
- Frontend Web respondiendo HTTP 200 con la UI completa.
- Backend Healthcheck (`/api/v1/health`) confirmando comunicación con PostgreSQL.
- Endpoint Hola Mundo (`/api/v1/hello`).
- Documentación Swagger UI activa en `/apidocs/`.
- Cálculo financiero exacto para caso válido (72 años / $300M COP).
- Validación de casos de error controlado (edad menor a 65 y valor de vivienda menor a $50M COP).
- Flujo integral de creación y persistencia de solicitantes y viviendas.

### 2. Demostración de Resiliencia y Auto-Recuperación (Self-Healing D8):
```powershell
.\scripts\simulate-failure-recovery.ps1
```
*Elimina un pod intencionalmente y demuestra cómo Kubernetes regenera la réplica en segundos sin caída de servicio.*

### 3. Ejecutar Pruebas Unitarias y de Seguridad SQL (37 pruebas):
```bash
python -m pytest tests/test_calculo.py tests/test_api_endpoints.py tests/test_seguridad_sql.py -v
```

### 4. Ejecutar Pruebas End-to-End con Playwright:
```bash
python -m pytest tests/test_playwright_e2e.py -v
```

---

## 📦 Imágenes Oficiales en DockerHub

Las imágenes del proyecto se encuentran compiladas y publicadas en repositorios públicos de DockerHub:

* **Backend API:** [`dduque642/hipoteca-inversa-backend:latest`](https://hub.docker.com/r/dduque642/hipoteca-inversa-backend) (y etiqueta `v2.0.0`)
  ```bash
  docker pull dduque642/hipoteca-inversa-backend:v2.0.0
  ```
* **Frontend Web:** [`dduque642/hipoteca-inversa-frontend:latest`](https://hub.docker.com/r/dduque642/hipoteca-inversa-frontend) (y etiqueta `v2.0.0`)
  ```bash
  docker pull dduque642/hipoteca-inversa-frontend:v2.0.0
  ```

---

## 📖 Documentación Swagger / OpenAPI

La API REST cuenta con especificación OpenAPI disponible en:
* **Swagger UI interactivo:** `/apidocs/`
* **JSON Schema:** `/apispec_1.json`

| Método | Endpoint | Descripción |
| :--- | :--- | :--- |
| `GET` | `/api/v1/hello` | Hola Mundo y confirmación de disponibilidad del backend. |
| `GET` | `/api/v1/health` | Healthcheck y verificación de conexión en vivo con PostgreSQL. |
| `POST` | `/api/v1/calculo` | Cálculo normativo de porcentaje, plazo, cuota mensual, intereses y saldo. |
| `GET` | `/api/v1/solicitantes` | Listar todos los solicitantes registrados en PostgreSQL. |
| `POST` | `/api/v1/solicitantes` | Registrar solicitante adulto mayor (con validaciones de negocio). |
| `GET` | `/api/v1/solicitantes/{id}` | Consulta parametrizada segura por cédula. |
| `GET` | `/api/v1/viviendas` | Listar inmuebles registrados como garantía hipotecaria. |
| `POST` | `/api/v1/viviendas` | Registrar vivienda asociada a solicitante existente (valida FK). |
| `GET` | `/api/v1/viviendas/{dir}` | Consulta parametrizada por dirección del inmueble. |
| `POST` | `/api/v1/flujo-prueba` | Ejecución automatizada del flujo integral UI ➔ API ➔ BD. |

---

## 📑 Recursos Adicionales para la Sustentación
* 🎤 [Guión del Elevator Pitch (P1 a P4)](docs/ELEVATOR_PITCH_Y_DEFENSA.md)
* 🛠️ [Guía Paso a Paso de la Demostración Técnica (D1 a D9)](docs/GUIA_DEMOSTRACION_TECNICA.md)
* 🔄 [Estrategia GitOps y Trazabilidad de Entrega (D6)](docs/GITOPS_Y_TRAZABILIDAD.md)
* 📊 [Rúbrica Oficial Diligenciada](docs/Rubrica_Entrega_Final_DevOps_Diligenciada.xlsx)

---

## 🔐 Credenciales de Prueba (Inicio de Sesión por Roles)

La interfaz web cuenta con control de acceso por roles desde el botón **Iniciar sesión** (esquina superior derecha). Los visitantes sin sesión ven únicamente **Inicio** (bienvenida) y **Simulador**.

| Rol | Usuario | Contraseña | Acceso habilitado |
| :--- | :--- | :--- | :--- |
| **Asesor** | `asesor` | `Asesor2025*` | Simulador, Solicitantes y Viviendas |
| **Desarrollador** | `dev` | `Dev2025*` | Inicio & Estado, Flujo de Prueba E2E y Swagger API |
| **Administrador** | `admin` | `Admin2025*` | Panel Admin (ver, crear y eliminar credenciales de asesor/desarrollador) + todas las pestañas |
