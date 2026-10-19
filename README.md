# 🏦 Hipoteca Inversa CL — Segunda Entrega (2025-1)

Sistema integral de simulación financiera de **Hipotecas Inversas en Colombia** y administración de solicitantes e inmuebles en garantía. Este proyecto fue desarrollado bajo una arquitectura monorepo contenerizada con **Docker**, comunicando una aplicación **Frontend**, una API REST **Backend** documentada con **Swagger (OpenAPI)** y una base de datos relacional **PostgreSQL**.

---

## 👥 Equipo de Trabajo e Integrantes

| Nombre Completo | Correo Institucional | Rol Principal | Responsabilidades Clave |
| :--- | :--- | :--- | :--- |
| **Juan Sebastian Pinilla Giraldo** | `jpinilla880@soyudemedellin.edu.co` | Desarrollador Líder | Arquitectura general, gestión de repositorio, CRUD de solicitantes y viviendas, parametrización SQL de seguridad. |
| **Daniel Duque** | `dduque642@soyudemedellin.edu.co` | Desarrollador | Contenerización Docker & Docker Compose, API REST con Swagger OpenAPI, modelo de cálculo e intereses, pruebas Playwright E2E. |

---

## 🚀 Arquitectura y Estructura Monorepo

El repositorio sigue estrictamente la estructura recomendada para la entrega, separando frontend y backend como módulos desacoplados y contenerizados:

```text
Hipoteca-Inversa-CL-2025-1/
├── docker-compose.yml              # Orquestación de Frontend, Backend y PostgreSQL
├── README.md                       # Documentación técnica completa y guía de ejecución
├── sql/
│   ├── init.sql                    # Script de inicialización automática de esquema y seed data
│   ├── crear_tabla_solicitantes.sql # DDL de tabla solicitantes
│   ├── crear_tabla_viviendas.sql    # DDL de tabla viviendas
│   └── create_tables.py            # Utilidad de creación manual de tablas
├── frontend/                       # Aplicación Web Cliente
│   ├── Dockerfile                  # Imagen basada en Nginx 1.25 Alpine
│   ├── .dockerignore               # Archivos excluidos de la compilación
│   ├── nginx.conf                  # Servidor estático y Reverse Proxy hacia la API
│   └── src/
│       ├── index.html              # Interfaz interactiva SPA (Simulador, CRUDs, E2E)
│       ├── styles.css              # Estilos responsivos modernos y accesibles
│       └── app.js                  # Lógica cliente y conexión con la API REST
├── backend/                        # Aplicación Servidor API REST
│   ├── Dockerfile                  # Imagen basada en Python 3.12-slim y Gunicorn
│   ├── .dockerignore               # Archivos temporales excluidos
│   ├── requirements.txt            # Dependencias oficiales de Python
│   ├── app.py                      # API Flask con Swagger (Flasgger), CORS y endpoints
│   ├── secret_config_sample.py     # Plantilla de credenciales locales
│   ├── src/
│   │   ├── model/                  # Lógica de cálculo, validaciones y entidades
│   │   │   ├── calculo.py          # Fórmulas de cuota, TEA/TEM, intereses y saldo final
│   │   │   ├── excepciones.py      # Excepciones de negocio (edad, valor vivienda)
│   │   │   ├── solicitante.py      # Entidad Solicitante con serialización JSON
│   │   │   └── vivienda.py         # Entidad Vivienda con serialización JSON
│   │   └── controller/             # Controladores con SQL parametrizado seguro
│   │       ├── controlador_solicitante.py
│   │       └── controlador_vivienda.py
│   └── templates/                  # Vistas web tradicionales (compatibilidad)
└── tests/                          # Suite de pruebas automatizadas
    ├── test_calculo.py             # 24 pruebas unitarias de reglas matemáticas de negocio
    ├── test_api_endpoints.py       # 10 pruebas de endpoints API y documentación Swagger
    ├── test_seguridad_sql.py       # 3 pruebas de prevención de inyección SQL
    └── test_playwright_e2e.py      # Pruebas End-to-End con Playwright (navegador Chromium)
```

