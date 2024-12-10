import subprocess
import threading

def ejecutar_red():
    print("Iniciando script de configuración de red")
    subprocess.run(["python3", "red.py"])
    print("Script de red terminado.")

def ejecutar_servidortcp():
    print("Iniciando servidor TCP")
    subprocess.run(["python3", "servidortcp.py"])
    print("Servidor TCP terminado.")
    
def ejecutar_wireshark():
    print("Iniciando wireshark")
    subprocess.run(["python3", "Wireshark.py"])
    print("Wireshark terminado")
    
def ejecutar_base_de_datos():
    print("Iniciando base de datos")
    subprocess.run(["python3","BaseDeDatos.py"])
    print("Base de datos cerrada")
    
def ejecutar_servidorudp():
    print("Iniciando servidor UDP")
    subprocess.run(["python3", "server_udp.py"])
    print("Servidor UDP cerrada")

def main():
    try:
        # Crear hilos para ejecutar los scripts simultáneamente
        hilo_red = threading.Thread(target=ejecutar_red)
        hilo_servidorudp= threading.Thread(target=ejecutar_servidorudp)
        hilo_servidortcp = threading.Thread(target=ejecutar_servidortcp)
        #hilo_wireshark = threading.Thread(target=ejecutar_wireshark)
        #hilo_base_de_datos = threading.Thread(target=ejecutar_base_de_datos)

        # Iniciar los hilos
        hilo_red.start()
        hilo_servidorudp.start()
        hilo_servidortcp.start()
        #hilo_wireshark.start()
        #hilo_base_de_datos.start()


    except KeyboardInterrupt:
        print("\nInterrupción detectada. Cerrando los procesos...")
        # Los procesos se detendrán automáticamente al recibir la señal
    except Exception as e:
        print(f"Error al ejecutar los scripts: {e}")

if __name__ == "__main__":
    main()
