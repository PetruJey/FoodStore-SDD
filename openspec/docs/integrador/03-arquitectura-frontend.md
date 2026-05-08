# 2.2 Capas del Frontend — Feature-Sliced Design

El frontend aplica Feature-Sliced Design. Cada feature es autocontenida: sus componentes, hooks y estilos no son accesibles desde otras features. Los imports fluyen de arriba hacia abajo: Pages → Features → Hooks/Stores → API → Types.

[DIAGRAMA: Patron Unit of Work - Flujo Crear Pedido] Diagrama de secuencia con cuatro actores: Router, Service, Unit of Work y PostgreSQL. Pasos: (1) Router recibe POST /api/v1/pedidos y valida CrearPedidoRequest. (2) Router abre contexto UnitOfWork y llama service.crear_pedido(uow,...). (3) Service itera items, verifica disponible=true (SELECT). (4) Service calcula total: precio_snap x cantidad. (5) Service crea pedido + flush, obtiene id (INSERT). (6) Service crea DetallePedido por cada item con snapshots (INSERT x N). (7) Service crea HistorialEstadoPedido con estado_desde=NULL (INSERT). (8) UoW hace COMMIT atomico. Si hay error: ROLLBACK, nada persiste.

Figura 2 — Capas del frontend y organización feature-sliced

**Separación Zustand / TanStack Query:**

Zustand gestiona el estado del CLIENTE: carrito, sesión, proceso de pago, UI local (modales, sidebar).

TanStack Query gestiona el estado del SERVIDOR: productos, pedidos, dashboard. Datos remotos con caché automático.

Mezclar ambos tipos de estado en el mismo store es un error arquitectónico que debe evitarse.
