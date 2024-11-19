import subprocess
import socket

# Configuración de la red Wi-Fi
ssid = "MiRedWiFi"
password = "pepe1234"
interfaz = "wlp0s20f3"  # Cambia esto al nombre de tu interfaz Wi-Fi
tcp_port = 5000  # Puerto TCP para recibir paquetes

def crear_punto_acceso(ssid, password, interfaz):
    try:
        # Crear el punto de acceso usando nmcli
        subprocess.run(
            ["sudo", "nmcli", "dev", "wifi", "hotspot", 
             "ifname", interfaz, 
             "ssid", ssid, 
             "password", password], 
            check=True
        )
        print(f"Punto de acceso '{ssid}' creado exitosamente.")
    except subprocess.CalledProcessError as e:
        print(f"Error al crear el punto de acceso: {e}")

def detener_punto_acceso(ssid):
    try:
        # Detener el punto de acceso
        subprocess.run(
            ["sudo", "nmcli", "connection", "down", "id", ssid], 
            check=True
        )
        print(f"Punto de acceso '{ssid}' detenido exitosamente.")
    except subprocess.CalledProcessError as e:
        print(f"Error al detener el punto de acceso: {e}")

def servidor_tcp(puerto):
    # Crear un socket TCP
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as servidor:
        servidor.bind(("", puerto))  # Escucha en todas las interfaces disponibles
        servidor.listen()
        print(f"Servidor TCP escuchando en el puerto {puerto}")

        while True:
            # Esperar una conexión
            cliente, direccion = servidor.accept()
            print(f"Conexión desde {direccion}")
            with cliente:
                # Esperar y recibir el mensaje del cliente
                datos = cliente.recv(1024)
                if datos:
                    mensaje = datos.decode()
                    print(f"Mensaje recibido: {mensaje}")
                else:
                    print("No se recibió ningún mensaje o la conexión se cerró inesperadamente.")

# Crear el punto de acceso
crear_punto_acceso(ssid, password, interfaz)

# Iniciar el servidor TCP en el hilo principal para que espere indefinidamente
servidor_tcp(tcp_port)

# Nota: No necesitas detener el punto de acceso aquí, ya que el programa no terminará automáticamente.
# Puedes detener el punto de acceso manualmente después de finalizar el programa.
