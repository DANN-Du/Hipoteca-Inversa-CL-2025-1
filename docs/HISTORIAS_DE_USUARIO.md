# Documentación de Historias de Usuario - Hipoteca Inversa CL

**Proyecto:** Hipoteca Inversa CL (2025-1)  
**Materia:** Gestión de la Configuración / DevOps  
**Equipo de Trabajo:**
- **Juan Sebastián Pinilla Giraldo** (`jpinilla880@soyudemedellin.edu.co`) - *Desarrollador Líder*
- **Daniel Duque** (`dduque642@soyudemedellin.edu.co`) - *Desarrollador DevOps*

---

## Matriz de Distribución de Responsabilidades

| ID | Historia de Usuario | Responsable | Capa / Área | Estado |
|---|---|---|---|---|
| **HU-01** | Simulación Financiera de Hipoteca Inversa | Juan Sebastián Pinilla Giraldo | Backend / Lógica de Negocio | **Completado** |
| **HU-02** | Registro y Consulta de Solicitantes con Validación de Edad | Juan Sebastián Pinilla Giraldo | Backend / Base de Datos | **Completado** |
| **HU-03** | Registro y Consulta de Viviendas en Garantía | Juan Sebastián Pinilla Giraldo | Backend / Base de Datos | **Completado** |
| **HU-04** | Seguridad y Prevención de Inyección SQL | Juan Sebastián Pinilla Giraldo | Base de Datos / Seguridad | **Completado** |
| **HU-05** | Interfaz Web Unificada de Gestión y Simulación | Juan Sebastián Pinilla Giraldo | Frontend / UX | **Completado** |
| **HU-06** | Documentación Interactiva de API REST con Swagger OpenAPI | Daniel Duque | Backend / API | **Completado** |
| **HU-07** | Contenerización Multi-Servicio con Docker y Docker Compose | Daniel Duque | Infraestructura / DevOps | **Completado** |
| **HU-08** | Pipeline CI/CD Automatizado con GitHub Actions | Daniel Duque | CI/CD / DevOps | **Completado** |
| **HU-09** | Despliegue Declarativo en Kubernetes / Minikube con Resiliencia | Daniel Duque | Orquestación / Kubernetes | **Completado** |
| **HU-10** | Pruebas Automatizadas End-to-End con Playwright | Daniel Duque | QA / Automatización | **Completado** |

---

## Detalle de Historias de Usuario

### HU-01: Simulación Financiera de Hipoteca Inversa
- **Responsable:** Juan Sebastián Pinilla Giraldo
- **Como:** Adulto mayor o asesor financiero.
- **Quiero:** Ingresar la edad del solicitante y el avalúo comercial de la vivienda.
- **Para:** Obtener el cálculo exacto de la cuota mensual proyectada, el porcentaje financiado (30% a 50%), el plazo en años y los intereses acumulados bajo la tasa EA del 24.78%.
- **Criterios de Aceptación:**
  1. Si la edad está entre 65 y 69 años: 30% del valor a 20 años.
  2. Si la edad está entre 70 y 74 años: 40% del valor a 15 años.
  3. Si la edad es >= 75 años: 50% del valor a 10 años.
  4. Si la edad es < 65 o >= 115 años, el sistema rechaza la solicitud con error explicativo (HTTP 400).
  5. El valor del inmueble debe ser de mínimo $50,000,000 COP.
- **Evidencia Técnica:** `backend/src//calculo.py`, `tests/test_calculo.py` (24 pruebas unitarias aprobadas).

---

### HU-02: Registro y Consulta de Solicitantes
- **Responsable:** Juan Sebastián Pinilla Giraldo
- **Como:** Asesor bancario.
- **Quiero:** Registrar los datos personales del solicitante (nombre, cédula, fecha de nacimiento, edad) y consultarlo por identificación.
- **Para:** Mantener trazabilidad de las personas interesadas en el producto financiero.
- **Criterios de Aceptación:**
  1. La cédula debe ser única en el sistema (Primary Key).
  2. La fecha de nacimiento debe coincidir coherentemente con la edad calculada.
  3. Los datos deben persistir en la tabla `solicitantes` de PostgreSQL.
