# 7. Patrón Unit of Work (UoW)

El Unit of Work actúa como director de orquesta que garantiza que todas las operaciones de base de datos dentro de una transacción de negocio tengan éxito o fallen como un conjunto. El commit ya no ocurre en el service.

## 7.1 Flujo de una Operación con UoW — Crear Pedido

[DIAGRAMA: Gestion de Estado - Zustand 4 Stores] Cuatro stores con responsabilidades separadas: (1) authStore: accessToken, usuario, isAuthenticated. Metodos: login(), logout(), refreshToken(), hasRole(). Persiste: solo accessToken. (2) cartStore: items CartItem[] con producto_id, nombre, precio, cantidad, imagen_url. Metodos: addItem(), removeItem(), clearCart(), updateCantidad(), subtotal(), costoEnvio(), total(). Persiste: items completos. (3) paymentStore: status idle/processing/approved/rejected/error, mpPaymentId, statusDetail. Metodo: setPaymentStatus(), reset(). SIN persistencia. (4) uiStore: cartOpen, sidebarOpen, confirmModal. Metodos: openCart(), closeCart(), toggleSidebar(). SIN persistencia. Separacion: Zustand gestiona estado del CLIENTE; TanStack Query gestiona estado del SERVIDOR.

Figura 4 — Flujo de creación de pedido con Unit of Work. Todos los INSERT son atómicos.

| Paso | Capa | Operación | ¿Toca BD? |
|------|------|-----------|-----------|
| 1 | Router | Recibe POST /api/v1/pedidos. Valida body con CrearPedidoRequest. | No |
| 2 | Router | Abre contexto: with UnitOfWork() as uow: — llama service.crear_pedido(uow, body, usuario_id). | No |
| 3 | Service | Itera items. Para cada uno: uow.productos.get_by_id(). Verifica disponible = true. | Lectura |
| 4 | Service | Calcula total como suma de precio_snapshot × cantidad. | No |
| 5 | Service | Llama uow.pedidos.create(pedido). uow.flush() → obtiene pedido.id. | INSERT + flush |
| 6 | Service | Crea DetallePedido por cada item con nombre_snapshot y precio_snapshot. | INSERT × N |
| 7 | Service | Crea primer HistorialEstadoPedido con estado_desde=None (RN-02). | INSERT |
| 8 | UoW | \_\_exit\_\_ sin excepción → session.commit(). Todo persiste atómicamente. | COMMIT |
| 9 | Router | Serializa pedido con PedidoRead.model_validate(pedido). Retorna HTTP 201. | No |
| ERR | UoW | Si cualquier paso 3-7 lanza excepción → \_\_exit\_\_ llama rollback(). Nada persiste. | ROLLBACK |

## 7.2 BaseRepository[T] Genérico

| Método | Descripción |
|--------|-------------|
| get_by_id(entity_id: int) → T \| None | Obtiene entidad por clave primaria. Retorna None si no existe. |
| list_all(skip: int, limit: int) → list[T] | Listado simple sin filtros. Para listados complejos, el repo específico define su propio método. |
| count() → int | Cantidad total de registros. Útil para paginación. |
| create(entity: T) → T | Agrega a sesión + flush() + refresh(). Retorna entidad con ID asignado. |
| update(entity: T) → T | Agrega entidad modificada a sesión + flush() + refresh(). |
| soft_delete(entity: T) → None | Asigna deleted_at = now(). Solo para entidades con soft-delete. |
| hard_delete(entity: T) → None | Hard delete. Solo se usa cuando el modelo no tiene soft-delete. |
