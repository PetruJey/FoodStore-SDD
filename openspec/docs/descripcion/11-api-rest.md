# API REST

## Filosofía de Diseño

La API de Food Store sigue principios RESTful consistentes a lo largo de todos sus endpoints. Todas las rutas están prefijadas con `/api/v1` para permitir versionado futuro sin romper clientes existentes. Los errores se devuelven siguiendo el estándar **RFC 7807** (Problem Details for HTTP APIs), que define una estructura JSON consistente con campos como `type`, `title`, `status`, `detail` e `instance`. Esto permite que los clientes manejen errores de forma uniforme sin necesidad de interpretar formatos ad-hoc.

Los listados implementan **paginación** mediante parámetros `skip` (offset) y `limit` (cantidad), con valores por defecto razonables. Las respuestas paginadas incluyen metadatos como el total de registros disponibles para que el frontend pueda construir controles de paginación.

El filtrado por soft delete se maneja de forma transparente: por defecto, todos los endpoints de listado excluyen los registros con `eliminado_en` no nulo. Los endpoints de administración pueden incluir un parámetro `incluir_eliminados` para ver también los registros borrados lógicamente.

## Módulo Auth

El módulo de autenticación expone los endpoints fundamentales para el ciclo de vida de la sesión del usuario.

El endpoint **POST /api/v1/auth/login** recibe un email y una contraseña, los valida contra la base de datos, y si son correctos devuelve un objeto con el access token, el refresh token, el tipo de token ("Bearer") y los datos del usuario incluyendo sus roles. Si las credenciales son inválidas, devuelve 401. Si se excede el rate limit, devuelve 429.

El endpoint **POST /api/v1/auth/register** permite la creación de nuevas cuentas de cliente. Recibe nombre, email, contraseña y teléfono opcional. Verifica que el email no esté registrado (devuelve 409 si ya existe), hashea la contraseña con bcrypt, crea el usuario, le asigna automáticamente el rol CLIENT, y devuelve los tokens y datos del usuario como si fuera un login automático post-registro.

El endpoint **POST /api/v1/auth/refresh** recibe un refresh token válido, verifica que exista en la base de datos, que no esté revocado, y que no haya expirado. Si todo es correcto, revoca el token actual, emite un nuevo par de tokens (access + refresh), y los devuelve. Si el refresh token es inválido, devuelve 401.

El endpoint **POST /api/v1/auth/logout** recibe el refresh token y lo marca como revocado en la base de datos. El access token simplemente se elimina del lado del cliente. Devuelve 204 (No Content) en caso de éxito.

## Módulo Productos

El módulo de productos gestiona el catálogo completo de la tienda.

El endpoint **GET /api/v1/productos** devuelve el listado paginado de productos disponibles. Soporta filtros opcionales por categoría, por nombre (búsqueda parcial), por rango de precio, y por disponibilidad. Para el público general, solo devuelve productos con `disponible = true` y `eliminado_en IS NULL`. Para usuarios con rol STOCK o ADMIN, puede incluir productos no disponibles.

El endpoint **GET /api/v1/productos/{id}** devuelve el detalle completo de un producto específico, incluyendo sus categorías asociadas, sus ingredientes (con la información de alérgenos), el stock disponible y todas las imágenes.

El endpoint **POST /api/v1/productos** permite crear un nuevo producto. Requiere rol STOCK o ADMIN. Recibe los datos del producto incluyendo precio, stock inicial, categorías e ingredientes. Valida que las categorías e ingredientes referenciados existan.

El endpoint **PUT /api/v1/productos/{id}** permite actualizar un producto existente. Requiere rol STOCK o ADMIN. Permite modificar cualquier campo incluyendo precio, stock, disponibilidad, categorías e ingredientes.

El endpoint **DELETE /api/v1/productos/{id}** realiza un soft delete del producto (establece `eliminado_en`). Requiere rol STOCK o ADMIN. El producto no desaparece de la base de datos — simplemente deja de mostrarse en los listados públicos.

## Módulo Pedidos

El módulo de pedidos es el más complejo de la API y gestiona todo el ciclo de vida de las órdenes.

El endpoint **POST /api/v1/pedidos** permite a un cliente crear un nuevo pedido. Recibe la lista de ítems (cada uno con ID de producto, cantidad y personalización opcional), el ID de la dirección de entrega y el ID de la forma de pago. El servicio valida que todos los productos existan y estén disponibles, verifica que haya stock suficiente para cada ítem, calcula los subtotales usando los precios actuales (creando snapshots), calcula el costo de envío, crea el pedido en estado PENDIENTE con todos sus detalles, y registra la entrada inicial en el historial de estados. Todo esto ocurre dentro de una única transacción.

El endpoint **GET /api/v1/pedidos** devuelve los pedidos según el rol del usuario. Si es CLIENT, devuelve solo sus propios pedidos. Si es PEDIDOS o ADMIN, devuelve todos los pedidos del sistema. Soporta filtros por estado, por fecha, y paginación.

El endpoint **GET /api/v1/pedidos/{id}** devuelve el detalle completo de un pedido incluyendo todos sus ítems con sus snapshots de precio, el historial de estados con timestamps y usuarios responsables, la dirección de entrega (snapshot), y la información de pagos asociados.

El endpoint **PATCH /api/v1/pedidos/{id}/avanzar** permite avanzar el estado de un pedido al siguiente estado válido según la máquina de estados. Recibe opcionalmente una observación que se registra en el historial. Valida que la transición sea válida según las reglas de negocio y que el usuario tenga el rol necesario para ejecutarla. En el caso de la transición a CONFIRMADO, también ejecuta el decremento de stock.

El endpoint **PATCH /api/v1/pedidos/{id}/cancelar** permite cancelar un pedido. Valida que el pedido esté en un estado cancelable y que el usuario tenga permiso para cancelarlo según su rol. Si el pedido ya había sido confirmado, ejecuta la restauración de stock. Registra la transición en el historial con la observación proporcionada.

## Módulo Pagos

El módulo de pagos gestiona la integración con MercadoPago.

El endpoint **POST /api/v1/pagos/crear-preferencia** (o su equivalente para la API de Orders) recibe el ID de un pedido en estado PENDIENTE y crea una preferencia de pago en MercadoPago. Esta preferencia incluye los ítems del pedido con sus precios snapshot, la URL de retorno para redireccionar al cliente después del pago, la URL del webhook para recibir notificaciones IPN, y el `external_reference` que vincula la preferencia con el pedido en Food Store. Devuelve el ID de la preferencia y la URL de pago para redirigir al cliente.

El endpoint **POST /api/v1/pagos/webhook** (o **POST /api/v1/pagos/ipn**) recibe las notificaciones de MercadoPago. Cuando MercadoPago notifica un evento de pago, este endpoint extrae el ID del pago, consulta la API de MercadoPago para obtener el estado actual, actualiza el registro de pago en la base de datos, y si el estado es "approved", dispara automáticamente la transición del pedido de PENDIENTE a CONFIRMADO. Este endpoint debe responder con 200 rápidamente para que MercadoPago no reintente el webhook.

El endpoint **GET /api/v1/pagos/pedido/{pedido_id}** devuelve todos los pagos asociados a un pedido específico, permitiendo ver el historial de intentos de pago incluyendo los rechazados.
