# Unit of Work

## El Patrón

El Unit of Work (UoW) es un patrón de diseño que agrupa múltiples operaciones de base de datos en una única transacción lógica. En Food Store, el UoW encapsula una sesión de SQLAlchemy y expone todos los repositorios necesarios como atributos. Cuando el servicio comienza una operación, el UoW abre una transacción. Todas las operaciones de los repositorios se ejecutan dentro de esa transacción. Si todo sale bien, el UoW hace commit. Si algo falla, el UoW ejecuta rollback y ninguna de las operaciones se persiste. Esto garantiza la atomicidad — o todo se guarda o nada se guarda.

El UoW se implementa como un context manager de Python, permitiendo su uso con la sintaxis `with` (o `async with` en el caso asíncrono). Al entrar al contexto, se crea la sesión y se inicializan los repositorios. Al salir exitosamente, se hace commit. Si se lanza una excepción dentro del contexto, se hace rollback automáticamente.

## Flujo de Creación de un Pedido

Para ilustrar el poder del patrón UoW, veamos el flujo completo de creación de un pedido, que es la operación más compleja del sistema e involucra múltiples tablas en una sola transacción:

**Paso 1 — Validación del usuario y la dirección**: El servicio utiliza el repositorio de usuarios para verificar que el usuario existe y está activo, y el repositorio de direcciones para verificar que la dirección proporcionada pertenece a ese usuario.

**Paso 2 — Validación de la forma de pago**: Se verifica que la forma de pago exista y esté activa mediante el repositorio de formas de pago.

**Paso 3 — Validación de productos y stock**: Para cada ítem del pedido, el servicio utiliza el repositorio de productos para obtener el producto, verificar que esté disponible (`disponible = true`), que no haya sido eliminado (`eliminado_en IS NULL`), y que tenga stock suficiente (`stock_cantidad >= cantidad solicitada`). Si alguna validación falla, se lanza una excepción inmediatamente.

**Paso 4 — Creación de snapshots**: Para cada producto, se captura el precio actual como `precio_snapshot`. Para la dirección de entrega, se serializa la dirección completa como `direccion_snapshot`. Estos snapshots garantizan que los datos del pedido sean inmutables independientemente de cambios futuros.

**Paso 5 — Cálculo de totales**: Se calcula el subtotal de cada línea (cantidad × precio snapshot), el subtotal general (suma de todos los subtotales de línea), el costo de envío según las reglas de negocio, y el total final.

**Paso 6 — Creación del pedido**: Se crea el registro en la tabla Pedido con el estado PENDIENTE, los totales calculados, y los snapshots. Se usa el repositorio de pedidos.

**Paso 7 — Creación de los detalles**: Para cada ítem, se crea un registro en DetallePedido con el producto, cantidad, precio snapshot, subtotal y personalización. Se usa el repositorio de detalles de pedido.

**Paso 8 — Registro en historial**: Se crea el registro inicial en HistorialEstadoPedido, documentando la creación del pedido (transición de null a PENDIENTE).

**Paso 9 — Commit**: Si todos los pasos anteriores se completaron sin error, el UoW ejecuta commit y todos los registros se persisten atómicamente.

**En caso de error** en cualquier paso (por ejemplo, stock insuficiente en el paso 3, o un error de base de datos en el paso 7), el UoW ejecuta rollback automáticamente. Esto significa que no queda ningún registro parcial — ni el pedido incompleto, ni detalles huérfanos, ni historial sin pedido. El sistema mantiene su consistencia.

## BaseRepository[T]

El `BaseRepository[T]` es una clase genérica que proporciona operaciones CRUD comunes para cualquier entidad. Se parametriza con el tipo de modelo SQLModel (`T`) y recibe la sesión de base de datos en su constructor. Sus métodos son:

- **get_by_id(id)**: Busca un registro por su clave primaria. Retorna el objeto o `None` si no existe. Por defecto, excluye registros con soft delete.

- **list_all(skip, limit, filters)**: Devuelve una lista paginada de registros. Acepta un offset (`skip`), un límite (`limit`), y filtros opcionales. Excluye registros eliminados por defecto.

- **count(filters)**: Devuelve el total de registros que coinciden con los filtros proporcionados, excluyendo eliminados. Útil para paginación.

- **create(obj)**: Recibe un objeto del tipo `T`, lo agrega a la sesión, ejecuta flush (para obtener el ID generado sin hacer commit), y retorna el objeto con su ID.

- **update(id, data)**: Busca el registro por ID, actualiza los campos proporcionados en `data`, ejecuta flush, y retorna el objeto actualizado. Si el registro no existe, lanza una excepción.

- **soft_delete(id)**: Busca el registro por ID y establece `eliminado_en` con el timestamp actual. No elimina el registro físicamente.

- **hard_delete(id)**: Elimina el registro físicamente de la base de datos. Se usa raramente — solo para datos que no necesitan preservarse como refresh tokens expirados.

Los repositorios especializados heredan de `BaseRepository[T]` y agregan métodos específicos del dominio. Por ejemplo, `ProductoRepository` agrega `buscar_por_categoria(categoria_id)` y `actualizar_stock(producto_id, cantidad)`. `PedidoRepository` agrega `listar_por_usuario(usuario_id)` y `listar_por_estado(estado_id)`.
