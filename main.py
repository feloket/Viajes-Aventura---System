"""
Sistema de Reservas - Viajes Aventura.
Programa principal con menu.
"""
from conexion_db import Database
from modelos import Cliente, Usuario, Destino
from paquetes_reservas import PaqueteTuristico, Reserva
from datetime import datetime, date


# Variable global para el usuario autenticado
USUARIO_ACTUAL = None


def limpiar_pantalla():
    """Simula limpiar la pantalla con lineas en blanco"""
    print("\n" * 2)


def mostrar_menu_principal():
    """Muestra el menu principal del sistema"""
    print("\n" + "="*70)
    print(" " * 18 + "SISTEMA DE RESERVAS - VIAJES AVENTURA")
    print("="*70)
    print("1. Gestion de Destinos")
    print("2. Gestion de Paquetes Turisticos")
    print("3. Gestion de Clientes")
    print("4. Realizar Reserva")
    print("5. Ver Mis Reservas")
    print("6. Administracion de Usuarios")
    print("7. Ver Todas las Reservas (Admin)")
    print("0. Cerrar Sesion y Salir")
    print("="*70)


def menu_destinos(db):
    """
    Menu de gestion de destinos.
    Permite crear, listar, modificar y eliminar destinos.
    """
    while True:
        limpiar_pantalla()
        print("\n" + "="*70)
        print(" " * 25 + "GESTION DE DESTINOS")
        print("="*70)
        print("1. Agregar nuevo destino")
        print("2. Listar todos los destinos")
        print("3. Modificar destino")
        print("4. Eliminar destino")
        print("0. Volver al menu principal")
        print("="*70)

        opcion = input("\nSeleccione una opcion: ").strip()

        if opcion == "1":
            # Agregar destino
            print("\n--- AGREGAR NUEVO DESTINO ---")
            nombre = input("Nombre del destino: ").strip()
            descripcion = input("Descripcion: ").strip()
            actividades = input("Actividades disponibles: ").strip()

            try:
                costo_base = float(input("Costo base: ").strip())
            except ValueError:
                print("Error: El costo debe ser un numero")
                input("\nPresione Enter para continuar...")
                continue

            destino = Destino(db, nombre=nombre, descripcion=descripcion,
                              actividades=actividades, costo_base=costo_base)
            destino.guardar()
            input("\nPresione Enter para continuar...")

        elif opcion == "2":
            # Listar destinos
            print("\n--- LISTA DE DESTINOS ---")
            destinos = Destino.listar_todos(db)

            if destinos:
                for i, dest in enumerate(destinos, 1):
                    print(f"\n{i}. {dest}")
                    print(f"   Descripcion: {dest.descripcion}")
                    print(f"   Actividades: {dest.actividades}")
            else:
                print("No hay destinos registrados")

            input("\nPresione Enter para continuar...")

        elif opcion == "3":
            # Modificar destino
            print("\n--- MODIFICAR DESTINO ---")

            try:
                id_destino = int(input("ID del destino a modificar: ").strip())
            except ValueError:
                print("Error: ID invalido")
                input("\nPresione Enter para continuar...")
                continue

            destino = Destino.buscar_por_id(db, id_destino)

            if destino:
                print(f"\nDestino actual: {destino.nombre}")
                print("Deje en blanco para mantener el valor actual")

                nombre = input(f"Nuevo nombre [{destino.nombre}]: ").strip()
                if nombre:
                    destino.nombre = nombre

                descripcion = input(
                    f"Nueva descripcion [{destino.descripcion}]: ").strip()
                if descripcion:
                    destino.descripcion = descripcion

                actividades = input(
                    f"Nuevas actividades [{destino.actividades}]: ").strip()
                if actividades:
                    destino.actividades = actividades

                costo = input(f"Nuevo costo [{destino.costo_base}]: ").strip()
                if costo:
                    try:
                        destino.costo_base = float(costo)
                    except ValueError:
                        print("Error: Costo invalido, se mantiene el anterior")

                destino.actualizar()
            else:
                print("Destino no encontrado")

            input("\nPresione Enter para continuar...")

        elif opcion == "4":
            # Eliminar destino
            print("\n--- ELIMINAR DESTINO ---")

            try:
                id_destino = int(input("ID del destino a eliminar: ").strip())
            except ValueError:
                print("Error: ID invalido")
                input("\nPresione Enter para continuar...")
                continue

            confirmar = input("Esta seguro? (s/n): ").strip().lower()

            if confirmar == 's':
                Destino.eliminar(db, id_destino)
            else:
                print("Operacion cancelada")

            input("\nPresione Enter para continuar...")

        elif opcion == "0":
            break
        else:
            print("Opcion invalida")
            input("\nPresione Enter para continuar...")


