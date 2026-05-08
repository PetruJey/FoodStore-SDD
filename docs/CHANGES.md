# Mapa de Changes — Food Store E-Commerce

## Introducción

Este documento establece el mapa completo de changes para desarrollar Food Store de principio a fin, organizado por Sprint según el plan de implementación recomendado. Cada change representa una unidad de trabajo atómica que agrupa historias de usuario relacionadas con sus dependencias claras.

---

## Sprint 0 — Infraestructura y Setup

### change-setup-project-structure

**Funcionalidad**: Scaffolding del monorepo con estructura backend (feature-first) y frontend (Feature-Sliced Design).

**Historias de usuario**:
- US-000: Inicialización del repositorio y estructura del proyecto

**Dependencias**: Ninguna (fundacional)

**Justificación**: Sin estructura de carpetas, el equipo no tiene dónde escribir código de forma consistente. Establece las convenciones que todo el código posterior seguirá.

---

### change-setup-backend

**Funcionalidad**: Configuración del entorno backend con FastAPI, SQLModel, BaseRepository, Unit of Work, middleware de errores y validación.

**Historias de usuario**:
- US-000a: Configuración del entorno backend (FastAPI + dependencias)
- US-000d: Implementación de patrones base (BaseRepository, Unit of Work, dependencias FastAPI)
- US-068: Manejo de errores estandarizado en backend
- US-074: Validación y sanitización de inputs

**Dependencias**: change-setup-project-structure

**Justificación**: Los patrones BaseRepository y Unit of Work son la fundación de todo acceso a datos. Sin atomicidad en transacciones, el sistema no puede garantizar consistencia.

---

### change-setup-database

**Funcionalidad**: PostgreSQL con migraciones Alembic, modelos SQLModel y script de seed (roles, estados de pedido, formas de pago, usuario admin).

**Historias de usuario**:
- US-000b: Configuración de PostgreSQL, migraciones y seed data

**Dependencias**: change-setup-backend

**Justificación**: Sin seed data, no existen los roles, estados ni formas de pago que todo el sistema necesita. Los IDs de seed deben ser estables para referenciarlos en código.

---

### change-setup-frontend

**Funcionalidad**: Configuración del frontend con React, TypeScript, Vite, TanStack Query, Axios con interceptores JWT y Zustand stores base.

**Historias de usuario**:
- US-000c: Configuración del entorno frontend (React + Vite + dependencias)
- US-000e: Configuración de los stores de Zustand (authStore, cartStore, paymentStore, uiStore)

**Dependencias**: change-setup-project-structure

**Justificación**: Los cuatro stores de Zustand son la fundación del estado del cliente. Sin interceptor JWT, no hay forma de hacer requests autenticados.

---

## Sprint 1 — Autenticación, Autorización y Navegación

### change-auth-module

**Funcionalidad**: Módulo de autenticación completo: registro, login, refresh token con rotación, logout.

**Historias de usuario**:
- US-001: Registro de cliente
- US-002: Login de usuario
- US-003: Refresh de token
- US-004: Logout

**Dependencias**: change-setup-database

**Justificación**: La autenticación es la puerta de entrada. El refresh con rotación (RN-AU04) es obligatorio por seguridad. El logout debe invalidar el token en BD.

---

### change-rbac-module

**Funcionalidad**: Sistema RBAC: asignación de roles, verificación por endpoint, rate limiting en login.

**Historias de usuario**:
- US-005: Gestión de roles (RBAC)
- US-006: Protección de rutas por rol
- US-073: Rate limiting en endpoints sensibles

**Dependencias**: change-auth-module

**Justificación**: Sin RBAC, cualquier usuario puede acceder a cualquier recurso. Los cuatro roles (ADMIN, STOCK, PEDIDOS, CLIENT) deben estar protegidos por sensibilidad.

---

### change-frontend-navigation

**Funcionalidad**: Navegación adaptada al rol, guards de autenticación, manejo de token expirado y errores globales.

**Historias de usuario**:
- US-075: Navegación por rol
- US-076: Protección de rutas en frontend
- US-066: Manejo de token expirado en frontend
- US-067: Manejo de errores global en frontend

