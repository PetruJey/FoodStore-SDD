# AGENTS.md — Instrucciones para Agentes IA

## Índice

1. [Documentación del Sistema](#documentación-del-sistema)
2. [Visión General del Proyecto](#visión-general-del-proyecto)
3. [Stack Tecnológico](#stack-tecnológico)
4. [Arquitectura del Sistema](#arquitectura-del-sistema)
5. [Modelo de Datos](#modelo-de-datos)
6. [Máquina de Estados del Pedido](#máquina-de-estados-del-pedido)
7. [Autenticación y Autorización](#autenticación-y-autorización)
8. [Convenciones de Código](#convenciones-de-código)
9. [Estructura de Archivos](#estructura-de-archivos)
10. [Workflow SDD](#workflow-sdd)
11. [Reglas de Negocio Clave](#reglas-de-negocio-clave)
12. [Integración MercadoPago](#integración-mercadopago)
13. [Gemas del Proyecto](#gemas-del-proyecto)
14. [SDD Multi-Agent Delegation System](#sdd-multi-agent-delegation-system)

---

## 📚 Documentación del Sistema

Antes de proponer, diseñar o implementar cualquier cambio, leé la documentación modular desde `openspec/docs/index.md`:

1. Abrí `openspec/docs/index.md` — es el **mapa completo** de toda la documentación
2. Desde ahí navegá al archivo específico que necesités (descripción, historias, integrador)
3. **No leas los archivos monolíticos** `docs/Descripcion.txt`, `docs/Integrador.txt` ni `docs/Historias_de_usuario.txt` — su contenido ya está dividido en `openspec/docs/`

Los archivos fuente originales están en `docs/` pero la documentación modular en `openspec/docs/` es la que debe usar el agente. Si necesitás una sección específica (ej: reglas de autenticación, API de pedidos), buscá el archivo correspondiente en el índice en lugar de leer el documento entero.

Además, **`docs/CHANGES.md`** contiene el mapa completo de épicas con versiones, dependencias y palabras clave para `/opsx:propose`. Es la hoja de ruta de implementación — consultalo antes de empezar cualquier change para entender qué sigue y de qué depende.

> ⚠️ Esta sección reemplaza a la referencia a los 3 archivos `docs/` que estaba en versiones anteriores.

---

## Visión General del Proyecto

**Food Store** es un sistema de e-commerce para la venta de productos alimenticios.

- **5 actores**: Cliente, Admin, Gestor de Stock, Gestor de Pedidos, Sistema
- **Funcionalidades principales**: catálogo de productos, carrito de compras, pedidos con FSM de 6 estados, pagos con MercadoPago, panel de administración
- **Metodología**: Spec-Driven Development (SDD) con cambios atómicos
- **Total de historias de usuario**: 77 (US-000 a US-076, incluyendo sub-letras como US-000a-e)

---

## Stack Tecnológico

### Frontend

| Tecnología | Rol |
|------------|-----|
| React 18.x + TypeScript 5.x | UI y componentes |
| Vite 5.x | Build tool y dev server |
| TanStack Query 5.x | Estado del servidor (fetching, caché) |
| TanStack Form | Formularios con validación |
| Zustand 4.x | Estado del cliente (carrito, sesión, UI) |
| Axios | Cliente HTTP con interceptores JWT |
| Tailwind CSS 3.x | Estilos utility-first |
| recharts | Gráficos del dashboard |
| @mercadopago/sdk-js | Tokenización de tarjetas (PCI) |

### Backend

| Tecnología | Rol |
|------------|-----|
| FastAPI 0.111+ | Framework REST + OpenAPI |
| SQLModel | ORM + schemas Pydantic |
| PostgreSQL 15+ | Base de datos relacional |
| Alembic | Migraciones |
| Passlib (bcrypt) | Hashing de contraseñas |
| slowapi | Rate limiting |
| python-jose | Tokens JWT |
| mercadopago SDK Python | Integración de pagos |

---

## Arquitectura del Sistema

### Backend — Capas (flow de dependencias)

```
Router → Service → Unit of Work → Repository → Model
```

- **Router**: HTTP puro, valida schemas Pydantic, delega al Service
- **Service**: Lógica de negocio stateless, orquesta vía UoW
- **Unit of Work**: Transacción atómica, provee repositorios, commit/rollback automático
- **Repository**: Acceso a BD, hereda de BaseRepository[T] genérico
- **Model**: Tablas SQLModel, sin imports de capas superiores

### Frontend — Feature-Sliced Design

```
pages → features → entities → shared
```

| Capa | Descripción |
|------|-----------|
| pages | Definiciones de rutas |
| features | Interacciones de usuario específicas |
| entities | Modelos del dominio + operaciones básicas |
| shared | Componentes UI, utilidades, configuración API |

### Separación de Estado

- **Zustand**: Estado del CLIENTE (carrito, sesión, UI local)
- **TanStack Query**: Estado del SERVIDOR (productos, pedidos, datos remotos)

---

## Modelo de Datos

### Dominio 1 — Identidad y Acceso

| Entidad | Descripción |
|---------|-----------|
| Usuario | Datos del usuario, soft-delete |
| Rol | ADMIN, STOCK, PEDIDOS, CLIENT |
| UsuarioRol | Relación M2M entre usuario y rol |
| RefreshToken | Tokens de renovación revocables |
| DireccionEntrega | Direcciones del cliente |

### Dominio 2 — Catálogo

| Entidad | Descripción |
|---------|-----------|
| Categoria | Jerárquica con FK autoreferencial (padre_id) |
| Producto | Catalogo con precio, stock, disponible |
| Ingrediente | Con flag es_alergeno |
| ProductoCategoria | Relación M2M |
| ProductoIngrediente | Relación M2M |

### Dominio 3 — Ventas

| Entidad | Descripción |
|---------|-----------|
| Pedido | Con snapshots de precio y dirección |
| DetallePedido | Líneas del pedido con personalización (INTEGER[]) |
| HistorialEstadoPedido | Audit trail append-only |
| Pago | Integración MercadoPago |
| EstadoPedido | Catálogo: PENDIENTE, CONFIRMADO, EN_PREPARACION, EN_CAMINO, ENTREGADO, CANCELADO |
| FormaPago | MERCADOPAGO, EFECTIVO |

---

## Máquina de Estados del Pedido

```
┌────────────┐     ┌────────────┐     ┌────────────┐     ┌──────────┐
│ PENDIENTE │────▶│ CONFIRMADO │────▶│EN_PREPARA│────▶│EN_CAMINO│
└────────────┘     └────────────┘     └────────────┘     └──────────┘
       │                   │                   │                   │
       │                   │                   │              ┌──┴──┐
       ▼                   ▼                   ▼              ▼     │
│  CANCELADO ◀──────── CANCELADO ◀────── CANCELADO ─────▶ ENTREGADO │
└────────────┘     └────────────┘     └────────────┘     └──────────┘
```

| Estado | Descripción | Transiciones válidas |
|--------|------------|----------------------|
| PENDIENTE | Creado, esperando pago | → CONFIRMADO, → CANCELADO |
| CONFIRMADO | Pago aprobado | → EN_PREPARACION, → CANCELADO |
| EN_PREPARACION | En cocina | → EN_CAMINO, → CANCELADO (solo ADMIN) |
| EN_CAMINO | Despachado | → ENTREGADO |
| ENTREGADO | Entregado (terminal) | — |
| CANCELADO | Cancelado (terminal) | — |

**Reglas clave**:
- RN-FS01: Solo el siguiente estado en la secuencia
- RN-FS02: PENDIENTE → CONFIRMADO es AUTOMÁTICO (webhook MP)
- RN-FS03: Al confirmar, decrementar stock atómicamente
- RN-FS04: Si decremento falla, rollback completo
- RN-FS05: Al cancelar confirmado, restaurar stock
- RN-FS06: ENTREGADO y CANCELADO son terminales

---

## Autenticación y Autorización

### Flujo JWT

1. **Login** → access token (30 min) + refresh token (7 días)
2. **Access token** → header `Authorization: Bearer <token>`
3. **Refresh** → rota el token, invalidate anterior
4. **Logout** → marca refresh token como revocado en BD

### Roles y Permisos (RBAC)

| Rol | Permisos |
|-----|---------|
| ADMIN | Completo: usuarios, catálogo, pedidos, métricas, config |
| STOCK | Catálogo: productos, categorías, ingredientes, stock |
| PEDIDOS | Pedidos: ver todos, avanzar estados, cancelar (no EN_PREPARACION) |
| CLIENT | Propios: catálogo, carrito, pedidos, direcciones, perfil |

### Rate Limiting

- Login: máximo 5 intentos por IP en 15 minutos
- respuesta: HTTP 429 con header `Retry-After`

---

## Convenciones de Código

### Backend

| Convención | Padrón |
|-----------|--------|
| Archivos | snake_case: `productos.py`, `unit_of_work.py` |
| Clases | PascalCase: `class ProductoService`, `class BaseRepository` |
| Funciones | snake_case: `def get_by_id`, `def create_product` |
| Modelos SQLModel | PascalCase con suffijo modelo: `ProductoModel` |
| Schemas Pydantic | PascalCase con suffijo Request/Response: `ProductoCreate`, `ProductoRead` |
| Rutas API | prefijo `/api/v1`, plural: `/productos`, `/pedidos` |
| HTTP verbs | GET (listar), GET /{id} (detalle), POST (crear), PUT (actualizar), PATCH (parcial), DELETE (borrar) |
| Códigos HTTP | 200 OK, 201 Created, 204 No Content, 400 Bad Request, 401 Unauthorized, 403 Forbidden, 404 Not Found, 422 Unprocessable, 429 Too Many, 500 Error |

### Frontend

| Convención | Padrón |
|-----------|--------|
| Archivos | kebab-case: `product-card.tsx`, `api-client.ts` |
| Componentes | PascalCase: `ProductoCard`, `CartSummary` |
| Hooks | camelCase con prefijo use: `useProductos`, `useAuth` |
| Stores Zustand | camelCase: `authStore`, `cartStore` |
| Rutas | kebab-case: `/productos`, `/mi-carrito` |
| Estilos Tailwind | utility classes en el markup |

### Git

- Commits: [Conventional Commits](https://conventionalcommits.org)
- Estructura: `tipo(modulo): descripción`
- Tipos: `feat`, `fix`, `docs`, `style`, `refactor`, `test`, `chore`, `perf`, `ci`

---

## Estructura de Archivos

### Backend (feature-first)

```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py                    # FastAPI app entry point
│   ├── core/
│   │   ├── config.py             # Environment variables
│   │   ├── database.py         # SQLAlchemy engine
│   │   ├── security.py        # Hashing, JWT
│   │   ├── errors.py        # Custom exceptions
│   │   └── unit_of_work.py  # Unit of Work
│   ├── modules/
│   │   ├── auth/            # Login, registro, refresh, logout
│   │   ├── usuarios/         # CRUD usuarios
│   │   ├── direcciones/      # Direcciones del cliente
│   │   ├── categorias/       # Categorías jerárquicas
│   │   ├── productos/       # Catálogo
│   │   ├── ingredientes/    # Ingredientes con alérgenos
│   │   ├── pedidos/         # Pedidos + FSM
│   │   ├── pagos/          # MercadoPago
│   │   └── admin/          # Métricas y gestión
│   └── db/
│       ├── models.py        # Todos los modelos SQLModel
│       ├── schemas.py       # Todos los schemas Pydantic
│       └── seed.py        # Datos iniciales
├── alembic/
│   └── versions/           # Migraciones
├── requirements.txt
├── .env.example
└──.env                   # NO commiteado
```

### Frontend (FSD)

```
frontend/
├── src/
│   ├── app/
│   │   ├── App.tsx           # Root component
│   │   ├── router.tsx        # Routes
│   │   └── providers.tsx      # Query, form providers
│   ├── pages/
│   │   ├── CatalogoPage.tsx
│   │   ├── CarritoPage.tsx
│   │   ├── CheckoutPage.tsx
│   │   ├── MisPedidosPage.tsx
│   │   ├── AdminDashboardPage.tsx
│   │   └── ...
│   ├── features/
│   │   ├── auth/           # Login, registro
│   │   ├── catalogo/       # Listado, detalle producto
│   │   ├── carrito/       # Gestión del carrito
│   │   ├──Checkout/      # Proceso de pago
│   │   ├── pedidos/       # Lista, detalle, FSM
│   │   └── admin/        # Dashboard, CRUDs
│   ├── entities/
│   │   ├── producto/     # Tipo + API
│   │   ├── pedido/       # Tipo + API
│   │   └── ...
│   ├── shared/
│   │   ├── api/         # Axios instance
│   │   ├── components/  # UI genéricos
│   │   ├── stores/      # Zustand stores
│   │   └── utils/      # Utilidades
│   ├── hooks/
│   │   └── ...
│   └── types/
│       └── ...
├── index.html
├── package.json
├── vite.config.ts
├── tailwind.config.js
├── tsconfig.json
└── .env.example
```

---

## Workflow SDD

### Hoja de ruta

Antes de proponer cualquier change, consultá **`docs/CHANGES.md`** — contiene el mapa completo de épicas con versiones, dependencias y el orden de implementación. Cada épica tiene una palabra clave para usar con `/opsx:propose`.

### Comandos SDD en este proyecto

```bash
# Ver estado actual
openspec list --json
openspec status --change <nombre> --json

# Workflow completo
/opsx:propose <nombre-del-change>  # Crear proposal + design + tasks
/opsx:apply <nombre-del-change>    # Implementar tareas
/opsx:archive <nombre-del-change>   # Sincronizar specs + archivar
```

### Artefactos del Change

```
openspec/changes/<nombre>/
├── proposal.md   # QUÉ se va a construir y POR QUÉ
├── design.md     # CÓMO técnicamente
├── tasks.md      # CHECKLIST de implementación
└── specs/       # Specs delta (opcional)
```

### Specs del Sistema

```
openspec/specs/<capability>/
└── spec.md      # Specificación completa
```

### Reglas SDD

1. **Nunca implementar sin proposal y design aprobados**
2. **El orden importa**: A archivado antes de proponer B
3. **Un change = un commit** (o varios atómicos)
4. **Specs son código**: Versionar en git

---

## Reglas de Negocio Clave

### Autenticación

- RN-AU01: Contraseña hasheada con bcrypt (cost >= 10)
- RN-AU02: Access token 30 min, refresh 7 días
- RN-AU04: Rotación de refresh token al usar
- RN-AU08: No diferenciar "email no existe" de "contraseña incorrecta"

### Catálogo

- RN-CA01: Categorías jerárquicas con CTE recursivo
- RN-CA02: No permitir ciclos en jerarquía
- RN-CA03: No eliminar categoría con productos activos
- RN-CA05: Stock >= 0, nunca negativo

### Pedidos

- RN-PE01: Creación ATÓMICA (Unit of Work)
- RN-PE02: Snapshot de precios al crear
- RN-PE03: Snapshot de dirección al crear
- RN-PE04: Validar stock DENTRO de la transacción

### Pagos

- RN-PA01: Tokenización en browser (PCI DSS SAQ-A)
- RN-PA02: Idempotency key para evitar cobros duplicados
- RN-PA05: Pago approved → transición automática PENDIENTE → CONFIRMADO

### Datos

- RN-DA01: Campos de auditoría (creado_en, actualizado_en)
- RN-DA06: Snapshots inmutables preservan historial
- RN-DA05: HistorialEstadoPedido append-only (nunca UPDATE/DELETE)

---

## Integración MercadoPago

### Flujo

```
1. Cliente → POST /api/v1/pagos/crear (pedidoId)
2. Backend → Crea preferencia en MP, devuelve URL/checkout
3. Cliente → Completa pago en entorno MP
4. MP ejecuta webhook → POST /api/v1/pagos/webhook
5. Backend:
   - Si approved → Pedido PENDIENTE → CONFIRMADO (auto)
   - Restaura stock si cancela
```

### Webhook

- Endpoint público (valida firma)
- Responde 200 inmediatamente
- Procesa idempotentemente
- Registra en tabla Pago

### Tarjetas Sandbox

| Número | Red | Resultado | CVV | Vencimiento |
|--------|-----|----------|-----|-------------|
| 4509 9535 6623 3704 | Visa | Aprobado | 123 | 11/25 |
| 3714 496353 98431 | Amex | Aprobado | 1234 | 11/25 |
| 4000 0000 0000 0002 | Visa | Rechazado | 123 | 11/25 |

---

## Gemas del Proyecto

### Gemas arsitektur

1. **Unit of Work**: Transacciones atómicas garantizadas
2. **Snapshot pattern**: Inmutabilidad de pedidos históricos
3. **FSM estricto**: Transiciones validadas, sin estados inválidos
4. **Append-only audit**: Trazabilidad completa
5. **Separación Zustand/TanStack Query**: Estado limpio

### Gemas de implementation

1. **Feature-first Backend**: Módulos autocontenidos
2. **FSD Frontend**: Límites de importación claros
3. **Interceptores JWT**: Auth transparente
4. **TanStack Query**: Fetch declarativo con caché

### Gemas de UX

1. **Persistencia localStorage**: Carrito sobrevive al close
2. **Refresh automático**: Token expirado no corta sesión
3. **Feedback visual**: Confirmaciones claras en cada paso
4. **Perfill por rol**: Menú adaptado al usuario

---

## Errores Frecuentes (evitar)

| Error | Por qué es un problema |
|-------|---------------------|
| Login que diferencia "email no existe" | Información que revela cuentas válidas |
| Guardar precios sin snapshots | Cambios afectan pedidos históricos |
| Stock decrement fuera de транзакции | Race conditions, inventario inconsistente |
| HistorialEstadoPedido con UPDATE | Pierde auditoría |
| Tokens en localStorage (sin httpOnly) | XSS expone credenciales |
| Mezclar Zustand con TanStack Query | Duplicación y desincronización de estado |
| Queries concatenadas (no parametrizadas) | SQL injection |
| Commits masivos | Imposible de revisar, revertir |
| Implementar sin proposal | Sin trazabilidad, sin diseño |

---

## Variables de Entorno

### Backend (.env)

```bash
DATABASE_URL=postgresql://user:pass@localhost:5432/foodstore_db
SECRET_KEY=your-secret-key-min-32-chars
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7
CORS_ORIGINS=["http://localhost:5173"]
MP_ACCESS_TOKEN=TEST-xxxx
MP_NOTIFICATION_URL=https://dominio.com/api/v1/pagos/webhook
```

### Frontend (.env)

```bash
VITE_API_BASE_URL=http://localhost:8000/api/v1
VITE_MP_PUBLIC_KEY=TEST-xxxx
```

---

## Recursos

- FastAPI: https://fastapi.tiangolo.com
- SQLModel: https://sqlmodel.tiangolo.com
- TanStack Query: https://tanstack.com/query
- Zustand: https://zustand-demo.pmnd.rs
- Tailwind: https://tailwindcss.com
- MercadoPago: https://www.mercadopago.com.ar/developers

---

## Glosario

| Término | Significado |
|---------|-------------|
| change | Unidad mínima de trabajo en SDD |
| UoW | Unit of Work — transacción atómica |
| soft delete | Borrado lógico (campo deleted_at) |
| snapshot | Copia inmutable de datos al crear |
| append-only | Solo INSERT, nunca UPDATE/DELETE |
| FSM | Finite State Machine |
| CTE | Common Table Expression (recursiva) |
| RBAC | Role-Based Access Control |
| PCI SAQ-A | Estándar de seguridad para tarjetas |
| IPN | Instant Payment Notification |

<!-- jr-stack:sdd-agent-delegation -->
## SDD Multi-Agent Delegation System

### 13.1 Principio Fundamental — PERMANENTE

Para TODA tarea, sin excepción, el orchestrator DEBE delegar trabajo sustantivo a subagentes internos. El orchestrator NUNCA ejecuta implementación, diseño, exploración, revisión, debugging, tareas frontend, ni ningún otro trabajo sustantivo por su cuenta. Su único rol es:

1. **Analizar** el request del usuario
2. **Coordinar** qué subagente ejecuta cada paso
3. **Validar** consistencia final entre lo delegado y lo esperado

La delegación no es opcional — es el mecanismo único y obligatorio para:

- Mantener contexto enfocado y evitar contaminación de tokens
- Garantizar revisión crítica antes de dar por terminado un cambio
- Separar concerns arquitectónicos, de implementación y de revisión
- Optimizar el uso de recursos en cada sub-tarea

**Este principio es permanente y absoluto.** Independientemente del AI orchestrator (BigPickle hoy, GitHub Copilot mañana), la delegación a subagentes siempre aplica. No existen tareas "chicas", "simples" o "triviales" que el orchestrator pueda hacer solo. Si el trabajo implica leer, escribir, analizar o modificar código, DELEGA.

---

### 13.2 Workflow de Delegación — PERMANENTE

Para TODA tarea, el orchestrator sigue esta secuencia:

```
 1. Orchestrator analiza el request
       │
 2. Architect valida arquitectura internamente
       │
 3. Orchestrator coordina planificación
       │
 4. Implementación especializada
       │
 5. Especialista Frontend refina UI (si aplica)
       │
 6. Reviewer inspecciona críticamente
       │
 7. Orchestrator valida consistencia final
```

Cada paso se ejecuta con las herramientas disponibles en el entorno (`task`, `delegate`, `skill`, etc.). Lo importante es la **secuencia**, no el mecanismo específico.

Los pasos 2, 4, 5 y 6 son SIEMPRE ejecutados por subagentes. El orchestrator NUNCA los ejecuta directamente.

---

### 13.3 Subagentes Actuales — TEMPORAL

> ⚠️ **Implementación actual**. Cuando el orchestrator migre a GitHub Copilot, estos subagentes se reemplazan. El patrón de delegación (13.1 y 13.2) persiste.

| Subagente | Rol | Propósito | Uso Obligatorio |
|-----------|-----|-----------|-----------------|
| **BigPickle** | SDD Orchestrator | Coordinación, workflow, token optimization, validación de consistencia | Siempre — entry point de todo request |
| **Nemotron 3 Super** | Architect | Análisis arquitectónico, validación de dependencias, planificación, escalabilidad | Siempre — antes de cualquier implementación o cambio arquitectónico |
| **DeepSeek** | Reviewer & Debug | Bug detection, edge cases, lógica, seguridad, maintainabilidad | Siempre — después de toda implementación, modificación de negocio, o debugging |
| **Hy3 Preview** | Frontend/UI | UI consistency, UX improvements, responsive layouts, estilos | Siempre — en TODA tarea frontend, modificación UI, estilos, o mejora UX |

#### Tool Mapping

| Subagente | Herramienta Real |
|-----------|-----------------|
| Nemotron 3 Super | `task(explore)`, `delegate` |
| DeepSeek | `task(general)`, `delegate` |
| Hy3 Preview | `delegate`, `skill` |

---

### 13.4 Reglas de Optimización de Tokens — PERMANENTE

- Dividir operaciones complejas en subtareas más pequeñas y delegables
- Evitar reescribir archivos completos sin necesidad — preferir ediciones quirúrgicas (diff-style)
- Delegar trabajo exploratorio a subagentes para reducir contaminación de contexto principal
- Reutilizar estructuras y patrones existentes del repositorio
- Priorizar outputs concisos y mantenibles
- **Nunca ejecutar trabajo sustantivo directamente** — si la tarea implica leer, escribir, analizar o modificar código, delegar siempre

---

### 13.5 Integración con OPSX — PERMANENTE

El sistema de delegación opera DENTRO del workflow OPSX existente. Los comandos que usa el desarrollador no cambian:

```
/opsx:explore  →  Architect (análisis arquitectónico)
/opsx:propose  →  Orchestrator + Architect (validación)
/opsx:apply    →  Orchestrator → Implementación → Hy3 (UI) → DeepSeek (review)
/opsx:archive  →  Orchestrator (consistencia)
```

El sistema de delegación es OBLIGATORIO — el orchestrator nunca ejecuta trabajo sustantivo por su cuenta. El orchestrator aplica automáticamente este sistema en cada interacción.

---

*Este archivo se regenera automáticamente desde docs/ cuando cambia la especificación.*