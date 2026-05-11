# Mapa de Changes — Food Store E-Commerce

## Introducción

Este documento establece el mapa completo de Épicas para desarrollar **Food Store** de principio a fin, organizado por Sprint. Cada Épica tiene su propia **versión** y **palabra clave** (change name) para ejecutar el workflow OPSX de forma ordenada y paso a paso.

### Cómo usar este mapa

Cada Épica es una unidad de trabajo atómica que se implementa con el ritual OPSX completo:

```bash
/opsx:propose <palabra-clave>   # Crear proposal + design + tasks
/opsx:apply <palabra-clave>      # Implementar tareas una por una
/opsx:archive <palabra-clave>    # Sincronizar specs + commitear + archivar
```

Cada checkbox `- [ ]` marca una Épica. Se tilda `- [x]` cuando está archivada y pusheada.

---

## Sprint 0 — Infraestructura y Setup

- [x] **v0.1 — Proyecto Base** → `change-setup-project-structure`

  `/opsx:propose change-setup-project-structure`

  **Funcionalidad**: Scaffolding completo del monorepo: backend FastAPI con estructura feature-first, frontend React+Vite+TypeScript con FSD, PostgreSQL con Alembic, patrones base (BaseRepository, Unit of Work, JWT), stores Zustand y cliente HTTP con interceptores.

  **Historias**: US-000, US-000a, US-000b, US-000c, US-000d, US-000e, US-068, US-074

  **Dependencias**: Ninguna (fundacional)

---

## Sprint 1 — Autenticación, Autorización y Navegación

- [ ] **v1.0 — Módulo de Autenticación** → `change-auth-module`

  `/opsx:propose change-auth-module`

  **Funcionalidad**: Módulo de autenticación completo: registro, login, refresh token con rotación, logout.

  **Historias**: US-001, US-002, US-003, US-004

  **Dependencias**: change-setup-database

- [ ] **v1.1 — Control de Acceso RBAC** → `change-rbac-module`

  `/opsx:propose change-rbac-module`

  **Funcionalidad**: Sistema RBAC: asignación de roles, verificación por endpoint, rate limiting en login.

  **Historias**: US-005, US-006, US-073

  **Dependencias**: change-auth-module

- [ ] **v1.2 — Navegación Frontend** → `change-frontend-navigation`

  `/opsx:propose change-frontend-navigation`

  **Funcionalidad**: Navegación adaptada al rol, guards de autenticación, manejo de token expirado y errores globales.

  **Historias**: US-075, US-076, US-066, US-067

  **Dependencias**: change-auth-module, change-rbac-module, change-setup-frontend

---

## Sprint 2 — Catálogo: Categorías e Ingredientes

- [ ] **v2.0 — CRUD de Categorías** → `change-categories-crud`

  `/opsx:propose change-categories-crud`

  **Funcionalidad**: CRUD de categorías con soporte jerárquico (CTE recursivo), soft delete y validación de ciclos.

  **Historias**: US-007, US-008, US-009, US-010

  **Dependencias**: change-setup-database, change-rbac-module

- [ ] **v2.1 — CRUD de Ingredientes** → `change-ingredients-crud`

  `/opsx:propose change-ingredients-crud`

  **Funcionalidad**: CRUD de ingredientes con campo `es_alergeno` para identificar alérgenos.

  **Historias**: US-011, US-012, US-013, US-014

  **Dependencias**: change-setup-database, change-rbac-module

---

## Sprint 3 — Catálogo: Productos y Perfil del Cliente

- [ ] **v3.0 — CRUD de Productos** → `change-products-crud`

  `/opsx:propose change-products-crud`

  **Funcionalidad**: CRUD de productos, asociación a categorías e ingredientes, stock, catálogo público y filtros por alérgenos.

  **Historias**: US-015, US-016, US-017, US-018, US-019, US-020, US-021, US-022, US-023

  **Dependencias**: change-setup-database, change-categories-crud, change-ingredients-crud, change-rbac-module

