# Usa una imagen base con Python 3.9 y una distribución Debian más completa
FROM python:3.9-buster

# Actualizar los repositorios y las listas de paquetes
RUN apt-get update -y && apt-get upgrade -y

# Instalar las dependencias necesarias
RUN apt-get install -y \
    network-manager \
    libnm-dev \
    libc6 \
    libreadline8 \
    python3-pip \
    dbus 
    

# Limpiar la caché para reducir el tamaño de la imagen
RUN apt-get clean && rm -rf /var/lib/apt/lists/*

# Establecer el directorio de trabajo en /app
WORKDIR /app

# Copiar los archivos de tu aplicación al contenedor
COPY . /app

# Instalar las dependencias de Python
RUN pip install -r requirements.txt

# Ejecutar el script principal cuando el contenedor se inicie
CMD ["python3", "main.py"]
