# Sistema de Reservas - Viajes Aventura

Sistema de gestion de reservas para agencia de viajes desarrollado con Python y MySQL, implementando programacion orientada a objetos y metodologias agiles.

## Descripcion del Proyecto

Viajes Aventura es un sistema de reservas en linea que permite a los clientes planificar y reservar vacaciones de manera conveniente. El sistema gestiona destinos, paquetes turisticos y permite a los clientes personalizar sus viajes mediante un sistema de autenticacion seguro.

## Caracteristicas Principales

### Gestion de Destinos

- Agregar nuevos destinos con informacion detallada
- Listar todos los destinos disponibles
- Modificar informacion de destinos existentes
- Eliminar destinos del sistema
- Cada destino incluye: nombre, descripcion, actividades, costo base

### Paquetes Turisticos

- Crear paquetes que combinan multiples destinos
- Definir fechas especificas de viaje
- Calcular precio total automaticamente
- Gestionar cupos disponibles
- Verificar disponibilidad en tiempo real
- Busqueda por rangos de fechas

### Sistema de Reservas

- Clientes autenticados pueden realizar reservas
- Validacion automatica de disponibilidad
- Calculo de precio total por numero de personas
- Estados de reserva (pendiente, confirmada, cancelada)
- Historial de reservas por cliente

### Autenticacion y Autorizacion

- Sistema de usuarios con bcrypt (hash con sal)
- Tres niveles de roles: admin, empleado, cliente
- Control de acceso basado en permisos
- Autenticacion segura con intentos limitados

## Tecnologias Utilizadas

- Python 3.8+
- MySQL 8.0+
- bcrypt para hash de contrasenas
- mysql-connector-python para conexion a base de datos

## Patrones de Diseno Implementados

### Singleton

- Clase Database: Garantiza una unica instancia de conexion a base de datos

### Entity

- Clases Cliente, Usuario, Destino, PaqueteTuristico, Reserva
- Representan entidades del modelo de negocio

### Aggregate

- Clase PaqueteTuristico: Agrupa multiples destinos en un paquete

### Transaction

- Clase Reserva: Implementa transacciones atomicas con rollback

## Estructura del Proyecto

```
viajes-aventura/
├── conexion_db.py          # Gestion de base de datos
├── modelos.py              # Clases Cliente, Usuario, Destino
├── paquetes_reservas.py    # Clases PaqueteTuristico, Reserva
├── main.py                 # Programa principal con menus
├── requirements.txt        # Dependencias
└── README.md              # Este archivo
```

## Instalacion

### 1. Clonar o descargar el proyecto

```bash
cd viajes-aventura
```

### 2. Crear entorno virtual (recomendado)

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

### 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 4. Configurar MySQL

Editar `conexion_db.py` con tu configuracion:

```python
self.__host = "localhost"
self.__port = 3306 # cambiar a tu puerto
self.__user = "root"
self.__password = ""  # Tu contrasena de MySQL
self.__database = "viajes_aventura_db"
```

### 5. Ejecutar el sistema

```bash
python main.py
```

El sistema creara automaticamente la base de datos y las tablas en la primera ejecucion.

## Uso del Sistema

### Primera Ejecucion

1. El sistema creara las tablas necesarias
2. Deberas autenticarte para acceder al sistema
3. Crear un usuario administrador manualmente en la base de datos para comenzar

### Crear Usuario Administrador Inicial

Ejecutar en MySQL:

```sql
USE viajes_aventura_db;

-- Crear cliente
INSERT INTO Clientes (nombre_completo, email, telefono, direccion)
VALUES ('Administrador Sistema', 'admin@viajes.com', '123456789', 'Oficina Central');

-- Crear usuario admin
-- La contrasena "admin123" hasheada con bcrypt
INSERT INTO Usuarios (nombre_usuario, password_hash, rol, id_cliente, activo)
VALUES ('admin', '$2b$12$ejemplo...', 'admin', 1, TRUE);
```

Nota: Debes generar el hash real usando bcrypt o crear el usuario desde el menu.

### Flujo de Trabajo Tipico

#### Como Administrador:

1. Crear destinos turisticos
2. Crear paquetes turisticos
3. Agregar destinos a paquetes
4. Registrar clientes y crear usuarios
5. Ver todas las reservas del sistema

#### Como Cliente:

1. Autenticarse en el sistema
2. Ver paquetes disponibles
3. Realizar reservas
4. Ver historial de reservas

## Esquema de Base de Datos

### Tabla Clientes

- id_cliente (PK)
- nombre_completo
- email (UNIQUE)
- telefono
- direccion
- fecha_registro