**Dependencias**: change-auth-module, change-rbac-module, change-setup-frontend

**Justificación**: El menú debe mostrar solo opciones del rol. El interceptor de 401 con refresh evita que el usuario pierda sesión por expiración.

---

## Sprint 2 — Catálogo: Categorías e Ingredientes

### change-categories-crud

**Funcionalidad**: CRUD de categorías con soporte jerárquico (CTE recursivo), soft delete y validación de ciclos.

**Historias de usuario**:
- US-007: Crear categoría
- US-008: Listar categorías jerárquicas
- US-009: Editar categoría
- US-010: Eliminar categoría (soft delete)

**Dependencias**: change-setup-database, change-rbac-module

**Justificación**: Las categorías son la base del catálogo. La jerarquía (RN-CA01) y validación de ciclos (RN-CA02) son requerimientos del dominio.

---

### change-ingredients-crud

**Funcionalidad**: CRUD de ingredientes con campo es_alergeno para identificar alérgenos.

**Historias de usuario**:
- US-011: Crear ingrediente
- US-012: Listar ingredientes
- US-013: Editar ingrediente
- US-014: Eliminar ingrediente (soft delete)

**Dependencias**: change-setup-database, change-rbac-module

**Justificación**: Los ingredientes con flag es_alergeno son críticos para que clientes con restricciones dietarias filtren productos (US-023).

---

## Sprint 3 — Catálogo: Productos y Perfil del Cliente

### change-products-crud

**Funcionalidad**: CRUD de productos, asociación a categorías e ingredientes, stock, catálogo público y filtros por alérgenos.

**Historias de usuario**:
- US-015: Crear producto
- US-016: Asociar producto a categorías
- US-017: Associar ingredientes a producto
- US-018: Listar productos del catálogo (público)
- US-019: Ver detalle de producto
- US-020: Editar producto
- US-021: Gestionar stock de producto
- US-022: Eliminar producto (soft delete)
- US-023: Filtrar productos por alérgenos

**Dependencias**: change-setup-database, change-categories-crud, change-ingredients-crud, change-rbac-module

**Justificación**: El producto es la entidad central del e-commerce. Las asociaciones M2M permiten navegación y filtrado. El stock gestiona disponibilidad.

---

### change-client-profile

**Funcionalidad**: Gestión del perfil del cliente: ver, editar datos personales y cambiar contraseña.

**Historias de usuario**:
- US-061: Ver perfil propio
- US-062: Editar perfil propio
- US-063: Cambiar contraseña

**Dependencias**: change-auth-module

**Justificación**: El cliente debe mantener sus datos actualizados. El email no es editable (es el identificador). El cambio de contraseña debe invalidar todos los refresh tokens.

---

## Sprint 4 — Carrito y Direcciones

### change-delivery-addresses

**Funcionalidad**: CRUD de direcciones de entrega con dirección predeterminada por usuario.

**Historias de usuario**:
- US-024: Crear dirección de entrega
- US-025: Listar direcciones del cliente
- US-026: Editar dirección de entrega
- US-027: Eliminar dirección de entrega
- US-028: Establecer dirección predeterminada

**Dependencias**: change-setup-database, change-auth-module

**Justificación**: La dirección es obligatoria para crear pedido. El snapshot (RN-PE03) preserva los datos al momento de la compra.

---

### change-shopping-cart

**Funcionalidad**: Carrito client-side con Zustand: agregar, personalizar (excluir ingredientes), modificar cantidades, eliminar, ver resumen, vaciar.

**Historias de usuario**:
- US-029: Agregar producto al carrito
- US-030: Personalizar producto (exclusión de ingredientes)
- US-031: Modificar cantidad de item en el carrito
- US-032: Eliminar item del carrito
- US-033: Ver resumen del carrito
- US-034: Vaciar carrito

**Dependencias**: change-products-crud, change-ingredients-crud, change-setup-frontend

**Justificación**: El carrito es client-side only (RN-CR01). La persistencia en localStorage permite que sobreviva al cierre del navegador.

---

## Sprint 5 — Creación de Pedidos

