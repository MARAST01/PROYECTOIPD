# Usar una imagen base oficial de Python
FROM python:3.9

# Establecer el directorio de trabajo en el contenedor
WORKDIR /app

# Copiar los archivos necesarios al contenedor
COPY backend.py /app/
COPY requirements.txt /app/

# Instalar dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Exponer el puerto donde correrá el backend
EXPOSE 5000

# Comando para ejecutar la aplicación
CMD ["python", "backend.py"]
