# Tasks — change-setup-project-structure

> Total: 40 tareas

## 1. Backend — Project Scaffold & Configuration

- [x] 1.1 Crear estructura de directorios: `app/`, `app/__init__.py`, `app/core/`, `app/modules/`, `app/db/`
- [x] 1.2 Crear `app/main.py` con FastAPI app, CORS middleware, health check `GET /`
- [x] 1.3 Crear `app/core/__init__.py` y `app/core/config.py` con Pydantic Settings (.env)
- [x] 1.4 Crear `app/core/database.py` con SQLModel engine y `get_session` dependency
- [x] 1.5 Crear `requirements.txt` con todas las dependencias
- [x] 1.6 Crear `pyproject.toml` con metadata y Python >=3.11

## 2. Backend — Core Utilities

- [x] 2.1 Crear `app/core/security.py` con JWT (HS256) y bcrypt hashing (cost >= 10)
- [x] 2.2 Crear `app/core/errors.py` con excepciones custom
- [x] 2.3 Crear `app/core/unit_of_work.py` con UnitOfWork genérico

## 3. Backend — Database & Migrations

- [x] 3.1 Crear `app/db/__init__.py` y `app/db/models.py` (Usuario, Rol, UsuarioRol con soft-delete)
- [x] 3.2 Crear `app/db/schemas.py` con schemas Pydantic
- [x] 3.3 Crear `app/db/seed.py` con roles default y admin user
- [x] 3.4 Inicializar Alembic y configurar `env.py` para SQLModel metadata
- [x] 3.5 Generar migración inicial con `alembic revision --autogenerate`
- [x] 3.6 Crear `.env` con valores por defecto para desarrollo

## 4. Backend — Repository Pattern

- [x] 4.1 Crear `app/db/repository.py` con `BaseRepository[T]` genérico

## 5. Frontend — Project Scaffold & Configuration

- [x] 5.1 Crear `package.json` con todas las dependencias del frontend
- [x] 5.2 Instalar dependencias npm (`npm install`)
- [x] 5.3 Crear estructura FSD: `src/app/`, `src/pages/`, `src/features/`, `src/entities/`, `src/shared/`, `src/hooks/`
- [x] 5.4 Configurar `tsconfig.json` con strict mode, `@/` path alias a `src/`
- [x] 5.5 Configurar `vite.config.ts` con alias `@/` y proxy `/api` a backend
- [x] 5.6 Instalar y configurar Tailwind CSS (`tailwind.config.js` + `postcss.config.js`)
- [x] 5.7 Crear `src/index.css` con directivas Tailwind
- [x] 5.8 Configurar ESLint con TypeScript y React recommended rulesets
- [x] 5.9 Configurar Prettier (`.prettierrc`)
- [x] 5.10 Crear `index.html` entry point con `<div id="root">`
- [x] 5.11 Crear `.env` con `VITE_API_BASE_URL` y `VITE_MP_PUBLIC_KEY`

## 6. Frontend — Core Infrastructure

- [x] 6.1 Crear `src/shared/api/client.ts` con Axios instance preconfigurada
- [x] 6.2 Agregar request interceptor JWT (`Authorization: Bearer <token>`)
- [x] 6.3 Agregar response interceptor 401 → token refresh flow
- [x] 6.4 Crear `src/shared/stores/authStore.ts` con Zustand (token, user, login/logout)
- [x] 6.5 Crear `src/shared/stores/cartStore.ts` con Zustand + localStorage persist
- [x] 6.6 Crear `src/app/providers.tsx` con QueryClientProvider
- [x] 6.7 Crear `src/app/router.tsx` con React Router (/, /productos, /carrito, etc.)
- [x] 6.8 Crear `src/app/App.tsx` componiendo providers + router
- [x] 6.9 Crear `src/main.tsx` entry point con StrictMode

## 7. DevOps & Developer Experience

- [x] 7.1 Crear `docker-compose.yml` con PostgreSQL 15 + Adminer
- [x] 7.2 Verificar backend: `uvicorn app.main:app --reload` sin errores de import
- [x] 7.3 Verificar frontend: `npm run dev` sin errores de compilación
- [x] 7.4 Crear `.gitignore` para backend y frontend
