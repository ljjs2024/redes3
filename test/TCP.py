import subprocess
import socket
import threading

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
                # Recibir datos del cliente
                while True:
                    datos = cliente.recv(1024)
                    if not datos:
                        break
                    mensaje = datos.decode()
                    print(f"Mensaje recibido: {mensaje}")

# Crear el punto de acceso
crear_punto_acceso(ssid, password, interfaz)

# Iniciar el servidor TCP en un hilo separado
servidor_hilo = threading.Thread(target=servidor_tcp, args=(tcp_port,))
servidor_hilo.daemon = True  # Para que se cierre cuando el programa termine
servidor_hilo.start()

# Detener el punto de acceso (ejecutar este comando cuando necesites detener la red)
# detener_punto_acceso(ssid)
import subprocess
import socket
import threading

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
        servidor.bind(("192.168.88.156", puerto))  # Escucha en todas las interfaces disponibles
        servidor.listen()
        print(f"Servidor TCP escuchando en el puerto {puerto}")

        while True:
            # Esperar una conexión
            cliente, direccion = servidor.accept()
            print(f"Conexión desde {direccion}")
            with cliente:
                # Recibir datos del cliente
                while True:
                    datos = cliente.recv(1024)
                    if not datos:
                        break
                    print(f"Datos recibidos: {datos.decode()}")

# Crear el punto de acceso
crear_punto_acceso(ssid, password, interfaz)

# Iniciar el servidor TCP en un hilo separado
servidor_hilo = threading.Thread(target=servidor_tcp, args=(tcp_port,))
servidor_hilo.daemon = True  # Para que se cierre cuando el programa termine
servidor_hilo.start()

# Detener el punto de acceso (ejecutar este comando cuando necesites detener la red)
# detener_punto_acceso(ssid)
