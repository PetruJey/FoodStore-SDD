# 3.4 Máquina de Estados — Pedido

La entidad EstadoPedido es un catálogo. La capa de servicio valida la transición contra el mapa definido antes de cada INSERT en HistorialEstadoPedido. Ningún router puede saltear esta validación.

[DIAGRAMA: Maquina de Estados - Pedido FSM] Seis estados con transiciones validas. Estados activos: PENDIENTE (orden 1), CONFIRMADO (orden 2), EN_PREP (orden 3), EN_CAMINO (orden 4). Estados terminales: ENTREGADO (orden 5), CANCELADO (orden 6). Flujo principal: PENDIENTE -pago MP- CONFIRMADO, EN_PREP, EN_CAMINO, ENTREGADO. Flechas rojas punteadas hacia CANCELADO desde PENDIENTE, CONFIRMADO y EN_PREP. Reglas: RN-01: es_terminal=true no admite transiciones salientes; RN-02: primer historial con estado_desde=NULL; RN-03: HistorialEstadoPedido es append-only.

Figura 3 — Máquina de estados del Pedido (FSM). Las flechas rojas punteadas indican transición → CANCELADO

| Código | Descripción | Orden | es_terminal | Transiciones válidas |
|--------|------------|-------|-------------|---------------------|
| PENDIENTE | Pedido creado, pago pendiente | 1 | false | → CONFIRMADO, → CANCELADO |
| CONFIRMADO | Pago procesado y confirmado | 2 | false | → EN_PREP, → CANCELADO |
| EN_PREP | En preparación en cocina | 3 | false | → EN_CAMINO, → CANCELADO (solo ADMIN/PEDIDOS) |
| EN_CAMINO | Despachado al cliente | 4 | false | → ENTREGADO |
| ENTREGADO | Entrega confirmada | 5 | TRUE ✓ | — (estado terminal) |
| CANCELADO | Pedido cancelado | 6 | TRUE ✓ | — (estado terminal) |

**Reglas de negocio — Pedidos:**

- RN-01: Un estado con es_terminal = true no admite transiciones salientes. Validación en Service.
- RN-02: El primer registro de HistorialEstadoPedido siempre tiene estado_desde = NULL.
- RN-03: La tabla HistorialEstadoPedido es append-only. Ninguna capa puede emitir UPDATE ni DELETE.
- RN-04: El total, nombre y precio en DetallePedido son un snapshot inmutable al crear el pedido.
- RN-05: El motivo es obligatorio si nuevo_estado = CANCELADO.
