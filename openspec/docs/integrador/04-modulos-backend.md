# 2.3 Módulos Backend (Feature-First)

| Módulo | Ruta | Descripción |
|--------|------|-------------|
| auth | app/modules/auth/ | Login, registro, refresh, logout. JWT access (30 min) + refresh (7 días). Rate limiting. |
| refreshtokens | app/modules/refreshtokens/ | Modelo RefreshToken en BD para invalidación segura en logout. |
| usuarios | app/modules/usuarios/ | CRUD usuarios + asignación de roles RBAC. Soft delete. |
| direcciones | app/modules/direcciones/ | CRUD completo DireccionEntrega por usuario. PATCH /principal. |
| categorias | app/modules/categorias/ | Categorías jerárquicas con CTE recursiva. Soft delete con validación. |
| productos | app/modules/productos/ | Catálogo con Ingrediente (es_alergeno). Stock como campo en Producto. |
| pedidos | app/modules/pedidos/ | Dominio central: máquina de estados FSM, audit trail, historial append-only. |
| pagos | app/modules/pagos/ | Integración MercadoPago: crear pago, webhook IPN, registro de transacciones. |
| admin | app/modules/admin/ | Dashboard con métricas, gestión de stock y usuarios desde el panel. |
