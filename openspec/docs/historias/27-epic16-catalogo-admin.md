# EPIC 16 — Gestion Avanzada de Catalogo (Admin)

## US-064: Gestion completa de catalogo (Admin)

- **Titulo**: CRUD de catalogo con privilegios de Admin
- **Historia**: Como **Admin**, quiero tener acceso completo a la gestion del catalogo (productos, categorias, ingredientes), para intervenir cuando sea necesario sin depender del Gestor de Stock.
- **Prioridad**: Media
- **Dependencias**: US-015, US-007, US-011

**Criterios de Aceptacion**:
- [ ] GIVEN un Admin, WHEN accede a los endpoints de gestion de catalogo, THEN tiene los mismos permisos que el Gestor de Stock.
- [ ] El Admin puede crear, editar y eliminar productos, categorias e ingredientes.
- [ ] Los endpoints de catalogo aceptan tanto rol ADMIN como STOCK.

**Notas Tecnicas**:
- Guard/middleware: `@Roles('ADMIN', 'STOCK')` en endpoints de gestion de catalogo

## US-065: Gestion completa de pedidos (Admin)

- **Titulo**: Control total sobre pedidos
- **Historia**: Como **Admin**, quiero poder gestionar cualquier pedido (ver, avanzar estado, cancelar), para resolver situaciones excepcionales.
- **Prioridad**: Media
- **Dependencias**: US-051, US-043

**Criterios de Aceptacion**:
- [ ] GIVEN un Admin, WHEN accede a los endpoints de gestion de pedidos, THEN tiene los mismos permisos que el Gestor de Pedidos.
- [ ] Los endpoints de pedidos aceptan tanto rol ADMIN como PEDIDOS.

**Notas Tecnicas**:
- Guard/middleware: `@Roles('ADMIN', 'PEDIDOS')` en endpoints de gestion de pedidos
