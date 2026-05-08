# 3.2 Dominio 2 — Catálogo de Productos

| Entidad | Campo clave | Tipo | Restricción | Notas |
|---------|------------|------|-------------|-------|
| Categoria | parent_id | BIGINT | FK self-ref, NULL | Jerarquía recursiva. ON DELETE SET NULL. CTE. |
| Producto | precio_base | DECIMAL(10,2) | CHECK ≥ 0, NN | Snapshot al crear pedido |
| Producto ★ | stock_cantidad | INTEGER | CHECK ≥ 0, NN, default 0 | Gestionado por rol STOCK |
| Producto ★ | disponible | BOOLEAN | NN, default true | Toggle manual independiente del stock |
| Ingrediente ★ | nombre | VARCHAR(100) | UQ, NN | Especificación completa en v5 |
| Ingrediente ★ | es_alergeno | BOOLEAN | NN, default false | Badge de alérgenos en UI |
| ProductoCategoria | (producto_id, cat_id) | BIGINT×2 | PK compuesta | Pivot N:M. es_principal. |
| ProductoIngrediente ★ | es_removible | BOOLEAN | NN | Habilita personalización del pedido |
| FormaPago ★ | codigo | VARCHAR(20) | PK semántica | MERCADOPAGO \| EFECTIVO \| TRANSFERENCIA |
| FormaPago ★ | habilitado | BOOLEAN | NN, default true | Se puede deshabilitar sin eliminar |
