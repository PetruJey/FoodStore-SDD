## Why

El proyecto Food Store está completamente especificado (docs/, AGENTS.md) con 77 historias de usuario, pero carece de la estructura de proyecto real para empezar a implementar. Los directorios `backend/` y `frontend/` están vacíos (solo `.gitkeep`). Sin infraestructura base no se puede codificar ni una sola US.

Este cambio sienta las bases para todo el desarrollo posterior — proyectos funcionales con dependencias, configuración de herramientas, estructura de directorios y pipeline de base de datos.

## What Changes

- Crear proyecto **FastAPI** completo en `backend/` con estructura feature-first modular
- Crear proyecto **React + Vite + TypeScript** en `frontend/` con estructura Feature-Sliced Design (FSD)
- Configurar **Alembic** para migraciones de base de datos PostgreSQL
- Crear modelos SQLModel iniciales (Usuario, Rol, UsuarioRol)
- Configurar `requirements.txt` con todas las dependencias del backend
- Configurar `package.json` con todas las dependencias del frontend
- Establecer archivos de configuración: `pyproject.toml`, `tsconfig.json`, `vite.config.ts`, `tailwind.config.js`
- Configurar Docker Compose para PostgreSQL local + Adminer
- Implementar Unit of Work pattern genérico
- Crear stores Zustand (auth, cart) con persistencia localStorage
- Configurar Axios con interceptores JWT y refresh automático
- Establecer TanStack Query Provider con defaults sensibles

## Capabilities

### New Capabilities
- `backend-setup`: Infraestructura base del backend FastAPI — estructura de directorios, dependencias, configuración de base de datos, Alembic, modelos iniciales, repositorio genérico, Unit of Work
- `frontend-setup`: Infraestructura base del frontend React — Vite, TypeScript, TanStack Query, Zustand, Tailwind CSS, estructura FSD, Axios con interceptores JWT

### Modified Capabilities
_(Ninguna — es el primer cambio de implementación del proyecto)_

## Impact

- **Backend**: Se crean `app/`, `app/core/`, `app/modules/`, `app/db/`, `alembic/`. Se agrega `requirements.txt`, `pyproject.toml`, Docker Compose.
- **Frontend**: Se crean `src/app/`, `src/pages/`, `src/features/`, `src/entities/`, `src/shared/`, `src/hooks/`. Se agrega `package.json`, configs de Vite, TypeScript, Tailwind, ESLint, Prettier.
- **Base de datos**: Schema inicial con migración Alembic + seed data (roles, admin user).
- **Dev UX**: Setup de Docker Compose para BD local + Adminer, scripts de inicio rápido documentados.