- **Evidencia Técnica:** `backend/src//controlador_solicitante.py`, `tests/test_solicitante.py`.

---

### HU-03: Registro y Consulta de Viviendas en Garantía
- **Responsable:** Juan Sebastián Pinilla Giraldo
- **Como:** Asesor bancario o evaluador de crédito.
- **Quiero:** Registrar la información física y legal de la vivienda (dirección, barrio, ciudad, propietario, avalúo).
- **Para:** Respaldar el contrato de hipoteca inversa con una garantía hipotecaria verificada.
- **Criterios de Aceptación:**
  1. La dirección debe ser única en el sistema.
  2. El avalúo debe cumplir el monto mínimo de ley ($50,000,000 COP).
  3. Los datos deben persistir en la tabla `viviendas` de PostgreSQL.
- **Evidencia Técnica:** `backend/src//controlador_vivienda.py`, `tests/test_vivienda.py`.

---

### HU-04: Seguridad y Prevención de Inyección SQL
- **Responsable:** Juan Sebastián Pinilla Giraldo
- **Como:** Oficial de seguridad de la información.
- **Quiero:** Que todas las consultas hacia la base de datos se ejecuten mediante parámetros tipados (`%s`) y nunca mediante interpolación directa de cadenas (`f-strings`).
- **Para:** Evitar brechas de seguridad, robo de datos personales o alteración no autorizada de tablas.
- **Criterios de Aceptación:**
  1. Pruebas de inyección SQL con vectores tipo `' OR '1'='1` o `'; DROP TABLE solicitantes; --` deben ser neutralizadas como cadenas literales sin alterar la sintaxis SQL.
  2. Todas las operaciones CRUD deben usar `cursor.execute(sql, (param1, param2))`.
- **Evidencia Técnica:** `tests/test_seguridad_sql.py` (3 pruebas unitarias de inyección SQL aprobadas).

---

### HU-05: Interfaz Web Unificada de Gestión y Simulación
- **Responsable:** Juan Sebastián Pinilla Giraldo
- **Como:** Usuario final (adulto mayor o asesor).
- **Quiero:** Una interfaz gráfica web responsiva con pestañas de navegación para Simulador, Solicitantes, Viviendas y Flujo de Prueba.
- **Para:** Operar el sistema desde cualquier navegador web sin requerir instalaciones de escritorio locales.
- **Criterios de Aceptación:**
  1. Interfaz desacoplada servida por Nginx en puerto 80 / 3000 / 30080.
  2. Integración asíncrona mediante `fetch()` contra la API REST en `/api/v1/`.
  3. Mensajes visuales claros de éxito y error.
- **Evidencia Técnica:** `frontend/src/index.html`, `frontend/src/app.js`, `frontend/src/styles.css`.

---

### HU-06: Documentación Interactiva de API REST con Swagger OpenAPI
- **Responsable:** Daniel Duque
- **Como:** Desarrollador o integrador de sistemas externos.
- **Quiero:** Contar con una especificación OpenAPI viva y una interfaz Swagger UI interactiva.
- **Para:** Explorar y probar los endpoints de la API (`/api/v1/calculo`, `/api/v1/solicitantes`, `/api/v1/viviendas`, `/api/v1/health`) con esquemas de entrada y salida detallados.
- **Criterios de Aceptación:**
  1. Swagger UI disponible en la ruta `/apidocs/`.
  2. Esquema JSON de la especificación OpenAPI accesible en `/apispec_1.json`.
  3. Códigos de respuesta HTTP documentados (200, 201, 400, 404, 500, 503).
- **Evidencia Técnica:** `backend/app.py` (Flasgger), `tests/test_api_endpoints.py`.

---

