## Context

El proyecto Food Store está completamente especificado (docs/, AGENTS.md) pero sin implementación. Los directorios `backend/` y `frontend/` están vacíos. Este diseño establece la infraestructura base para empezar a desarrollar las 77 historias de usuario.

La arquitectura target está definida en AGENTS.md:
- **Backend**: FastAPI + SQLModel + PostgreSQL, layers: Router → Service → UoW → Repository → Model
- **Frontend**: React + Vite + TypeScript, Feature-Sliced Design: pages → features → entities → shared

## Goals / Non-Goals

**Goals:**
- Proyecto backend funcional con FastAPI, estructura modular feature-first, conexión a BD
- Proyecto frontend funcional con React, Vite, TypeScript, estructura FSD
- Migraciones Alembic con schema inicial (Usuario, Rol, UsuarioRol)
- Docker Compose para PostgreSQL 15 + Adminer
- Seed data inicial para desarrollo (roles, admin user)
- Archivos de configuración del ecosistema (pyproject.toml, tsconfig, vite, tailwind, eslint, prettier)
- Cliente HTTP (Axios) preconfigurado con interceptores JWT y refresh automático
- Stores Zustand para carrito (con persistencia localStorage) y sesión
- TanStack Query Provider configurado con defaults sensibles
- Unit of Work pattern genérico para transacciones atómicas

**Non-Goals:**
- Implementación de lógica de negocio de features específicas (eso viene en changes posteriores tipo `epicXX-*`)
- Tests automatizados (se agregan cuando haya lógica que testear)
- CI/CD pipeline
- Deploy a producción
- Documentación de API más allá de la generada automáticamente por FastAPI

## Decisions

### 1. FastAPI con estructura feature-first (no flat)

- **Decisión**: Cada módulo de negocio (auth, productos, pedidos, etc.) es un subpaquete con sus propios routers, services y schemas.
- **Por qué**: Escala mejor que un solo archivo de routers. Cada feature es autocontenida y se puede desarrollar en paralelo por diferentes developers.
- **Alternativa considerada**: Estructura flat tipo "controllers/". Se descartó porque con ~8 módulos se vuelve inmanejable.

### 2. SQLModel como ORM único (no SQLAlchemy + Pydantic separados)

- **Decisión**: Usar SQLModel que unifica modelos de BD y schemas Pydantic en una sola clase.
- **Por qué**: Elimina la duplicación modelo/schema. Un cambio en el modelo se refleja automáticamente en los schemas Pydantic.
- **Riesgo**: SQLModel es más nuevo que SQLAlchemy. Mitigación: la versión 0.111+ ya es estable para producción. SQLAlchemy sigue siendo transitive dependency.

### 3. Feature-Sliced Design en frontend (no pages-first)

- **Decisión**: Estructura FSD con 4 capas: pages → features → entities → shared.
- **Por qué**: Separa claramente responsabilidades, evita importaciones circulares, escala a equipos grandes. Las capas tienen reglas de importación estrictas.
- **Alternativa considerada**: Estructura plana tipo `components/`, `pages/`, `hooks/`. Se descartó porque al crecer el proyecto se vuelve un caos de imports.

### 4. Unit of Work pattern desde el inicio

- **Decisión**: Implementar UoW genérico como capa de transacciones atómicas con `BaseRepository[T]`.
- **Por qué**: Es el patrón central del backend (RN-PE01 exige creación atómica de pedidos). Mejor tenerlo desde el día 1 que refactorizar después.
- **Implementación**: `UnitOfWork` context manager que provee repositorios y maneja commit/rollback automáticamente.

### 5. Zustand + TanStack Query (no Redux)

- **Decisión**: Zustand para estado del cliente, TanStack Query para estado del servidor.
- **Por qué**: Separación clara de concerns. TanStack Query maneja caché, refetch, loading states automáticamente. Zustand es liviano para carrito y UI local con persistencia a localStorage.
- **Alternativa considerada**: Redux Toolkit. Se descartó porque agrega boilerplate innecesario para este alcance.

### 6. Axios con interceptores JWT (no fetch API plano)

- **Decisión**: Axios como cliente HTTP con interceptores para JWT y refresh automático.
- **Por qué**: Los interceptores permiten adjuntar el token automáticamente y manejar 401 globalmente sin repetir lógica en cada request.

### 7. Docker Compose para PostgreSQL, no instalación nativa

- **Decisión**: `docker-compose.yml` con PostgreSQL 15 + Adminer opcional.
- **Por qué**: Entorno reproducible, evita "en mi máquina funciona", mismo para todo el equipo. Adminer útil para inspeccionar datos en desarrollo.

## Risks / Trade-offs

- **[Dependencias] Las versiones de packages pueden quedar obsoletas** → Usar rangos amplios en requirements.txt (ej. `fastapi>=0.111.0`) y `^` en package.json
- **[SQLModel] Al ser más nuevo, algunos edge cases pueden no estar cubiertos** → Tener SQLAlchemy como transitive dependency (ya viene con SQLModel) y conocer workarounds
- **[FSD] Developer Experience inicial más lenta** → La estructura requiere más archivos de boilerplate al empezar, pero el payoff es enorme cuando el proyecto escala a 77 US
- **[Windows compat] Scripts de setup en bash no funcionan en Windows nativo** → Documentar alternativas PowerShell o usar Docker
- **[Seed data] Datos hardcodeados pueden desactualizarse** → Mantener seed actualizado con los modelos; considerar migraciones de datos si crece

## Migration Plan

Este es el cambio inicial de implementación del proyecto. No hay migración desde un estado anterior. Plan:

1. Crear toda la estructura de directorios de backend y frontend
2. Configurar dependencias y archivos de configuración
3. Crear modelos SQLModel iniciales y migración Alembic
4. Crear repositorio genérico y Unit of Work
5. Configurar Docker Compose
6. Inicializar proyecto frontend con Vite, instalar dependencias
7. Configurar Axios, Zustand stores, TanStack Query
8. Verificar que ambos proyectos levantan sin errores

Rollback: Git revert del commit.
