# Food Store E-Commerce

Sistema de e-commerce para productos alimenticios con gestión de pedidos, pagos y administración.

## Stack

- **Backend**: Python + FastAPI + SQLModel + PostgreSQL
- **Frontend**: React + TypeScript + Vite + Tailwind CSS
- **Infra**: Docker Compose (PostgreSQL)

## Requisitos

- Python 3.11+
- Node.js 18+
- Docker Desktop (opcional, para BD local)

## Setup rápido

### 1. Base de datos

```bash
# Opción A: Con Docker
docker compose up -d

# Opción B: PostgreSQL local
# Crear BD: foodstore_db
```

### 2. Backend

```bash
cd backend
python -m venv .venv
.venv\Scripts\activate   # Windows
# source .venv/bin/activate  # Linux/Mac
pip install -r requirements.txt
cp .env.example .env     # Configurar variables
alembic upgrade head     # Migraciones
python -m app.db.seed    # Datos iniciales
uvicorn main:app --reload  # Servidor en :8000
```

### 3. Frontend

```bash
cd frontend
npm install
cp .env.example .env.local
npm run dev  # Servidor en :5173
```

## Documentación API

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Variables de entorno

Ver `.env.example` en `/backend` y `/frontend` para la lista completa.
