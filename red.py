import pywifi
from pywifi import const
import time

def configurar_punto_acceso(ssid, password):
    wifi = pywifi.PyWiFi()
    iface = wifi.interfaces()[0]  # Obtén la primera interfaz Wi-Fi disponible

    # Desconectar cualquier conexión existente
    iface.disconnect()
    time.sleep(1)
    if iface.status() in [const.IFACE_DISCONNECTED, const.IFACE_INACTIVE]:
        print("Interfaz Wi-Fi desconectada correctamente.")

    # Configuración del punto de acceso
    profile = pywifi.Profile()
    profile.ssid = ssid
    profile.auth = const.AUTH_ALG_OPEN
    profile.akm.append(const.AKM_TYPE_WPA2PSK)
    profile.cipher = const.CIPHER_TYPE_CCMP
    profile.key = password

    # Eliminar perfiles antiguos y agregar el nuevo
    iface.remove_all_network_profiles()
    iface.add_network_profile(profile)

    # Conectar al punto de acceso
    iface.connect(profile)
    print(f"Punto de acceso '{ssid}' configurado.")
    time.sleep(5)  # Esperar un poco para estabilizar la conexión

if __name__ == "__main__":
    ssid = "MiRedWiFi"
    password = "pepe1234"
    configurar_punto_acceso(ssid, password)
