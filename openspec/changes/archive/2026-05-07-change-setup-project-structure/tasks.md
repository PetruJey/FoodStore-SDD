## 1. Backend — Project Scaffold & Configuration

- [ ] 1.1 Create backend directory structure: `app/`, `app/__init__.py`, `app/core/`, `app/modules/`, `app/db/`
- [ ] 1.2 Create `app/main.py` with FastAPI app initialization, CORS middleware, and health check endpoint
- [ ] 1.3 Create `app/core/__init__.py` and `app/core/config.py` with Pydantic Settings reading from `.env`
- [ ] 1.4 Create `app/core/database.py` with SQLModel engine creation from `DATABASE_URL`
- [ ] 1.5 Create `requirements.txt` with all dependencies: fastapi, sqlmodel, alembic, passlib[bcrypt], python-jose, python-multipart, slowapi, pydantic-settings, psycopg2-binary, uvicorn, mercadopago
- [ ] 1.6 Create `pyproject.toml` with project metadata and Python version constraints

## 2. Backend — Core Utilities

- [ ] 2.1 Create `app/core/security.py` with JWT creation/verification (HS256) and bcrypt password hashing
- [ ] 2.2 Create `app/core/errors.py` with custom exception classes (NotFoundError, ConflictError, UnauthorizedError, etc.)
- [ ] 2.3 Create `app/core/unit_of_work.py` with generic UnitOfWork class providing transaction-scoped sessions and repository access
- [ ] 2.4 Create `app/core/__init__.py` aggregating core exports (if needed)

## 3. Backend — Database & Migrations

- [ ] 3.1 Create `app/db/models.py` with initial SQLModel models: Usuario, Rol, UsuarioRol (M2M)
- [ ] 3.2 Create `app/db/schemas.py` with Pydantic schemas for initial models (UsuarioCreate, UsuarioRead, etc.)
- [ ] 3.3 Create `app/db/seed.py` with initial seed data (admin user, default roles)
- [ ] 3.4 Initialize Alembic with `alembic init alembic` and configure `env.py` to use SQLModel metadata
- [ ] 3.5 Generate initial Alembic migration for Usuario, Rol, UsuarioRol tables
- [ ] 3.6 Create `.env` from `.env.example` with default development values

## 4. Backend — Repository Pattern

- [ ] 4.1 Create `app/db/repository.py` with generic `BaseRepository[T]` class (get_by_id, list, create, update, delete)
- [ ] 4.2 Verify BaseRepository supports soft-delete pattern (`deleted_at` field)

## 5. Frontend — Project Scaffold & Configuration

- [ ] 5.1 Initialize Vite + React + TypeScript project in `frontend/`
- [ ] 5.2 Create FSD directory structure: `src/app/`, `src/pages/`, `src/features/`, `src/entities/`, `src/shared/`, `src/hooks/`
- [ ] 5.3 Configure `tsconfig.json` with `strict: true` and `@/` path alias to `src/`
- [ ] 5.4 Configure `vite.config.ts` with `@/` path alias resolve and API proxy for development
- [ ] 5.5 Install and configure Tailwind CSS with `tailwind.config.js` and PostCSS
- [ ] 5.6 Create `src/index.css` with Tailwind directives (`@tailwind base`, `@tailwind components`, `@tailwind utilities`)
- [ ] 5.7 Configure ESLint with TypeScript and React rules
- [ ] 5.8 Configure Prettier for consistent code formatting

## 6. Frontend — Core Infrastructure

- [ ] 6.1 Create `src/shared/api/` with preconfigured Axios instance reading `VITE_API_URL`
- [ ] 6.2 Add Axios request interceptor for JWT `Authorization` header
- [ ] 6.3 Add Axios response interceptor for automatic 401 → token refresh flow
- [ ] 6.4 Create `src/shared/stores/authStore.ts` with Zustand: token, user data, login/logout actions
- [ ] 6.5 Create `src/shared/stores/cartStore.ts` with Zustand: items, add/remove/update, total, localStorage persist
- [ ] 6.6 Create `src/app/providers.tsx` with QueryClientProvider (TanStack Query) configured with sensible defaults
- [ ] 6.7 Create `src/app/router.tsx` with React Router routes (home, productos, carrito, checkout, login, register, admin)
- [ ] 6.8 Create `src/app/App.tsx` composing providers and router
- [ ] 6.9 Create `src/main.tsx` as entry point rendering App

## 7. DevOps & Developer Experience

- [ ] 7.1 Create `docker-compose.yml` with PostgreSQL 15 service (port 5432, volume for data)
- [ ] 7.2 Verify backend starts with `uvicorn app.main:app --reload` without import errors
- [ ] 7.3 Verify frontend starts with `npm run dev` without compilation errors
- [ ] 7.4 Create `.gitignore` entries for both projects (node_modules, __pycache__, .venv, .env, dist)
