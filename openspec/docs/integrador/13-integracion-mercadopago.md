# 8. Integración MercadoPago

Food Store integra MercadoPago Checkout API. Permite procesar pagos con tarjeta de crédito/débito, Rapipago, Pago Fácil y Cuenta MercadoPago sin redirigir al cliente fuera del sitio.

**¿Por qué Checkout API con Orders?**

- Única integración para múltiples medios de pago. Sin múltiples APIs separadas.
- Datos de tarjeta tokenizados por MercadoPago.js — NUNCA pasan por el servidor de Food Store (PCI SAQ-A).
- Notificaciones push (IPN/webhook) para confirmación asíncrona del pago.
- idempotency_key UUID generado por el backend evita cobros duplicados por reintento.

## 8.1 Flujo Completo de Pago

[DIAGRAMA: Flujo de Pago - MercadoPago Checkout API] Diagrama de secuencia con tres actores: Frontend React, Backend FastAPI y MercadoPago. Pasos: (1) Frontend renderiza CardPayment con SDK de MercadoPago. (2) Cliente ingresa tarjeta, SDK tokeniza a card_token. (3) Frontend llama POST /api/v1/pagos/crear. (4) Backend genera idempotency_key UUID y llama a MercadoPago API. (5) MercadoPago devuelve mp_payment_id y status. (5b) Backend hace INSERT en tabla Pago via UoW. (6) MercadoPago envia POST /pagos/webhook IPN con topic=payment. (7) Si approved: UoW avanza Pedido a CONFIRMADO. (8) Frontend detecta con polling y actualiza UI. Nota: datos de tarjeta nunca pasan por el servidor de Food Store; es PCI SAQ-A compliant.

Figura 5 — Flujo completo de pago MercadoPago. Los datos de tarjeta nunca pasan por Food Store.

## 8.2 Estados de Pago y Acciones del Sistema

| Estado MP | Descripción | Acción en Food Store |
|-----------|-------------|---------------------|
| approved | Pago aprobado y acreditado | Webhook avanza el pedido a CONFIRMADO de forma automática vía UoW. |
| pending | Pago iniciado o en proceso (efectivo pendiente) | Pedido permanece en PENDIENTE. El webhook confirmará cuando se acredite. |
| rejected | Pago rechazado por el banco o MP | Se muestra status_detail al cliente. El pedido permanece en PENDIENTE. |
| in_process | Pago en revisión manual por MP | Pedido permanece en PENDIENTE. El webhook notificará la resolución. |
| cancelled | Pago cancelado | El cliente puede reintentar o cancelar el pedido. |

## 8.3 Tarjetas de Prueba — Sandbox

| Número de tarjeta | Red | Resultado | CVV | Vencimiento |
|-------------------|-----|-----------|-----|-------------|
| 4509 9535 6623 3704 | Visa | Pago aprobado | 123 | 11/25 |
| 3714 496353 98431 | American Express | Pago aprobado | 1234 | 11/25 |
| 4000 0000 0000 0002 | Visa | Pago rechazado | 123 | 11/25 |
