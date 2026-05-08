# Arquitectura del Backend

El backend de Food Store sigue una arquitectura en capas con flujo de dependencia unidireccional. Esto significa que cada capa solo conoce y depende de la capa inmediatamente inferior, nunca de las superiores. Esta restricción es fundamental para mantener la testabilidad, la mantenibilidad y la separación de responsabilidades.

Las capas, de exterior a interior, son las siguientes:

**Router** es la capa más externa y se encarga exclusivamente de recibir las peticiones HTTP, validar los datos de entrada mediante schemas Pydantic, invocar al servicio correspondiente, y devolver la respuesta HTTP apropiada. Los routers no contienen lógica de negocio — son delegadores puros. Cada router está asociado a un módulo funcional (por ejemplo, `router_productos.py`, `router_pedidos.py`) y se registra en la aplicación FastAPI con un prefijo de ruta específico.

**Service** es la capa que contiene toda la lógica de negocio. Aquí se implementan las reglas, validaciones, cálculos y orquestación de operaciones. Un servicio puede coordinar múltiples repositorios a través del Unit of Work, aplicar reglas de negocio como la validación de transiciones de estado, calcular totales de pedidos con sus snapshots, y decidir qué hacer en caso de error. Los servicios son clases o funciones que reciben el Unit of Work como dependencia.

**Unit of Work (UoW)** es la capa que gestiona la transacción de base de datos. Encapsula una sesión de SQLAlchemy y expone los repositorios necesarios como atributos. El UoW se encarga de abrir la transacción, coordinar los commits y, en caso de error, ejecutar el rollback. Esto garantiza que operaciones complejas que involucran múltiples tablas (como crear un pedido con sus detalles, actualizar stock y registrar el historial de estados) sean atómicas.

**Repository** es la capa de acceso a datos. Cada repositorio implementa operaciones CRUD sobre una entidad específica, abstrayendo los detalles de SQLAlchemy y SQLModel. Existe un `BaseRepository[T]` genérico que proporciona las operaciones comunes, y repositorios especializados que agregan queries específicas del dominio (como buscar productos por categoría o listar pedidos por estado).

**Model** es la capa más interna y define las entidades de base de datos mediante clases SQLModel. Cada modelo mapea directamente a una tabla de PostgreSQL y define sus columnas, tipos, relaciones y restricciones.

El flujo de una petición típica es: el cliente envía un request HTTP → el Router lo recibe y valida los datos de entrada → invoca al Service pasándole el UoW → el Service ejecuta la lógica de negocio usando los Repositories del UoW → los Repositories interactúan con los Models para leer o escribir en la base de datos → el resultado asciende de vuelta por las capas hasta convertirse en una respuesta HTTP.

La organización del código sigue un enfoque **feature-first** (también llamado modular o vertical). En lugar de agrupar todos los routers en una carpeta, todos los servicios en otra y todos los modelos en otra, cada funcionalidad del sistema tiene su propia carpeta que contiene todos los archivos que necesita. Los módulos principales son:

- **auth**: Login, registro, renovación de tokens, logout.
- **refreshtokens**: Gestión del ciclo de vida de refresh tokens.
- **usuarios**: CRUD de usuarios, asignación de roles.
- **direcciones**: Gestión de direcciones de entrega del cliente.
- **categorias**: CRUD de categorías con soporte jerárquico.
- **productos**: CRUD de productos, ingredientes, relaciones con categorías.
- **pedidos**: Creación de pedidos, avance de estados, historial.
- **pagos**: Integración con MercadoPago, procesamiento de webhooks.
- **admin**: Panel de métricas y operaciones administrativas.

Cada módulo contiene típicamente: un archivo de modelo (`model.py`), un archivo de schemas Pydantic (`schemas.py`), un repositorio (`repository.py`), un servicio (`service.py`) y un router (`router.py`). Esta estructura hace que sea extremadamente claro dónde buscar y dónde agregar código relacionado con una funcionalidad específica.
