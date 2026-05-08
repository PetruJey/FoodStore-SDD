# EPIC 12 — Maquina de Estados de Pedidos (FSM)

## US-039: Transicion de estado — PENDIENTE a CONFIRMADO

- **Titulo**: Confirmacion del pedido tras pago aprobado
- **Historia**: Como **Sistema**, quiero que el pedido pase automaticamente de PENDIENTE a CONFIRMADO cuando el pago es aprobado, para iniciar su preparacion.
- **Prioridad**: Alta
- **Dependencias**: US-035, US-046 (pagos)

**Criterios de Aceptacion**:
- [ ] GIVEN un pedido en estado PENDIENTE, WHEN se recibe webhook de pago aprobado, THEN el estado cambia a CONFIRMADO.
- [ ] Se descuenta el stock atomicamente al confirmar (RN-FS03).
- [ ] Se registra en HistorialEstadoPedido: estado anterior, estado nuevo, timestamp, actor (SISTEMA) (RN-FS07).
- [ ] La transicion PENDIENTE -> CONFIRMADO solo ocurre por pago aprobado, no manualmente.

**Reglas de Negocio**: RN-FS01 (FSM estricta), RN-FS02, RN-FS03 (decremento atomico), RN-FS04, RN-FS07 (auditoria), RN-FS09.

**Notas Tecnicas**:
- Patron State Machine: validar transicion contra mapa de transiciones permitidas
- `{ PENDIENTE: ['CONFIRMADO', 'CANCELADO'], CONFIRMADO: ['EN_PREPARACION', 'CANCELADO'], ... }`
- Stock: `UPDATE Producto SET stock = stock - :cant WHERE id = :id AND stock >= :cant`

## US-040: Transicion — CONFIRMADO a EN_PREPARACION

- **Titulo**: Inicio de preparacion del pedido
- **Historia**: Como **Gestor de Pedidos**, quiero marcar un pedido confirmado como en preparacion, para que el equipo de cocina comience a trabajar en el.
- **Prioridad**: Alta
- **Dependencias**: US-039

**Criterios de Aceptacion**:
- [ ] GIVEN un pedido en estado CONFIRMADO, WHEN el Gestor de Pedidos avanza el estado, THEN pasa a EN_PREPARACION.
- [ ] Se registra en HistorialEstadoPedido con el usuario que realizo la accion (RN-FS07).
- [ ] GIVEN un pedido en cualquier otro estado, WHEN se intenta pasar a EN_PREPARACION, THEN se rechaza con error (RN-FS01).

**Reglas de Negocio**: RN-FS01, RN-FS07, RN-FS09.

**Notas Tecnicas**:
- Endpoint: `PATCH /api/pedidos/:id/estado` (body: `{ nuevoEstado: 'EN_PREPARACION' }`)
- Validar transicion contra FSM antes de persistir

## US-041: Transicion — EN_PREPARACION a EN_CAMINO

- **Titulo**: Despacho del pedido
- **Historia**: Como **Gestor de Pedidos**, quiero marcar un pedido como en camino, para indicar que fue despachado para entrega.
- **Prioridad**: Alta
- **Dependencias**: US-040

**Criterios de Aceptacion**:
- [ ] GIVEN un pedido en EN_PREPARACION, WHEN se avanza el estado, THEN pasa a EN_CAMINO.
- [ ] Se registra en HistorialEstadoPedido (RN-FS07).
- [ ] La transicion solo es valida desde EN_PREPARACION (RN-FS01).

**Reglas de Negocio**: RN-FS01, RN-FS07, RN-FS09.

**Notas Tecnicas**:
- Mismo endpoint `PATCH /api/pedidos/:id/estado`

## US-042: Transicion — EN_CAMINO a ENTREGADO

- **Titulo**: Entrega del pedido
- **Historia**: Como **Gestor de Pedidos**, quiero marcar un pedido como entregado, para cerrar su ciclo de vida.
- **Prioridad**: Alta
- **Dependencias**: US-041

**Criterios de Aceptacion**:
- [ ] GIVEN un pedido en EN_CAMINO, WHEN se marca como entregado, THEN pasa a ENTREGADO.
- [ ] Se registra en HistorialEstadoPedido (RN-FS07).
- [ ] Un pedido en estado ENTREGADO no puede cambiar a ningun otro estado (RN-FS06).

**Reglas de Negocio**: RN-FS01, RN-FS06, RN-FS07, RN-FS09.

**Notas Tecnicas**:
- Mismo endpoint `PATCH /api/pedidos/:id/estado`
- ENTREGADO es estado terminal

## US-043: Cancelar pedido

- **Titulo**: Cancelacion de pedido
- **Historia**: Como **Gestor de Pedidos**, quiero cancelar un pedido en estado PENDIENTE o CONFIRMADO, para gestionar pedidos que no se van a completar.
- **Prioridad**: Alta
- **Dependencias**: US-035

**Criterios de Aceptacion**:
- [ ] GIVEN un pedido en estado PENDIENTE, WHEN se cancela, THEN pasa a CANCELADO (RN-FS08).
- [ ] GIVEN un pedido en estado CONFIRMADO, WHEN se cancela, THEN pasa a CANCELADO y se devuelve el stock descontado (RN-FS08, RN-FS05).
- [ ] GIVEN un pedido en EN_PREPARACION, EN_CAMINO o ENTREGADO, WHEN se intenta cancelar, THEN se rechaza con error (RN-FS08, RN-RB08).
- [ ] Se registra en HistorialEstadoPedido el motivo de cancelacion (RN-FS07).
- [ ] CANCELADO es estado terminal (RN-FS06).

**Reglas de Negocio**: RN-FS01, RN-FS05 (restauracion de stock), RN-FS06, RN-FS07, RN-FS08, RN-FS09, RN-RB08.

**Notas Tecnicas**:
- Endpoint: `PATCH /api/pedidos/:id/estado` (body: `{ nuevoEstado: 'CANCELADO', motivo: '...' }`)
- Si venia de CONFIRMADO: `UPDATE Producto SET stock = stock + :cant WHERE id = :id`
- Transaccion atomica: cambio de estado + devolucion de stock

## US-044: Auditoria de cambios de estado

- **Titulo**: Historial de estados del pedido
- **Historia**: Como **Admin**, quiero ver el historial completo de estados de un pedido, para auditar su procesamiento y resolver incidentes.
- **Prioridad**: Alta
- **Dependencias**: US-039

**Criterios de Aceptacion**:
- [ ] GIVEN un pedido, WHEN se consulta su historial, THEN se retorna una lista cronologica de todas las transiciones con: estado anterior, estado nuevo, fecha/hora, usuario/sistema que realizo el cambio.
- [ ] El historial es append-only: no se pueden editar ni eliminar registros.
- [ ] Cada transicion incluye motivo (obligatorio para cancelaciones).

**Reglas de Negocio**: RN-FS07, RN-FS09, RN-DA05.

**Notas Tecnicas**:
- Endpoint: `GET /api/pedidos/:id/historial`
- Tabla: `HistorialEstadoPedido` con `id`, `pedidoId`, `estadoAnterior`, `estadoNuevo`, `timestamp`, `usuarioId`, `motivo`
- Sin UPDATE ni DELETE en esta tabla (append-only)