def menu_paquetes(db):
    """
    Menu de gestion de paquetes turisticos.
    Permite crear, listar y consultar disponibilidad de paquetes.
    """
    while True:
        limpiar_pantalla()
        print("\n" + "="*70)
        print(" " * 20 + "GESTION DE PAQUETES TURISTICOS")
        print("="*70)
        print("1. Crear nuevo paquete")
        print("2. Listar todos los paquetes")
        print("3. Ver paquetes disponibles")
        print("4. Buscar paquetes por fechas")
        print("5. Ver detalles de un paquete")
        print("0. Volver al menu principal")
        print("="*70)

        opcion = input("\nSeleccione una opcion: ").strip()

        if opcion == "1":
            # Crear paquete
            print("\n--- CREAR NUEVO PAQUETE ---")
            nombre = input("Nombre del paquete: ").strip()
            descripcion = input("Descripcion: ").strip()

            try:
                fecha_inicio_str = input("Fecha inicio (YYYY-MM-DD): ").strip()
                fecha_inicio = datetime.strptime(
                    fecha_inicio_str, "%Y-%m-%d").date()

                fecha_fin_str = input("Fecha fin (YYYY-MM-DD): ").strip()
                fecha_fin = datetime.strptime(fecha_fin_str, "%Y-%m-%d").date()

                if fecha_inicio < date.today():
                    print("Error: La fecha de inicio no puede ser anterior a hoy")
                    input("\nPresione Enter para continuar...")
                    continue

                if fecha_fin <= fecha_inicio:
                    print("Error: La fecha de fin debe ser posterior a la de inicio")
                    input("\nPresione Enter para continuar...")
                    continue

                precio_total = float(
                    input("Precio total del paquete: ").strip())
                cupo_disponible = int(input("Cupo disponible: ").strip())

            except ValueError as e:
                print(f"Error en los datos ingresados: {e}")
                input("\nPresione Enter para continuar...")
                continue

            paquete = PaqueteTuristico(db, nombre=nombre, descripcion=descripcion,
                                       fecha_inicio=fecha_inicio, fecha_fin=fecha_fin,
                                       precio_total=precio_total,
                                       cupo_disponible=cupo_disponible)

            id_paquete = paquete.guardar()

            if id_paquete:
                # Agregar destinos al paquete
                agregar_destinos = input(
                    "\nDesea agregar destinos al paquete? (s/n): ").strip().lower()

                if agregar_destinos == 's':
                    # Mostrar destinos disponibles
                    destinos = Destino.listar_todos(db, solo_disponibles=True)

                    if destinos:
                        print("\nDestinos disponibles:")
                        for i, dest in enumerate(destinos, 1):
                            print(
                                f"{i}. {dest.nombre} - ${dest.costo_base:,.2f}")

                        while True:
                            try:
                                id_destino = int(
                                    input("\nID del destino a agregar (0 para terminar): ").strip())

                                if id_destino == 0:
                                    break

                                orden = int(input("Orden de visita: ").strip())
                                paquete.agregar_destino(id_destino, orden)

                            except ValueError:
                                print("Error: Debe ingresar un numero valido")
                    else:
                        print("No hay destinos disponibles")

            input("\nPresione Enter para continuar...")

        elif opcion == "2":
            # Listar todos los paquetes
            print("\n--- LISTA DE PAQUETES TURISTICOS ---")
            paquetes = PaqueteTuristico.listar_todos(db)

            if paquetes:
                for i, paq in enumerate(paquetes, 1):
                    print(f"\n{i}. {paq}")
                    print(f"   Descripcion: {paq.descripcion}")
            else:
                print("No hay paquetes registrados")

            input("\nPresione Enter para continuar...")

        elif opcion == "3":
            # Ver paquetes disponibles
            print("\n--- PAQUETES DISPONIBLES ---")
            paquetes = PaqueteTuristico.listar_todos(db, solo_disponibles=True)

            if paquetes:
                for i, paq in enumerate(paquetes, 1):
                    print(f"\n{i}. {paq}")
                    print(f"   Descripcion: {paq.descripcion}")
            else:
                print("No hay paquetes disponibles")

            input("\nPresione Enter para continuar...")

        elif opcion == "4":
            # Buscar por fechas
            print("\n--- BUSCAR PAQUETES POR FECHAS ---")

            try:
                fecha_inicio_str = input(
                    "Fecha inicio deseada (YYYY-MM-DD): ").strip()
                fecha_inicio = datetime.strptime(
                    fecha_inicio_str, "%Y-%m-%d").date()

                fecha_fin_str = input(
                    "Fecha fin deseada (YYYY-MM-DD): ").strip()
                fecha_fin = datetime.strptime(fecha_fin_str, "%Y-%m-%d").date()

                paquetes = PaqueteTuristico.buscar_por_fechas(
                    db, fecha_inicio, fecha_fin)

                if paquetes:
                    print(
                        f"\nPaquetes disponibles entre {fecha_inicio} y {fecha_fin}:")
                    for i, paq in enumerate(paquetes, 1):
                        print(f"\n{i}. {paq}")
                else:
                    print("No se encontraron paquetes para esas fechas")

            except ValueError:
                print("Error: Formato de fecha invalido")

            input("\nPresione Enter para continuar...")

        elif opcion == "5":
            # Ver detalles de un paquete
            print("\n--- DETALLES DEL PAQUETE ---")

            try:
                id_paquete = int(input("ID del paquete: ").strip())
                paquete = PaqueteTuristico.buscar_por_id(db, id_paquete)

                if paquete:
                    print(f"\n{paquete}")
                    print(f"Descripcion: {paquete.descripcion}")

                    if paquete.destinos:
                        print("\nDestinos incluidos:")
                        for dest in paquete.destinos:
                            print(
                                f"  - {dest['nombre']} (Orden {dest['orden_visita']})")
                            print(f"    {dest['actividades']}")
                    else:
                        print("\nNo hay destinos asociados a este paquete")
                else:
                    print("Paquete no encontrado")

            except ValueError:
                print("Error: ID invalido")

            input("\nPresione Enter para continuar...")

        elif opcion == "0":
            break
        else:
            print("Opcion invalida")
            input("\nPresione Enter para continuar...")


