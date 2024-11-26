import subprocess
import socket
import threading


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



                    # Inicia servidor TCP en hilo separado
servidor_hilo = threading.Thread(target=servidor_tcp, args=(tcp_port,))
servidor_hilo.daemon = True  # para cuando el programa termine
servidor_hilo.start()