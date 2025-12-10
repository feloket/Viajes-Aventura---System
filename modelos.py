"""
Modelos de datos del sistema de reservas
Viajes Aventura - Clases del negocio
"""
import bcrypt
from datetime import date, datetime
from mysql.connector import Error


class Cliente:
    """Clase que representa un cliente de la agencia."""

    def __init__(self, db, id_cliente=None, nombre_completo="", email="",
                 telefono="", direccion="", fecha_registro=None):
        """Construye un cliente."""
        self.db = db
        self.id_cliente = id_cliente
        self.nombre_completo = nombre_completo
        self.email = email
        self.telefono = telefono
        self.direccion = direccion
        self.fecha_registro = fecha_registro or date.today()

    def __str__(self):
        """representa en string del cliente."""
        # esto es para que el usuario vea
        return (f"Cliente: {self.nombre_completo} | Email: {self.email} | "
                f"Telefono: {self.telefono}")

    def guardar(self):
        """Guarda el cliente en la base de datos."""
        sql = """
            INSERT INTO Clientes (nombre_completo, email, telefono, direccion, fecha_registro)
            VALUES (%s, %s, %s, %s, %s)
        """
        values = (self.nombre_completo, self.email, self.telefono,
                  self.direccion, self.fecha_registro)

        try:
            connection = self.db.conectar()
            cursor = connection.cursor()
            cursor.execute(sql, values)
            connection.commit()
            self.id_cliente = cursor.lastrowid
            print(
                f"Cliente '{self.nombre_completo}' registrado con ID: {self.id_cliente}")
            return self.id_cliente

        except Error as e:
            connection.rollback()
            print(f"Error al registrar cliente: {e}")
            return None
        finally:
            cursor.close()

    def actualizar(self):
        """Actualiza los datos del cliente."""
        sql = """
            UPDATE Clientes 
            SET nombre_completo=%s, email=%s, telefono=%s, direccion=%s
            WHERE id_cliente=%s
        """
        values = (self.nombre_completo, self.email, self.telefono,
                  self.direccion, self.id_cliente)

        try:
            connection = self.db.conectar()
            cursor = connection.cursor()
            cursor.execute(sql, values)
            connection.commit()
            print(f"Cliente ID {self.id_cliente} actualizado correctamente")
            return True

        except Error as e:
            connection.rollback()
            print(f"Error al actualizar cliente: {e}")
            return False
        finally:
            cursor.close()

    @staticmethod
    def listar_todos(db):
        """Lista todos los clientes registrados."""
        try:
            connection = db.conectar()
            cursor = connection.cursor(dictionary=True)
            cursor.execute("SELECT * FROM Clientes ORDER BY nombre_completo")
            resultados = cursor.fetchall()

            clientes = []
            for row in resultados:
                cliente = Cliente(
                    db,
                    id_cliente=row['id_cliente'],
                    nombre_completo=row['nombre_completo'],
                    email=row['email'],
                    telefono=row['telefono'],
                    direccion=row['direccion'],
                    fecha_registro=row['fecha_registro']
                )
                clientes.append(cliente)

            return clientes

        except Error as e:
            print(f"Error al listar clientes: {e}")
            return []
        finally:
            cursor.close()

    @staticmethod
    def buscar_por_id(db, id_cliente):
        """Busca un cliente por su ID."""
        try:
            connection = db.conectar()
            cursor = connection.cursor(dictionary=True)
            cursor.execute(
                "SELECT * FROM Clientes WHERE id_cliente = %s", (id_cliente,))
            row = cursor.fetchone()

            if row:
                return Cliente(
                    db,
                    id_cliente=row['id_cliente'],
                    nombre_completo=row['nombre_completo'],
                    email=row['email'],
                    telefono=row['telefono'],
                    direccion=row['direccion'],
                    fecha_registro=row['fecha_registro']
                )
            return None

        except Error as e:
            print(f"Error al buscar cliente: {e}")
            return None
        finally:
            cursor.close()

    @staticmethod
    def buscar_por_email(db, email):
        """Busca un cliente por su email."""
        try:
            connection = db.conectar()
            cursor = connection.cursor(dictionary=True)
            cursor.execute("SELECT * FROM Clientes WHERE email = %s", (email,))
            row = cursor.fetchone()

            if row:
                return Cliente(
                    db,
                    id_cliente=row['id_cliente'],
                    nombre_completo=row['nombre_completo'],
                    email=row['email'],
                    telefono=row['telefono'],
                    direccion=row['direccion'],
                    fecha_registro=row['fecha_registro']
                )
            return None

        except Error as e:
            print(f"Error al buscar cliente por email: {e}")
            return None
        finally:
            cursor.close()