def menu_clientes(db):
    """
    Menu de gestion de clientes.
    Permite registrar y listar clientes.
    """
    while True:
        limpiar_pantalla()
        print("\n" + "="*70)
        print(" " * 25 + "GESTION DE CLIENTES")
        print("="*70)
        print("1. Registrar nuevo cliente")
        print("2. Listar todos los clientes")
        print("3. Buscar cliente por email")
        print("0. Volver al menu principal")
        print("="*70)

        opcion = input("\nSeleccione una opcion: ").strip()

        if opcion == "1":
            # Registrar cliente
            print("\n--- REGISTRAR NUEVO CLIENTE ---")
            nombre_completo = input("Nombre completo: ").strip()
            email = input("Email: ").strip()
            telefono = input("Telefono: ").strip()
            direccion = input("Direccion: ").strip()

            cliente = Cliente(db, nombre_completo=nombre_completo, email=email,
                              telefono=telefono, direccion=direccion)

            id_cliente = cliente.guardar()

            if id_cliente:
                crear_usuario = input(
                    "\nDesea crear usuario para este cliente? (s/n): ").strip().lower()

                if crear_usuario == 's':
                    nombre_usuario = input("Nombre de usuario: ").strip()
                    password = input("Contrasena: ").strip()

                    usuario = Usuario(db, nombre_usuario=nombre_usuario, password=password,
                                      rol="cliente", id_cliente=id_cliente)
                    usuario.registrar()

            input("\nPresione Enter para continuar...")

        elif opcion == "2":
            # Listar clientes
            print("\n--- LISTA DE CLIENTES ---")
            clientes = Cliente.listar_todos(db)

            if clientes:
                for i, cli in enumerate(clientes, 1):
                    print(f"\n{i}. {cli}")
                    print(f"   Direccion: {cli.direccion}")
                    print(f"   Fecha registro: {cli.fecha_registro}")
            else:
                print("No hay clientes registrados")

            input("\nPresione Enter para continuar...")

        elif opcion == "3":
            # Buscar por email
            print("\n--- BUSCAR CLIENTE ---")
            email = input("Email del cliente: ").strip()
            cliente = Cliente.buscar_por_email(db, email)

            if cliente:
                print(f"\n{cliente}")
                print(f"Direccion: {cliente.direccion}")
                print(f"Fecha registro: {cliente.fecha_registro}")
            else:
                print("Cliente no encontrado")

            input("\nPresione Enter para continuar...")

        elif opcion == "0":
            break
        else:
            print("Opcion invalida")
            input("\nPresione Enter para continuar...")


