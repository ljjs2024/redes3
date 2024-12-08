import scapy.all as scapy
from scapy.all import sniff, wrpcap

# Lista para almacenar los paquetes
paquetes_capturados = []

def analizar_paquete(paquete):
    print("\n--- Paquete capturado ---")
    paquete.show()  # Muestra información del paquete
    paquetes_capturados.append(paquete)  # Almacena el paquete en la lista

# Configura la interfaz de red que será monitoreada
INTERFAZ_RED = "eth0"  # Cambiar según el caso (e.g., wlan0 para Wi-Fi)

try:
    print(f"Iniciando captura de paquetes en la interfaz {INTERFAZ_RED}...\nPresiona Ctrl+C para detener la captura.")
    # Captura los paquetes en tiempo real, aplicando la función analizar_paquete a cada uno
    sniff(iface=INTERFAZ_RED, prn=analizar_paquete, store=False, timeout=60)  # Captura durante 60 segundos

    # Guarda los paquetes capturados en un archivo pcap
    wrpcap("captura_trafico.pcap", paquetes_capturados)
    print("\nPaquetes capturados guardados en 'captura_trafico.pcap'. Puedes abrirlo en Wireshark.")

except PermissionError:
    print("Error: Debes ejecutar este script con permisos de superusuario (sudo).")
except Exception as e:
    print(f"Ocurrió un error: {e}")

