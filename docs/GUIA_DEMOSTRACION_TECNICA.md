# 🛠️ Guía Paso a Paso de la Demostración Técnica (15 a 20 Minutos)
## Proyecto: Hipoteca Inversa CL — Rúbrica Analítica de Entrega Final DevOps

Esta guía contiene la secuencia exacta de pasos, comandos, explicaciones y contingencias para obtener la calificación máxima (Nivel 4 · Excelente) en los 9 criterios de la demostración técnica (**D1 a D9**).

---

## 📋 Resumen de la Demostración

| Criterio | Peso | Qué se demuestra en vivo | Comando / Evidencia |
| :--- | :---: | :--- | :--- |
| **D1: Arquitectura y Git** | 8% | Monorepo limpio, ramas `main`/`develop`, historial de commits y README detallado. | `git status`, `git log --oneline`, `tree` o visualización en GitHub. |
| **D2: CI y Pruebas** | 12% | GitHub Actions ejecutando pruebas unitarias, Playwright E2E y fallo controlado. | Pestaña Actions en GitHub, logs de jobs, runner de pytest. |
| **D3: Docker e Imágenes** | 8% | Dockerfiles limpios (multi-stage/alpine), buenas prácticas, imágenes en DockerHub. | `docker images`, DockerHub oficial (`dduque642/...`). |
| **D4: Despliegue en Minikube** | 14% | Pods saludables, Services, ConfigMaps, Secrets, PVC persistente y Probes. | `kubectl get all,pvc,secret -n hipoteca-inversa`, `deploy-minikube.ps1`. |
| **D5: Flujo Funcional E2E** | 14% | Registro en UI ➔ Proceso en API ➔ Persistencia en BD ➔ Verificación y Error controlado. | Navegador web en vivo ([http://localhost:8080](http://localhost:8080) o Minikube IP). |
| **D6: Trazabilidad y GitOps** | 10% | Commit SHA ➔ Pipeline CI ➔ Tag Docker ➔ Manifiesto k8s/ ➔ Pod ejecutando. | `git rev-parse HEAD`, `kubectl get pods -o jsonpath`. |
| **D7: Seguridad y Secretos** | 5% | ConfigMaps para entorno, Secrets para contraseñas, consultas SQL parametrizadas. | `tests/test_seguridad_sql.py`, `k8s/postgres-secret.yaml` (generado desde `k8s/postgres-secret.example.yaml`, en `.gitignore`). |
| **D8: Observabilidad y Falla** | 5% | `kubectl logs`, `describe`, simulación de caída forzada de pod y auto-reparación. | `scripts/simulate-failure-recovery.ps1`. |
| **D9: Calidad y Autonomía** | 4% | Dominio compartido del equipo, orden y respuestas claras a preguntas del docente. | Participación alternada de Juan Sebastian y Daniel. |

---

## 🎬 Paso 1: Arquitectura y Repositorio Git (D1 - 8%)
**Responsable: Juan Sebastian Pinilla Giraldo**

1. **Abrir el repositorio en GitHub y en la terminal local:**
   ```bash
   git status
   git log -n 5 --oneline --graph
   ```
2. **Explicación del orador:**
   > *"Como observamos, el proyecto se estructura bajo un modelo monorepo ordenado y desacoplado: una carpeta `frontend/` para la aplicación cliente estática con Nginx, una carpeta `backend/` para la API REST en Python Flask con Swagger, una carpeta `sql/` para el esquema relacional, una carpeta `k8s/` con todos los manifiestos declarativos de Kubernetes, y una carpeta `tests/` con las suites de pruebas automatizadas.*
   >
   > *El repositorio cuenta con ramas principales (`main` y `develop`), commits descriptivos y un README exhaustivo que detalla tecnologías, versiones y pasos de ejecución."*

---

## 🎬 Paso 2: Integración Continua (CI) y Control de Fallas (D2 - 12%)
**Responsable: Daniel Duque**

1. **Mostrar en el navegador la pestaña de GitHub Actions:**
   * Enlace: `https://github.com/DANN-Du/Hipoteca-Inversa-CL-2025-1/actions`
2. **Mostrar la ejecución del workflow `.github/workflows/ci.yml`:**
   * Etapa 1: `automated-tests` (37 pruebas unitarias + 3 pruebas Playwright E2E con servicio PostgreSQL de prueba).
   * Etapa 2: `validate-k8s` (validación declarativa de manifiestos con `kubectl apply -k k8s/ --dry-run=client`).
   * Etapa 3: `docker-build` (compilación de imágenes con etiquetas de versión y SHA del commit).
   * Etapa 4: `quality-gate` (aprobación final).
3. **Demostración de Control de Fallas (Prevención de Promoción):**
   * Explicar el job de control:
   > *"Nuestra política de CI es estricta: si una sola prueba matemática, de seguridad SQL o de interfaz falla, el job se detiene inmediatamente con código de error, bloquea los jobs dependientes (`validate-k8s` y `docker-build`) e impide que el código llegue a producción o se fusione en `main`."*
4. **Ejecutar las pruebas en vivo en la terminal:**
   ```bash
   python -m pytest tests/test_calculo.py tests/test_api_endpoints.py tests/test_seguridad_sql.py -v
   ```
   *Resultado:* `37 passed`.

---

## 🎬 Paso 3: Docker e Imágenes Publicadas en DockerHub (D3 - 8%)
**Responsable: Juan Sebastian Pinilla Giraldo**

1. **Mostrar los Dockerfiles:**
   * [`backend/Dockerfile`](file:///c:/Users/danie/Downloads/Hipoteca-Inversa-CL-2025-1/backend/Dockerfile): Uso de imagen base ligera `python:3.12-slim`, servidor WSGI Gunicorn, Healthcheck nativo, sin secretos.
   * [`frontend/Dockerfile`](file:///c:/Users/danie/Downloads/Hipoteca-Inversa-CL-2025-1/frontend/Dockerfile): Imagen `nginx:1.25-alpine`, configuración de proxy inverso hacia el backend, sin dependencias innecesarias.
2. **Mostrar los repositorios oficiales en DockerHub:**
   * Backend: `dduque642/hipoteca-inversa-backend:latest` (y tag `v2.0.0`)
   * Frontend: `dduque642/hipoteca-inversa-frontend:latest` (y tag `v2.0.0`)
3. **Explicación:**
   > *"Cada imagen cuenta con versionado semántico (`v2.0.0`), etiquetas por commit SHA y tag `latest`. No contienen secretos quemados ni archivos temporales gracias a los archivos `.dockerignore`."*

---

## 🎬 Paso 4: Despliegue en Minikube / Kubernetes (D4 - 14%)
**Responsable: Daniel Duque**

1. **Ejecutar el script automatizado o comando de despliegue:**
   ```powershell
   .\scripts\deploy-minikube.ps1
   # O directamente con kubectl:
   kubectl apply -k k8s/
   ```
2. **Verificar el estado de todos los recursos en vivo:**
   ```bash
   kubectl get all,pvc,configmap,secret,ingress -n hipoteca-inversa -o wide
   ```
3. **Puntos clave a resaltar al docente:**
   * **Pods:** 2 réplicas del frontend (`frontend-deployment`), 2 réplicas del backend (`backend-deployment`) y 1 pod de PostgreSQL (`postgres-deployment`), todos en estado `Running` y `Ready (1/1)`.
   * **Persistencia:** `postgres-pvc` en estado `Bound`, persistiendo los datos en disco independientemente del ciclo de vida del pod.
   * **Probes de Salud:** Explicar que los pods cuentan con `livenessProbe` y `readinessProbe` que consultan `/api/v1/health` en el backend y `pg_isready` en PostgreSQL.
   * **Límites de Recursos:** Requests y limits de CPU y memoria configurados en cada deployment para evitar sobrecarga del cluster.

---

## 🎬 Paso 5: Flujo Funcional End-to-End en Vivo (D5 - 14%)
**Responsables: Juan Sebastian Pinilla y Daniel Duque**

1. **Habilitar acceso (si se requiere port-forward):**
   ```bash
   kubectl port-forward svc/frontend-service 8080:80 -n hipoteca-inversa
   ```
2. **Abrir el navegador en [http://localhost:8080](http://localhost:8080):**
   * **Paso A: Demostración de Estado de Componentes (Pestaña Inicio):**
     * Mostrar los tres recuadros verdes: Frontend Online (Puerto 80), Backend Online (Puerto 5000) y Base de Datos Conectada (PostgreSQL 16).
   * **Paso B: Simulación de Hipoteca Inversa (Pestaña Simulador):**
     * Cargar caso de prueba: Edad = 72 años, Valor Inmueble = $300.000.000 COP.
     * Clic en *Calcular Hipoteca*.
     * Mostrar resultados en vivo: Porcentaje financiado = 40%, Plazo = 15 años (180 meses), Pago mensual = $666.667 COP, Intereses proyectados y Saldo final de la deuda.
   * **Paso C: Caso de Error Controlado (Validación de Negocio):**
     * Ingresar Edad = 55 años (menor a 65).
     * El sistema muestra en pantalla de forma controlada el mensaje de error de negocio sin caerse con error 500 ni exponer trazas internas.
   * **Paso D: Registro de Solicitante y Vivienda (Persistencia en PostgreSQL):**
     * Registrar un nuevo solicitante (Ej: "Carlos Restrepo", Cédula: "71234567", Fecha: "1954-08-10", Edad: 71).
     * Registrar una vivienda asociada a dicha cédula.
     * Consultar el registro para verificar que fue almacenado y recuperado exitosamente desde la base de datos PostgreSQL.
   * **Paso E: Flujo Automatizado E2E:**
     * Ir a la pestaña *"🔄 Flujo de Prueba E2E"* y presionar *"▶️ Ejecutar Flujo Completo"*.
     * Mostrar la ejecución en tiempo real de los 4 pasos y la terminal con código 200 OK.

---

## 🎬 Paso 6: Trazabilidad de Entrega y GitOps (D6 - 10%)
**Responsable: Daniel Duque**

1. **Demostrar la cadena de trazabilidad:**
   ```bash
   # 1. Obtener commit SHA actual en Git:
   git rev-parse --short HEAD

   # 2. Verificar que los pods en Minikube corresponden exactamente a los manifiestos:
   kubectl get deployment backend-deployment -n hipoteca-inversa -o jsonpath='{.spec.template.spec.containers[0].image}'
   ```
2. **Explicación del modelo declarativo GitOps:**
   > *"El directorio `k8s/` es nuestra Única Fuente de Verdad. Siguiendo los principios de GitOps, cualquier cambio en infraestructura se realiza mediante un commit en Git. Herramientas como ArgoCD o nuestro script `scripts/gitops-sync.ps1` detectan cualquier desviación (drift) entre el cluster y el repositorio y reconcilian automáticamente el estado deseado."*

---

## 🎬 Paso 7: Configuración, Seguridad y Secretos (D7 - 5%)
**Responsable: Juan Sebastian Pinilla Giraldo**

1. **Revisar cómo se gestionan los secretos en Kubernetes:**
   ```bash
   kubectl get secret postgres-secret -n hipoteca-inversa -o yaml
   kubectl get configmap postgres-configmap -n hipoteca-inversa -o yaml
   ```
2. **Demostración de Seguridad SQL:**
   * Mostrar el código en `backend/src//controlador_solicitante.py` donde se reemplazaron los f-strings por `%s`.
   * Ejecutar la prueba de inyección SQL:
     ```bash
     python -m pytest tests/test_seguridad_sql.py -v
     ```
   > *"Garantizamos que ninguna credencial reside en las imágenes ni en el código fuente. Toda la configuración de entorno reside en ConfigMaps y Secrets de Kubernetes, y los controladores previenen ataques de inyección SQL mediante consultas estrictamente parametrizadas."*

---

## 🎬 Paso 8: Observabilidad, Diagnóstico y Falla Provocada (D8 - 5%)
**Responsables: Ambos integrantes**

1. **Inspección de logs y eventos en vivo:**
   ```bash
   kubectl logs -l app=backend -n hipoteca-inversa --tail=15
   ```
2. **Ejecutar la simulación de falla y auto-recuperación (Self-Healing):**
   ```powershell
   .\scripts\simulate-failure-recovery.ps1
   ```
3. **Qué se observa:**
   * Se elimina un pod del backend deliberadamente (`kubectl delete pod`).
   * El Deployment detecta inmediatamente que sólo hay 1 pod disponible cuando la regla exige 2.
   * Kubernetes programa instantáneamente un nuevo pod de reemplazo que pasa sus pruebas de salud y queda en estado `Running`.
   * El servicio frontend continuó respondiendo sin interrupciones gracias al balanceo de carga entre réplicas.

---

## 🎬 Paso 9: Cierre, Calidad y Preguntas (D9 - 4%)
**Responsables: Ambos integrantes**

* Agradecer la atención del docente.
* Indicar que los pasos de reproducibilidad están documentados en el README para que cualquier evaluador clone y ejecute el proyecto con un solo comando.
* Responder preguntas técnicas con seguridad y respaldo en los archivos del repositorio.
