import red
import servidortcp
import Wireshark

ssid = "MiRedWiFi"
password = "pepe1234"
interfaz = "wlp0s20f3"  # Cambia esto al nombre de tu interfaz Wi-Fi

def main():
    print("Ejecutando proyecto de redes...")
    red.crear_punto_acceso()
    servidortcp.servidor_tcp()
    Wireshark.analizar_paquete()
    
    
    
if __name__ == '__main__':
    main()



 


