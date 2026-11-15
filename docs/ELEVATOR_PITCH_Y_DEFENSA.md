# 🎤 Guión del Elevator Pitch y Defensa Oral (4 a 5 Minutos)
## Proyecto: Hipoteca Inversa CL — Entrega Final DevOps (2025-1)

---

### 👥 Equipo y Roles en la Presentación
* **Juan Sebastian Pinilla Giraldo** (`jpinilla880@soyudemedellin.edu.co`) — Desarrollador Líder
* **Daniel Duque** (`dduque642@soyudemedellin.edu.co`) — Desarrollador DevOps

---

### ⏱️ Cronograma del Pitch (Total: 4:30 minutos)

| Minuto | Bloque de la Rúbrica | Contenido Principal | Orador Responsable |
| :---: | :--- | :--- | :--- |
| **0:00 - 1:00** | **P1: Problema y Motivación (5%)** | Contexto pensional en Colombia, adultos mayores 65+, vivienda como único activo ilíquido, falta de transparencia bancaria. | Juan Sebastian Pinilla |
| **1:00 - 2:00** | **P2: Propuesta de Valor y Alcance (5%)** | Solución web interactiva, cálculo según Banco de la República 2025, simulación de cuotas, intereses y gestión de garantías. | Daniel Duque |
| **2:00 - 3:15** | **P3: Justificación Técnica y DevOps (5%)** | Por qué arquitectura en 3 capas, contenerización, CI/CD, despliegue en Minikube/Kubernetes, trazabilidad y resiliencia. | Daniel Duque |
| **3:15 - 4:15** | **P4: Transición a la Demo en Vivo y Roles** | Presentación de la cadena de valor lista para demostrar: Git ➔ CI ➔ Docker ➔ Minikube ➔ Flujo E2E. | Juan Sebastian Pinilla |
| **4:15 - 4:30** | **Cierre y Apertura a Preguntas** | Conclusión de impacto social y solidez de ingeniería de software. | Ambos integrantes |

---

## 📜 Guión Literal para la Exposición Oral

### Minuto 0:00 a 1:00 — Problema y Motivación (P1)
**Orador: Juan Sebastian Pinilla Giraldo**

> *"Buenos días profesor y compañeros. En Colombia, más del 70% de los adultos mayores de 65 años no cuenta con una pensión de jubilación que garantice su sustento diario; sin embargo, una gran mayoría de ellos es propietaria de su vivienda, un patrimonio valioso pero completamente ilíquido.*
>
> *Aunque la ley colombiana y el Banco de la República habilitaron la figura de la **Hipoteca Inversa** para que un adulto mayor reciba una renta mensual sin perder el derecho a vivir en su hogar, hoy existe una enorme barrera: los bancos no ofrecen herramientas digitales transparentes que permitan a los adultos mayores y a sus familias simular con claridad matemática cuánto dinero recibirían, qué porcentaje de su casa respaldará el crédito, cuántos intereses se acumularán y cómo quedará su saldo final.*
>
> *Esta falta de herramientas genera desconfianza, cálculos erróneos y desprotección financiera para una de las poblaciones más vulnerables del país."*

---

### Minuto 1:00 a 2:00 — Propuesta de Valor y Alcance (P2)
**Orador: Daniel Duque**

> *"Para responder a esta necesidad, desarrollamos **Hipoteca Inversa CL**, una plataforma web completa, intuitiva y accesible que democratiza la orientación financiera para adultos mayores y asesores bancarios.*
>
> *Nuestra propuesta de valor se apoya en tres capacidades clave:*
> 1. * **Simulador Financiero Normativo:** Aplica de forma estricta las reglas colombianas para 2025: tasa efectiva anual del 24.78% (TEM de 1.86%), plazos de amortización según rangos de edad (de 3 a 20 años) y porcentajes de financiación del 30% al 70%, detallando cuota mensual, intereses proyectados y saldo final de la deuda.*
> 2. * **Gestión Integral de Solicitantes e Inmuebles:** Módulo seguro de registro y consulta de adultos mayores y sus viviendas en garantía sobre PostgreSQL, con validaciones estrictas y protección contra inyección SQL.*
> 3. * **Transparencia Total mediante API Abierta:** Exponemos toda la lógica a través de una API REST documentada interactivamente con Swagger (OpenAPI).*
>
> *Delimitamos con honestidad nuestro alcance: la plataforma orienta, simula y administra las solicitudes; no reemplaza el desembolso notarial ni la aprobación crediticia formal de la entidad bancaria."*