def menu_reservas(db, usuario):
    """
    Menu para realizar reservas.
    Solo clientes autenticados pueden reservar.
    """
    if not usuario or not usuario.id_cliente:
        print("Error: Debe estar autenticado como cliente para realizar reservas")
        input("\nPresione Enter para continuar...")
        return

    limpiar_pantalla()
    print("\n" + "="*70)
    print(" " * 27 + "REALIZAR RESERVA")
    print("="*70)

    # Mostrar paquetes disponibles
    paquetes = PaqueteTuristico.listar_todos(db, solo_disponibles=True)

    if not paquetes:
        print("No hay paquetes disponibles en este momento")
        input("\nPresione Enter para continuar...")
        return

    print("\nPaquetes disponibles:")
    for i, paq in enumerate(paquetes, 1):
        print(f"\n{i}. {paq}")
        print(f"   {paq.descripcion}")

    try:
        seleccion = int(
            input("\nSeleccione el numero del paquete (0 para cancelar): ").strip())

        if seleccion == 0:
            return

        if seleccion < 1 or seleccion > len(paquetes):
            print("Seleccion invalida")
            input("\nPresione Enter para continuar...")
            return

        paquete_seleccionado = paquetes[seleccion - 1]

        # Mostrar detalles del paquete
        paquete_seleccionado.cargar_destinos()
        print(f"\nPaquete seleccionado: {paquete_seleccionado.nombre}")
        print(f"Precio por persona: ${paquete_seleccionado.precio_total:,.2f}")

        if paquete_seleccionado.destinos:
            print("\nDestinos incluidos:")
            for dest in paquete_seleccionado.destinos:
                print(f"  - {dest['nombre']}")

        # Solicitar numero de personas
        numero_personas = int(input("\nNumero de personas: ").strip())

        if numero_personas < 1:
            print("Error: Debe reservar para al menos una persona")
            input("\nPresione Enter para continuar...")
            return

        # Calcular precio total
        precio_total = paquete_seleccionado.precio_total * numero_personas
        print(f"\nPrecio total: ${precio_total:,.2f}")

        notas = input("Notas adicionales (opcional): ").strip()

        confirmar = input("\nConfirmar reserva? (s/n): ").strip().lower()

        if confirmar == 's':
            # Crear reserva
            reserva = Reserva(db, id_cliente=usuario.id_cliente,
                              id_paquete=paquete_seleccionado.id_paquete,
                              numero_personas=numero_personas,
                              notas=notas)

            if reserva.crear():
                print("\nReserva creada exitosamente!")
                print(f"Numero de reserva: {reserva.id_reserva}")
                print(f"Estado: {reserva.estado}")
        else:
            print("Reserva cancelada")

    except ValueError:
        print("Error: Datos invalidos")

    input("\nPresione Enter para continuar...")


def menu_mis_reservas(db, usuario):
    """
    Menu para ver las reservas del usuario actual.
    """
    if not usuario or not usuario.id_cliente:
        print("Error: Debe estar autenticado como cliente")
        input("\nPresione Enter para continuar...")
        return

    limpiar_pantalla()
    print("\n" + "="*70)
    print(" " * 27 + "MIS RESERVAS")
    print("="*70)

    reservas = Reserva.listar_por_cliente(db, usuario.id_cliente)

    if reservas:
        for i, res in enumerate(reservas, 1):
            print(f"\n{i}. {res}")

            # Obtener detalles del paquete
            paquete = PaqueteTuristico.buscar_por_id(db, res.id_paquete)
            if paquete:
                print(f"   Paquete: {paquete.nombre}")
                print(
                    f"   Fechas: {paquete.fecha_inicio} a {paquete.fecha_fin}")

            if res.notas:
                print(f"   Notas: {res.notas}")
    else:
        print("No tiene reservas registradas")

    input("\nPresione Enter para continuar...")


