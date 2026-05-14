## Why

Los usuarios necesitan identificarse en la plataforma para acceder a funcionalidades de compra, gestión de pedidos y administración. Actualmente no existe ningún mecanismo de autenticación — el proyecto tiene las utilidades base de JWT y el modelo `Usuario` del Sprint 0, pero no los endpoints ni el flujo completo de registro, login, refresh y logout. Sin este módulo, el sistema no puede distinguir usuarios, proteger rutas ni asociar pedidos a cuentas.

## What Changes

- **Endpoint de registro** (`POST /api/auth/register`): crea cuentas con rol CLIENT por defecto, hashea la contraseña con bcrypt, retorna par de tokens
- **Endpoint de login** (`POST /api/auth/login`): valida credenciales, genera access token (30 min) + refresh token (7 días), con rate limiting (5 intentos/15 min por IP)
- **Endpoint de refresh** (`POST /api/auth/refresh`): rota el par de tokens con detección de replay attack (invalida todos los tokens de la familia si se reusa)
- **Endpoint de logout** (`POST /api/auth/logout`): invalida el refresh token actual en BD
- **Middleware de rate limiting** en login con slowapi
- **Auth store en frontend** (Zustand con persistencia localStorage): almacena tokens, maneja refresh automático vía interceptor Axios
- **Página de login y registro** en frontend con formularios validados

## Capabilities

### New Capabilities
- `user-auth`: registro de cliente, inicio de sesión con JWT, rotación de refresh tokens, cierre de sesión con invalidación de tokens

### Modified Capabilities
<!-- No existing capabilities are modified — backend-setup already defines JWT utilities base, but no auth endpoints or flows. -->

## Impact

- **Backend**: nuevo módulo `backend/app/modules/auth/` con router, service, schemas, y dependencias. Se agrega modelo `RefreshToken` a la BD (nueva migración Alembic).
- **Frontend**: nuevo feature `features/auth/` con login, registro, auth store, y páginas asociadas. Se modifica `shared/api/` para agregar el interceptor de refresh automático.
- **Configuración**: se requiere variable de entorno `REFRESH_TOKEN_EXPIRE_DAYS=7` (ya definida en settings del Sprint 0).
- **Rate limiting**: se integra slowapi a nivel de aplicación.
