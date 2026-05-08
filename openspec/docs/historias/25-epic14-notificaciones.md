# EPIC 14 — Notificaciones y Feedback UX

## US-071: Confirmacion de pedido creado

- **Titulo**: Feedback visual al crear pedido
- **Historia**: Como **Cliente**, quiero recibir una confirmacion visual clara cuando mi pedido se crea exitosamente, para saber que todo salio bien.
- **Prioridad**: Media
- **Dependencias**: US-035

**Criterios de Aceptacion**:
- [ ] GIVEN un pedido creado exitosamente, WHEN se completa la transaccion, THEN se muestra pantalla de confirmacion con: numero de pedido, resumen de items, total, direccion, y estado "PENDIENTE - Esperando pago".
- [ ] Se incluye un boton/link para ir a pagar.
- [ ] Se incluye un boton para ver el detalle del pedido.

**Notas Tecnicas**:
- Componente: `OrderConfirmation`
- Redirigir automaticamente post-creacion

## US-072: Feedback de estado de pago

- **Titulo**: Retorno de MercadoPago al sitio
- **Historia**: Como **Cliente**, quiero ver el resultado de mi pago al volver de MercadoPago, para saber si debo reintentar o si el pago fue exitoso.
- **Prioridad**: Alta
- **Dependencias**: US-045

**Criterios de Aceptacion**:
- [ ] GIVEN un pago exitoso (callback con status=approved), WHEN el cliente vuelve al sitio, THEN ve mensaje de exito con estado actualizado del pedido.
- [ ] GIVEN un pago rechazado, WHEN vuelve al sitio, THEN ve mensaje de rechazo con opcion de reintentar.
- [ ] GIVEN un pago pendiente, WHEN vuelve, THEN ve mensaje de que esta en proceso con indicacion de esperar.

**Notas Tecnicas**:
- URLs de callback de MercadoPago: `success_url`, `failure_url`, `pending_url`
- Pagina de retorno que consulta el estado actual del pedido/pago
