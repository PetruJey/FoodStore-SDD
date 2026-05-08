# Reglas de Negocio — Pedidos: Creacion

| ID | Regla | Historias Asociadas |
| --- | --- | --- |
| RN-PE01 | La creación de un pedido es ATÓMICA (Unit of Work): si falla cualquier parte, no se persiste nada | US-035, US-036 |
| RN-PE02 | Al crear un pedido se genera snapshot del precio de cada producto (precio_snapshot en DetallePedido) | US-035, US-037 |
| RN-PE03 | Al crear un pedido se genera snapshot de la dirección de entrega (direccion_snapshot en Pedido) | US-035, US-038 |
| RN-PE04 | Se debe validar stock suficiente DENTRO de la transacción (SELECT FOR UPDATE) antes de crear el pedido | US-036 |
| RN-PE05 | Si algún producto no tiene stock suficiente, no se crea NINGÚN ítem del pedido (todo o nada) | US-036 |
| RN-PE06 | Todo pedido nace en estado PENDIENTE con registro inicial en HistorialEstadoPedido | US-035 |
| RN-PE07 | La personalización se almacena como INTEGER[] (array de PostgreSQL) en DetallePedido | US-035 |
| RN-PE08 | El total del pedido = suma de subtotales (cantidad x precio_snapshot) + costo de envío | US-035 |