### change-checkout-validation

**Funcionalidad**: Validaciones previas al checkout: disponibilidad de stock y detección de cambios de precio.

**Historias de usuario**:
- US-069: Validar disponibilidad al hacer checkout
- US-070: Verificar precios actualizados al hacer checkout

**Dependencias**: change-shopping-cart, change-products-crud

**Justificación**: Estas validacionesprevienen errores en el momento crítico. Si el stock cambió o el precio aumentó, el cliente debe saberlo antes de pagar.

---

### change-order-creation

**Funcionalidad**: Creación atómica de pedidos con Unit of Work, snapshots de precios y dirección, validación de stock dentro de la transacción.

**Historias de usuario**:
- US-035: Crear pedido desde el carrito
- US-036: Validación de stock al crear pedido
- US-037: Snapshot de precios en el pedido
- US-038: Snapshot de dirección en el pedido

**Dependencias**: change-setup-backend, change-shopping-cart, change-delivery-addresses, change-checkout-validation

**Justificación**: Este es el cambio más complejo. La atomicidad (RN-PE01) garantiza que o todo persiste o nada. Los snapshots preservan datos inmutables.

---

## Sprint 6 — Pagos y FSM de Pedidos

### change-mercadopago-integration

**Funcionalidad**: Integración con MercadoPago: creación de preferencia, webhook IPN, procesamiento de estados y reintentos.

**Historias de usuario**:
- US-045: Iniciar proceso de pago
- US-046: Procesar webhook de pago (IPN)
- US-047: Consultar estado de pago
- US-048: Reintentar pago rechazado

**Dependencias**: change-order-creation, change-setup-database

**Justificación**: La integración con MercadoPago es el corazón del flujo de compra. Los webhooks actualizan el estado y disparan transiciones automáticas.

---

### change-order-fsm

**Funcionalidad**: Máquina de estados de pedidos: transiciones, decremento/restauración de stock, cancelaciones y auditoría append-only.

**Historias de usuario**:
- US-039: Transición PENDIENTE a CONFIRMADO
- US-040: Transición CONFIRMADO a EN_PREPARACION
- US-041: Transición EN_PREPARACION a EN_CAMINO
- US-042: Transición EN_CAMINO a ENTREGADO
- US-043: Cancelar pedido
- US-044: Auditoría de cambios de estado

**Dependencias**: change-order-creation, change-mercadopago-integration

**Justificación**: La FSM garantiza transicionesinválidas se rechacen. El decremento de stock (RN-FS03) y su restauración (RN-FS05) mantienen integridad del inventario. El historial append-only proporciona trazabilidad.

---

## Sprint 7 — Visualización de Pedidos y Feedback

### change-order-viewing

**Funcionalidad**: Visualización de pedidos: historial del cliente, detalle propio, panel de gestión para Gestor de Pedidos.

**Historias de usuario**:
- US-049: Ver mis pedidos (Cliente)
- US-050: Ver detalle de mi pedido (Cliente)
- US-051: Ver todos los pedidos (Gestor de Pedidos)
- US-052: Ver detalle de cualquier pedido (Gestor/Admin)

**Dependencias**: change-order-creation, change-order-fsm, change-rbac-module

**Justificación**: El cliente solo ve sus propios pedidos. El Gestor necesita ver todos para gestionar el flujo.

---

### change-order-feedback

**Funcionalidad**: Feedback visual: confirmación de pedido creado y resultado del pago al retornar de MercadoPago.

**Historias de usuario**:
- US-071: Confirmación de pedido creado
- US-072: Feedback de estado de pago

**Dependencias**: change-order-creation, change-mercadopago-integration

**Justificación**: La confirmaciónda certeza al cliente. El feedback al retornar de MP indica si debe reintentar o si fue exitoso.

---

## Sprint 8 — Administración

### change-admin-user-management

**Funcionalidad**: Panel de gestión de usuarios: listado, edición de roles, activación/desactivación.

**Historias de usuario**:
- US-053: Listar usuarios del sistema
- US-054: Editar usuario (Admin)
- US-055: Desactivar usuario

