# Dockerfile para la aplicación Frontend - Hipoteca Inversa CL
# Tecnologías: HTML5, CSS3, JavaScript ES6+, Nginx Alpine
FROM nginx:1.25-alpine

# Eliminar configuración por defecto de Nginx
RUN rm -rf /etc/nginx/conf.d/default.conf

# Copiar la configuración personalizada de Nginx
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Copiar los archivos estáticos de la aplicación Frontend
COPY src/ /usr/share/nginx/html/

EXPOSE 80

# Chequeo de salud del servidor Nginx
HEALTHCHECK --interval=30s --timeout=3s --retries=3 \
  CMD wget --quiet --tries=1 --spider http://localhost/ || exit 1

CMD ["nginx", "-g", "daemon off;"]
