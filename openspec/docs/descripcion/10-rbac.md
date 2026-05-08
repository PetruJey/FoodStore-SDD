# Control de Acceso Basado en Roles (RBAC)

La autorización en Food Store sigue el modelo RBAC (Role-Based Access Control) con cuatro roles predefinidos:

**ADMIN** tiene acceso total al sistema. Puede gestionar usuarios y sus roles, administrar todo el catálogo de productos y categorías, supervisar y modificar todos los pedidos, acceder al panel de métricas, y configurar parámetros del sistema. Es el único rol que puede cancelar pedidos que ya están en preparación.

**STOCK** (Gestor de Stock) tiene permisos limitados al catálogo. Puede crear, editar y desactivar productos, gestionar ingredientes y alérgenos, modificar cantidades de stock, y administrar categorías. No tiene acceso a pedidos, usuarios ni métricas.

**PEDIDOS** (Gestor de Pedidos) tiene permisos limitados a la operación de pedidos. Puede ver todos los pedidos del sistema, avanzar el estado de los pedidos siguiendo la máquina de estados, y cancelar pedidos que estén en estado PENDIENTE o CONFIRMADO. No tiene acceso al catálogo ni a la gestión de usuarios.

**CLIENT** es el rol asignado automáticamente a cada usuario que se registra. Puede ver el catálogo de productos, gestionar su carrito de compras, crear pedidos, realizar pagos, ver el historial de sus propios pedidos, y gestionar sus direcciones de entrega. Un cliente solo puede ver y operar sobre sus propios datos — nunca los de otros usuarios.

La verificación de roles se implementa mediante la dependencia `require_role` de FastAPI, que es un generador de dependencias parametrizado. Se utiliza de la siguiente manera: un endpoint que requiere rol ADMIN declarará `require_role(["ADMIN"])` como dependencia, y uno que permite tanto ADMIN como PEDIDOS declarará `require_role(["ADMIN", "PEDIDOS"])`. Si el usuario autenticado no posee ninguno de los roles requeridos, la dependencia lanza una excepción HTTP 403 (Forbidden).

## Rate Limiting

Para proteger el sistema contra ataques de fuerza bruta, el endpoint de login implementa rate limiting mediante la librería slowapi. La configuración limita a **5 intentos de login cada 15 minutos** por dirección IP. Cuando se excede el límite, el servidor responde con HTTP 429 (Too Many Requests) e incluye un header `Retry-After` que indica cuántos segundos debe esperar el cliente antes de reintentar. Este mecanismo es transparente para usuarios legítimos (5 intentos en 15 minutos es más que suficiente para un humano) pero efectivo contra scripts automatizados.
