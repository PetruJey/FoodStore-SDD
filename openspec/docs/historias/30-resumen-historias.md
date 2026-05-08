# Resumen de Historias por Epica

| Epica | Historias | Prioridad general |
| ----- | --------- | ----------------- |
| 00 - Infraestructura y Setup | US-000, US-000a, US-000b, US-000c, US-000d, US-000e, US-068, US-074 | Alta |
| 01 - Auth y Autorizacion | US-001 a US-006, US-073 | Alta |
| 02 - Navegacion y Layout Base | US-075, US-076, US-066, US-067 | Alta |
| 03 - Categorias | US-007 a US-010 | Alta |
| 04 - Ingredientes y Alergenos | US-011 a US-014 | Alta |
| 05 - Productos y Catalogo | US-015 a US-023 | Alta |
| 06 - Perfil del Cliente | US-061, US-062, US-063 | Media |
| 07 - Direcciones de Entrega | US-024 a US-028 | Alta |
| 08 - Carrito de Compras | US-029 a US-034 | Alta |
| 09 - Validaciones Pre-Checkout | US-069, US-070 | Alta/Media |
| 10 - Creacion de Pedidos | US-035 a US-038 | Alta |
| 11 - Pagos MercadoPago | US-045 a US-048 | Alta |
| 12 - FSM de Pedidos | US-039 a US-044 | Alta |
| 13 - Visualizacion de Pedidos | US-049 a US-052 | Alta |
| 14 - Notificaciones y Feedback UX | US-071, US-072 | Media/Alta |
| 15 - Admin Usuarios | US-053 a US-055 | Alta/Media |
| 16 - Catalogo Admin | US-064, US-065 | Media |
| 17 - Metricas y Dashboard | US-056 a US-059 | Media |
| 18 - Configuracion del Sistema | US-060 | Baja |

**Total: 77 historias de usuario** (US-000 a US-076) organizadas en 19 epicas, ordenadas por dependencia logica de implementacion.

---

# Orden de Implementacion Recomendado (Plan de Sprints)

**Sprint 0**: EPIC 00 — Infraestructura y Setup
> Scaffolding monorepo, backend FastAPI, PostgreSQL + Alembic + seed, frontend React+Vite, patrones base, stores Zustand, manejo de errores backend (RFC 7807), validacion y sanitizacion de inputs.

**Sprint 1**: EPIC 01 (Auth y Autorizacion) + EPIC 02 (Navegacion y Layout Base)
> Registro, login, refresh, logout, RBAC, proteccion de rutas backend, rate limiting, navegacion por rol, proteccion de rutas frontend, manejo de token expirado, manejo de errores global frontend.

**Sprint 2**: EPIC 03 (Categorias) + EPIC 04 (Ingredientes y Alergenos)
> CRUD completo de categorias (jerarquicas) e ingredientes con flag de alergenos.

**Sprint 3**: EPIC 05 (Productos y Catalogo) + EPIC 06 (Perfil del Cliente)
> Alta, edicion, eliminacion de productos, asociacion a categorias e ingredientes, catalogo publico, filtros por alergenos. Perfil del cliente: ver, editar, cambiar contrasena.

**Sprint 4**: EPIC 07 (Direcciones de Entrega) + EPIC 08 (Carrito de Compras)
> CRUD de direcciones, direccion predeterminada. Carrito client-side con Zustand: agregar, personalizar, modificar, eliminar, vaciar.

**Sprint 5**: EPIC 09 (Validaciones Pre-Checkout) + EPIC 10 (Creacion de Pedidos)
> Validacion de disponibilidad y precios al checkout. Creacion atomica de pedidos con snapshots de precio y direccion, validacion de stock.

**Sprint 6**: EPIC 11 (Pagos con MercadoPago) + EPIC 12 (FSM de Pedidos)
> Integracion con MercadoPago Orders API, webhooks IPN, consulta de estado de pago, reintento. Maquina de estados completa: PENDIENTE -> CONFIRMADO -> EN_PREPARACION -> EN_CAMINO -> ENTREGADO, cancelacion, auditoria.

**Sprint 7**: EPIC 13 (Visualizacion de Pedidos) + EPIC 14 (Notificaciones y Feedback UX)
> Historial de pedidos del cliente, detalle de pedido, panel de gestion para Gestor de Pedidos. Confirmacion visual de pedido creado, feedback de retorno de MercadoPago.

**Sprint 8**: EPIC 15 (Admin Usuarios) + EPIC 16 (Catalogo Admin) + EPIC 17 (Metricas y Dashboard)
> Panel de usuarios (listar, editar, desactivar). Acceso Admin a catalogo y pedidos. Dashboard de metricas: ventas, ranking productos, distribucion por estado. Configuracion del sistema.
