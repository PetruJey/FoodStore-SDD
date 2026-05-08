# Integración MercadoPago

## Checkout API con Orders

La integración de pagos en Food Store utiliza la **API de Orders (Checkout)** de MercadoPago. Cuando un cliente está listo para pagar su pedido, el backend crea una orden en MercadoPago que contiene los ítems del pedido con sus precios snapshot, la información del pagador, y las URLs de callback. MercadoPago devuelve una URL de checkout a la que el cliente es redirigido para completar el pago de forma segura en el entorno de MercadoPago.

## Cumplimiento PCI SAQ-A

Food Store cumple con el nivel **PCI DSS SAQ-A** de seguridad en el manejo de datos de tarjetas. Esto significa que los datos sensibles de las tarjetas de crédito (número, CVV, fecha de vencimiento) NUNCA pasan por el servidor de Food Store. La tokenización ocurre directamente en el navegador del cliente mediante el SDK de JavaScript de MercadoPago (MercadoPago.js). El SDK captura los datos de la tarjeta, los envía directamente a los servidores de MercadoPago, y devuelve un token que representa la tarjeta de forma segura. Este token es lo que Food Store envía a su backend para crear el pago — el backend nunca ve ni almacena datos reales de tarjetas.

## Webhooks IPN

Las **Instant Payment Notifications (IPN)** son el mecanismo mediante el cual MercadoPago notifica a Food Store sobre cambios en el estado de los pagos. Cuando un pago cambia de estado (por ejemplo, de "pending" a "approved"), MercadoPago envía un POST al webhook configurado en Food Store.

El flujo del webhook es:

El endpoint recibe la notificación con el tipo de evento y el ID del recurso. Verifica que la notificación sea legítima (validación de firma o headers de MercadoPago). Consulta la API de MercadoPago para obtener el estado actual y completo del pago (nunca confía únicamente en los datos del webhook, siempre verifica). Busca el pedido correspondiente usando el `external_reference`. Actualiza el registro de pago en la base de datos con el nuevo estado. Si corresponde, ejecuta acciones automáticas basadas en el estado. Responde con HTTP 200 inmediatamente para evitar reintentos.

## Clave de Idempotencia

El campo `idempotency_key` en la entidad Pago es una clave única que previene el procesamiento duplicado de pagos. MercadoPago puede enviar múltiples webhooks para el mismo evento (por ejemplo, si el primer intento no recibió un 200 a tiempo), y la clave de idempotencia garantiza que el sistema procese cada pago exactamente una vez. Antes de procesar un webhook, el servicio verifica si ya existe un registro con esa `idempotency_key` — si existe, ignora la notificación duplicada.

## Estados de Pago y Acciones del Sistema

Cada estado de pago en MercadoPago dispara una acción específica en Food Store:

**approved** indica que el pago fue aprobado exitosamente. El sistema registra el pago con estado "approved", y automáticamente transiciona el pedido de PENDIENTE a CONFIRMADO, lo cual a su vez dispara el decremento de stock de todos los productos del pedido.

**pending** indica que el pago está en proceso pero aún no fue confirmado (por ejemplo, un pago en efectivo que el cliente aún no realizó, o una transferencia bancaria pendiente). El sistema registra el pago con estado "pending" pero no modifica el estado del pedido — permanece en PENDIENTE.

**rejected** indica que el pago fue rechazado (tarjeta sin fondos, datos incorrectos, fraude detectado). El sistema registra el pago con estado "rejected". El pedido permanece en PENDIENTE, permitiendo al cliente reintentar el pago con un método diferente.

**in_process** indica que MercadoPago está revisando el pago (verificación antifraude en curso). Similar a "pending", el sistema registra el estado pero no modifica el pedido.

**cancelled** indica que el pago fue cancelado, ya sea por el cliente o por MercadoPago. El sistema registra el pago con estado "cancelled". Si no hay otros pagos pendientes o aprobados para ese pedido, se podría considerar la cancelación automática del pedido según las reglas de negocio configuradas.

## Tarjetas de Prueba en Sandbox

Para el desarrollo y testing, MercadoPago proporciona un entorno Sandbox con tarjetas de prueba que simulan diferentes resultados:

- Tarjetas que siempre resultan en pago aprobado.
- Tarjetas que siempre resultan en pago rechazado.
- Tarjetas que resultan en pago pendiente de revisión.

Estas tarjetas tienen números específicos documentados por MercadoPago y se utilizan con cualquier fecha de vencimiento futura y cualquier CVV. El entorno Sandbox es completamente independiente del entorno de producción y no procesa pagos reales.
