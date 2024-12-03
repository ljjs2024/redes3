import socket
tcp_port = 5001  # Puerto TCP para recibir paquetes




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
                    
                    
servidor_tcp(tcp_port)