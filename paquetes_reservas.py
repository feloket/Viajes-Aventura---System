"""
Clases para gestion de paquetes turisticos y reservas
Viajes Aventura
"""
from datetime import date, datetime
from mysql.connector import Error


class PaqueteTuristico:
    """Clase que representa un paquete turistico."""

    def __init__(self, db, id_paquete=None, nombre="", descripcion="",
                 fecha_inicio=None, fecha_fin=None, precio_total=0.0,
                 cupo_disponible=0, disponible=True):
        """Construye un paquete turistico."""
        self.db = db
        self.id_paquete = id_paquete
        self.nombre = nombre
        self.descripcion = descripcion
        self.fecha_inicio = fecha_inicio
        self.fecha_fin = fecha_fin
        self.precio_total = precio_total
        self.cupo_disponible = cupo_disponible
        self.disponible = disponible
        self.destinos = []

    def __str__(self):
        """representa en string el paquete."""
        estado = "Disponible" if self.disponible else "No disponible"
        return (f"Paquete: {self.nombre} | {self.fecha_inicio} a {self.fecha_fin} | "
                f"Precio: ${self.precio_total:,.2f} | Cupo: {self.cupo_disponible} | "
                f"Estado: {estado}")

    def agregar_destino(self, id_destino, orden_visita=1):
        """Agrega un destino al paquete turistico."""
        sql = """
            INSERT INTO Paquetes_Destinos (id_paquete, id_destino, orden_visita)
            VALUES (%s, %s, %s)
        """
        values = (self.id_paquete, id_destino, orden_visita)

        try:
            connection = self.db.conectar()
            cursor = connection.cursor()
            cursor.execute(sql, values)
            connection.commit()
            print(
                f"Destino {id_destino} agregado al paquete {self.id_paquete}")
            return True

        except Error as e:
            connection.rollback()
            print(f"Error al agregar destino al paquete: {e}")
            return False
        finally:
            cursor.close()

    def cargar_destinos(self):
        """Carga los destinos asociados al paquete."""
        sql = """
            SELECT d.*, pd.orden_visita
            FROM Destinos d
            INNER JOIN Paquetes_Destinos pd ON d.id_destino = pd.id_destino
            WHERE pd.id_paquete = %s
            ORDER BY pd.orden_visita
        """

        try:
            connection = self.db.conectar()
            cursor = connection.cursor(dictionary=True)
            cursor.execute(sql, (self.id_paquete,))
            self.destinos = cursor.fetchall()
            return self.destinos

        except Error as e:
            print(f"Error al cargar destinos del paquete: {e}")
            return []
        finally:
            cursor.close()

    def guardar(self):
        """Guarda el paquete en la base de datos."""
        sql = """
            INSERT INTO PaquetesTuristicos 
            (nombre, descripcion, fecha_inicio, fecha_fin, precio_total, 
             cupo_disponible, disponible)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        values = (self.nombre, self.descripcion, self.fecha_inicio,
                  self.fecha_fin, self.precio_total, self.cupo_disponible,
                  self.disponible)

        try:
            connection = self.db.conectar()
            cursor = connection.cursor()
            cursor.execute(sql, values)
            connection.commit()
            self.id_paquete = cursor.lastrowid
            print(f"Paquete '{self.nombre}' creado con ID: {self.id_paquete}")
            return self.id_paquete

        except Error as e:
            connection.rollback()
            print(f"Error al crear paquete: {e}")
            return None
        finally:
            cursor.close()

    def actualizar(self):
        """Actualiza los datos del paquete."""
        sql = """
            UPDATE PaquetesTuristicos 
            SET nombre=%s, descripcion=%s, fecha_inicio=%s, fecha_fin=%s, 
                precio_total=%s, cupo_disponible=%s, disponible=%s
            WHERE id_paquete=%s
        """
        values = (self.nombre, self.descripcion, self.fecha_inicio,
                  self.fecha_fin, self.precio_total, self.cupo_disponible,
                  self.disponible, self.id_paquete)

        try:
            connection = self.db.conectar()
            cursor = connection.cursor()
            cursor.execute(sql, values)
            connection.commit()
            print(f"Paquete ID {self.id_paquete} actualizado correctamente")
            return True

        except Error as e:
            connection.rollback()
            print(f"Error al actualizar paquete: {e}")
            return False
        finally:
            cursor.close()

    def verificar_disponibilidad(self, numero_personas=1):
        """Verifica si el paquete tiene disponibilidad."""
        if not self.disponible:
            print("El paquete no esta disponible")
            return False

        if self.cupo_disponible < numero_personas:
            print(f"Cupo insuficiente. Disponible: {self.cupo_disponible}")
            return False

        if self.fecha_inicio < date.today():
            print("El paquete ya ha iniciado o finalizado")
            return False

        return True

    def reducir_cupo(self, numero_personas):
        """Reduce el cupo disponible del paquete."""
        self.cupo_disponible -= numero_personas

        if self.cupo_disponible == 0:
            self.disponible = False

        return self.actualizar()

    @staticmethod
    def listar_todos(db, solo_disponibles=False):
        """Lista todos los paquetes turisticos."""
        try:
            connection = db.conectar()
            cursor = connection.cursor(dictionary=True)

            if solo_disponibles:
                cursor.execute("""
                    SELECT * FROM PaquetesTuristicos 
                    WHERE disponible = TRUE AND fecha_inicio >= CURDATE()
                    ORDER BY fecha_inicio
                """)
            else:
                cursor.execute(
                    "SELECT * FROM PaquetesTuristicos ORDER BY fecha_inicio")

            resultados = cursor.fetchall()

            paquetes = []
            for row in resultados:
                paquete = PaqueteTuristico(
                    db,
                    id_paquete=row['id_paquete'],
                    nombre=row['nombre'],
                    descripcion=row['descripcion'],
                    fecha_inicio=row['fecha_inicio'],
                    fecha_fin=row['fecha_fin'],
                    precio_total=row['precio_total'],
                    cupo_disponible=row['cupo_disponible'],
                    disponible=row['disponible']
                )
                paquetes.append(paquete)

            return paquetes

        except Error as e:
            print(f"Error al listar paquetes: {e}")
            return []
        finally:
            cursor.close()

    @staticmethod
    def buscar_por_id(db, id_paquete):
        """Busca un paquete por su ID."""
        try:
            connection = db.conectar()
            cursor = connection.cursor(dictionary=True)
            cursor.execute("SELECT * FROM PaquetesTuristicos WHERE id_paquete = %s",
                           (id_paquete,))
            row = cursor.fetchone()

            if row:
                paquete = PaqueteTuristico(
                    db,
                    id_paquete=row['id_paquete'],
                    nombre=row['nombre'],
                    descripcion=row['descripcion'],
                    fecha_inicio=row['fecha_inicio'],
                    fecha_fin=row['fecha_fin'],
                    precio_total=row['precio_total'],
                    cupo_disponible=row['cupo_disponible'],
                    disponible=row['disponible']
                )
                paquete.cargar_destinos()
                return paquete
            return None

        except Error as e:
            print(f"Error al buscar paquete: {e}")
            return None
        finally:
            cursor.close()

    @staticmethod
    def buscar_por_fechas(db, fecha_inicio, fecha_fin):
        """Busca paquetes disponibles en un rango de fechas."""
        sql = """
            SELECT * FROM PaquetesTuristicos 
            WHERE disponible = TRUE 
            AND fecha_inicio >= %s 
            AND fecha_fin <= %s
            AND fecha_inicio >= CURDATE()
            ORDER BY fecha_inicio
        """

        try:
            connection = db.conectar()
            cursor = connection.cursor(dictionary=True)
            cursor.execute(sql, (fecha_inicio, fecha_fin))
            resultados = cursor.fetchall()

            paquetes = []
            for row in resultados:
                paquete = PaqueteTuristico(
                    db,
                    id_paquete=row['id_paquete'],
                    nombre=row['nombre'],
                    descripcion=row['descripcion'],
                    fecha_inicio=row['fecha_inicio'],
                    fecha_fin=row['fecha_fin'],
                    precio_total=row['precio_total'],
                    cupo_disponible=row['cupo_disponible'],
                    disponible=row['disponible']
                )
                paquetes.append(paquete)

            return paquetes

        except Error as e:
            print(f"Error al buscar paquetes por fechas: {e}")
            return []
        finally:
            cursor.close()


class Reserva:
    """Clase que representa una reserva de paquete turistico."""

    def __init__(self, db, id_reserva=None, id_cliente=None, id_paquete=None,
                 fecha_reserva=None, numero_personas=1, precio_total=0.0,
                 estado="pendiente", notas=""):
        """Construye una reserva."""
        self.db = db
        self.id_reserva = id_reserva
        self.id_cliente = id_cliente
        self.id_paquete = id_paquete
        self.fecha_reserva = fecha_reserva or datetime.now()
        self.numero_personas = numero_personas
        self.precio_total = precio_total
        self.estado = estado
        self.notas = notas

    def __str__(self):
        """Representa en string la reserva."""
        return (f"Reserva #{self.id_reserva} | Cliente: {self.id_cliente} | "
                f"Paquete: {self.id_paquete} | Personas: {self.numero_personas} | "
                f"Total: ${self.precio_total:,.2f} | Estado: {self.estado}")

    def crear(self):
        """Crea una nueva reserva en la base de datos."""
        # Verificar disponibilidad del paquete
        paquete = PaqueteTuristico.buscar_por_id(self.db, self.id_paquete)

        if not paquete:
            print("El paquete no existe")
            return None

        if not paquete.verificar_disponibilidad(self.numero_personas):
            return None

        # Calcular precio total
        self.precio_total = paquete.precio_total * self.numero_personas

        sql = """
            INSERT INTO Reservas 
            (id_cliente, id_paquete, fecha_reserva, numero_personas, 
             precio_total, estado, notas)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        values = (self.id_cliente, self.id_paquete, self.fecha_reserva,
                  self.numero_personas, self.precio_total, self.estado, self.notas)

        try:
            connection = self.db.conectar()
            cursor = connection.cursor()

            # Iniciar transaccion
            connection.start_transaction()

            # Crear reserva
            cursor.execute(sql, values)
            self.id_reserva = cursor.lastrowid

            # Reducir cupo del paquete
            if not paquete.reducir_cupo(self.numero_personas):
                connection.rollback()
                print("Error al actualizar cupo del paquete")
                return None

            # Confirmar transaccion
            connection.commit()
            print(f"Reserva #{self.id_reserva} creada exitosamente")
            print(f"Total a pagar: ${self.precio_total:,.2f}")
            return self.id_reserva

        except Error as e:
            connection.rollback()
            print(f"Error al crear reserva: {e}")
            return None
        finally:
            cursor.close()

    def actualizar_estado(self, nuevo_estado):
        """Actualiza el estado de la reserva."""
        if nuevo_estado not in ['pendiente', 'confirmada', 'cancelada']:
            print("Estado invalido")
            return False

        sql = "UPDATE Reservas SET estado = %s WHERE id_reserva = %s"

        try:
            connection = self.db.conectar()
            cursor = connection.cursor()
            cursor.execute(sql, (nuevo_estado, self.id_reserva))
            connection.commit()
            self.estado = nuevo_estado
            print(
                f"Reserva #{self.id_reserva} actualizada a estado: {nuevo_estado}")
            return True

        except Error as e:
            connection.rollback()
            print(f"Error al actualizar estado de reserva: {e}")
            return False
        finally:
            cursor.close()

    @staticmethod
    def listar_por_cliente(db, id_cliente):
        """Lista todas las reservas de un cliente."""
        sql = """
            SELECT r.*, p.nombre as nombre_paquete, p.fecha_inicio, p.fecha_fin
            FROM Reservas r
            INNER JOIN PaquetesTuristicos p ON r.id_paquete = p.id_paquete
            WHERE r.id_cliente = %s
            ORDER BY r.fecha_reserva DESC
        """

        try:
            connection = db.conectar()
            cursor = connection.cursor(dictionary=True)
            cursor.execute(sql, (id_cliente,))
            resultados = cursor.fetchall()

            reservas = []
            for row in resultados:
                reserva = Reserva(
                    db,
                    id_reserva=row['id_reserva'],
                    id_cliente=row['id_cliente'],
                    id_paquete=row['id_paquete'],
                    fecha_reserva=row['fecha_reserva'],
                    numero_personas=row['numero_personas'],
                    precio_total=row['precio_total'],
                    estado=row['estado'],
                    notas=row['notas']
                )
                reservas.append(reserva)

            return reservas

        except Error as e:
            print(f"Error al listar reservas del cliente: {e}")
            return []
        finally:
            cursor.close()

    @staticmethod
    def listar_todas(db):
        """Lista todas las reservas del sistema."""
        sql = """
            SELECT r.*, c.nombre_completo, p.nombre as nombre_paquete
            FROM Reservas r
            INNER JOIN Clientes c ON r.id_cliente = c.id_cliente
            INNER JOIN PaquetesTuristicos p ON r.id_paquete = p.id_paquete
            ORDER BY r.fecha_reserva DESC
        """

        try:
            connection = db.conectar()
            cursor = connection.cursor(dictionary=True)
            cursor.execute(sql)
            return cursor.fetchall()

        except Error as e:
            print(f"Error al listar reservas: {e}")
            return []
        finally:
            cursor.close()

    @staticmethod
    def buscar_por_id(db, id_reserva):
        """Busca una reserva por su ID."""
        try:
            connection = db.conectar()
            cursor = connection.cursor(dictionary=True)
            cursor.execute(
                "SELECT * FROM Reservas WHERE id_reserva = %s", (id_reserva,))
            row = cursor.fetchone()

            if row:
                return Reserva(
                    db,
                    id_reserva=row['id_reserva'],
                    id_cliente=row['id_cliente'],
                    id_paquete=row['id_paquete'],
                    fecha_reserva=row['fecha_reserva'],
                    numero_personas=row['numero_personas'],
                    precio_total=row['precio_total'],
                    estado=row['estado'],
                    notas=row['notas']
                )
            return None

        except Error as e:
            print(f"Error al buscar reserva: {e}")
            return None
        finally:
            cursor.close()
