import servidortcp
import red


def main():
    print("Ejecutando proyecto de redes...")
    red.crear_punto_acceso()
    servidortcp.servidor_tcp()
    
if __name__ == '__main__':
    main()



 