> **Nota sobre Submódulos Git:** Si se requiere desacoplar el frontend y backend en repositorios independientes de GitHub manteniendo esta raíz monorepo, pueden vincularse como submódulos mediante:
> ```bash
> git submodule add https://github.com/PGSebas/hipoteca-frontend.git frontend
> git submodule add https://github.com/PGSebas/hipoteca-backend.git backend
> ```

---

## 🛠️ Tecnologías y Versiones Utilizadas

| Componente | Tecnología | Versión | Propósito |
| :--- | :--- | :--- | :--- |
| **Frontend** | HTML5 / CSS3 / JavaScript | ES6+ | Interfaz web interactiva con pestañas para simulador, CRUDs y flujo de prueba. |
| **Servidor Web Frontend** | Nginx | `1.25-alpine` | Servir interfaz estática y actuar como Reverse Proxy hacia el backend. |
| **Backend / API** | Python / Flask | `3.12+` / `3.1.3` | API RESTful orientada a servicios con validaciones de negocio. |
| **Documentación API** | Flasgger (OpenAPI / Swagger) | `0.9.7.1` | Documentación interactiva Swagger UI disponible en `/apidocs/`. |
| **Servidor WSGI** | Gunicorn | `21.2+` | Servidor de aplicaciones HTTP WSGI de grado productivo. |
| **Base de Datos** | PostgreSQL | `16-alpine` | Almacenamiento relacional de solicitantes e inmuebles en garantía. |
| **Driver de BD** | psycopg2-binary | `2.9.13` | Conexión optimizada de Python con PostgreSQL. |
| **Contenerización** | Docker & Docker Compose | `29.7+` / `v5.5+` | Empaquetado en contenedores y orquestación multi-servicio. |
| **Pruebas Unitarias** | Unittest & Pytest | `9.1+` | Cobertura de cálculos matemáticos, endpoints y seguridad SQL. |
| **Pruebas End-to-End** | Playwright (Chromium) | `1.64+` | Pruebas automatizadas en navegador real de las funcionalidades críticas. |

---

## 📦 Descarga del Proyecto e Imágenes DockerHub

### 1. Clonar el repositorio desde GitHub
```bash
git clone https://github.com/PGSebas/Hipoteca-Inversa-CL-2025-1.git
cd Hipoteca-Inversa-CL-2025-1
```

### 2. Descargar las imágenes oficiales desde DockerHub
Las imágenes contenerizadas del frontend y backend se encuentran configuradas con tags de DockerHub:

```bash
# Descargar imagen del Backend
docker pull dduque642/hipoteca-inversa-backend:latest

# Descargar imagen del Frontend
docker pull dduque642/hipoteca-inversa-frontend:latest

# Descargar imagen de la Base de Datos
docker pull postgres:16-alpine
```

### 3. Compilación y publicación en DockerHub (Guía de Integración)
Para construir y subir imágenes a su propio repositorio de DockerHub:
```bash
# Iniciar sesión en DockerHub
docker login

# Compilar y etiquetar Backend
docker build -t dduque642/hipoteca-inversa-backend:latest ./backend
docker push dduque642/hipoteca-inversa-backend:latest

# Compilar y etiquetar Frontend
docker build -t dduque642/hipoteca-inversa-frontend:latest ./frontend
docker push dduque642/hipoteca-inversa-frontend:latest
```

---

## ⚙️ Instalación y Puesta en Marcha

### Opción A: Ejecución con Docker Compose (Recomendada)

Garantiza la inicialización automática de los tres servicios, sus redes, volúmenes persistentes y el script de inicialización SQL.

1. **Asegúrese de tener Docker Desktop o el Docker Daemon en ejecución.**
2. **Levantar los servicios:**
   ```bash
   docker-compose up --build -d
   ```
3. **Verificar el estado de los contenedores:**
   ```bash
   docker-compose ps
   ```
