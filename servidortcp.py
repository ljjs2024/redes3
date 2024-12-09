import socket
import time
from datetime import datetime, timedelta

tcp_port = 5001  # Puerto TCP 
baneados = {}  # Diccionario de las direcciones IP baneadas y tiempos de ban
errores_por_cliente = {}  # Diccionario para rastrear errores por dirección IP
MAX_CONEXIONES = 3 
VENTANA_TIEMPO = 5  # Tiempo en segundos verificacion conexiones
conexiones_por_cliente = {}

def verificar_conexiones(ip_cliente):
    
    #Verifica si una IP ha tenido varias conexiones en un tiempo determinado.
    
    ahora = datetime.now()

    # Eliminar conexiones antiguas fuera de la ventana de tiempo
    conexiones_por_cliente[ip_cliente] = [
        t for t in conexiones_por_cliente.get(ip_cliente, []) if ahora - t <= timedelta(seconds=VENTANA_TIEMPO)
    ]

    # Contar las conexiones recientes
    conexiones_recientes = len(conexiones_por_cliente[ip_cliente])
    if conexiones_recientes >= MAX_CONEXIONES:
        return False  # Excedió el límite
    else:
        # Registrar la nueva conexión
        conexiones_por_cliente[ip_cliente].append(ahora)
        return True


def verificar_baneo(direccion):
    
    # Verifica si el cliente está baneado y si su tiempo ha expirado.
    
    if direccion in baneados:
        if datetime.now() < baneados[direccion]:
            return True  # El cliente sigue baneado
        else:
            del baneados[direccion]  # Eliminar del ban si ha expirado
    return False


def servidor_tcp(puerto):
    # Socket TCP
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as servidor:
        servidor.bind(("", puerto))  # Escucha todas las interfaces disponibles
        servidor.listen()
        print(f"Servidor TCP escuchando en el puerto {puerto}")

        while True:
            # Aceptar una nueva conexión
            cliente, direccion = servidor.accept()
            ip_cliente = direccion[0]  # Obtener solo la IP del cliente
            print(f"Conexión desde {ip_cliente}")

            # Verificar si el cliente está baneado
            if verificar_baneo(ip_cliente):
                print(f"{ip_cliente} está baneado. Rechazando conexión.")
                cliente.close()
                continue  # Rechazar la conexión y continuar con la siguiente

            try:
                with cliente:
                    # Recibe datos del cliente
                    datos = cliente.recv(1024)
                    if datos:
                        # Decodificar mensaje recibido
                        try:
                            mensaje = datos.decode("utf-8")
                            print(f"Mensaje recibido de {ip_cliente}: {mensaje}")
                        except UnicodeDecodeError:
                            print(f"Datos corruptos recibidos de {ip_cliente}.")
                            
                            # Contador de errores para el cliente
                            errores_por_cliente[ip_cliente] = errores_por_cliente.get(ip_cliente, 0) + 1

                            # Verificación del segundo error
                            if errores_por_cliente[ip_cliente] >= 2:
                                print(f"{ip_cliente} ha sido baneado por 2 minutos.")
                                baneados[ip_cliente] = datetime.now() + timedelta(minutes=2)
                                del errores_por_cliente[ip_cliente]  # Resetear errores al banear
                                cliente.close()  # Cerrar la conexión con el cliente
                                continue  # Continuar con la siguiente conexión
                            else:
                                print(f"Advertencia enviada a {ip_cliente} por datos corruptos.")
                    else:
                        print(f"Conexión cerrada por {ip_cliente} o mensaje vacío.")
            except Exception as e:
                print(f"Error procesando la conexión de {ip_cliente}: {e}")


# Iniciar el servidor TCP
servidor_tcp(tcp_port)