- [ ] **v3.1 — Perfil del Cliente** → `change-client-profile`

  `/opsx:propose change-client-profile`

  **Funcionalidad**: Gestión del perfil del cliente: ver, editar datos personales y cambiar contraseña.

  **Historias**: US-061, US-062, US-063

  **Dependencias**: change-auth-module

---

## Sprint 4 — Carrito y Direcciones

- [ ] **v4.0 — Direcciones de Entrega** → `change-delivery-addresses`

  `/opsx:propose change-delivery-addresses`

  **Funcionalidad**: CRUD de direcciones de entrega con dirección predeterminada por usuario.

  **Historias**: US-024, US-025, US-026, US-027, US-028

  **Dependencias**: change-setup-database, change-auth-module

- [ ] **v4.1 — Carrito de Compras** → `change-shopping-cart`

  `/opsx:propose change-shopping-cart`

  **Funcionalidad**: Carrito client-side con Zustand: agregar, personalizar (excluir ingredientes), modificar cantidades, eliminar, ver resumen, vaciar.

  **Historias**: US-029, US-030, US-031, US-032, US-033, US-034

  **Dependencias**: change-products-crud, change-ingredients-crud, change-setup-frontend

---

## Sprint 5 — Creación de Pedidos

- [ ] **v5.0 — Validación de Checkout** → `change-checkout-validation`

  `/opsx:propose change-checkout-validation`

  **Funcionalidad**: Validaciones previas al checkout: disponibilidad de stock y detección de cambios de precio.

  **Historias**: US-069, US-070

  **Dependencias**: change-shopping-cart, change-products-crud

- [ ] **v5.1 — Creación Atómica de Pedidos** → `change-order-creation`

  `/opsx:propose change-order-creation`

  **Funcionalidad**: Creación atómica de pedidos con Unit of Work, snapshots de precios y dirección, validación de stock dentro de la transacción.

  **Historias**: US-035, US-036, US-037, US-038

  **Dependencias**: change-setup-backend, change-shopping-cart, change-delivery-addresses, change-checkout-validation

---

## Sprint 6 — Pagos y FSM de Pedidos

- [ ] **v6.0 — Integración MercadoPago** → `change-mercadopago-integration`

  `/opsx:propose change-mercadopago-integration`

  **Funcionalidad**: Integración con MercadoPago: creación de preferencia, webhook IPN, procesamiento de estados y reintentos.

  **Historias**: US-045, US-046, US-047, US-048

  **Dependencias**: change-order-creation, change-setup-database

- [ ] **v6.1 — Máquina de Estados del Pedido** → `change-order-fsm`

  `/opsx:propose change-order-fsm`

  **Funcionalidad**: Máquina de estados de pedidos: transiciones, decremento/restauración de stock, cancelaciones y auditoría append-only.

  **Historias**: US-039, US-040, US-041, US-042, US-043, US-044

  **Dependencias**: change-order-creation, change-mercadopago-integration

---

## Sprint 7 — Visualización de Pedidos y Feedback

- [ ] **v7.0 — Visualización de Pedidos** → `change-order-viewing`

  `/opsx:propose change-order-viewing`

  **Funcionalidad**: Visualización de pedidos: historial del cliente, detalle propio, panel de gestión para Gestor de Pedidos.

  **Historias**: US-049, US-050, US-051, US-052

  **Dependencias**: change-order-creation, change-order-fsm, change-rbac-module

- [ ] **v7.1 — Feedback de Pedido y Pago** → `change-order-feedback`

  `/opsx:propose change-order-feedback`

  **Funcionalidad**: Feedback visual: confirmación de pedido creado y resultado del pago al retornar de MercadoPago.

  **Historias**: US-071, US-072

  **Dependencias**: change-order-creation, change-mercadopago-integration

---

## Sprint 8 — Administración

- [ ] **v8.0 — Gestión de Usuarios** → `change-admin-user-management`

  `/opsx:propose change-admin-user-management`

  **Funcionalidad**: Panel de gestión de usuarios: listado, edición de roles, activación/desactivación.

  **Historias**: US-053, US-054, US-055

  **Dependencias**: change-auth-module, change-rbac-module, change-setup-database

