import socket
import hashlib
from datetime import datetime, timedelta

udp_port = 5000  # Puerto UDP
baneados = {}  # Diccionario de las direcciones IP baneadas y tiempos de ban
errores_por_cliente = {}  # Diccionario para rastrear errores por dirección IP
MAX_CONEXIONES = 3
VENTANA_TIEMPO = 5  # Tiempo en segundos verificación conexiones
conexiones_por_cliente = {}

def calculate_checksum(data):
    """Calcula un checksum simple usando SHA256."""
    return hashlib.sha256(data).hexdigest()

def is_corrupt(data, received_checksum):
    """Verifica si los datos están corruptos comparando checksums."""
    calculated_checksum = calculate_checksum(data)
    return calculated_checksum != received_checksum

def verificar_conexiones(ip_cliente):
    ahora = datetime.now()
    conexiones_por_cliente[ip_cliente] = [
        t for t in conexiones_por_cliente.get(ip_cliente, []) if ahora - t <= timedelta(seconds=VENTANA_TIEMPO)
    ]
    conexiones_recientes = len(conexiones_por_cliente[ip_cliente])
    if conexiones_recientes >= MAX_CONEXIONES:
        return False  # Excedió el límite
    else:
        conexiones_por_cliente[ip_cliente].append(ahora)
        return True

def verificar_baneo(direccion):
    if direccion in baneados:
        if datetime.now() < baneados[direccion]:
            return True  # El cliente sigue baneado
        else:
            del baneados[direccion]  # Eliminar del ban si ha expirado
    return False

def udp_server(host='localhost', port=udp_port):
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
        sock.bind((host, port))
        print(f"Servidor UDP escuchando en {host}:{port}")

        while True:
            data, addr = sock.recvfrom(4096)  # Recibe hasta 4096 bytes
            ip_cliente = addr[0]
            print(f"Conexión desde {ip_cliente}")

            if verificar_baneo(ip_cliente):
                print(f"{ip_cliente} está baneado. Rechazando conexión.")
                continue

            if len(data) < 64:
                print("Paquete recibido es demasiado pequeño para contener un checksum válido.")
                continue

            received_checksum = data[-64:].decode()  # Últimos 64 bytes son el checksum
            actual_data = data[:-64]  # Datos reales

            if is_corrupt(actual_data, received_checksum):
                print(f"Paquete corrupto recibido de {ip_cliente}, descartado.")
                errores_por_cliente[ip_cliente] = errores_por_cliente.get(ip_cliente, 0) + 1
                if errores_por_cliente[ip_cliente] >= 2:
                    print(f"{ip_cliente} ha sido baneado por 2 minutos.")
                    baneados[ip_cliente] = datetime.now() + timedelta(minutes=2)
                    del errores_por_cliente[ip_cliente]
                else:
                    print(f"Advertencia enviada a {ip_cliente} por datos corruptos.")
            else:
                print(f"Paquete válido recibido de {ip_cliente}: {actual_data.decode()}")
                confirmation_message = "Mensaje recibido correctamente."
                sock.sendto(confirmation_message.encode(), addr)

if __name__ == "__main__":
    udp_server()
