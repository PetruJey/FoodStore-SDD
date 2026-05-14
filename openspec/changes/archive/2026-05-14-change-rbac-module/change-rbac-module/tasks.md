# Tasks — RBAC Module

## 1. Core Infrastructure

- [x] 1.1 Add `roles` and `usuarios_roles` repository properties to `UnitOfWork` in `core/uow.py` (BaseRepository[RolModel] and BaseRepository[UsuarioRolModel])
- [x] 1.2 Add `selectinload(UsuarioModel.roles).selectinload(UsuarioRolModel.rol)` to `get_current_user()` in `core/dependencies.py` to eager-load roles (fix N+1 per spec issue SU-013)
- [x] 1.3 Add `get_user_key()` function in `core/security.py` that extracts user ID from JWT Authorization header for per-user rate limiting, with fallback to `get_remote_address`
- [x] 1.4 Add Pydantic schemas `RolResponse`, `UsuarioRolesResponse`, `AsignarRolesRequest` in `admin/schemas.py` per design decision 7

## 2. Role Management API

- [x] 2.1 Create `admin/rbac_router.py` with `RolesService` class implementing: list roles, get user roles, assign roles (replace), remove role with last-ADMIN protection (RN-RB04 — HTTP 422 when only admin self-removes)
- [x] 2.2 Implement `GET /roles` — returns all roles (requires ADMIN via `require_role`)
- [x] 2.3 Implement `GET /usuarios/{id}/roles` — returns roles for a given user (requires ADMIN)
- [x] 2.4 Implement `PUT /usuarios/{id}/roles` — replaces all role assignments for the user (requires ADMIN, validates role IDs exist per spec scenario)
- [x] 2.5 Implement `DELETE /usuarios/{id}/roles/{rol_id}` — removes a single role, rejects last ADMIN self-removal with HTTP 409 "LAST_ADMIN" per spec (design says 422, spec says 409 — use spec: 409)
- [x] 2.6 Register `rbac_router` in `main.py` with `prefix=API_PREFIX` so URLs are `/api/v1/roles`, `/api/v1/usuarios/{id}/roles`, etc.

## 3. Route Protection Wiring

- [x] 3.1 Wire `require_role(["ADMIN"])` into `admin/` router (all endpoints — health check is admin-only)
- [x] 3.2 Wire `get_current_user` only (no role) into `auth/logout`
- [x] 3.3 Wire `require_role(["ADMIN"])` into `usuarios/` router (all endpoints)
- [x] 3.4 Wire `require_role(["ADMIN", "STOCK"])` into `productos/` POST, PUT, DELETE; keep GET public
- [x] 3.5 Wire `require_role(["ADMIN", "STOCK"])` into `categorias/` POST, PUT, DELETE; keep GET public
- [x] 3.6 Wire `require_role(["ADMIN", "STOCK"])` into `ingredientes/` POST, PUT, DELETE; keep GET public
- [x] 3.7 Wire `require_role(["ADMIN", "PEDIDOS"])` into `pedidos/` GET list all, PATCH estado, DELETE cancel; `require_role(["CLIENT"])` into `pedidos/` POST create and GET own order
- [x] 3.8 Wire `require_role(["CLIENT"])` into `pagos/` POST (initiate); keep webhook public
- [x] 3.9 Wire `require_role(["CLIENT"])` into `direcciones/` router (all endpoints)
- [x] 3.10 Ensure `require_role(["ADMIN"])` on cancel for orders in EN_PREPARACION status per RN-RB08

## 4. Rate Limiting Expansion

- [x] 4.1 Verify `@limiter.limit("3/hour")` on register endpoint is correctly configured (already exists per design)
- [x] 4.2 Add `@limiter.limit("10/hour", key_func=get_user_key)` to the create order endpoint in `pedidos/router.py` per spec requirement
- [x] 4.3 Verify Retry-After, X-RateLimit-Limit, X-RateLimit-Remaining, X-RateLimit-Reset headers are present in 429 responses

## 5. Tests

- [x] 5.1 Create `tests/test_rbac.py` with tests for role listing: ADMIN can list all roles, non-admin gets 403, unauthenticated gets 401
- [x] 5.2 Test user role retrieval: ADMIN gets user roles, non-existent user returns 404
- [x] 5.3 Test role assignment: ADMIN assigns valid roles (replace semantics), non-existent role ID returns 422, non-existent user returns 404, non-admin gets 403
- [x] 5.4 Test role removal: ADMIN removes role (204), last ADMIN self-removal blocked with 409 "LAST_ADMIN", non-existent assignment returns 404, non-admin gets 403
- [x] 5.5 Test route enforcement: insufficient role returns 403, missing token returns 401, expired token returns 401, no-role user on any protected route returns 403
- [x] 5.6 Test public routes: login, register, catalog GET, webhook — all work without token
- [x] 5.7 Test role segregation per spec: STOCK can access catalog but not orders/users, PEDIDOS can access orders but not catalog/users, CLIENT can only access own data, ADMIN accesses everything
- [x] 5.8 Test EN_PREPARACION cancel restriction: only ADMIN can cancel; PEDIDOS gets 403 per RN-RB08
- [x] 5.9 Test rate limiting: registration exceeds 3/IP/hour → 429, order creation exceeds 10/user/hour → 429, verify Retry-After and rate limit headers present
- [x] 5.10 Test rate limiting key isolation: different users have independent counters, same user across different IPs counts toward same limit

## 6. Integration Verification

- [x] 6.1 Run full test suite: `pytest backend/tests/ -v` and confirm all existing tests still pass
- [x] 6.2 Manual smoke test: start server, register user, login, verify protected routes return 403 without ADMIN role
- [x] 6.3 Verify last-ADMIN protection: attempt to remove ADMIN from the only admin user and confirm 409
