# Usar una imagen base de Python
FROM python:3.12-slim

# Configurar el directorio de trabajo
WORKDIR /app

# Copiar los archivos al contenedor
COPY . .

# Instalar las dependencias (si hay un archivo requirements.txt)
RUN pip install --no-cache-dir -r requirements.txt

# Default command
CMD ["python", "main.py"]
