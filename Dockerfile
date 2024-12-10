FROM python:3.12-slim

# Instalar las dependencias necesarias
WORKDIR /app
COPY . /app
RUN pip install -r requirements.txt

# Ejecutar la aplicación
CMD ["python", "main.py"]