4. **Ver los logs en tiempo real:**
   ```bash
   docker-compose logs -f
   ```
5. **Detener la aplicación:**
   ```bash
   docker-compose down
   ```

---

### Opción B: Ejecución Local sin Docker

#### 1. Requisitos previos
- Python 3.12 o superior instalado.
- Base de datos PostgreSQL local o en la nube (Render / Supabase / Neon).

#### 2. Configurar entorno virtual e instalar dependencias
```bash
# Crear y activar entorno virtual
python -m venv venv
# En Windows:
venv\Scripts\activate
# En Linux/macOS:
source venv/bin/activate

# Instalar dependencias del backend
pip install -r backend/requirements.txt
pip install pytest playwright pytest-playwright
python -m playwright install chromium
```

#### 3. Configurar variables de base de datos
Puede configurar las variables de entorno o crear `secret_config.py` a partir de la plantilla:
```powershell
copy secret_config_sample.py secret_config.py
```
O exportar variables de entorno:
```powershell
$env:DB_HOST="localhost"
$env:DB_PORT="5432"
$env:DB_NAME="hipoteca_db"
$env:DB_USER="postgres"
$env:DB_PASSWORD="su_password"
```

#### 4. Inicializar tablas en PostgreSQL
```bash
python sql/create_tables.py
```

#### 5. Ejecutar Backend
```bash
python backend/app.py
```
*El backend quedará escuchando en `http://localhost:5000`.*

---

## 🌐 URLs y Puntos de Acceso