class Usuario:
    """Clase para autenticacion y autorizacion de usuarios."""

    def __init__(self, db, id_usuario=None, nombre_usuario="", password="",
                 rol="cliente", id_cliente=None, activo=True):
        """Construye un usuario del sistema."""
        self.db = db
        self.id_usuario = id_usuario
        self.nombre_usuario = nombre_usuario
        self.password = password
        self.rol = rol
        self.id_cliente = id_cliente
        self.activo = activo

    def __str__(self):
        """representa en string al usuario."""
        return f"Usuario: {self.nombre_usuario} | Rol: {self.rol}"

    @staticmethod
    def _hash_password(password):
        """Genera hash bcrypt de la contrasena con sal automatica."""
        salt = bcrypt.gensalt(rounds=12)
        hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
        return hashed.decode('utf-8')

    def registrar(self):
        """Registra un nuevo usuario en el sistema."""
        password_hash = self._hash_password(self.password)

        sql = """
            INSERT INTO Usuarios (nombre_usuario, password_hash, rol, id_cliente, activo)
            VALUES (%s, %s, %s, %s, %s)
        """
        values = (self.nombre_usuario, password_hash, self.rol,
                  self.id_cliente, self.activo)

        try:
            connection = self.db.conectar()
            cursor = connection.cursor()
            cursor.execute(sql, values)
            connection.commit()
            self.id_usuario = cursor.lastrowid
            print(
                f"Usuario '{self.nombre_usuario}' registrado con ID: {self.id_usuario}")
            print(f"Rol: {self.rol} | Contrasena hasheada con bcrypt + sal")
            return self.id_usuario

        except Error as e:
            connection.rollback()
            print(f"Error al registrar usuario: {e}")
            return None
        finally:
            cursor.close()

    def autenticar(self):
        """
        Autentica un usuario verificando sus credenciales.
        """
        try:
            connection = self.db.conectar()
            cursor = connection.cursor(dictionary=True)

            cursor.execute(
                "SELECT * FROM Usuarios WHERE nombre_usuario = %s AND activo = TRUE",
                (self.nombre_usuario,)
            )
            resultado = cursor.fetchone()

            if resultado:
                stored_hash = resultado['password_hash'].encode('utf-8')

                if bcrypt.checkpw(self.password.encode('utf-8'), stored_hash):
                    self.id_usuario = resultado['id_usuario']
                    self.rol = resultado['rol']
                    self.id_cliente = resultado['id_cliente']
                    print(
                        f"Autenticacion exitosa: {self.nombre_usuario} ({self.rol})")
                    return True
                else:
                    print("Usuario o contrasena incorrectos")
                    return False
            else:
                print("Usuario o contrasena incorrectos")
                return False

        except Error as e:
            print(f"Error en autenticacion: {e}")
            return False
        finally:
            cursor.close()

    def tiene_permiso(self, rol_requerido):
        """Verifica si el usuario tiene el rol requerido."""
        jerarquia = {"admin": 3, "empleado": 2, "cliente": 1}
        return jerarquia.get(self.rol, 0) >= jerarquia.get(rol_requerido, 0)

    @staticmethod
    def listar_todos(db):
        """Lista todos los usuarios del sistema."""
        try:
            connection = db.conectar()
            cursor = connection.cursor(dictionary=True)
            cursor.execute("""
                SELECT id_usuario, nombre_usuario, rol, id_cliente, activo, fecha_creacion
                FROM Usuarios
                ORDER BY nombre_usuario
            """)
            return cursor.fetchall()

        except Error as e:
            print(f"Error al listar usuarios: {e}")
            return []
        finally:
            cursor.close()


