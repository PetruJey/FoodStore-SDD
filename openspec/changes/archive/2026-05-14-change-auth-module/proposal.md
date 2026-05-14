## Why

El Sprint 0 dejó la infraestructura base de autenticación (hashing, JWT, dependencias get_current_user y require_role), pero sin los endpoints reales de negocio. Este change implementa el módulo de autenticación completo que permite a los usuarios registrarse, iniciar sesión, refrescar su sesión y cerrarla, habilitando así el acceso al sistema para todos los actores.

## What Changes

- Endpoint `POST /api/auth/register` — registro de nuevo cliente con asignación automática de rol CLIENT
- Endpoint `POST /api/auth/login` — inicio de sesión con credenciales, rate limiting anti-fuerza bruta
- Endpoint `POST /api/auth/refresh` — rotación de refresh token con detección de replay attack
- Endpoint `POST /api/auth/logout` — cierre de sesión con invalidación de refresh token
- Rate limiting en login (5 intentos/IP/15min), registro (3/IP/1h) y endpoints sensibles
- Frontend: páginas de Login y Register con integración a authStore
- Frontend: navegación condicional (mostrar login/register vs perfil/logout según autenticación)
- Frontend: redirección post-login a dashboard, post-register a login con mensaje de éxito
- Actualización de authStore existente para manejar tokens desde el backend real

## Capabilities

### New Capabilities
- `user-auth`: Backend endpoints de autenticación (register, login, refresh, logout) con validaciones, rate limiting y rotación segura de refresh tokens
- `frontend-auth`: Páginas de Login y Register con integración a authStore, navegación condicional y manejo de estados (loading, error, éxito)

### Modified Capabilities
- `auth-infrastructure`: Se agregan requirements para rate limiting en login/registro, refresh token rotation con familyId, y detección de replay attack

## Impact

- **Backend**: Implementación completa del módulo `backend/auth/` (service.py, schemas.py con request/response DTOs, router.py con 4 endpoints, repository.py con operaciones de RefreshToken)
- **Frontend**: Nuevas páginas `frontend/src/pages/Login.tsx` y `frontend/src/pages/Register.tsx`, componentes de formulario, integración con authStore existente
- **Rate limiting**: Configuración de slowapi con límites específicos para cada endpoint
- **Dependencias**: slowapi ya incluido en requirements.txt del Sprint 0
- **No breaking**: Los cambios son aditivos sobre la infraestructura existente