def menu_usuarios(db):
    """
    Menu de administracion de usuarios.
    Solo para Admins.
    """
    limpiar_pantalla()
    print("\n" + "="*70)
    print(" " * 22 + "ADMINISTRACION DE USUARIOS")
    print("="*70)
    print("1. Crear nuevo usuario")
    print("2. Listar todos los usuarios")
    print("0. Volver al menu principal")
    print("="*70)

    opcion = input("\nSeleccione una opcion: ").strip()

    if opcion == "1":
        # Crear usuario
        print("\n--- CREAR NUEVO USUARIO ---")
        nombre_usuario = input("Nombre de usuario: ").strip()
        password = input("Contrasena: ").strip()
        rol = input("Rol (admin/empleado/cliente): ").strip().lower()

        if rol not in ['admin', 'empleado', 'cliente']:
            print("Rol invalido")
            input("\nPresione Enter para continuar...")
            return

        id_cliente_str = input(
            "ID del cliente (dejar vacio si no aplica): ").strip()
        id_cliente = int(id_cliente_str) if id_cliente_str else None

        usuario = Usuario(db, nombre_usuario=nombre_usuario, password=password,
                          rol=rol, id_cliente=id_cliente)
        usuario.registrar()

        input("\nPresione Enter para continuar...")

    elif opcion == "2":
        # Listar usuarios
        print("\n--- LISTA DE USUARIOS ---")
        usuarios = Usuario.listar_todos(db)

        if usuarios:
            for i, usr in enumerate(usuarios, 1):
                activo = "Activo" if usr['activo'] else "Inactivo"
                print(f"{i}. Usuario: {usr['nombre_usuario']} | Rol: {usr['rol']} | "
                      f"Estado: {activo}")
        else:
            print("No hay usuarios registrados")

        input("\nPresione Enter para continuar...")


def menu_todas_reservas(db):
    """
    Menu para ver todas las reservas del sistema.
    Solo para administradores.
    """
    limpiar_pantalla()
    print("\n" + "="*70)
    print(" " * 24 + "TODAS LAS RESERVAS")
    print("="*70)

    reservas = Reserva.listar_todas(db)

    if reservas:
        for i, res in enumerate(reservas, 1):
            print(f"\n{i}. Reserva #{res['id_reserva']}")
            print(f"   Cliente: {res['nombre_completo']}")
            print(f"   Paquete: {res['nombre_paquete']}")
            print(f"   Personas: {res['numero_personas']}")
            print(f"   Total: ${res['precio_total']:,.2f}")
            print(f"   Estado: {res['estado']}")
            print(f"   Fecha: {res['fecha_reserva']}")
    else:
        print("No hay reservas registradas")

    input("\nPresione Enter para continuar...")


def verificar_usuarios_existentes(db):
    """Verifica si existen usuarios en el sistema."""
    try:
        connection = db.conectar()
        cursor = connection.cursor()
        cursor.execute("SELECT COUNT(*) FROM Usuarios")
        count = cursor.fetchone()[0]
        cursor.close()
        return count > 0
    except Exception as e:
        print(f"Error al verificar usuarios: {e}")
        return False


def crear_usuario_inicial(db):
    """Crea un usuario administrador inicial cuando no existen usuarios."""
    print("\n" + "="*70)
    print(" " * 15 + "CONFIGURACION INICIAL DEL SISTEMA")
    print("="*70)
    print("\nNo hay usuarios registrados en el sistema.")
    print("Es necesario crear un usuario administrador para comenzar.\n")

    # Crear cliente para el administrador
    print("--- DATOS DEL ADMINISTRADOR ---")
    nombre_completo = input("Nombre completo: ").strip()
    email = input("Email: ").strip()
    telefono = input("Telefono: ").strip()
    direccion = input("Direccion: ").strip()

    cliente = Cliente(db, nombre_completo=nombre_completo, email=email,
                      telefono=telefono, direccion=direccion)
    id_cliente = cliente.guardar()

    if not id_cliente:
        print("\nError al crear el cliente. Intente nuevamente.")
        return None

    # Crear usuario administrador
    print("\n--- CREDENCIALES DE ACCESO ---")
    nombre_usuario = input("Nombre de usuario: ").strip()
    password = input("Contrasena: ").strip()
    password_confirm = input("Confirmar contrasena: ").strip()

    if password != password_confirm:
        print("\nLas contrasenas no coinciden.")
        return None

    usuario = Usuario(db, nombre_usuario=nombre_usuario, password=password,
                      rol="admin", id_cliente=id_cliente)
    id_usuario = usuario.registrar()

    if id_usuario:
        print("\n" + "="*70)
        print("Usuario administrador creado exitosamente!")
        print("Ahora puede iniciar sesion con sus credenciales.")
        print("="*70)
        input("\nPresione Enter para continuar...")
        return True
    else:
        print("\nError al crear el usuario. Intente nuevamente.")
        return None


