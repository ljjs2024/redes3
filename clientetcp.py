import socket

# Configuración del cliente
ip_servidor = "localhost"  # Cambia esto a la IP del servidor
puerto_servidor = 5000  # Debe coincidir con el puerto del servidor

def enviar_mensaje(mensaje):
    try:
        # Crear un socket TCP
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as cliente:
            # Conectarse al servidor
            cliente.connect((ip_servidor, puerto_servidor))
            print("Conectado al servidor.")
            
            # Enviar el mensaje
            cliente.sendall(mensaje.encode())
            print(f"Mensaje enviado: {mensaje}")
    except Exception as e:
        print(f"Error al conectar o enviar el mensaje: {e}")

# Ejemplo de envío de mensaje
mensaje = "Hola desde el cliente!"
enviar_mensaje(mensaje)
