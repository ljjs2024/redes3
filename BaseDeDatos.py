import psycopg2
from psycopg2 import sql
import logging
import os

# Configurar logging
logging.basicConfig(
    filename="sistema_red.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def conectar_postgres(db_name):
    try:
        conexion = psycopg2.connect(
            host=os.getenv("DB_HOST", "localhost"),
            database=db_name,
            user=os.getenv("DB_USER", "postgres"),
            password=os.getenv("DB_PASSWORD", "pepe1234")
        )
        conexion.autocommit = True
        return conexion
    except Exception as e:
        logging.error(f"Error al conectar a PostgreSQL: {e}")
        return None

def crear_base_de_datos(conexion, nombre_bd):
    try:
        with conexion.cursor() as cursor:
            cursor.execute(sql.SQL("CREATE DATABASE {}").format(sql.Identifier(nombre_bd)))
            logging.info(f"Base de datos '{nombre_bd}' creada exitosamente.")
    except psycopg2.errors.DuplicateDatabase:
        logging.warning(f"La base de datos '{nombre_bd}' ya existe.")
    except Exception as e:
        logging.error(f"Error al crear la base de datos: {e}")

def crear_tablas(cursor):
    try:
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS dispositivos (
            id SERIAL PRIMARY KEY,
            nombre_dispositivo VARCHAR(100) NOT NULL,
            ip VARCHAR(15) NOT NULL UNIQUE,
            estado VARCHAR(50) DEFAULT 'conectado',
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """)
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS paquetes (
            id SERIAL PRIMARY KEY,
            dispositivo_id INTEGER REFERENCES dispositivos(id) ON DELETE CASCADE,
            contenido TEXT NOT NULL,
            protocolo VARCHAR(10) NOT NULL,
            valido BOOLEAN NOT NULL,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """)
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS eventos (
            id SERIAL PRIMARY KEY,
            descripcion TEXT NOT NULL,
            dispositivo_id INTEGER REFERENCES dispositivos(id) ON DELETE SET NULL,
            tipo_evento VARCHAR(50),
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """)
        logging.info("Tablas creadas exitosamente.")
    except Exception as e:
        logging.error(f"Error al crear las tablas: {e}")

def registrar_dispositivo(cursor, nombre_dispositivo, ip):
    try:
        cursor.execute("""
        INSERT INTO dispositivos (nombre_dispositivo, ip)
        VALUES (%s, %s) RETURNING id
        """, (nombre_dispositivo, ip))
        dispositivo_id = cursor.fetchone()[0]
        logging.info(f"Dispositivo '{nombre_dispositivo}' registrado con ID {dispositivo_id}.")
        return dispositivo_id
    except psycopg2.errors.UniqueViolation:
        logging.warning(f"El dispositivo con IP {ip} ya está registrado.")
        return None
    except Exception as e:
        logging.error(f"Error al registrar el dispositivo: {e}")
        return None

def registrar_paquete(cursor, dispositivo_id, contenido, protocolo, valido):
    try:
        cursor.execute("""
        INSERT INTO paquetes (dispositivo_id, contenido, protocolo, valido)
        VALUES (%s, %s, %s, %s)
        """, (dispositivo_id, contenido, protocolo, valido))
        logging.info(f"Paquete registrado: {contenido} (Protocolo: {protocolo}, Válido: {valido}).")
    except Exception as e:
        logging.error(f"Error al registrar el paquete: {e}")

def registrar_evento(cursor, descripcion, dispositivo_id=None, tipo_evento=None):
    try:
        cursor.execute("""
        INSERT INTO eventos (descripcion, dispositivo_id, tipo_evento)
        VALUES (%s, %s, %s)
        """, (descripcion, dispositivo_id, tipo_evento))
        logging.info(f"Evento registrado: {descripcion} (Tipo: {tipo_evento}).")
    except Exception as e:
        logging.error(f"Error al registrar el evento: {e}")

def main():
    db_name = os.getenv("DB_NAME", "red_raspberry")  # Base de datos configurable

    # Conexión inicial para verificar/crear la base de datos
    conexion_inicial = conectar_postgres("postgres")
    if conexion_inicial:
        crear_base_de_datos(conexion_inicial, db_name)
        conexion_inicial.close()

    # Conexión a la base de datos principal
    conexion = conectar_postgres(db_name)
    if conexion:
        try:
            with conexion.cursor() as cursor:
                crear_tablas(cursor)

                dispositivo_id = registrar_dispositivo(cursor, "Sensor1", "192.168.0.9")
                if dispositivo_id:
                    registrar_evento(cursor, "Conexión establecida", dispositivo_id, "conexión")
                    registrar_paquete(cursor, dispositivo_id, "Datos válidos de temperatura", "TCP", True)
                    registrar_evento(cursor, "Desconexión del dispositivo", dispositivo_id, "desconexión")
        except Exception as e:
            logging.error(f"Error durante las operaciones: {e}")
        finally:
            conexion.close()

if __name__ == "__main__":
    main()