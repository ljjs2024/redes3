import subprocess
import socket
import threading

# Configuración de la red Wi-Fi
ssid = "MiRedWiFi"
password = "pepe1234"
interfaz = "wlp0s20f3"  # nombre de tu interfaz Wi-Fi
tcp_port = 5000  # Puerto TCP 

def crear_punto_acceso(ssid, password, interfaz):
    try:
        # punto de acceso usando nmcli
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
        # Detener punto de acceso
        subprocess.run(
            ["sudo", "nmcli", "connection", "down", "id", ssid], 
            check=True
        )
        print(f"Punto de acceso '{ssid}' detenido exitosamente.")
    except subprocess.CalledProcessError as e:
        print(f"Error al detener el punto de acceso: {e}")

def servidor_tcp(puerto):
    # Creacion socket TCP
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as servidor:
        servidor.bind(("", puerto))  # colocar ip rasperry
        servidor.listen()
        print(f"Servidor TCP escuchando en el puerto {puerto}")

        while True:
            # Espera conexion
            cliente, direccion = servidor.accept()
            print(f"Conexión desde {direccion}")
            with cliente:
                # Recibe datos
                while True:
                    datos = cliente.recv(1024)
                    if not datos:
                        break
                    mensaje = datos.decode()
                    print(f"Mensaje recibido: {mensaje}")

# Crear el punto de acceso
crear_punto_acceso(ssid, password, interfaz)

# Inicia servidor TCP en hilo separado
servidor_hilo = threading.Thread(target=servidor_tcp, args=(tcp_port,))
servidor_hilo.daemon = True  # para cuando el programa termine
servidor_hilo.start()