**Dependencias**: change-auth-module, change-rbac-module, change-setup-database

**Justificación**: El admin gestiona usuarios del sistema. No puede degradarse al último admin (RN-RB04). La desactivación invalida todos los refresh tokens.

---

### change-admin-catalog

**Funcionalidad**: Acceso completo del Admin al catálogo y pedidos: privilegios completos sobre todos los módulos.

**Historias de usuario**:
- US-064: Gestión completa de catálogo (Admin)
- US-065: Gestión completa de pedidos (Admin)

**Dependencias**: change-products-crud, change-categories-crud, change-order-viewing

**Justificación**: El admin debe poder intervenir en cualquier módulo sin depender de otros roles.

---

### change-admin-dashboard

**Funcionalidad**: Dashboard de métricas: KPIs, evolución de ventas, ranking de productos, distribución por estado.

**Historias de usuario**:
- US-056: Dashboard de métricas generales
- US-057: Gráfico de ventas por período
- US-058: Top productos más vendidos
- US-059: Métricas de pedidos por estado

**Dependencias**: change-order-creation, change-admin-user-management

**Justificación**: El dashboard proporciona visibilidad del negocio para tomar decisiones. Las métricas usan consultas de agregación.

---

### change-system-configuration

**Funcionalidad**: Panel de configuración del sistema: parámetros operativos editables por el ADMIN.

**Historias de usuario**:
- US-060: Configuración del sistema

**Dependencias**: change-setup-database

**Justificación**: Permite ajustar parámetros sin cambiar código. Registra quién modificó qué y cuándo. Es el change de menor prioridad.

---

## Resumen por Sprint

| Sprint | Changes | Historias |
|--------|---------|----------|
| **0** | setup-project-structure, setup-backend, setup-database, setup-frontend | US-000, US-000a, US-000b, US-000c, US-000d, US-000e, US-068, US-074 |
| **1** | auth-module, rbac-module, frontend-navigation | US-001 a US-006, US-073, US-075, US-076, US-066, US-067 |
| **2** | categories-crud, ingredients-crud | US-007 a US-014 |
| **3** | products-crud, client-profile | US-015 a US-023, US-061 a US-063 |
| **4** | delivery-addresses, shopping-cart | US-024 a US-034 |
| **5** | checkout-validation, order-creation | US-035 a US-038, US-069, US-070 |
| **6** | mercadopago-integration, order-fsm | US-039 a US-048 |
| **7** | order-viewing, order-feedback | US-049 a US-052, US-071, US-072 |
| **8** | admin-user-management, admin-catalog, admin-dashboard, system-configuration | US-053 a US-060 |

**Total: 20 changes, 77 historias de usuario**

---

## Dependencias entre Changes (Topológico)

```
Sprint 0
│
├───► setup-project-structure
│         │
│         ├───► setup-backend ──► setup-database
│         │                           │
│         │                           ├───► auth-module ──► rbac-module
│         │                           │                    │
│         │                           │                    ├──► categories-crud
│         │                           │                    │
│         │                           │                    ├──► ingredients-crud
│         │                           │                    │
│         │                           │                    └──► client-profile
│         │                           │
│         │                           └──► delivery-addresses
│         │
│         └──► setup-frontend ──► shopping-cart
│                                           │
│                                           └───► checkout-validation
│                                                       │
│                                                       └───► order-creation
│                                                                   │
│                                                                   ├──► mercadopago-integration
│                                                                   │
│                                                                   ├──► order-fsm
│                                                                   │
│                                                                   └──► order-viewing
│                                                                       │
│                                                                       └──► order-feedback
│
│
│  (Sprint 8 admin cambios dependendechanges base)
│
```

---

## Reglas de Implementación

1. **Nunca implementar sin proposal y design aprobados.** Si no existen los artefactos del change, no hay apply.

2. **El orden importa.** Si el change B necesita código del change A, A debe estar archivado antes de proponer B.

3. **Un change = un commit** (o varios commits atómicos). Nunca mezcles dos changes en un mismo commit.

4. **Las specs son código.** Se versionan en git, se revisan en PRs, evolucionan con el proyecto.