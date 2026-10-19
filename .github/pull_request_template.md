## 📌 Resumen de Cambios (Segunda Entrega)

Este Pull Request implementa todos los requerimientos y elementos de la **Segunda Entrega** del proyecto semestral:
- **Frontend desacoplado y contenerizado** con Nginx Alpine (`frontend/Dockerfile`, `frontend/nginx.conf`, SPA responsiva con simulador, CRUDs de solicitantes/viviendas y panel de flujo de prueba).
- **Backend API REST contenerizado** con Python 3.12-slim y Gunicorn (`backend/Dockerfile`, `backend/app.py`, CORS y endpoints).
- **Documentación Swagger / OpenAPI** integrada con Flasgger en `/apidocs/` y `/apispec_1.json`.
- **Base de datos PostgreSQL 16** con esquema definido en `sql/init.sql` e inicialización automática.
- **Orquestación con Docker Compose** (`docker-compose.yml`) con redes, volúmenes y healthchecks.
- **Prevención de Inyección SQL** parametrizando todas las consultas en `ControladorSolicitante` y `ControladorVivienda` (F-03 / HU-05).
- **Cálculo de intereses y saldo final** proyectado según normativa Banco de la República 2025 TEA 24.78% (F-02 / HU-04).
- **Exposición de CRUD de viviendas** en frontend y API REST (F-01 / HU-03).
- **Suites de Pruebas Automatizadas**: 37 pruebas unitarias/API/seguridad y 3 pruebas Playwright E2E.
- **Pipeline de CI** configurado con GitHub Actions en `.github/workflows/ci.yml`.

### 👥 Responsables
- Juan Sebastian Pinilla Giraldo (`jpinilla880@soyudemedellin.edu.co`)
- Daniel Duque (`dduque642@soyudemedellin.edu.co`)
