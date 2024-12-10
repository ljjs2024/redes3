import socket
import hashlib

ip_servidor = "localhost"  # Cambia esto a la IP del servidor
puerto_servidor = 5001  # Debe coincidir con el puerto del servidor

def calculate_checksum(data):
    """Calcula un checksum simple usando SHA256."""
    return hashlib.sha256(data).hexdigest()

def udp_client(host=ip_servidor, port=puerto_servidor, message='Hola desde el cliente!'):
    data = message.encode()
    checksum = calculate_checksum(data).encode()
    data_with_checksum = data + checksum

    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
        sock.sendto(data_with_checksum, (host, port))
        print(f"Mensaje enviado a {host}:{port}")

        # Espera la confirmación del servidor
        confirmation, _ = sock.recvfrom(4096)
        print(f"Confirmación del servidor: {confirmation.decode()}")

if __name__ == "__main__":
    udp_client(message="Este es un mensaje UDP con checksum.")