class Destino:
    """Clase que representa un destino turistico."""

    def __init__(self, db, id_destino=None, nombre="", descripcion="",
                 actividades="", costo_base=0.0, disponible=True):
        """Construye un destino turistico."""
        self.db = db
        self.id_destino = id_destino
        self.nombre = nombre
        self.descripcion = descripcion
        self.actividades = actividades
        self.costo_base = costo_base
        self.disponible = disponible

    def __str__(self):
        """representa en string el destino."""
        estado = "Disponible" if self.disponible else "No disponible"
        return (f"Destino: {self.nombre} | Costo: ${self.costo_base:,.2f} | "
                f"Estado: {estado}")

    def guardar(self):
        """Guarda el destino en la base de datos."""
        sql = """
            INSERT INTO Destinos (nombre, descripcion, actividades, costo_base, disponible)
            VALUES (%s, %s, %s, %s, %s)
        """
        values = (self.nombre, self.descripcion, self.actividades,
                  self.costo_base, self.disponible)

        try:
            connection = self.db.conectar()
            cursor = connection.cursor()
            cursor.execute(sql, values)
            connection.commit()
            self.id_destino = cursor.lastrowid
            print(f"Destino '{self.nombre}' creado con ID: {self.id_destino}")
            return self.id_destino

        except Error as e:
            connection.rollback()
            print(f"Error al crear destino: {e}")
            return None
        finally:
            cursor.close()

    def actualizar(self):
        """Actualiza los datos del destino."""
        sql = """
            UPDATE Destinos 
            SET nombre=%s, descripcion=%s, actividades=%s, costo_base=%s, disponible=%s
            WHERE id_destino=%s
        """
        values = (self.nombre, self.descripcion, self.actividades,
                  self.costo_base, self.disponible, self.id_destino)

        try:
            connection = self.db.conectar()
            cursor = connection.cursor()
            cursor.execute(sql, values)
            connection.commit()
            print(f"Destino ID {self.id_destino} actualizado correctamente")
            return True

        except Error as e:
            connection.rollback()
            print(f"Error al actualizar destino: {e}")
            return False
        finally:
            cursor.close()

    @staticmethod
    def eliminar(db, id_destino):
        """Elimina un destino de la base de datos."""
        try:
            connection = db.conectar()
            cursor = connection.cursor()
            cursor.execute(
                "DELETE FROM Destinos WHERE id_destino = %s", (id_destino,))
            connection.commit()
            print(f"Destino ID {id_destino} eliminado")
            return True

        except Error as e:
            connection.rollback()
            print(f"Error al eliminar destino: {e}")
            return False
        finally:
            cursor.close()

    @staticmethod
    def listar_todos(db, solo_disponibles=False):
        """Lista todos los destinos."""
        try:
            connection = db.conectar()
            cursor = connection.cursor(dictionary=True)

            if solo_disponibles:
                cursor.execute(
                    "SELECT * FROM Destinos WHERE disponible = TRUE ORDER BY nombre")
            else:
                cursor.execute("SELECT * FROM Destinos ORDER BY nombre")

            resultados = cursor.fetchall()

            destinos = []
            for row in resultados:
                destino = Destino(
                    db,
                    id_destino=row['id_destino'],
                    nombre=row['nombre'],
                    descripcion=row['descripcion'],
                    actividades=row['actividades'],
                    costo_base=row['costo_base'],
                    disponible=row['disponible']
                )
                destinos.append(destino)

            return destinos

        except Error as e:
            print(f"Error al listar destinos: {e}")
            return []
        finally:
            cursor.close()

    @staticmethod
    def buscar_por_id(db, id_destino):
        """Busca un destino por su ID."""
        try:
            connection = db.conectar()
            cursor = connection.cursor(dictionary=True)
            cursor.execute(
                "SELECT * FROM Destinos WHERE id_destino = %s", (id_destino,))
            row = cursor.fetchone()

            if row:
                return Destino(
                    db,
                    id_destino=row['id_destino'],
                    nombre=row['nombre'],
                    descripcion=row['descripcion'],
                    actividades=row['actividades'],
                    costo_base=row['costo_base'],
                    disponible=row['disponible']
                )
            return None

        except Error as e:
            print(f"Error al buscar destino: {e}")
            return None
        finally:
            cursor.close()
