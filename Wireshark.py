import socket
import struct

paquetes_capturados = []

def obtener_mac(bytes_direccion):
    bytes_str = map('{:02x}'.format, bytes_direccion)
    direccion_mac = ':'.join(bytes_str).upper()
    return direccion_mac

def analizar_paquete(raw_data):
    dest_mac, src_mac, eth_proto, data = ethernet_frame(raw_data)
    print('\nEthernet Frame:')
    print(f'Dest MAC: {dest_mac}, Src MAC: {src_mac}, Protocol: {eth_proto}')

    paquetes_capturados.append(raw_data)  # Almacena el paquete en la lista

def ethernet_frame(data):
    dest_mac = obtener_mac(data[0:6])
    src_mac = obtener_mac(data[6:12])
    proto = struct.unpack('!H', data[12:14])[0]
    return dest_mac, src_mac, proto, data[14:]

def main():
    INTERFAZ_RED = 'wlp0s20f3'  #interfaz Wi-Fi

    try:
        conn = socket.socket(socket.AF_PACKET, socket.SOCK_RAW, socket.ntohs(3))
        conn.bind((INTERFAZ_RED, 0))
    except PermissionError:
        print("Error: Debes ejecutar este script con permisos de superusuario (sudo).")
        return
    except Exception as e:
        print(f"Ocurrió un error al crear el socket: {e}")
        return

    print(f"Iniciando captura de paquetes en la interfaz {INTERFAZ_RED}...\nPresiona Ctrl+C para detener la captura.")
    
    try:
        while True:
            raw_data, addr = conn.recvfrom(65536)
            analizar_paquete(raw_data)
    except KeyboardInterrupt:
        print("\nCaptura de paquetes detenida.")
    except Exception as e:
        print(f"Ocurrió un error durante la captura de paquetes: {e}")

    try:
        with open('captura_trafico.bin', 'wb') as f:
            for paquete in paquetes_capturados:
                f.write(paquete)
        print("\nPaquetes capturados guardados en 'captura_trafico.bin'. Puedes abrirlo en un analizador de paquetes compatible con formato binario.")
    except Exception as e:
        print(f"Ocurrió un error al guardar los paquetes: {e}")

if __name__ == "__main__":
    main()
