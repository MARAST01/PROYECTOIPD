# Usar una imagen base de Nginx
FROM nginx:alpine

# Elimina la configuración predeterminada de Nginx
RUN rm /etc/nginx/conf.d/default.conf

# Copia la configuración personalizada de Nginx
COPY nginx.conf /etc/nginx/conf.d/

# Copia el archivo frontend.html al directorio raíz que Nginx servirá
COPY frontend.html /usr/share/nginx/html/index.html

# Exponer el puerto 80 para el servidor web
#EXPOSE 80