- [ ] **v8.1 — Gestión Completa de Catálogo y Pedidos** → `change-admin-catalog`

  `/opsx:propose change-admin-catalog`

  **Funcionalidad**: Acceso completo del Admin al catálogo y pedidos: privilegios completos sobre todos los módulos.

  **Historias**: US-064, US-065

  **Dependencias**: change-products-crud, change-categories-crud, change-order-viewing

- [ ] **v8.2 — Dashboard de Métricas** → `change-admin-dashboard`

  `/opsx:propose change-admin-dashboard`

  **Funcionalidad**: Dashboard de métricas: KPIs, evolución de ventas, ranking de productos, distribución por estado.

  **Historias**: US-056, US-057, US-058, US-059

  **Dependencias**: change-order-creation, change-admin-user-management

- [ ] **v8.3 — Configuración del Sistema** → `change-system-configuration`

  `/opsx:propose change-system-configuration`

  **Funcionalidad**: Panel de configuración del sistema: parámetros operativos editables por el ADMIN.

  **Historias**: US-060

  **Dependencias**: change-setup-database

---

## Resumen por Sprint

| Sprint | Épicas | Versiones | Historias |
|--------|--------|-----------|-----------|
| **0** ✅ | setup-project-structure | v0.1 | US-000, US-000a-e, US-068, US-074 |
| **1** | auth-module, rbac-module, frontend-navigation | v1.0 — v1.2 | US-001 a US-006, US-073, US-075, US-076, US-066, US-067 |
| **2** | categories-crud, ingredients-crud | v2.0 — v2.1 | US-007 a US-014 |
| **3** | products-crud, client-profile | v3.0 — v3.1 | US-015 a US-023, US-061 a US-063 |
| **4** | delivery-addresses, shopping-cart | v4.0 — v4.1 | US-024 a US-034 |
| **5** | checkout-validation, order-creation | v5.0 — v5.1 | US-035 a US-038, US-069, US-070 |
| **6** | mercadopago-integration, order-fsm | v6.0 — v6.1 | US-039 a US-048 |
| **7** | order-viewing, order-feedback | v7.0 — v7.1 | US-049 a US-052, US-071, US-072 |
| **8** | admin-user-management, admin-catalog, admin-dashboard, system-configuration | v8.0 — v8.3 | US-053 a US-060 |

**Total: 17 Épicas, 77 historias de usuario**

---

## Dependencias entre Épicas (Topológico)

```
Sprint 0
│
└───► setup-project-structure ✅
            │
            ├───► auth-module ──► rbac-module
            │                    │
            │                    ├──► categories-crud
            │                    │
            │                    ├──► ingredients-crud
            │                    │
            │                    └──► client-profile
            │
            ├──► delivery-addresses
            │
            └──► shopping-cart ──► checkout-validation
                                          │
                                          └───► order-creation
                                                       │
                                                       ├──► mercadopago-integration
                                                       │
                                                       ├──► order-fsm
                                                       │
                                                       └──► order-viewing
                                                           │
                                                           └──► order-feedback

(Sprint 8 admin épicas dependen de changes base)
```

---

## Formato de Seguimiento

Cada Épica se implementa con el ritual OPSX completo:

```bash
/opsx:propose <keyword>    # Crea proposal, design y tasks
/opsx:apply <keyword>       # Implementa tareas una por una
/opsx:archive <keyword>     # Sincroniza specs, commitea y archiva
```

### Convenciones

- **Checkboxes**: Cada Épica tiene un `- [ ]` en el `CHANGES.md`. Se tilda `- [x]` solo cuando está archivada y pusheada.
- **Una Épica a la vez**: Nunca se trabajan dos Épicas en paralelo. Se completa una y se tilda antes de arrancar la siguiente.
- **Tasks en checkboxes**: Los `tasks.md` de cada change usan `- [x]` / `- [ ]` — nada de tablas. El CLI `openspec status` parsea este formato nativamente.
- **Sin atajos**: Ninguna tarea pasa de pendiente a completada sin implementarse y verificarse.
- **Un change = un commit**: Al archivar, el CLI genera el commit automáticamente.
