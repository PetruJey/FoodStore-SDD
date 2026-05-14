## Why

Este es el change fundacional de Food Store. Sin esta base no existe nada del sistema: necesitamos el scaffolding completo del monorepo con backend FastAPI (estructura feature-first), frontend React+Vite+TypeScript (Feature-Sliced Design), base de datos PostgreSQL con migraciones Alembic, y todos los patrones de infraestructura (BaseRepository, Unit of Work, JWT, stores Zustand, cliente HTTP) para que las 19 épicas restantes puedan construirse sobre una base sólida y consistente.

## What Changes

- Creación del monorepo con estructura `/backend` (feature-first) y `/frontend` (Feature-Sliced Design)
- Configuración del backend: FastAPI, SQLModel, Alembic, dependencias core, middleware CORS + rate limiting
- Configuración del frontend: React + TypeScript + Vite, Tailwind CSS, TanStack Query, Axios, Zustand
- Base de datos PostgreSQL con migraciones Alembic (autogenerate desde modelos SQLModel) y script de seed idempotente
- Patrones de infraestructura: `BaseRepository[T]` genérico, `UnitOfWork` como context manager asíncrono, dependencias FastAPI (`get_current_user`, `require_role`)
- Stores Zustand: `authStore`, `cartStore`, `paymentStore`, `uiStore` con persistencia y suscripción por slice
- Cliente HTTP Axios con interceptores de token JWT y refresh automático
- Manejo de errores estandarizado RFC 7807 con clases de error custom
- Routing base con react-router-dom (rutas públicas y privadas)
- Archivos de configuración: `.env.example`, `.gitignore`, `docker-compose.yml`
- Documentación: `README.md` raíz con instrucciones de setup

## Capabilities

### New Capabilities

- `project-scaffold`: Estructura del monorepo, carpetas backend (feature-first) y frontend (Feature-Sliced Design), `.gitignore`, `README.md`, `docker-compose.yml`
- `backend-core`: Configuración FastAPI, `config.py`, `database.py`, `security.py`, `main.py` con CORS + rate limiting + routers, `requirements.txt` / `pyproject.toml` con todas las dependencias
- `database-migrations`: Modelos SQLModel de todas las tablas del ERD, migraciones Alembic con autogenerate, script de seed idempotente (roles, estados, formas de pago, admin por defecto)
- `frontend-core`: Setup React + Vite + TypeScript + Tailwind, `tsconfig.json` strict, `vite.config.ts`, `index.html`, `App.tsx` con QueryClientProvider y RouterProvider
- `http-client`: Axios instance centralizada con interceptores de token JWT y refresh automático en 401
- `base-repository`: `BaseRepository[T]` genérico con CRUD, soft delete, paginación, filtros
- `unit-of-work`: `UnitOfWork` como context manager asíncrono con acceso a repositorios, commit/rollback automático
- `auth-infrastructure`: Funciones de security (hashing bcrypt, JWT), dependencias FastAPI (`get_current_user`, `require_role`)
- `error-handling`: Exception handlers RFC 7807, clases de error custom (`ValidationError`, `UnauthorizedError`, `ForbiddenError`, `NotFoundError`)
- `zustand-stores`: `authStore`, `cartStore`, `paymentStore`, `uiStore` con persistencia y acciones base

### Modified Capabilities

- *(Ninguna — es el change fundacional, no hay capacidades existentes)*

## Impact

- **Código nuevo**: Aproximadamente 40+ archivos nuevos entre backend y frontend
- **Dependencias nuevas**: FastAPI, SQLModel, Alembic, Passlib, python-jose, slowapi, uvicorn, mercadopago (backend) + React, Vite, TanStack Query, TanStack Form, Zustand, Axios, Tailwind, recharts (frontend)
- **Infraestructura**: PostgreSQL requerido (local o Docker), archivo `docker-compose.yml` para levantar BD
- **Breaking**: N/A — es la base del proyecto, no hay nada existente que romper
