# Schemas Pydantic v2

Food Store utiliza Pydantic v2 para la validación de datos de entrada y la serialización de respuestas. Los schemas siguen una convención estricta de separación en tres variantes por entidad:

- **Create** (o Request): Define los campos necesarios para crear un recurso. Solo incluye los campos que el cliente debe proporcionar. Ejemplo: `RegisterRequest` incluye nombre, email y contraseña, pero no incluye ID ni fechas de auditoría.

- **Update**: Define los campos que pueden ser modificados. Generalmente todos los campos son opcionales (usando `Optional[T]`), permitiendo actualizaciones parciales donde el cliente solo envía los campos que desea cambiar.

- **Read** (o Response): Define la estructura de datos que se devuelve al cliente. Incluye el ID, los campos de la entidad, datos de relaciones anidadas cuando corresponde, y excluye campos sensibles como hashes de contraseña.

## Schemas de Autenticación

**LoginRequest** contiene dos campos obligatorios: `email` (validado como formato de email) y `password` (string con longitud mínima de 8 caracteres). Es el schema que recibe el endpoint de login.

**RegisterRequest** extiende los campos de login con: `nombre` (string con longitud mínima de 2 caracteres), `telefono` (string opcional con validación de formato), y opcionalmente `password_confirmation` para validación en el frontend. El validator de Pydantic verifica que la contraseña cumple con requisitos mínimos de complejidad.

**TokenResponse** es el schema de respuesta del login y el refresh. Contiene: `access_token` (string JWT), `refresh_token` (string UUID), `token_type` (siempre "Bearer"), y `user` (un objeto UserResponse anidado con los datos del usuario).

**UserResponse** contiene los datos públicos del usuario: `id`, `nombre`, `email`, `telefono`, `roles` (lista de strings con los nombres de los roles), `creado_en` y `actualizado_en`. Nunca incluye el hash de la contraseña.

## Schemas de Pedidos

**CrearPedidoRequest** es el schema de entrada para crear un pedido. Contiene: `items` (lista no vacía de `ItemPedidoRequest`), `direccion_id` (entero, ID de la dirección de entrega), y `forma_pago_id` (entero, ID de la forma de pago). Incluye un validator que verifica que la lista de ítems no esté vacía.

**ItemPedidoRequest** define cada línea del pedido. Contiene: `producto_id` (entero), `cantidad` (entero positivo, mínimo 1), y `personalizacion` (lista opcional de enteros, representando los IDs de ingredientes a excluir). Si la personalización no se proporciona, se asume una lista vacía.

**AvanzarEstadoRequest** es el schema para las transiciones de estado. Contiene un único campo opcional: `observacion` (string, máximo 500 caracteres) que se registra en el historial de estados para documentar el motivo de la transición.

**PedidoRead** es el schema de respuesta para listados de pedidos. Contiene: `id`, `estado` (nombre del estado actual), `total`, `costo_envio`, `creado_en`, `actualizado_en`, y datos resumidos del usuario y la dirección. No incluye los detalles de cada ítem para mantener las respuestas de listado livianas.

**PedidoDetail** extiende PedidoRead con información completa. Agrega: `detalles` (lista de `DetallePedidoRead` con cada ítem), `historial_estados` (lista ordenada cronológicamente de todas las transiciones), `pagos` (lista de pagos asociados), y los snapshots completos de dirección y forma de pago.

**DetallePedidoRead** contiene la información de cada línea del pedido: `id`, `producto_id`, `producto_nombre`, `cantidad`, `precio_unitario` (el snapshot del precio), `subtotal`, y `personalizacion` (lista de IDs de ingredientes excluidos con sus nombres para facilitar la visualización).
