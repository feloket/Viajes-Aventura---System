"""
Modulo de conexion a la base de datos
Sistema de Reservas - Viajes Aventura
"""
import mysql.connector
from mysql.connector import Error


class Database:
    """Clase para manejar la conexion a la base de datos MySQL."""

    _instance = None

    def __new__(cls):
        """
        Garantiza que solo exista una instancia de Database.
        """
        if cls._instance is None:
            cls._instance = super(Database, cls).__new__(cls)
            cls._instance.__initialized = False
        return cls._instance

    def __init__(self):
        """Constructor de la configuracion de la base de datos."""
        if self.__initialized:
            return

        self.__host = "localhost"
        self.__port = 3308  # Cambiar si se tiene otro
        self.__user = "root"
        self.__password = ""
        self.__database = "viajes_aventura_db"
        self.__connection = None
        self.__initialized = True

    def conectar(self):
        """Establece conexion con la base de datos."""
        try:
            if self.__connection is None or not self.__connection.is_connected():
                self.__connection = mysql.connector.connect(
                    host=self.__host,
                    port=self.__port,
                    user=self.__user,
                    password=self.__password,
                    database=self.__database
                )
                print(
                    f"Conexion establecida con la base de datos '{self.__database}'")

            if self.__connection.is_connected():
                return self.__connection

        except Error as e:
            if "Unknown database" in str(e):
                print(
                    f"Base de datos '{self.__database}' no existe. Creando...")
                self._crear_base_datos()
                return self.conectar()
            else:
                print(f"Error de conexion: {e}")
                raise Exception(f"Error de conexion: {e}")

    def _crear_base_datos(self):
        """Crea la base de datos si no existe."""
        try:
            temp_connection = mysql.connector.connect(
                host=self.__host,
                port=self.__port,
                user=self.__user,
                password=self.__password
            )
            cursor = temp_connection.cursor()
            cursor.execute(f"CREATE DATABASE IF NOT EXISTS {self.__database}")
            cursor.close()
            temp_connection.close()
            print(f"Base de datos '{self.__database}' creada exitosamente")

        except Error as e:
            raise Exception(f"Error al crear la base de datos: {e}")

    def crear_tablas(self):
        """Crea el esquema completo de la base de datos."""
        if self.__connection and self.__connection.is_connected():
            try:
                cursor = self.__connection.cursor()

                # Tabla Clientes (Usuarios del sistema)
                print("Creando tabla Clientes...")
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS Clientes (
                        id_cliente INT AUTO_INCREMENT PRIMARY KEY,
                        nombre_completo VARCHAR(150) NOT NULL,
                        email VARCHAR(100) NOT NULL UNIQUE,
                        telefono VARCHAR(20),
                        direccion VARCHAR(200),
                        fecha_registro DATE DEFAULT (CURRENT_DATE)
                    );
                """)
                self.__connection.commit()

                # Tabla Usuarios (Autenticacion)
                print("Creando tabla Usuarios...")
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS Usuarios (
                        id_usuario INT AUTO_INCREMENT PRIMARY KEY,
                        nombre_usuario VARCHAR(50) NOT NULL UNIQUE,
                        password_hash VARCHAR(255) NOT NULL,
                        rol VARCHAR(20) DEFAULT 'cliente',
                        id_cliente INT,
                        activo BOOLEAN DEFAULT TRUE,
                        fecha_creacion DATETIME DEFAULT CURRENT_TIMESTAMP,
                        FOREIGN KEY (id_cliente) REFERENCES Clientes(id_cliente)
                            ON DELETE CASCADE
                    );
                """)
                self.__connection.commit()

                # Tabla Destinos
                print("Creando tabla Destinos...")
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS Destinos (
                        id_destino INT AUTO_INCREMENT PRIMARY KEY,
                        nombre VARCHAR(100) NOT NULL,
                        descripcion TEXT,
                        actividades TEXT,
                        costo_base DECIMAL(10,2) NOT NULL,
                        disponible BOOLEAN DEFAULT TRUE,
                        fecha_creacion DATE DEFAULT (CURRENT_DATE)
                    );
                """)
                self.__connection.commit()

                # Tabla Paquetes Turisticos
                print("Creando tabla PaquetesTuristicos...")
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS PaquetesTuristicos (
                        id_paquete INT AUTO_INCREMENT PRIMARY KEY,
                        nombre VARCHAR(100) NOT NULL,
                        descripcion TEXT,
                        fecha_inicio DATE NOT NULL,
                        fecha_fin DATE NOT NULL,
                        precio_total DECIMAL(10,2) NOT NULL,
                        cupo_disponible INT DEFAULT 0,
                        disponible BOOLEAN DEFAULT TRUE,
                        fecha_creacion DATE DEFAULT (CURRENT_DATE)
                    );
                """)
                self.__connection.commit()

                # Tabla intermedia: Paquetes_Destinos (relacion muchos a muchos)
                print("Creando tabla Paquetes_Destinos...")
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS Paquetes_Destinos (
                        id_paquete_destino INT AUTO_INCREMENT PRIMARY KEY,
                        id_paquete INT NOT NULL,
                        id_destino INT NOT NULL,
                        orden_visita INT DEFAULT 1,
                        FOREIGN KEY (id_paquete) REFERENCES PaquetesTuristicos(id_paquete)
                            ON DELETE CASCADE,
                        FOREIGN KEY (id_destino) REFERENCES Destinos(id_destino)
                            ON DELETE CASCADE,
                        UNIQUE KEY unique_paquete_destino (id_paquete, id_destino)
                    );
                """)
                self.__connection.commit()

                # Tabla Reservas
                print("Creando tabla Reservas...")
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS Reservas (
                        id_reserva INT AUTO_INCREMENT PRIMARY KEY,
                        id_cliente INT NOT NULL,
                        id_paquete INT NOT NULL,
                        fecha_reserva DATETIME DEFAULT CURRENT_TIMESTAMP,
                        numero_personas INT DEFAULT 1,
                        precio_total DECIMAL(10,2) NOT NULL,
                        estado VARCHAR(20) DEFAULT 'pendiente',
                        notas TEXT,
                        FOREIGN KEY (id_cliente) REFERENCES Clientes(id_cliente)
                            ON DELETE CASCADE,
                        FOREIGN KEY (id_paquete) REFERENCES PaquetesTuristicos(id_paquete)
                            ON DELETE RESTRICT
                    );
                """)
                self.__connection.commit()

                print("Todas las tablas fueron creadas exitosamente")

            except Error as e:
                print(f"Error creando tablas: {e}")
                raise
            finally:
                if cursor:
                    cursor.close()
        else:
            raise Exception("No hay conexion activa a la base de datos")

    def ejecutar_query(self, query, params=None):
        """Ejecuta un query SQL de manera segura."""
        try:
            connection = self.conectar()
            cursor = connection.cursor(dictionary=True)

            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)

            return cursor

        except Error as e:
            print(f"Error ejecutando query: {e}")
            raise

    def desconectar(self):
        """Cierra la conexion a la base de datos."""
        if self.__connection and self.__connection.is_connected():
            self.__connection.close()
            self.__connection = None
            print("Conexion cerrada correctamente")

    def __del__(self):
        """Destructor que asegura que la conexion se cierre."""
        self.desconectar()
