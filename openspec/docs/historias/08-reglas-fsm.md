# Reglas de Negocio — Pedidos: Maquina de Estados (FSM)

| ID | Regla | Historias Asociadas |
| --- | --- | --- |
| RN-FS01 | Un pedido solo puede avanzar al siguiente estado en la secuencia; no se permiten saltos ni retrocesos | US-039 a US-042 |
| RN-FS02 | La transición PENDIENTE → CONFIRMADO es EXCLUSIVAMENTE automática (por pago aprobado); nadie la ejecuta manual | US-039, US-046 |
| RN-FS03 | Al confirmar (PENDIENTE→CONFIRMADO), se decrementa atómicamente el stock de cada producto del pedido | US-039 |
| RN-FS04 | Si el decremento de stock falla para cualquier producto, toda la operación se revierte (rollback) | US-039 |
| RN-FS05 | Al cancelar un pedido que ya fue CONFIRMADO, se debe restaurar el stock de forma atómica (operación inversa) | US-043 |
| RN-FS06 | ENTREGADO y CANCELADO son estados terminales; no se permite ninguna transición adicional desde ellos | US-042, US-043 |
| RN-FS07 | Todo cambio de estado se registra en HistorialEstadoPedido (append-only: solo INSERT, nunca UPDATE ni DELETE) | US-039 a US-044 |
| RN-FS08 | Cancelación posible desde: PENDIENTE (Cliente/Gestor/Admin), CONFIRMADO (Gestor/Admin), EN_PREPARACIÓN (solo Admin) | US-043 |
| RN-FS09 | Cada registro de historial incluye: estado anterior, estado nuevo, timestamp, usuario o SISTEMA, observación | US-044 |
