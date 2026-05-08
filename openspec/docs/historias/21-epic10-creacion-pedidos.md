# EPIC 10 — Creacion de Pedidos

## US-035: Crear pedido desde el carrito

- **Titulo**: Creacion de pedido
- **Historia**: Como **Cliente**, quiero confirmar mi carrito y crear un pedido, para proceder al pago y recibir mis productos.
- **Prioridad**: Alta
- **Dependencias**: US-029, US-024

**Criterios de Aceptacion**:
- [ ] GIVEN un carrito con items y una direccion seleccionada, WHEN el cliente confirma el pedido, THEN se crea un pedido en estado PENDIENTE.
- [ ] Se genera un snapshot del precio de cada producto al momento de la creacion (RN-PE02).
- [ ] Se genera un snapshot de la direccion de entrega seleccionada (RN-PE03).
- [ ] La creacion es atomica: si falla cualquier parte, no se persiste nada (Unit of Work).
- [ ] Las exclusiones de ingredientes se almacenan como `INTEGER[]` en cada linea del pedido.
- [ ] Se vacia el carrito tras la creacion exitosa.
- [ ] Se registra la entrada inicial en `HistorialEstadoPedido` con estado PENDIENTE (RN-FS07).

**Reglas de Negocio**: RN-PE01, RN-PE02 (precio snapshot), RN-PE03 (direccion snapshot), RN-PE04, RN-PE05, RN-PE06, RN-PE07, RN-PE08, RN-FS07 (auditoria).

**Notas Tecnicas**:
- Endpoint: `POST /api/pedidos`
- Body: `{ direccionId, items: [{ productoId, cantidad, exclusiones: number[] }] }`
- Patron: Unit of Work — transaccion con INSERT en `Pedido`, `DetallePedido[]`, `HistorialEstadoPedido`
- Snapshot: copiar precio actual y datos de direccion a campos del pedido, no FK directa
- Validar stock disponible DENTRO de la transaccion (SELECT FOR UPDATE)

## US-036: Validacion de stock al crear pedido

- **Titulo**: Verificacion de disponibilidad al confirmar
- **Historia**: Como **Sistema**, quiero validar que haya stock suficiente de cada producto al crear un pedido, para evitar ventas de productos agotados.
- **Prioridad**: Alta
- **Dependencias**: US-035

**Criterios de Aceptacion**:
- [ ] GIVEN un item del pedido con cantidad 3 y stock disponible 2, WHEN se intenta crear el pedido, THEN se rechaza con error indicando el producto y stock disponible.
- [ ] La verificacion se hace de forma atomica dentro de la transaccion (SELECT FOR UPDATE).
- [ ] Si algun producto no tiene stock suficiente, no se crea NINGUN item del pedido.

**Reglas de Negocio**: RN-PE04, RN-PE05 (stock atomico dentro de transaccion).

**Notas Tecnicas**:
- `SELECT stock FROM Producto WHERE id = ? FOR UPDATE` dentro de la transaccion
- Validar TODOS los items antes de hacer cualquier INSERT

## US-037: Snapshot de precios en el pedido

- **Titulo**: Captura de precios al momento de la compra
- **Historia**: Como **Sistema**, quiero almacenar el precio de cada producto al momento de crear el pedido, para que cambios futuros de precios no afecten pedidos existentes.
- **Prioridad**: Alta
- **Dependencias**: US-035

**Criterios de Aceptacion**:
- [ ] GIVEN un pedido creado, WHEN el precio del producto cambia posteriormente, THEN el pedido mantiene el precio original de la compra.
- [ ] El precio snapshot se almacena en `DetallePedido.precioUnitario`.
- [ ] El total del pedido se calcula a partir de los precios snapshot.

**Reglas de Negocio**: RN-PE02, RN-DA06.

**Notas Tecnicas**:
- Campo `precioUnitario DECIMAL(10,2)` en `DetallePedido`
- Campo `total DECIMAL(10,2)` calculado y almacenado en `Pedido`

## US-038: Snapshot de direccion en el pedido

- **Titulo**: Captura de direccion al momento de la compra
- **Historia**: Como **Sistema**, quiero almacenar la direccion de entrega al momento de crear el pedido, para que modificaciones futuras de la direccion no afecten pedidos en curso.
- **Prioridad**: Alta
- **Dependencias**: US-035

**Criterios de Aceptacion**:
- [ ] GIVEN un pedido creado, WHEN el cliente modifica la direccion original, THEN el pedido mantiene la direccion snapshot.
- [ ] Los campos de direccion se copian directamente al pedido o a una tabla de snapshot.

**Reglas de Negocio**: RN-PE03, RN-DA06.

**Notas Tecnicas**:
- Campos en `Pedido`: `direccionCalle`, `direccionNumero`, `direccionPiso`, `direccionCiudad`, `direccionCP`
- Alternativa: JSON serializado en campo `direccionSnapshot`
