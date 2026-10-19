# Dockerfile para el Backend - Hipoteca Inversa CL
# Tecnologías: Python 3.12, Flask, Flasgger (OpenAPI/Swagger), Gunicorn
FROM python:3.12-slim

WORKDIR /app

# Instalar dependencias del sistema mínimas
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copiar dependencias de Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el código fuente y recursos
COPY src/ ./src/
COPY sql/ ./sql/
COPY templates/ ./templates/
COPY secret_config_sample.py ./secret_config_sample.py
COPY app.py .

# Configurar variables de entorno
ENV PYTHONUNBUFFERED=1 \
    PORT=5000 \
    PYTHONPATH=/app:/app/src

EXPOSE 5000

# Chequeo de salud del contenedor
HEALTHCHECK --interval=20s --timeout=5s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:5000/api/v1/health || exit 1

# Ejecución del servidor WSGI Gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "2", "--timeout", "60", "app:app"]