| Servicio | URL Local | Descripción |
| :--- | :--- | :--- |
| **Frontend Web** | [http://localhost:80](http://localhost:80) o [http://localhost](http://localhost) | Plataforma visual interactiva con simulador, gestión de personas, viviendas y prueba E2E. |
| **Backend API** | [http://localhost:5000](http://localhost:5000) | Servidor API RESTful. |
| **Documentación Swagger UI** | [http://localhost:5000/apidocs/](http://localhost:5000/apidocs/) | Documentación interactiva OpenAPI con prueba en vivo de endpoints. |
| **Especificación OpenAPI JSON** | [http://localhost:5000/apispec_1.json](http://localhost:5000/apispec_1.json) | Especificación JSON consumible por herramientas como Postman o Insomnia. |

---

## 📖 Endpoints de la API REST (Swagger / OpenAPI)

| Método | Endpoint | Etiqueta | Descripción |
| :--- | :--- | :--- | :--- |
| `GET` | `/api/v1/hello` | General | "Hola Mundo" del backend que confirma estado del servicio. |
| `GET` | `/api/v1/health` | General | Chequeo de salud del backend y verificación de conexión con PostgreSQL. |
| `POST` | `/api/v1/calculo` | Cálculo | Simulación de cuota mensual, porcentaje, plazo, intereses y saldo final. |
| `GET` | `/api/v1/solicitantes` | Solicitantes | Listar todos los solicitantes registrados en la BD. |
| `POST` | `/api/v1/solicitantes` | Solicitantes | Registrar un nuevo solicitante (valida nombre, cédula, fecha, edad). |
| `GET` | `/api/v1/solicitantes/{id}` | Solicitantes | Buscar solicitante por cédula mediante consulta parametrizada. |
| `PUT` | `/api/v1/solicitantes/{id}` | Solicitantes | Modificar los datos de un solicitante existente. |
| `GET` | `/api/v1/viviendas` | Viviendas | Listar todas las viviendas registradas en garantía. |
| `POST` | `/api/v1/viviendas` | Viviendas | Registrar vivienda asociada al solicitante propietario (valida FK). |
| `GET` | `/api/v1/viviendas/{dir}` | Viviendas | Buscar vivienda por su dirección única. |
| `GET` | `/api/v1/viviendas/propietario/{id}` | Viviendas | Buscar todas las viviendas pertenecientes a un propietario. |
| `POST` | `/api/v1/crear_tablas` | General | Crea las tablas `solicitantes` y `viviendas` si no existen. |
| `POST` | `/api/v1/flujo-prueba` | Pruebas | Ejecuta el flujo automatizado integral de verificación Frontend ⟷ Backend ⟷ BD. |

---

## 📋 Historias de Usuario con Responsable Asignado

Cada integrante del equipo responde por un conjunto definido de historias de usuario trabajadas y entregadas:

| ID | Historia de Usuario | Criterios de Aceptación | Estado | Responsable Asignado |
| :--- | :--- | :--- | :--- | :--- |
| **HU-01** | **Cálculo de Cuota y Rango de Edad**<br>*Como adulto mayor, quiero calcular la cuota mensual orientativa según mi edad y el valor de mi vivienda.* | - Valida edad entre 65 y 114 años.<br>- Rechaza valores de vivienda menores a $50.000.000 COP.<br>- Aplica porcentajes de 30%, 40%, 55% y 70%.<br>- Determina plazos de 20, 15, 10, 5 y 3 años. | **Completada** | **Daniel Duque** |
| **HU-02** | **Registro y Consulta de Solicitantes en BD**<br>*Como asesor bancario, quiero registrar y consultar adultos mayores en la base de datos por su cédula.* | - Persiste en tabla `solicitantes` de PostgreSQL.<br>- Valida que no se dupliquen identificaciones primarias.<br>- Búsqueda rápida por cédula. | **Completada** | **Juan Sebastian Pinilla Giraldo** |
| **HU-03** | **Registro y Consulta de Viviendas en Garantía**<br>*Como asesor bancario, quiero asociar inmuebles a solicitantes existentes y consultarlos desde la web.* | - Valida clave foránea hacia la cédula del solicitante.<br>- Permite buscar vivienda por dirección o por propietario.<br>- Expone endpoints y vistas web. | **Completada** | **Juan Sebastian Pinilla Giraldo** |
| **HU-04** | **Cálculo de Intereses y Saldo Final Proyectado**<br>*Como asesor, quiero visualizar el interés acumulado y saldo final del crédito para orientar al cliente.* | - Aplica tasa TEA 24.78% (TEM 1.86%).<br>- Muestra intereses totales proyectados.<br>- Calcula el saldo final que respaldará el inmueble. | **Completada** | **Daniel Duque** |
| **HU-05** | **Seguridad y Prevención de Inyección SQL**<br>*Como equipo, queremos garantizar que todas las consultas a la BD estén parametrizadas.* | - Se eliminan consultas con f-strings en controladores.<br>- Se utilizan parámetros `%s` en todas las consultas.<br>- Pruebas unitarias de inyección SQL aprobadas. | **Completada** | **Juan Sebastian Pinilla Giraldo** |
| **HU-06** | **Documentación Interactiva con Swagger (OpenAPI)**<br>*Como desarrollador/evaluador, quiero explorar y probar los endpoints de la API mediante Swagger UI.* | - Documentación OpenAPI en `/apidocs/`.<br>- Especificación JSON en `/apispec_1.json`.<br>- Modelos de entrada y salida documentados con ejemplos. | **Completada** | **Daniel Duque** |
| **HU-07** | **Contenerización Multi-servicio con Docker Compose**<br>*Como equipo DevOps, queremos desplegar frontend, backend y BD con un único comando reproducible.* | - Dockerfile optimizado para Frontend (Nginx Alpine).<br>- Dockerfile para Backend (Python 3.12-slim / Gunicorn).<br>- `docker-compose.yml` con healthchecks, networks y volúmenes. | **Completada** | **Daniel Duque** |
| **HU-08** | **Pruebas Automatizadas Unitarias y Playwright E2E**<br>*Como equipo de calidad, queremos suites de pruebas automáticas para la lógica crítica y la UI.* | - Pruebas unitarias matemáticas y de API con Pytest.<br>- Pruebas E2E en navegador Chromium con Playwright.<br>- Verificación de flujo integral completo. | **Completada** | **Juan Sebastian Pinilla Giraldo** & **Daniel Duque** |

---

## 🧪 Pruebas Automatizadas (Unitarias y Playwright E2E)

El proyecto cuenta con dos suites de pruebas automatizadas:

### 1. Ejecutar Pruebas Unitarias y de API (37 pruebas)
Prueban las fórmulas de negocio, validaciones de excepciones, consultas parametrizadas contra inyección SQL y todos los endpoints de la API REST:

```bash
python -m pytest tests/test_calculo.py tests/test_api_endpoints.py tests/test_seguridad_sql.py -v
```

*Resultado esperado:*
```text
tests/test_calculo.py::TestHipotecaInversa::test_caso_1_pago_mensual PASSED
...
tests/test_api_endpoints.py::TestApiEndpoints::test_swagger_ui_available PASSED
tests/test_seguridad_sql.py::TestSeguridadSQL::test_prevencion_sql_injection_solicitante PASSED
============================== 37 passed in 4.88s ==============================
```

### 2. Ejecutar Pruebas End-to-End con Playwright
Prueban de forma autónoma en el navegador Chromium la interfaz web, el formulario de simulación y la navegación por pestañas:

```bash
python -m pytest tests/test_playwright_e2e.py -v
```

*Resultado esperado:*
```text
tests/test_playwright_e2e.py::test_e2e_carga_inicial_hola_mundo PASSED
tests/test_playwright_e2e.py::test_e2e_simulador_calculo_exitoso PASSED
tests/test_playwright_e2e.py::test_e2e_navegacion_pestanas PASSED
============================== 3 passed in 29.63s ==============================
```

---

## 🔄 Flujo Completo de Prueba (Frontend ⟷ Backend ⟷ Base de Datos)

Para garantizar la comunicación integral entre los tres componentes:
1. Ingrese a la aplicación web en [http://localhost:80](http://localhost:80).
2. Diríjase a la pestaña **"🔄 Flujo de Prueba E2E"**.
3. Haga clic en **"▶️ Ejecutar Flujo Completo"**.
4. La aplicación ejecutará en vivo:
   - **Paso 1:** Petición HTTP desde el Frontend hacia la API del Backend (`POST /api/v1/flujo-prueba`).
   - **Paso 2:** El Backend genera un solicitante de prueba y lo inserta en la base de datos PostgreSQL.
   - **Paso 3:** El Backend asocia un inmueble con clave foránea en la tabla `viviendas`.
   - **Paso 4:** El Backend consulta de forma parametrizada el registro insertado y calcula la hipoteca inversa correspondiente.
   - **Paso 5:** El Frontend recibe la respuesta con código `200 OK` y muestra el estado **"100% Exitoso: Comunicación Frontend ⟷ Backend ⟷ Base de Datos Garantizada"**.

---

## 📄 Reglas de Negocio Financieras Aplicadas

1. **Tasa de Interés de Referencia:**
   - Tasa Efectiva Anual (TEA): **24.78%** (Banco de la República 2025).
   - Tasa Efectiva Mensual (TEM):
     $$i_{mensual} = (1 + 0.2478)^{\frac{1}{12}} - 1 \approx 1.86\%$$
2. **Porcentaje Financiado según Edad:**
   - 65 a 69 años: **30%** del valor comercial.
   - 70 a 79 años: **40%** del valor comercial.
   - 80 a 84 años: **55%** del valor comercial.
   - 85 a 114 años: **70%** del valor comercial.
3. **Plazo de Pago de Cuotas:**
   - 65 a 69 años: **20 años** (240 cuotas mensuales).
   - 70 a 74 años: **15 años** (180 cuotas mensuales).
   - 75 a 79 años: **10 años** (120 cuotas mensuales).
   - 80 a 84 años: **5 años** (60 cuotas mensuales).
   - 85 a 114 años: **3 años** (36 cuotas mensuales).
4. **Valor de Vivienda Mínimo:** $50.000.000 COP.