### HU-07: Contenerización Multi-Servicio con Docker y Docker Compose
- **Responsable:** Daniel Duque
- **Como:** Desarrollador DevOps.
- **Quiero:** Empaquetar el backend, el frontend y la base de datos en contenedores Docker independientes y orquestarlos con Docker Compose.
- **Para:** Garantizar entornos de desarrollo idénticos, reproducibles y aislados en cualquier sistema operativo.
- **Criterios de Aceptación:**
  1. Backend en imagen multi-stage Python 3.12-slim (`dduque642/hipoteca-inversa-backend:latest`).
  2. Frontend en imagen ligera Nginx Alpine (`dduque642/hipoteca-inversa-frontend:latest`).
  3. `docker-compose up -d` levanta los 3 servicios con orden de inicio condicionado por healthcheck (`depends_on: service_healthy`).
- **Evidencia Técnica:** `backend/Dockerfile`, `frontend/Dockerfile`, `docker-compose.yml`.

---

### HU-08: Pipeline CI/CD Automatizado con GitHub Actions
- **Responsable:** Daniel Duque
- **Como:** Desarrollador DevOps y auditor de calidad.
- **Quiero:** Un flujo de integración continua automatizado que se dispare en cada `push` o `pull_request` a `main`.
- **Para:** Validar la calidad del código, ejecutar pruebas unitarias/API/E2E, compilar imágenes Docker y verificar manifiestos de Kubernetes antes del despliegue.
- **Criterios de Aceptación:**
  1. Ejecución de 37 pruebas unitarias y de API con contenedor PostgreSQL como servicio en el runner.
  2. Pruebas E2E de navegador con Chromium Headless vía Playwright.
  3. Validación estricta de manifiestos K8s con `kubectl apply -k k8s/ --dry-run=client`.
  4. Compilación y publicación condicional de imágenes Docker.
- **Evidencia Técnica:** `.github/workflows/ci.yml`.

---

### HU-09: Despliegue Declarativo en Kubernetes / Minikube con Resiliencia
- **Responsable:** Daniel Duque
- **Como:** Ingeniero de Operaciones / Infraestructura.
- **Quiero:** Desplegar la solución en Kubernetes (Minikube) utilizando manifiestos declarativos y Kustomize.
- **Para:** Ofrecer alta disponibilidad (2 réplicas), auto-recuperación de pods caídos (self-healing), persistencia con PVC y exposición mediante NodePort e Ingress.
- **Criterios de Aceptación:**
  1. Manifiestos organizados en `k8s/` (Namespace, Deployments, Services, ConfigMaps, Secrets, PVC, Ingress, Kustomization).
  2. Sondas `livenessProbe` y `readinessProbe` HTTP configuradas contra `/api/v1/health`.
  3. Script de un solo clic `scripts/deploy-minikube.ps1` / `.sh` que verifique el rollout exitoso de todos los recursos.
  4. Auto-recuperación demostrable: si un pod es eliminado manualmente, K8s levanta un sustituto en < 5 segundos.
- **Evidencia Técnica:** `k8s/`, `scripts/deploy-minikube.ps1`, `scripts/simulate-failure-recovery.ps1`.

---

### HU-10: Pruebas Automatizadas End-to-End con Playwright
- **Responsable:** Daniel Duque
- **Como:** Ingeniero de Control de Calidad (QA).
- **Quiero:** Una suite de pruebas de interfaz de usuario con Playwright que interactúe con el navegador real.
- **Para:** Comprobar que los flujos críticos (carga de página, Hola Mundo, navegación entre pestañas y simulación de cálculo) funcionan correctamente de extremo a extremo.
- **Criterios de Aceptación:**
  1. Verificación del título y del mensaje de bienvenida "¡Hola Mundo desde el Frontend de Hipoteca Inversa CL!".
  2. Llenado y envío del formulario del simulador con comprobación de los resultados de cuota e interés en pantalla.
  3. Cambio dinámico y renderizado de las pestañas de Solicitantes, Viviendas y Flujo de Prueba.
- **Evidencia Técnica:** `tests/test_playwright_e2e.py`.
