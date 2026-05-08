# EPIC 13 — Visualizacion de Pedidos

## US-049: Ver mis pedidos (Cliente)

- **Titulo**: Historial de pedidos del cliente
- **Historia**: Como **Cliente**, quiero ver el listado de todos mis pedidos con su estado actual, para hacer seguimiento de mis compras.
- **Prioridad**: Alta
- **Dependencias**: US-035

**Criterios de Aceptacion**:
- [ ] GIVEN un cliente autenticado, WHEN consulta sus pedidos, THEN ve una lista paginada con: numero de pedido, fecha, estado actual, total, cantidad de items.
- [ ] Solo ve sus propios pedidos.
- [ ] Ordenados por fecha descendente (mas recientes primero).
- [ ] Soporta filtro por estado.

**Notas Tecnicas**:
- Endpoint: `GET /api/pedidos` (filtrado automatico por userId del JWT)
- Query params: `?estado=EN_CAMINO&page=1&limit=10`

## US-050: Ver detalle de mi pedido (Cliente)

- **Titulo**: Detalle completo de un pedido propio
- **Historia**: Como **Cliente**, quiero ver el detalle completo de uno de mis pedidos, para conocer los productos, cantidades, exclusiones, direccion y estado de pago.
- **Prioridad**: Alta
- **Dependencias**: US-049

**Criterios de Aceptacion**:
- [ ] GIVEN un pedido propio, WHEN consulto su detalle, THEN veo: items (nombre, cantidad, precio snapshot, exclusiones), direccion snapshot, estado actual, total, estado de pago.
- [ ] No puedo ver pedidos de otros clientes (403).

**Notas Tecnicas**:
- Endpoint: `GET /api/pedidos/:id`
- Join con `DetallePedido` para los items

## US-051: Ver todos los pedidos (Gestor de Pedidos)

- **Titulo**: Panel de gestion de pedidos
- **Historia**: Como **Gestor de Pedidos**, quiero ver todos los pedidos del sistema con filtros por estado, para gestionar el flujo de preparacion y entrega.
- **Prioridad**: Alta
- **Dependencias**: US-035

**Criterios de Aceptacion**:
- [ ] GIVEN un Gestor de Pedidos autenticado, WHEN accede al panel, THEN ve todos los pedidos de todos los clientes.
- [ ] Puede filtrar por estado (especialmente CONFIRMADO, EN_PREPARACION, EN_CAMINO).
- [ ] Puede filtrar por rango de fechas.
- [ ] Puede buscar por numero de pedido o nombre de cliente.
- [ ] Paginacion obligatoria.

**Notas Tecnicas**:
- Endpoint: `GET /api/admin/pedidos` (rol PEDIDOS o ADMIN)
- Query params: `?estado=CONFIRMADO&desde=2026-01-01&hasta=2026-03-31&page=1&limit=20`

## US-052: Ver detalle de cualquier pedido (Gestor/Admin)

- **Titulo**: Detalle completo de pedido para gestion
- **Historia**: Como **Gestor de Pedidos**, quiero ver el detalle completo de cualquier pedido, para tomar decisiones sobre su procesamiento.
- **Prioridad**: Alta
- **Dependencias**: US-051

**Criterios de Aceptacion**:
- [ ] GIVEN un pedido del sistema, WHEN el gestor consulta su detalle, THEN ve: items con snapshots, direccion snapshot, historial de estados, datos del cliente, estado de pago.
- [ ] Incluye el historial completo de estados con fechas y actores.

**Notas Tecnicas**:
- Endpoint: `GET /api/admin/pedidos/:id`
- Joins: DetallePedido + HistorialEstadoPedido + Pago
