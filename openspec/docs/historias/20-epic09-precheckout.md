# EPIC 09 — Validaciones Pre-Checkout

## US-069: Validar disponibilidad al hacer checkout

- **Titulo**: Verificacion de stock antes de crear el pedido
- **Historia**: Como **Sistema**, quiero validar la disponibilidad de cada producto del carrito antes de crear el pedido, para evitar que el cliente compre algo que ya no esta disponible.
- **Prioridad**: Alta
- **Dependencias**: US-029, US-035

**Criterios de Aceptacion**:
- [ ] GIVEN items en el carrito, WHEN el cliente inicia el checkout, THEN se verifica que cada producto siga disponible y con stock suficiente.
- [ ] GIVEN un producto sin stock suficiente, WHEN se detecta, THEN se notifica al cliente indicando que producto y cuanto stock queda.
- [ ] GIVEN un producto que fue eliminado o desactivado, WHEN se detecta, THEN se notifica al cliente y se sugiere eliminarlo del carrito.

**Notas Tecnicas**:
- Endpoint: `POST /api/pedidos/validar` o validacion dentro de `POST /api/pedidos`
- Pre-validacion client-side + validacion definitiva server-side en la transaccion

## US-070: Verificar precios actualizados al hacer checkout

- **Titulo**: Deteccion de cambios de precio antes de pagar
- **Historia**: Como **Cliente**, quiero ser notificado si un precio cambio desde que agregue el producto al carrito, para decidir si sigo con la compra al nuevo precio.
- **Prioridad**: Media
- **Dependencias**: US-069

**Criterios de Aceptacion**:
- [ ] GIVEN un producto en el carrito cuyo precio cambio desde que fue agregado, WHEN se inicia el checkout, THEN se notifica al cliente mostrando precio viejo vs. nuevo.
- [ ] El cliente puede aceptar el nuevo precio y continuar, o cancelar.

**Notas Tecnicas**:
- Comparar `cart.item.precio` (localStorage) vs `producto.precio` (DB) al validar
- Response incluye array de cambios detectados
