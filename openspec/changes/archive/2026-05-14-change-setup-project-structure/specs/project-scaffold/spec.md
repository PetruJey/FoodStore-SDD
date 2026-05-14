## ADDED Requirements

### Requirement: Monorepo root structure
The system SHALL have /backend and /frontend directories at the root

#### Scenario: Root directories exist
- **WHEN** the repository is cloned
- **THEN** `/backend` and `/frontend` directories SHALL exist at the repository root

### Requirement: Backend feature-first modules
The system SHALL have /backend with modules: auth/, usuarios/, productos/, categorias/, ingredientes/, pedidos/, pagos/, direcciones/, admin/, refreshtokens/ — each with model.py, schemas.py, repository.py, service.py, router.py

#### Scenario: Backend module structure
- **WHEN** inspecting `/backend`
- **THEN** each module directory SHALL contain `model.py`, `schemas.py`, `repository.py`, `service.py`, and `router.py`

### Requirement: Frontend FSD structure
The system SHALL have /frontend following FSD: app/, pages/, widgets/, features/, entities/, shared/

#### Scenario: Frontend FSD layers
- **WHEN** inspecting `/frontend/src`
- **THEN** the directory SHALL contain `app/`, `pages/`, `widgets/`, `features/`, `entities/`, and `shared/` directories following Feature-Sliced Design conventions

### Requirement: Gitignore
The system SHALL have .gitignore excluding .env, __pycache__/, node_modules/, .venv/, *.pyc, dist/, .DS_Store

#### Scenario: Gitignore excludes artifacts
- **WHEN** running `git status`
- **THEN** `.env`, `__pycache__/`, `node_modules/`, `.venv/`, `*.pyc`, `dist/`, and `.DS_Store` SHALL NOT appear as untracked files

### Requirement: Docker Compose
The system SHALL have docker-compose.yml with PostgreSQL service

#### Scenario: Docker Compose PostgreSQL
- **WHEN** running `docker-compose up -d`
- **THEN** a PostgreSQL container SHALL start and be accessible on the configured port

### Requirement: README
The system SHALL have README.md with setup instructions

#### Scenario: README exists
- **WHEN** opening the project
- **THEN** `README.md` SHALL exist with instructions for backend and frontend setup

### Requirement: Backend module __init__.py
Each module in backend SHALL have __init__.py

#### Scenario: Init files exist
- **WHEN** inspecting each backend module
- **THEN** every module directory SHALL contain an `__init__.py` file
