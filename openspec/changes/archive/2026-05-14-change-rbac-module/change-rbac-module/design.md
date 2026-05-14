## Context

El backend de Food Store actualmente autentica usuarios via JWT y asigna el rol CLIENT automáticamente al registrar, pero no existe protección por roles en los endpoints. `RolModel` y `UsuarioRolModel` ya existen en `app/models/identidad.py`, y la semilla crea 4 roles fijos (ADMIN=1, STOCK=2, PEDIDOS=3, CLIENT=4). La dependencia `require_role(roles: list[str])` en `core/dependencies.py` ya verifica roles contra `current_user.roles`, pero ningún endpoint la utiliza. El módulo `admin/` existe con estructura scaffold (solo health check). El rate limiting via slowapi ya está configurado globalmente (5/15min) y aplicado en auth (register 3/h, login 5/min, refresh 10/min).

## Goals / Non-Goals

**Goals:**
- Endpoints CRUD de asignación de roles (solo ADMIN): listar roles, listar roles de usuario, asignar roles, remover rol
- Proteger todos los endpoints existentes con `require_role()` según el rol necesario
- Rate limiting en registro (3/IP/hora) y creación de pedidos (10/usuario/hora)
- Regla de negocio: último ADMIN no puede auto-removerse
- Cobertura de tests para asignación, enforcement, rate limiting y edge cases (last-admin)

**Non-Goals:**
- Frontend de gestión de roles (es otro change)
- Password reset / OAuth / SSO
- Permisos finos (solo roles, no permiso individual sobre recursos)
- Cache distribuido para rate limiting (slowapi in-memory es suficiente para desarrollo)
- Embedding de roles en JWT (se mantiene carga desde DB)
- Migración a Redis para rate limiting

## Decisions

### 1. Ubicación: nuevo router en módulo `admin/` para endpoints RBAC

Se crea `backend/admin/rbac_router.py` con las 4 rutas de role management. Se registra en `main.py` con `prefix=API_PREFIX` para que las URLs sean `/api/v1/roles`, `/api/v1/usuarios/{id}/roles`, etc. La protección ADMIN viene de `require_role(["ADMIN"])`, no de la URL.

- **Por qué**: El módulo `admin/` ya existe y es el hogar natural de operaciones administrativas. Evita crear un módulo nuevo con estructura casi idéntica. El service y schemas de RBAC comparten el mismo directorio admin.
- **Alternativa descartada**: Módulo `roles/` separado — añade complejidad de imports y duplica estructura para 4 endpoints que comparten el mismo role guard.
- **Alternativa descartada**: Rutas dentro de `usuarios/router.py` — mezcla responsabilidades de usuario y autoría, y no existe módulo para solo listar roles.

### 2. Nuevos repositorios en UoW: `roles` y `usuarios_roles`

Se agregan dos properties a `UnitOfWork`:
- `roles`: apunta a `BaseRepository[RolModel]`
- `usuarios_roles`: apunta a `BaseRepository[UsuarioRolModel]`

- **Por qué**: El UoW es el punto único de acceso a repositorios. Todos los servicios existentes lo usan. No tiene sentido crear repositorios custom cuando las operaciones son CRUD simples (listar roles, insertar/eliminar rows en usuarios_roles).
- **Nota**: Para la query de "último ADMIN" (last-admin protection), se usa `select().where(...)` directamente desde el service, no necesita repositorio especializado.

### 3. Route protection via `require_role()` como dependencia

Cada endpoint protegido recibe `require_role([...])` como `Depends`:

| Módulo | Endpoints | Rol(es) |
|--------|-----------|---------|
| `auth/` | register, login, refresh | Público (sin auth) |
| `auth/` | logout | Authenticated (solo `get_current_user`) |
| `admin/` | todos | ADMIN |
| `usuarios/` | todos | ADMIN |
| `productos/` | GET (catálogo) | Público |
| `productos/` | POST, PUT, DELETE | ADMIN, STOCK |
| `categorias/` | GET | Público |
| `categorias/` | POST, PUT, DELETE | ADMIN, STOCK |
| `ingredientes/` | GET | Público |
| `ingredientes/` | POST, PUT, DELETE | ADMIN, STOCK |
| `pedidos/` | GET /{id} (propio) | CLIENT |
| `pedidos/` | GET / (todos) | ADMIN, PEDIDOS |
| `pedidos/` | POST (crear) | CLIENT |
| `pedidos/` | PATCH estado | ADMIN, PEDIDOS |
| `pedidos/` | DELETE (cancelar) | ADMIN, PEDIDOS (solo PENDIENTE), ADMIN (EN_PREPARACION por RN-RB08) |
| `pagos/` | POST (iniciar) | CLIENT |
| `pagos/` | Webhook MP | Público (sin auth) |
| `direcciones/` | GET, POST, PUT, DELETE | CLIENT (solo propias por RN-RB05) |

- **Por qué**: FastAPI dependency injection es explícita, testeable, y sigue el patrón existente de `get_current_user`. Cada endpoint declara qué roles necesita sin magia.
- **Alternativa descartada**: Middleware global con matcher de rutas — opaque, difícil de testear, y no permite granularidad fina (ej: GET catálogo público vs POST catálogo ADMIN/STOCK).

