# 3.3 Dominio 3 — Ventas, Pagos y Trazabilidad

| Entidad | Campo clave | Tipo | Restricción | Notas |
|---------|------------|------|-------------|-------|
| EstadoPedido | codigo | VARCHAR(20) | PK semántica | Catálogo. Ver máquina de estados. |
| EstadoPedido | es_terminal | BOOLEAN | NN | true = no admite transiciones salientes |
| Pedido | estado_codigo | VARCHAR(20) | FK → EstadoPedido | Estado actual del pedido |
| Pedido | total | DECIMAL(10,2) | CHECK ≥ 0, NN | Snapshot inmutable al crear |
| Pedido | costo_envio | DECIMAL(10,2) | NN, default 50.00 | Valor fijo v1. Documentado. |
| Pedido | forma_pago_codigo | VARCHAR(20) | FK → FormaPago | Alineado con PK semántica |
| Pedido | direccion_id | BIGINT | FK, SET NULL | NULL = retiro en local (válido) |
| DetallePedido | nombre_snapshot | VARCHAR(200) | NN, snap | Snapshot: nombre al crear. Inmutable. |
| DetallePedido | precio_snapshot | DECIMAL(10,2) | NN, snap | Snapshot: precio al crear. Inmutable. |
| DetallePedido | personalizacion | INTEGER[] | NULL | IDs de ingredientes removidos (v5: INTEGER[]) |
| HistorialEstadoPedido | estado_desde | VARCHAR(20) | FK, NULL | NULL = transición inicial (RN-02) |
| HistorialEstadoPedido | created_at | TIMESTAMPTZ | NN, append-only | Nunca updated_at. Append-only (RN-03). |
| Pago ★ | mp_payment_id | BIGINT | UQ, NULL | ID devuelto por MercadoPago |
| Pago ★ | mp_status | VARCHAR(30) | NN | pending / approved / rejected |
| Pago ★ | external_reference | VARCHAR(100) | UQ, NN | UUID del Pedido como referencia MP |
| Pago ★ | idempotency_key | VARCHAR(100) | UQ, NN | UUID generado por backend. Evita cobros duplicados. |
