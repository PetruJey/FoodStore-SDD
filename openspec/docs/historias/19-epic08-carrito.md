# EPIC 08 — Carrito de Compras

## US-029: Agregar producto al carrito

- **Titulo**: Agregado de producto al carrito
- **Historia**: Como **Cliente**, quiero agregar productos al carrito indicando cantidad, para ir armando mi pedido.
- **Prioridad**: Alta
- **Dependencias**: US-018

**Criterios de Aceptacion**:
- [ ] GIVEN un producto disponible con stock > 0, WHEN el cliente lo agrega al carrito con cantidad, THEN aparece en el carrito con el subtotal calculado.
- [ ] GIVEN un producto ya en el carrito, WHEN se agrega de nuevo, THEN se incrementa la cantidad.
- [ ] La cantidad debe ser >= 1.
- [ ] El carrito persiste al cerrar el navegador (localStorage).

**Notas Tecnicas**:
- Store: Zustand con middleware `persist` (localStorage)
- Sin endpoint backend — el carrito es client-side only
- Estructura: `{ items: [{ productoId, nombre, precio, cantidad, imagen, exclusiones }] }`

## US-030: Personalizar producto (exclusion de ingredientes)

- **Titulo**: Customizacion del producto en el carrito
- **Historia**: Como **Cliente**, quiero excluir ingredientes de un producto al agregarlo al carrito, para personalizar mi pedido segun mis preferencias o restricciones alimentarias.
- **Prioridad**: Alta
- **Dependencias**: US-029, US-017

**Criterios de Aceptacion**:
- [ ] GIVEN un producto con ingredientes asociados, WHEN el cliente selecciona ingredientes a excluir, THEN se almacenan las exclusiones en el item del carrito.
- [ ] Solo se pueden excluir ingredientes que el producto efectivamente tiene.
- [ ] Las exclusiones se muestran claramente en el resumen del carrito.
- [ ] Las exclusiones se representan como array de IDs de ingredientes.

**Notas Tecnicas**:
- En el Zustand store: `exclusiones: number[]` (IDs de ingredientes excluidos)
- Al crear el pedido, se envian como `INTEGER[]` al backend
- UI: checkboxes o toggles sobre la lista de ingredientes del producto

## US-031: Modificar cantidad de item en el carrito

- **Titulo**: Ajuste de cantidades en el carrito
- **Historia**: Como **Cliente**, quiero cambiar la cantidad de un producto en el carrito, para ajustar mi pedido antes de confirmarlo.
- **Prioridad**: Alta
- **Dependencias**: US-029

**Criterios de Aceptacion**:
- [ ] GIVEN un item en el carrito, WHEN se cambia la cantidad a un valor >= 1, THEN se actualiza el subtotal.
- [ ] GIVEN un item en el carrito, WHEN se pone cantidad 0, THEN se elimina del carrito.
- [ ] Los cambios se persisten inmediatamente en localStorage.

**Notas Tecnicas**:
- Zustand actions: `updateQuantity(productoId, newQty)`
- Recalcular totales reactivamente

## US-032: Eliminar item del carrito

- **Titulo**: Remocion de producto del carrito
- **Historia**: Como **Cliente**, quiero quitar un producto del carrito, para descartar algo que ya no quiero pedir.
- **Prioridad**: Alta
- **Dependencias**: US-029

**Criterios de Aceptacion**:
- [ ] GIVEN un item en el carrito, WHEN se elimina, THEN desaparece del carrito y se recalcula el total.
- [ ] El cambio persiste en localStorage.

**Notas Tecnicas**:
- Zustand action: `removeItem(productoId)`

## US-033: Ver resumen del carrito

- **Titulo**: Visualizacion del carrito
- **Historia**: Como **Cliente**, quiero ver un resumen del carrito con todos los productos, cantidades, exclusiones y el total, para revisar mi pedido antes de confirmarlo.
- **Prioridad**: Alta
- **Dependencias**: US-029

**Criterios de Aceptacion**:
- [ ] GIVEN items en el carrito, WHEN el cliente accede al carrito, THEN ve: nombre del producto, cantidad, precio unitario, exclusiones, subtotal por item, y total general.
- [ ] Si el carrito esta vacio, se muestra un mensaje indicandolo con link al catalogo.
- [ ] Los precios se muestran con 2 decimales.

**Notas Tecnicas**:
- Componente: `CartSummary`
- Selector derivado de Zustand para el total: `useCartStore(state => state.total())`

## US-034: Vaciar carrito

- **Titulo**: Limpieza completa del carrito
- **Historia**: Como **Cliente**, quiero vaciar el carrito de una vez, para empezar de cero si cambie de opinion.
- **Prioridad**: Baja
- **Dependencias**: US-029

**Criterios de Aceptacion**:
- [ ] GIVEN un carrito con items, WHEN el cliente elige vaciar, THEN se confirma la accion con un dialogo y se eliminan todos los items.
- [ ] El total pasa a $0.

**Notas Tecnicas**:
- Zustand action: `clearCart()`
- UI: boton con confirmacion modal
