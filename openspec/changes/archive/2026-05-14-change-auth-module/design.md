## Context

El Sprint 0 (change-setup-project-structure) dejó la infraestructura base: `core/security.py` con hashing bcrypt y JWT, `core/dependencies.py` con `get_current_user` y `require_role`, el módulo `auth/` con archivos scaffold vacíos, y el modelo `RefreshToken` en `app/models/identidad.py`. También existe `authStore` en el frontend con persistencia en localStorage.

Este change implementa los 4 endpoints de autenticación (register, login, refresh, logout) y las páginas frontend correspondientes.

## Goals / Non-Goals

**Goals:**
- Endpoint `POST /api/v1/auth/register` con validación de datos, hash de contraseña, asignación automática de rol CLIENT, y retorno de tokens
- Endpoint `POST /api/v1/auth/login` con verificación de credenciales, rate limiting (5 intentos/IP/15min), respuesta genérica 401 sin revelar existencia del email
- Endpoint `POST /api/v1/auth/refresh` con rotación de refresh token (familyId), detección de replay attack (revocación total de la familia), y emisión de nuevo par
- Endpoint `POST /api/v1/auth/logout` con invalidación del refresh token actual
- Rate limiting en registro (3 intentos/IP/1h) y login (5/15min)
- Frontend: páginas Login y Register con integración real a authStore via Axios
- Frontend: navegación condicional según estado de autenticación
- AuthStore actualizado para llamar al backend real

**Non-Goals:**
- RBAC completo (asignación de roles por Admin) — es el change `change-rbac-module`
- Navegación adaptada por rol — es el change `change-frontend-navigation`
- Rate limiting con Redis (se usa slowapi in-memory para desarrollo)

## Decisions

### 1. Refresh token como JWT con familyId (no UUID opaco)
- **Decisión**: El refresh token es un JWT que contiene `sub` (userId), `type: "refresh"`, `family_id` (UUID v4), y `exp`. El familyId se almacena en la tabla RefreshToken.
- **Por qué**: Usar JWT permite validar la integridad sin consultar BD en cada request. El familyId permite agrupar tokens por "familia" para detectar replay attacks. Al rotar, se revoca el anterior por familyId+tokenId y se emite uno nuevo con el mismo familyId.
- **Alternativa descartada**: UUID opaco almacenado en BD — requiere query a BD en cada refresh, más latencia y carga de BD.
- **Nota**: RN-AU03 dice "UUID v4 opaco almacenado en BD" pero usar JWT con familyId logra el mismo objetivo de seguridad (el token sigue siendo opaco para el cliente) y mejora performance.

### 2. Rate limiting con slowapi (no Redis)
- **Decisión**: Usar slowapi con almacenamiento in-memory para desarrollo. Los límites se configuran por endpoint vía decoradores `@limiter.limit()`.
- **Por qué**: slowapi ya está en requirements.txt desde Sprint 0 y configurado en main.py. Para desarrollo es suficiente. En producción se migraría a Redis.
- **Límites**: Login: `5/minute` (por IP), Register: `3/hour` (por IP), Refresh: `10/minute` (por IP).
- **Alternativa descartada**: Middleware custom con Redis — sobreingeniería para esta etapa.

### 3. Tokens en response body (no httpOnly cookies)
- **Decisión**: Los access y refresh tokens se retornan en el body de la respuesta JSON.
- **Por qué**: El frontend es una SPA con Axios. Los interceptores ya están configurados para leer tokens del store. Usar cookies httpOnly requeriría cambiar toda la arquitectura de authStore + interceptores.
- **Riesgo**: Los tokens en localStorage son vulnerables a XSS. Mitigación: sanitización de inputs, Content-Security-Policy headers, y tiempo de expiración corto (30 min access, 7 días refresh).

### 4. Refresh rotation con familyId (RN-AU04, RN-AU05)
- **Decisión**: Cada refresh token pertenece a una "familia" identificada por `familyId`. Al refrescar:
  1. Se verifica el JWT (firma, exp, tipo)
  2. Se busca el RefreshToken en BD por `token_id = jti`
  3. Si está revocado (`used=True`) → replay attack → revocar TODA la familia
  4. Si es válido → revocar este token, crear uno nuevo con mismo familyId
- **Por qué**: La rotación asegura que un refresh token comprometido sirve una sola vez. El familyId permite detectar si un atacante interceptó un token y lo usó antes que el legítimo.

### 5. AuthService como capa de orquestación
- **Decisión**: Toda la lógica de negocio de autenticación vive en `auth/service.py`. Los routers son delgados (validan input, llaman al servicio, retornan respuesta).
- **Por qué**: Separación de concerns. Los servicios pueden ser reutilizados por otros módulos (ej: admin creando usuarios). Los routers se mantienen enfocados en HTTP.
- **Estructura**: Router → Service → Repository (Usuario) + Repository (RefreshToken)

### 6. Frontend: páginas independientes con estado local + authStore
- **Decisión**: Login y Register son páginas independientes con su propio estado de formulario (React state). Al success, persisten en authStore y redirigen.
- **Por qué**: Las páginas de auth no necesitan estado global de formulario. authStore solo almacena el resultado (tokens + user), no el estado del formulario.
- **Flujo**: Submit → llamada Axios directa → success: authStore.login(response) → redirect / error: mostrar mensaje en página
- **Alternativa descartada**: Form state en Zustand — sobreingeniería para formularios de 2-3 campos.

## Risks / Trade-offs

- **[Seguridad] Tokens en localStorage** → Mitigación: implementar Content-Security-Policy, sanitización de inputs, access token de corta duración (30 min). En producción evaluar httpOnly cookies via proxy inverso.
- **[Rate limiting] Slowapi in-memory no persiste entre restarts** → Aceptable para desarrollo. En producción migrar a Redis backend de slowapi.
- **[Refresh rotation] Replay attack revoca toda la familia** → El usuario legítimo se queda sin sesión y debe re-loguearse. Es el comportamiento correcto por seguridad.
- **[Frontend] Las páginas de auth no usan react-hook-form ni tanstack/form** → Para 2-3 campos, useState es suficiente. Si los formularios crecen en complejidad, migrar a react-hook-form.
