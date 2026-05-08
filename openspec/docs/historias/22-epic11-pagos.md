# EPIC 11 — Pagos con MercadoPago

## US-045: Iniciar proceso de pago

- **Titulo**: Creacion de orden de pago en MercadoPago
- **Historia**: Como **Cliente**, quiero pagar mi pedido a traves de MercadoPago, para completar la compra de forma segura.
- **Prioridad**: Alta
- **Dependencias**: US-035

**Criterios de Aceptacion**:
- [ ] GIVEN un pedido en estado PENDIENTE, WHEN el cliente inicia el pago, THEN se crea una orden de pago en MercadoPago via Orders API.
- [ ] Se genera y almacena un idempotency key para evitar pagos duplicados.
- [ ] El cliente es redirigido al checkout de MercadoPago o se le muestra el formulario embebido.
- [ ] Los datos de tarjeta se tokenizan en el browser (PCI SAQ-A: nunca tocan nuestro servidor).

**Reglas de Negocio**: RN-PA01, RN-PA02, RN-PA09, RN-AU09.

**Notas Tecnicas**:
- Endpoint: `POST /api/pagos/crear` (body: `{ pedidoId }`)
- MercadoPago Orders API para crear la preferencia/orden
- Idempotency key: UUID almacenado en tabla `Pago` asociado al `pedidoId`
- Tokenizacion con SDK JS de MercadoPago en el frontend

## US-046: Procesar webhook de pago (IPN)

- **Titulo**: Recepcion y procesamiento de notificaciones de MercadoPago
- **Historia**: Como **Sistema**, quiero procesar las notificaciones IPN de MercadoPago, para actualizar el estado del pedido segun el resultado del pago.
- **Prioridad**: Alta
- **Dependencias**: US-045

**Criterios de Aceptacion**:
- [ ] GIVEN una notificacion IPN con status `approved`, WHEN se procesa, THEN el pedido pasa de PENDIENTE a CONFIRMADO.
- [ ] GIVEN una notificacion con status `rejected`, WHEN se procesa, THEN se marca el pago como rechazado y el pedido permanece en PENDIENTE.
- [ ] GIVEN una notificacion con status `pending` o `in_process`, WHEN se procesa, THEN se actualiza el estado del pago pero el pedido sigue PENDIENTE.
- [ ] GIVEN una notificacion con status `cancelled`, WHEN se procesa, THEN se registra y el pedido puede ser cancelado.
- [ ] El webhook responde 200 inmediatamente y procesa asincronicamente.
- [ ] Se valida la firma/origen de la notificacion.
- [ ] El procesamiento es idempotente: recibir la misma notificacion 2 veces no causa efectos duplicados.

**Reglas de Negocio**: RN-PA02, RN-PA03, RN-PA04, RN-PA05, RN-PA06, RN-PA07.

**Notas Tecnicas**:
- Endpoint: `POST /api/webhooks/mercadopago`
- Verificar header de firma de MercadoPago
- Idempotencia: verificar si la notificacion ya fue procesada antes de actuar
- Responder 200 OK antes de procesar (o usar cola)

## US-047: Consultar estado de pago

- **Titulo**: Verificacion del estado de pago de un pedido
- **Historia**: Como **Cliente**, quiero ver el estado de pago de mi pedido, para saber si el pago fue procesado correctamente.
- **Prioridad**: Media
- **Dependencias**: US-045

**Criterios de Aceptacion**:
- [ ] GIVEN un pedido propio, WHEN consulto su estado de pago, THEN veo: estado (aprobado, pendiente, rechazado, en_proceso, cancelado), monto, fecha de ultimo update.
- [ ] Solo puedo ver el estado de pago de mis propios pedidos.

**Notas Tecnicas**:
- Endpoint: `GET /api/pedidos/:id/pago`
- Tabla `Pago` con: `id`, `pedidoId`, `mercadoPagoOrderId`, `estado`, `monto`, `idempotencyKey`, `createdAt`, `updatedAt`

## US-048: Reintentar pago rechazado

- **Titulo**: Reintento de pago tras rechazo
- **Historia**: Como **Cliente**, quiero poder reintentar el pago si fue rechazado, para completar mi compra sin tener que crear un nuevo pedido.
- **Prioridad**: Media
- **Dependencias**: US-046

**Criterios de Aceptacion**:
- [ ] GIVEN un pedido en PENDIENTE con pago rechazado, WHEN el cliente reintenta, THEN se genera una nueva orden de pago con nuevo idempotency key.
- [ ] El pedido debe seguir en estado PENDIENTE para permitir reintento.
- [ ] Se mantiene el registro del intento anterior en la tabla de pagos.

**Notas Tecnicas**:
- Endpoint: `POST /api/pagos/crear` (misma logica, nuevo idempotency key)
- Relacion 1:N entre Pedido y Pago (multiples intentos)