---

### Minuto 2:00 a 3:15 — Justificación Técnica y Prácticas DevOps (P3)
**Orador: Daniel Duque**

> *"Un producto financiero que maneja datos patrimoniales sensibles no puede depender de implementaciones improvisadas. Por eso, desde el inicio aplicamos una sólida ingeniería DevOps:*
>
> *1. **Arquitectura desacoplada en tres capas:** Separamos un Frontend moderno en Nginx Alpine, un Backend en Python Flask optimizado con Gunicorn y un motor de base de datos relacional PostgreSQL 16 con persistencia de datos.*
>
> *2. **Contenerización y Reproducibilidad:** Eliminamos el problema del 'en mi máquina sí funciona' empaquetando cada servicio en contenedores Docker optimizados, sin secretos embebidos y versionados con imágenes públicas en DockerHub.*
>
> *3. **Entrega Continua (CI/CD) con GitHub Actions:** Cada cambio en el código pasa por una batería automatizada de 37 pruebas unitarias de negocio, API y seguridad SQL, pruebas End-to-End en navegador con Playwright, y validación estricta de manifiestos Kubernetes. Si una prueba falla, el pipeline bloquea el avance de forma controlada.*
>
> *4. **Orquestación y GitOps en Kubernetes (Minikube):** Llevamos el sistema al estándar de la industria mediante manifiestos declarativos en Git, ConfigMaps, Secrets, almacenamiento persistente (PVC) y sondas de salud (liveness y readiness). Esto nos brinda auto-recuperación (self-healing) ante caídas de pods y escalabilidad sin tiempo de inactividad."*

---

### Minuto 3:15 a 4:15 — Transición a la Demostración Técnica en Vivo (P4)
**Orador: Juan Sebastian Pinilla Giraldo**

> *"A continuación, en la demostración técnica, no les mostraremos diapositivas ni capturas estáticas. Les evidenciaremos en vivo la cadena de entrega completa:*
> 1. *Veremos el repositorio Git navegable con commits e historial limpio.*
> 2. *El pipeline de GitHub Actions ejecutando pruebas reales y mostrando el caso de fallo controlado.*
> 3. *Las imágenes publicadas en DockerHub listas para ser desplegadas.*
> 4. *El despliegue en Minikube con sus Pods, Services, PVC y sondas activas.*
> 5. *Un flujo funcional real de punta a punta: desde la interfaz web, pasando por la API y persistiendo en PostgreSQL.*
> 6. *Y finalmente, una prueba de resiliencia donde provocaremos la caída forzada de un pod y observaremos cómo Kubernetes se recupera automáticamente.*
>
> *Damos inicio a la demostración técnica."*

---

### 💡 Preguntas Frecuentes y Respuestas Preparadas (Defensa Técnica)

* **P: ¿Por qué eligieron Minikube en lugar de desplegar en un cluster en la nube (EKS/GKE)?**
  * **R:** Minikube permite reproducir fielmente un cluster de Kubernetes estándar en local, validando recursos reales (Pods, Services, PVC, Ingress, Secrets, ConfigMaps) sin incurrir en costos de nube y garantizando que cualquier evaluador pueda reproducir el 100% de la infraestructura con un solo comando (`scripts/deploy-minikube.sh`).
* **P: ¿Cómo aseguran que no se filtren contraseñas o tokens?**
  * **R:** Aplicamos el principio de separación de configuración y código (Twelve-Factor App). En Git solo existen manifiestos con `Secret` de Kubernetes y archivos de muestra (`secret_config_sample.py`). En el cluster, los pods consumen las credenciales mediante `valueFrom.secretKeyRef`, manteniéndolas fuera de las imágenes Docker y del código fuente.
* **P: ¿Qué pasa si la base de datos se reinicia en Kubernetes?**
  * **R:** Implementamos un `PersistentVolumeClaim` (`postgres-pvc`) vinculado al almacenamiento del nodo. Los datos residen en el volumen montado en `/var/lib/postgresql/data`, de modo que si el pod de PostgreSQL se reinicia o se reubica, la información de solicitantes y viviendas permanece intacta.
