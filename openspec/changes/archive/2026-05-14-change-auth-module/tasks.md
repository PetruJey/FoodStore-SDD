## 1. Modelo de Datos — RefreshToken

- [x] 1.1 Agregar modelo `RefreshToken` en `backend/app/db/models.py` con campos: id (UUID), usuario_id (FK), token_hash, family_id (UUID), expires_at, revoked_at (nullable), created_at
- [x] 1.2 Crear migración Alembic para la tabla `refreshtoken`
- [x] 1.3 Ejecutar `alembic upgrade head` — tablas `refreshtokens`, `roles`, `usuarios`, `usuarios_roles` creadas correctamente

## 2. Backend — Esquemas Pydantic

- [x] 2.1 Crear `backend/app/modules/auth/__init__.py`
- [x] 2.2 Crear `backend/app/modules/auth/schemas.py` con: `RegisterRequest` (nombre, email, password), `LoginRequest` (email, password), `TokenResponse` (access_token, refresh_token, token_type, user), `RefreshRequest` (refresh_token), `LogoutRequest` (refresh_token)
- [x] 2.3 Agregar validaciones: password mínimo 8 caracteres, email con regex RFC 5322 simplificado

## 3. Backend — Auth Service

- [x] 3.1 Crear `backend/app/modules/auth/service.py` con método `register(db, data)` → crea usuario + asigna rol CLIENT + genera tokens
- [x] 3.2 Implementar `login(db, data, request)` → verifica credenciales, genera par de tokens, registra refresh token en BD
- [x] 3.3 Implementar `refresh_token(db, token_str)` → valida refresh token, verifica hash, rota con familyId, detecta replay attack invalidando toda la familia
- [x] 3.4 Implementar `logout(db, token_str)` → marca refresh token como revocado
- [x] 3.5 Implementar helpers: `_create_tokens(usuario)` → genera access + refresh, `_hash_token()` y `_verify_token()`

## 4. Backend — Auth Router y Dependencies

- [x] 4.1 Crear `backend/app/modules/auth/dependencies.py` con `get_current_user` que decodifica JWT del header Authorization y retorna el usuario
- [x] 4.2 Crear `backend/app/modules/auth/router.py` con endpoints:
  - `POST /api/v1/auth/register` → llama a service.register
  - `POST /api/v1/auth/login` → llama a service.login + rate limiting con slowapi
  - `POST /api/v1/auth/refresh` → llama a service.refresh_token
  - `POST /api/v1/auth/logout` → llama a service.logout (requiere auth)
- [x] 4.3 Registrar el router en `backend/app/main.py` con prefijo `/api/v1/auth`
- [x] 4.4 Configurar slowapi: middleware global en `main.py`, decorador `@limiter.limit("5/15minutes")` en login

## 5. Frontend — Tipos y Auth Store

- [x] 5.1 Crear `frontend/src/features/auth/types.ts` con interfaces: `User`, `LoginRequest`, `RegisterRequest`, `AuthState`, `TokenResponse`
- [x] 5.2 Actualizar `frontend/src/shared/stores/authStore.ts` con Zustand + persist middleware:
  - Estado: `token`, `refreshToken`, `user`, `isLoading`, `error`
  - Acciones: `login()`, `register()`, `logout()`, `refresh()`, `clearError()`
  - Selector: `isAuthenticated`

## 6. Frontend — Interceptor Axios con Refresh Automático

- [x] 6.1 Actualizar `frontend/src/shared/api/client.ts` con interceptor de response:
  - Capturar 401, setear `_retry`, llamar `authStore.getState().refresh()`
  - Si refresh falla → `authStore.getState().logout()` + redirigir a login
  - Si refresh funciona → actualizar header Authorization y reintentar request original

## 7. Frontend — Páginas de Login y Registro

- [x] 7.1 Actualizar `frontend/src/pages/Login.tsx` con formulario completo:
  - Formulario de email + password con validación inline
  - Manejo de errores (credenciales inválidas, rate limiting)
  - Redirección a catálogo post-login exitoso
- [x] 7.2 Actualizar `frontend/src/pages/Register.tsx` con formulario completo:
  - Formulario de nombre + email + password + confirmar password
  - Validación: password >= 8 caracteres, email formato, passwords coinciden
  - Redirección a catálogo post-registro exitoso
- [x] 7.3 Verificar rutas `/login` y `/registro` en `frontend/src/app/router.tsx` (ya existían)

## 8. Verificación y Cierre

- [x] 8.1 Verificar que el servidor FastAPI inicia sin errores — health check responde `{"status": "ok", "version": "1.0.0"}`
- [x] 8.2 Verificar que la migración Alembic se ejecuta correctamente — `alembic upgrade head` ejecutado, tablas verificadas
- [x] 8.3 Probar flujo completo: registro (201) → login (200) → refresh (200) → logout (200) → replay protection (401) ✅