### Tabla Usuarios

- id_usuario (PK)
- nombre_usuario (UNIQUE)
- password_hash (bcrypt)
- rol (admin/empleado/cliente)
- id_cliente (FK)
- activo
- fecha_creacion

### Tabla Destinos

- id_destino (PK)
- nombre
- descripcion
- actividades
- costo_base
- disponible
- fecha_creacion

### Tabla PaquetesTuristicos

- id_paquete (PK)
- nombre
- descripcion
- fecha_inicio
- fecha_fin
- precio_total
- cupo_disponible
- disponible
- fecha_creacion

### Tabla Paquetes_Destinos (Relacion muchos a muchos)

- id_paquete_destino (PK)
- id_paquete (FK)
- id_destino (FK)
- orden_visita

### Tabla Reservas

- id_reserva (PK)
- id_cliente (FK)
- id_paquete (FK)
- fecha_reserva
- numero_personas
- precio_total
- estado
- notas

## Seguridad Implementada

### Autenticacion

- Hash de contrasenas con bcrypt
- Sal automatica en cada hash
- 12 rounds de hashing (4096 iteraciones)
- Limite de intentos de autenticacion

### Autorizacion

- Control de acceso basado en roles
- Jerarquia de permisos (admin > empleado > cliente)
- Verificacion de permisos en cada operacion

### Base de Datos

- Queries parametrizadas (previene SQL injection)
- Transacciones atomicas con rollback
- Foreign keys con integridad referencial
- Validacion de datos antes de insercion

## Validaciones Implementadas

### Fechas

- Fecha de inicio no puede ser anterior a hoy
- Fecha de fin debe ser posterior a fecha de inicio
- Validacion de formato de fechas

### Reservas

- Verificacion de cupo disponible
- Validacion de disponibilidad del paquete
- Calculo automatico de precio total
- Transaccion atomica (reserva + actualizacion de cupo)

### Datos

- Validacion de tipos de datos numericos
- Validacion de emails
- Campos obligatorios verificados

## Criterios de Evaluacion Cumplidos

### 4.1.1 Identificacion de requerimientos

- Gestion de destinos completa (CRUD)
- Paquetes turisticos con fechas y precios
- Sistema de reservas funcional
- Autenticacion de usuarios

### 4.1.2 Diagramas UML

- Diagrama de clases implementado en codigo
- Relaciones entre clases correctamente definidas
- Herencia y composicion aplicadas

### 4.1.3 Procesos de negocio (BPMN)

- Proceso de reserva implementado
- Validacion de disponibilidad
- Actualizacion de estados
- Transacciones atomicas

### 4.1.4 Metodologias agiles

- Desarrollo iterativo por funcionalidades
- Sprints por modulos (Destinos -> Paquetes -> Reservas)
- Codigo modular y reutilizable

### 4.1.5 Construccion con autenticacion y BD

- Sistema de autenticacion con bcrypt
- Conexion a base de datos MySQL
- Persistencia de todos los datos
- Queries parametrizadas

## Arquitectura del Sistema

### Capa de Datos

- Clase Database: Singleton para gestion de conexiones
- Metodos CRUD en cada clase de modelo
- Transacciones y rollback

### Capa de Negocio

- Clases de modelo con logica de negocio
- Validaciones en metodos de clase
- Calculo de precios y disponibilidad

### Capa de Presentacion

- Menus interactivos en consola
- Validacion de entrada de usuario
- Mensajes informativos y de error

## Pruebas Realizadas

### Pruebas Funcionales

- Creacion de destinos
- Creacion de paquetes con multiples destinos
- Registro de clientes y usuarios
- Autenticacion exitosa y fallida
- Creacion de reservas con validaciones
- Verificacion de disponibilidad
- Actualizacion de cupos

### Pruebas de Seguridad

- Intentos de autenticacion invalidos
- Acceso a funciones sin permisos
- SQL injection (prevenido con queries parametrizadas)

### Pruebas de Integridad

- Foreign keys funcionando correctamente
- Cascade delete en relaciones
- Transacciones con rollback

## Mejoras Futuras

- Interfaz web con Flask o Django
- Sistema de pagos integrado
- Notificaciones por email
- Reportes y estadisticas
- API REST para integracion con otros sistemas
- Sistema de calificaciones y comentarios
- Gestion de imagenes de destinos
- Sistema de descuentos y promociones

## Autores

Proyecto desarrollado para la asignatura TI3021 - Programacion Orientada a Objetos Segura
INACAP - 2024

## Licencia

Este proyecto es academico y fue desarrollado con fines educativos.