### 4. Eager loading de roles en `get_current_user` (N+1 fix)

Se modifica `get_current_user` para usar `selectinload(UsuarioModel.roles)` y `selectinload(UsuarioModel.roles, UsuarioRolModel.rol)` al cargar el usuario. Sin esto, cada request que pase por `require_role` dispara queries lazy separadas.

- **Por qué**: El current pattern (`select(UsuarioModel).where(...)`) produce N+1: una query para el usuario + una por cada rol al iterar `current_user.roles`. Con `selectinload` todo se resuelve en 2 queries totales (usuario + roles).
- **Alternativa descartada**: Embedding de roles en JWT claims — reduce queries a 0 pero requiere regenerar token al cambiar roles, añadiendo complejidad de invalidación. Se evaluará en versión futura.

### 5. Rate limiting: slowapi con key function custom para pedidos

- **Register** (3/IP/hour): ya implementado, se mantiene.
- **Create order** (10/user/hour): se implementa con `@limiter.limit("10/hour", key_func=get_user_key)` donde `get_user_key` extrae el user ID del JWT en el header Authorization, con fallback a `get_remote_address`.

```python
def get_user_key(request: Request) -> str:
    auth = request.headers.get("Authorization")
    if auth and auth.startswith("Bearer "):
        try:
            payload = decode_token(auth[7:])
            return f"user:{payload.get('sub', 'ip')}"
        except Exception:
            pass
    return get_remote_address(request)
```

- **Por qué**: slowapi ya está en el stack y configurado. El rate limiting por IP tiene sentido para register (no requiere auth), pero para crear pedidos un atacante autenticado puede rotar IPs fácilmente. Limitar por usuario es más efectivo.
- **Alternativa descartada**: slowapi con key por IP (default) — un atacante con IP rotativa puede evitar el límite. 
- **Alternativa descartada**: Middleware custom de rate limiting — reinventar la rueda. slowapi ya maneja headers Retry-After y response 429.
- **Riesgo**: slowapi evalúa `key_func` antes de que corran las dependencias de FastAPI, por lo que `decode_token` se llama dos veces (una en key_func, otra en `get_current_user`). Aceptable para desarrollo. En producción, migrar a Redis con contador por user ID desde el service.

### 6. Last-admin protection (RN-RB04)

Se implementa en `RolesService.remove_role()`: antes de eliminar el rol ADMIN de un usuario, se cuenta cuántos usuarios activos tienen rol ADMIN. Si es 1 y el usuario solicitante es el mismo, se rechaza con HTTP 422.

```python
async def remove_role(self, usuario_id: int, rol_id: int, current_user_id: int):
    if rol_id == ADMIN_ROL_ID and usuario_id == current_user_id:
        admin_count = await self._count_admins()
        if admin_count <= 1:
            raise HTTPException(422, "No puedes remover tu propio rol ADMIN siendo el último administrador")
```

- **Por qué**: La regla debe estar en el service (capa de negocio) no en el router. La query de conteo es simple (`select count(*) from usuarios_roles where rol_id = 1 join usuarios on ... where activo = true`).
- **Nota**: La constraint UNIQUE compuesta en `usuarios_roles` (usuario_id, rol_id) garantiza que no haya duplicados, pero la verificación de "último ADMIN" es adicional y no puede modelarse como constraint de BD.

### 7. Schemas Pydantic para role management

Se crean en `admin/schemas.py`:
- `RolResponse`: id, nombre, descripcion
- `UsuarioRolesResponse`: usuario_id, roles: list[RolResponse]
- `AsignarRolesRequest`: roles: list[int] (lista de rol_ids)

Se reutiliza el `UserRead` de `auth/schemas.py` cuando sea necesario (incluye roles list).

### 8. Integridad transaccional

Todas las operaciones de asignación/remoción de roles se ejecutan dentro del Unit of Work (commit automático al salir del `async with`). La creación de pedidos ya usa UoW (RN-PE01). No se requieren cambios adicionales para atomicidad.

## Risks / Trade-offs

- **[Rate limiting] Decodificar JWT dos veces por request en create order** → La key_func de slowapi y `get_current_user` decodifican el mismo token. Aceptable para desarrollo (< 1ms extra). En producción migrar a middleware con Redis y decode único.
- **[Route protection] N+1 mitigado pero no eliminado** → `selectinload` reduce de N+1 a 2 queries. Si la carga de usuarios concurrentes crece, se evaluará embedding de roles en JWT.
- **[Dependency explosion] Rutas con `Depends(require_role(...))` + `Depends(get_current_user)`** → `require_role` ya incluye `get_current_user`, no hay duplicación.
- **[Testabilidad] slowapi key_func con decode_token** → Testear rate limiting requiere mockear `decode_token` en la key_func o usar slowapi en modo test. Se documenta en los tests.
- **[Admin module] Módulo `admin/` mezcla health check, RBAC, y futuras métricas** → El módulo admin es por definición un agregador de operaciones administrativas. Es aceptable que tenga múltiples routers (uno por sub-dominio: rbac, metricas, config).
