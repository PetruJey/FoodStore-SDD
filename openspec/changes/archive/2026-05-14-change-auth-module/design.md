## Context

El Sprint 0 dejó la infraestructura base: proyecto FastAPI con estructura feature-first, modelo `Usuario` con soft-delete, modelo `Rol` con los 4 roles (ADMIN, STOCK, PEDIDOS, CLIENT), utilidades JWT (creación y verificación de tokens, hashing bcrypt), y `RefreshToken` modelado también a nivel de BD. Sin embargo, no existen endpoints de autenticación, ni el flujo completo de registro/login/refresh/logout, ni el frontend asociado.

Este change implementa el módulo de autenticación completo que permite a los usuarios registrarse, iniciar sesión, mantener la sesión activa mediante refresh tokens y cerrar sesión.

## Goals / Non-Goals

**Goals:**
- Endpoints funcionales de register, login, refresh y logout en backend
- Rate limiting en login (5 intentos / 15 min por IP)
- Rotación de refresh tokens con detección de replay attack
- Auth store en frontend con persistencia y refresh automático vía interceptor Axios
- Páginas de login y registro en frontend
- Migración Alembic para la tabla `RefreshToken`

**Non-Goals:**
- Gestión de roles (RBAC) — se implementa en `change-rbac-module` (Sprint 1.1)
- Protección de rutas por rol — idem, va en RBAC
- Navegación adaptada al rol — va en `change-frontend-navigation`
- Recuperación de contraseña — no está en las historias actuales

## Decisions

### 1. Estructura del módulo auth en backend
Módulo autocontenido dentro de `backend/app/modules/auth/`:
```
auth/
├── __init__.py
├── router.py       # Endpoints: register, login, refresh, logout
├── service.py      # Lógica de negocio (crear usuario, verificar creds, rotar tokens)
├── schemas.py      # Pydantic request/response schemas
└── dependencies.py # Dependencias FastAPI (get_current_user)
```
**Por qué**: Sigue el patrón feature-first establecido en el Sprint 0 (Router → Service → UoW → Repository). Cada módulo es autocontenido y se registra en `main.py`.

### 2. Refresh token rotation con familyId
Cada refresh token pertenece a una "familia". Al reusar un token ya canjeado, se invalidan TODOS los tokens de esa familia (detección de replay attack).
```
RefreshToken
├── id: UUID (PK)
├── usuario_id: FK → Usuario
├── token_hash: str (hash del token para búsqueda segura)
├── family_id: UUID (identificador de la familia)
├── expires_at: datetime
├── revoked_at: datetime (nullable — se setea al canjear o hacer logout)
├── created_at: datetime
```
**Por qué**: Es el estándar OWASP para refresh tokens. Almacenar el hash en vez del token plano evita que un leak de la BD exponga tokens válidos.

### 3. Rate limiting con slowapi
Se usa slowapi, que ya está en `requirements.txt` del Sprint 0. Se aplica con decorador `@limiter.limit("5/15minutes")` en el endpoint de login.
**Por qué**: slowapi es la librería recomendada por FastAPI, se integra nativamente como middleware, y ya está declarada como dependencia.

### 4. Auth store en frontend con Zustand + persist
```
features/auth/
├── store.ts        # Zustand store con persist middleware (localStorage)
├── LoginPage.tsx   # Página de inicio de sesión
├── RegisterPage.tsx # Página de registro
└── types.ts        # Tipos de auth (User, LoginRequest, etc.)
```
El store expone:
- `token`, `refreshToken`, `user` — estado
- `login()`, `register()`, `logout()`, `refresh()` — acciones
- `isAuthenticated` — selector derivado

**Por qué**: Sigue la separación establecida (Zustand para estado del cliente, TanStack Query para estado del servidor). El persist middleware de Zustand evita tener que manejar localStorage manualmente.

### 5. Interceptor Axios con refresh automático
El interceptor en `shared/api/` captura errores 401, intenta refrescar el token, y si falla, redirige al login.
```
api.interceptors.response.use(
  response => response,
  async error => {
    if (error.response?.status === 401 && !error.config._retry) {
      error.config._retry = true;
      await authStore.getState().refresh();
      return api(error.config);
    }
    return Promise.reject(error);
  }
);
```
**Por qué**: Es transparente para el usuario y para el código de negocio — ningún componente necesita saber que el token se refrescó.

## Risks / Trade-offs

| Riesgo | Mitigación |
|--------|------------|
| Replay attack con refresh token | Family-based rotation: al reusar un token ya canjeado, se invalidan todos los tokens de la familia |
| Access token robado (XSS) | Los tokens NO se almacenan en localStorage directo — se usa Zustand persist (que ya usa localStorage internamente, pero la capa de abstracción permite migrar a httpOnly cookies en el futuro) |
| Rate limiting en desarrollo | slowapi se configura condicionalmente: en desarrollo se puede deshabilitar vía env var |
| Migración conflictiva con datos existentes | Se crea nueva migración Alembic — no modifica tablas existentes, solo agrega `RefreshToken` |
