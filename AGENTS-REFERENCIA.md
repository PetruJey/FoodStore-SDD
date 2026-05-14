# AGENTS-REFERENCIA.md — Documentación de Referencia del Proyecto

> ⚡ Cargá este archivo on-demand cuando necesités detalles técnicos del stack, arquitectura, modelo de datos, FSM, etc.

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

## Máquina de Estados del Pedido (FSM)

```
┌────────────┐     ┌────────────┐     ┌──────────────┐     ┌──────────┐
│ PENDIENTE  │────▶│ CONFIRMADO │────▶│EN_PREPARACION│────▶│EN_CAMINO│
└────────────┘     └────────────┘     └──────────────┘     └──────────┘
       │                   │                   │                   │
       │                   │                   │              ┌───┴───┐
       ▼                   ▼                   ▼              ▼       │
  ┌──────────┐       ┌──────────┐       ┌──────────┐   ┌──────────┐  │
  │CANCELADO│◀───────│CANCELADO│◀───────│CANCELADO│───▶│ENTREGADO │  │
  └──────────┘       └──────────┘       └──────────┘   └──────────┘  │
                                                                      │
                                                                      ▼
                                                                (terminal)
```

| Estado | Descripción | Transiciones válidas |
|--------|------------|----------------------|
| PENDIENTE | Creado, esperando pago | → CONFIRMADO, → CANCELADO |
| CONFIRMADO | Pago aprobado | → EN_PREPARACION, → CANCELADO |
| EN_PREPARACION | En cocina | → EN_CAMINO, → CANCELADO (solo ADMIN) |
| EN_CAMINO | Despachado | → ENTREGADO |
| ENTREGADO | Entregado (terminal) | — |
| CANCELADO | Cancelado (terminal) | — |

**Reglas clave de la FSM**:
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
3. **Refresh** → rota el token, invalida anterior
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
- Respuesta: HTTP 429 con header `Retry-After`

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
│   │   ├── database.py           # SQLAlchemy engine
│   │   ├── security.py           # Hashing, JWT
│   │   ├── errors.py             # Custom exceptions
│   │   └── unit_of_work.py       # Unit of Work
│   ├── modules/
│   │   ├── auth/                 # Login, registro, refresh, logout
│   │   ├── usuarios/             # CRUD usuarios
│   │   ├── direcciones/          # Direcciones del cliente
│   │   ├── categorias/           # Categorías jerárquicas
│   │   ├── productos/            # Catálogo
│   │   ├── ingredientes/         # Ingredientes con alérgenos
│   │   ├── pedidos/              # Pedidos + FSM
│   │   ├── pagos/                # MercadoPago
│   │   └── admin/                # Métricas y gestión
│   └── db/
│       ├── models.py             # Todos los modelos SQLModel
│       ├── schemas.py            # Todos los schemas Pydantic
│       └── seed.py               # Datos iniciales
├── alembic/
│   └── versions/                 # Migraciones
├── requirements.txt
├── .env.example
└── .env                          # NO commiteado
```

### Frontend (FSD)

```
frontend/
├── src/
│   ├── app/
│   │   ├── App.tsx               # Root component
│   │   ├── router.tsx            # Routes
│   │   └── providers.tsx         # Query, form providers
│   ├── pages/
│   │   ├── CatalogoPage.tsx
│   │   ├── CarritoPage.tsx
│   │   ├── CheckoutPage.tsx
│   │   ├── MisPedidosPage.tsx
│   │   ├── AdminDashboardPage.tsx
│   │   └── ...
│   ├── features/
│   │   ├── auth/                 # Login, registro
│   │   ├── catalogo/             # Listado, detalle producto
│   │   ├── carrito/              # Gestión del carrito
│   │   ├── checkout/             # Proceso de pago
│   │   ├── pedidos/              # Lista, detalle, FSM
│   │   └── admin/                # Dashboard, CRUDs
│   ├── entities/
│   │   ├── producto/             # Tipo + API
│   │   ├── pedido/               # Tipo + API
│   │   └── ...
│   ├── shared/
│   │   ├── api/                  # Axios instance
│   │   ├── components/           # UI genéricos
│   │   ├── stores/               # Zustand stores
│   │   └── utils/                # Utilidades
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

### Gemas arquitectónicas

1. **Unit of Work**: Transacciones atómicas garantizadas
2. **Snapshot pattern**: Inmutabilidad de pedidos históricos
3. **FSM estricto**: Transiciones validadas, sin estados inválidos
4. **Append-only audit**: Trazabilidad completa
5. **Separación Zustand/TanStack Query**: Estado limpio

### Gemas de implementación

1. **Feature-first Backend**: Módulos autocontenidos
2. **FSD Frontend**: Límites de importación claros
3. **Interceptores JWT**: Auth transparente
4. **TanStack Query**: Fetch declarativo con caché

### Gemas de UX

1. **Persistencia localStorage**: Carrito sobrevive al cierre
2. **Refresh automático**: Token expirado no corta sesión
3. **Feedback visual**: Confirmaciones claras en cada paso
4. **Perfil por rol**: Menú adaptado al usuario

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
VITE_API_URL=http://localhost:8000
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

---

## Workflow OPSX (reemplaza SDD)

El sistema anterior de fases SDD (Spec-Driven Development con agentes BigPickle, Nemotron, DeepSeek, Hy3) fue reemplazado por **OPSX** — un workflow fluido basado en el CLI `openspec`.

El orchestrator (`big-pickle`) coordina todo el flujo usando los comandos `/opsx:explore`, `/opsx:propose`, `/opsx:apply`, `/opsx:archive`. Ya no hay fases rígidas ni asignación fija de modelos por fase — el orchestrator decide según el contexto.

Para más detalles, consultá las instrucciones del orchestrator en el system prompt del agente.
