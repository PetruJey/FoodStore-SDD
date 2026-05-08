## Context

El proyecto Food Store está completamente especificado (docs/, AGENTS.md) pero sin implementación. Los directorios `backend/` y `frontend/` están vacíos. Este diseño establece la infraestructura base para empezar a desarrollar historias de usuario reales.

La arquitectura target está definida en AGENTS.md:
- **Backend**: FastAPI + SQLModel + PostgreSQL, layers: Router → Service → UoW → Repository → Model
- **Frontend**: React + Vite + TypeScript, Feature-Sliced Design: pages → features → entities → shared

## Goals / Non-Goals

**Goals:**
- Proyecto backend funcional con FastAPI, estructura modular, conexión a BD
- Proyecto frontend funcional con React, Vite, TypeScript, estructura FSD
- Migraciones Alembic con schema inicial (Usuario, Rol, autenticación)
- Docker Compose para PostgreSQL + Adminer
- Seed data inicial para desarrollo
- Archivos de configuración del ecosistema (pyproject.toml, tsconfig, vite, tailwind, eslint)
- Cliente HTTP (Axios) preconfigurado con interceptores JWT
- Stores Zustand para carrito y sesión

**Non-Goals:**
- Implementación de lógica de negocio (features) — eso viene en changes posteriores
- Tests automatizados (se agregan cuando haya lógica que testear)
- CI/CD pipeline
- Deploy a producción
- Documentación de API más allá de la generada por FastAPI automáticamente

## Decisions

### 1. FastAPI con estructura feature-first (no flat)

- **Decisión**: Cada módulo de negocio (auth, productos, pedidos, etc.) es un subpaquete con sus propios routers, services y schemas.
- **Por qué**: Escala mejor que un solo archivo de routers. Cada feature es autocontenida y se puede desarrollar en paralelo.
- **Alternativa considerada**: Estructura flat tipo "controllers/". Se descartó porque con ~8 módulos se vuelve inmanejable.

### 2. SQLModel como ORM único (no SQLAlchemy + Pydantic separados)

- **Decisión**: Usar SQLModel que unifica modelos de BD y schemas Pydantic.
- **Por qué**: Elimina la duplicación modelo/schema. Un cambio en el modelo se refleja automáticamente en los schemas.
- **Riesgo**: SQLModel es más nuevo que SQLAlchemy. Mitigación: la versión 0.111+ ya es estable para producción.

### 3. Feature-Sliced Design en frontend (no pages-first)

- **Decisión**: Estructura FSD con 4 capas: pages → features → entities → shared.
- **Por qué**: Separa claramente responsabilidades, evita importaciones circulares, escala a equipos grandes.
- **Alternativa considerada**: Estructura plana tipo `components/`, `pages/`, `hooks/`. Se descartó porque al crecer el proyecto se vuelve un caos de imports.

### 4. Unit of Work pattern desde el inicio

- **Decisión**: Implementar UoW genérico como capa de transacciones atómicas.
- **Por qué**: Es el patrón central del backend (RN-PE01 exige creación atómica de pedidos). Mejor tenerlo desde el día 1 que refactorizar después.

### 5. Zustand + TanStack Query (no Redux)

- **Decisión**: Zustand para estado del cliente, TanStack Query para estado del servidor.
- **Por qué**: Separación clara de concerns. TanStack Query maneja caché, refetch, loading states automáticamente. Zustand es liviano para carrito y UI local.

### 6. Docker Compose para PostgreSQL, no instalación nativa

- **Decisión**: docker-compose.yml con PostgreSQL 15 + Adminer opcional.
- **Por qué**: Entorno reproducible, evita "en mi máquina funciona", mismo para todo el equipo.

## Risks / Trade-offs

- **[Dependencias] Las versiones de packages pueden quedar obsoletas** → Usar rangos amplios en requirements.txt (ej. fastapi>=0.111.0) y package.json (^)
- **[SQLModel] Al ser más nuevo, algunos edge cases pueden no estar cubiertos** → Tener SQLAlchemy como transitive dependency (ya viene con SQLModel) y conocer las workarounds
- **[FSD] Developer Experience inicial más lenta** → La estructura requiere más archivos de boilerplate al empezar, pero el payoff es enorme cuando el proyecto escala
- **[Windows compat] Scripts de setup (bash) no funcionan en Windows nativo** → Documentar alternativas PowerShell o usar Docker

## Migration Plan

Este es el cambio inicial del proyecto, no hay migración desde un estado anterior. El plan es:

1. Crear toda la estructura de directorios de backend
2. Crear toda la estructura de directorios de frontend
3. Configurar dependencias y archivos de configuración
4. Crear modelos iniciales y migración Alembic
5. Configurar Docker Compose
6. Verificar que ambos proyectos levantan sin errores

Rollback: Git revert del commit.

## Open Questions

- ¿Usamos `uv` o `pip` para el manejo de dependencias Python? → Decisión inicial: pip + requirements.txt (más universal). Se puede migrar a uv después.
- ¿Prettier + ESLint o solo ESLint para frontend? → Ambos, ESLint para reglas, Prettier para formato.
