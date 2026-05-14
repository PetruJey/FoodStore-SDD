# Food Store — Repositorio Base

Sistema de e-commerce de productos alimenticios desarrollado con **Spec-Driven Development (SDD)** usando OPSX y OpenCode.

---

## Documentación del sistema

Antes de escribir una línea de código, leé la documentación modular desde `openspec/docs/index.md`:

| Archivo | Contenido |
|---------|-----------|
| `openspec/docs/index.md` | **Entry point** — índice completo de toda la documentación del sistema |
| `openspec/docs/descripcion/` | Visión general, actores del sistema, stack tecnológico y arquitectura |
| `openspec/docs/historias/` | Reglas de negocio, épicas e historias de usuario (US-000 a US-076) |
| `openspec/docs/integrador/` | Especificación técnica: API REST, schemas, UoW, MercadoPago, etc. |
| `docs/CHANGES.md` | **Mapa de épicas** — sprints, versiones y orden de implementación |

> **Navegación rápida**: `openspec/docs/index.md` es el mapa de toda la documentación. `docs/CHANGES.md` es el mapa de implementación con el orden exacto de cada épica. Los archivos fuente originales están en `docs/`, pero siempre usá `openspec/docs/index.md` como entry point de documentación.

---

## Stack tecnológico

**Backend**: FastAPI · SQLModel · PostgreSQL · Alembic · bcrypt · python-jose · slowapi · MercadoPago SDK  
**Frontend**: React · TypeScript · Vite · TanStack Query · TanStack Form · Zustand · Axios · Tailwind CSS · Recharts

---

## Setup del entorno de desarrollo

### Requisitos previos
- Python 3.11+
- Node.js 18+
- PostgreSQL 15+
- OpenCode: agente orquestador (OpenCode / Cursor / GitHub Copilot)
- OpenSpec CLI: `npm install -g @fission-ai/openspec`

### 1. Clonar e inicializar

```bash
git clone <url-del-repo> food-store
cd food-store
```

### 2. Inicializar OpenSpec

```bash
npx @fission-ai/openspec@latest init
```

Esto genera la carpeta `openspec/` donde van a vivir todos los artefactos del proyecto.

### 3. Backend

```bash
cd backend
cp .env.example .env
# Completar las variables de entorno en .env

python -m venv .venv
source .venv/bin/activate   # Linux/Mac
.venv\Scripts\activate      # Windows

pip install -r requirements.txt
alembic upgrade head
python -m app.db.seed
uvicorn app.main:app --reload
```

API disponible en `http://localhost:8000`  
Documentación Swagger en `http://localhost:8000/docs`

### 4. Frontend

```bash
cd frontend
cp .env.example .env
# Completar VITE_API_URL=http://localhost:8000

npm install
npm run dev
```

App disponible en `http://localhost:5173`

---

## Flujo de desarrollo con OPSX

Todo cambio al sistema sigue este ciclo:

```
/opsx:explore   →  pensar antes de comprometerse (opcional)
/opsx:propose   →  generar propuesta + diseño + tareas
/opsx:apply     →  implementar tarea por tarea
/opsx:archive   →  sincronizar specs y cerrar el change
```

### Orden de implementación

El orden detallado está en [`docs/CHANGES.md`](./docs/CHANGES.md). Cada épica tiene versión y palabra clave para `/opsx:propose`:

```
Sprint 0 — Infraestructura y Setup       → v0.1  (completado ✅)
Sprint 1 — Autenticación, Autorización y Navegación    → v1.0 ✅, v1.1 a v1.2
Sprint 2 — Catálogo: Categ. e Ingred.    → v2.0  a v2.1
Sprint 3 — Productos y Perfil            → v3.0  a v3.1
Sprint 4 — Carrito y Direcciones         → v4.0  a v4.1
Sprint 5 — Creación de Pedidos           → v5.0  a v5.1
Sprint 6 — Pagos y FSM de Pedidos        → v6.0  a v6.1
Sprint 7 — Visualización y Feedback      → v7.0  a v7.1
Sprint 8 — Administración                → v8.0  a v8.3
```

> Ver `docs/CHANGES.md` para el detalle completo de cada épica, sus dependencias y palabras clave.

---

## Variables de entorno

Crear `backend/.env` a partir de `backend/.env.example`:

```env
DATABASE_URL=postgresql://user:password@localhost:5432/foodstore
SECRET_KEY=tu-clave-secreta-de-32-caracteres-minimo
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7
MP_ACCESS_TOKEN=TEST-tu-token-de-mercadopago
CORS_ORIGINS=http://localhost:5173
```

Crear `frontend/.env` a partir de `frontend/.env.example`:

```env
VITE_API_URL=http://localhost:8000
VITE_MP_PUBLIC_KEY=TEST-tu-public-key-de-mercadopago
```

---

## Convenciones de commits

```
feat(modulo): descripción del cambio
fix(modulo): descripción del bug corregido
refactor(modulo): descripción del refactor
test(modulo): descripción de los tests
docs(modulo): descripción del cambio en docs
```