def autenticar_usuario(db):
    """Pantalla de autenticacion de usuarios."""
    print("\n" + "="*70)
    print(" " * 22 + "AUTENTICACION DE USUARIO")
    print("="*70)

    nombre_usuario = input("\nNombre de usuario: ").strip()
    password = input("Contrasena: ").strip()

    usuario = Usuario(db, nombre_usuario=nombre_usuario, password=password)

    if usuario.autenticar():
        return usuario
    else:
        return None


def main():
    """
    Funcion principal del sistema.
    Punto de entrada de la aplicacion.
    """
    print("\n" + "="*70)
    print(" " * 15 + "INICIANDO SISTEMA VIAJES AVENTURA")
    print("="*70)

    # Conectar a la base de datos
    db = Database()

    try:
        connection = db.conectar()

        if connection:
            # Crear tablas si no existen
            db.crear_tablas()
            print("\nBase de datos lista")

            # Verificar si existen usuarios en el sistema
            if not verificar_usuarios_existentes(db):
                print("\n" + "="*70)
                print("PRIMERA EJECUCION DEL SISTEMA")
                print("="*70)
                if not crear_usuario_inicial(db):
                    print("\nNo se pudo crear el usuario inicial.")
                    print("El sistema se cerrara.")
                    return

            # Autenticacion
            USUARIO_ACTUAL = None
            intentos = 0
            max_intentos = 3

            while intentos < max_intentos:
                USUARIO_ACTUAL = autenticar_usuario(db)

                if USUARIO_ACTUAL:
                    break
                else:
                    intentos += 1
                    if intentos < max_intentos:
                        print(
                            f"\nIntentos restantes: {max_intentos - intentos}")

            if not USUARIO_ACTUAL:
                print("\nMaximo de intentos alcanzado. Cerrando sistema...")
                return

            # Menu principal
            while True:
                limpiar_pantalla()
                mostrar_menu_principal()

                print(
                    f"\nUsuario: {USUARIO_ACTUAL.nombre_usuario} | Rol: {USUARIO_ACTUAL.rol}")
                opcion = input("\nSeleccione una opcion: ").strip()

                if opcion == "1":
                    if USUARIO_ACTUAL.tiene_permiso("empleado"):
                        menu_destinos(db)
                    else:
                        print("No tiene permisos para esta opcion")
                        input("\nPresione Enter para continuar...")

                elif opcion == "2":
                    if USUARIO_ACTUAL.tiene_permiso("empleado"):
                        menu_paquetes(db)
                    else:
                        print("No tiene permisos para esta opcion")
                        input("\nPresione Enter para continuar...")

                elif opcion == "3":
                    if USUARIO_ACTUAL.tiene_permiso("empleado"):
                        menu_clientes(db)
                    else:
                        print("No tiene permisos para esta opcion")
                        input("\nPresione Enter para continuar...")

                elif opcion == "4":
                    menu_reservas(db, USUARIO_ACTUAL)

                elif opcion == "5":
                    menu_mis_reservas(db, USUARIO_ACTUAL)

                elif opcion == "6":
                    if USUARIO_ACTUAL.tiene_permiso("admin"):
                        menu_usuarios(db)
                    else:
                        print("No tiene permisos para esta opcion")
                        input("\nPresione Enter para continuar...")

                elif opcion == "7":
                    if USUARIO_ACTUAL.tiene_permiso("admin"):
                        menu_todas_reservas(db)
                    else:
                        print("No tiene permisos para esta opcion")
                        input("\nPresione Enter para continuar...")

                elif opcion == "0":
                    print("\nGracias por usar el sistema Viajes Aventura")
                    print("Cerrando sesion...")
                    break
                else:
                    print("Opcion invalida. Intente nuevamente")
                    input("\nPresione Enter para continuar...")

    except Exception as e:
        print(f"\nError fatal: {e}")

    finally:
        db.desconectar()
        print("\nSistema cerrado correctamente")
        print("="*70)


if __name__ == "__main__":
    main()
