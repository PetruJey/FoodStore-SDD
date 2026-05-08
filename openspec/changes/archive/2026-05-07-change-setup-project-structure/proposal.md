## Why

El proyecto Food Store existe como especificación (docs/, AGENTS.md, README.md) pero carece de la estructura de proyecto real. Backend y frontend son carpetas vacías con solo `.gitkeep`. Para poder empezar a implementar historias de usuario, necesitamos establecer la infraestructura base: proyectos funcionales con sus dependencias, configuración de herramientas, estructura de directorios y pipeline de base de datos.

Este cambio sienta las bases para todo el desarrollo posterior — sin esto, no se puede codificar ni una sola US.

## What Changes

- Crear proyecto **FastAPI** completo en `backend/` con estructura feature-first modular
- Crear proyecto **React + Vite + TypeScript** en `frontend/` con estructura Feature-Sliced Design
- Configurar **Alembic** para migraciones de base de datos PostgreSQL
- Crear modelos SQLModel iniciales (Usuario, Rol, etc.)
- Configurar `requirements.txt` con todas las dependencias del backend
- Configurar `package.json` con todas las dependencias del frontend
- Establecer archivos de configuración: `pyproject.toml`, `tsconfig.json`, `vite.config.ts`, `tailwind.config.js`
- Configurar Docker Compose para PostgreSQL local
- Pipeline de seed data inicial

## Capabilities

### New Capabilities
- `backend-setup`: Infraestructura base del backend FastAPI — estructura de directorios, dependencias, configuración de base de datos, Alembic, modelos iniciales
- `frontend-setup`: Infraestructura base del frontend React — Vite, TypeScript, TanStack Query, Zustand, Tailwind CSS, estructura FSD

### Modified Capabilities
_(Ninguna — es el primer cambio del proyecto)_

## Impact

- **Backend**: Se crean carpetas `app/`, `app/core/`, `app/modules/`, `app/db/`, `alembic/`. Se agrega `requirements.txt`, `pyproject.toml`, Docker Compose.
- **Frontend**: Se crean carpetas `src/app/`, `src/pages/`, `src/features/`, `src/entities/`, `src/shared/`. Se agrega `package.json`, configs de Vite, TypeScript, Tailwind.
- **Base de datos**: Schema inicial con migración Alembic + seed data.
- **Dev UX**: Setup de Docker Compose para BD local, scripts de inicio rápido.
