# Reglas de Negocio — Pagos: MercadoPago

| ID | Regla | Historias Asociadas |
| --- | --- | --- |
| RN-PA01 | Los datos de tarjeta se tokenizan en el browser via SDK MercadoPago.js (nunca tocan nuestro servidor) | US-045 |
| RN-PA02 | Cada pago tiene un idempotency_key único; si se recibe webhook duplicado con misma key, se ignora | US-045, US-046 |
| RN-PA03 | El webhook debe responder HTTP 200 inmediatamente para evitar reintentos de MercadoPago | US-046 |
| RN-PA04 | Siempre se verifica el estado real consultando la API de MercadoPago; nunca se confía solo en los datos del webhook | US-046 |
| RN-PA05 | Pago "approved" → transición automática PENDIENTE→CONFIRMADO + decremento de stock | US-046 |
| RN-PA06 | Pago "rejected" → pedido permanece PENDIENTE; el cliente puede reintentar con otro método | US-046, US-048 |
| RN-PA07 | Pago "pending"/"in_process" → se actualiza estado del pago pero el pedido sigue PENDIENTE | US-046 |
| RN-PA08 | Un pedido puede tener múltiples intentos de pago (relación 1:N Pedido→Pago) | US-048 |
| RN-PA09 | Se usa external_reference para vincular la preferencia de MercadoPago con el pedido en Food Store | US-045, US-046 |
