import subprocess

# Configuración de la red Wi-Fi
ssid = "MiRedWiFi"
password = "pepe1234"
interfaz = "wlp0s20f3"  # Cambia esto al nombre de tu interfaz Wi-Fi

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

# Crear el punto de acceso
crear_punto_acceso(ssid, password, interfaz)


# detener_punto_acceso(ssid)
