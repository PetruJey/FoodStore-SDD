## Why

The system currently authenticates users but lacks role-based authorization, meaning any authenticated user can access any protected endpoint. As the platform grows with distinct operational roles (stock managers, order processors, administrators), we need granular access control to enforce separation of duties and prevent unauthorized operations.

## What Changes

- Introduce a role management API for ADMIN users to assign and remove roles
- Protect every endpoint behind role checks using the existing `require_role()` dependency
- Expand rate limiting coverage beyond login to cover register and order creation
- Implement business rules for role constraints (last-admin protection, role-scoped data access)
- Ensure public endpoints (catalog, login, register) remain unauthenticated

## Capabilities

### New Capabilities
- `role-authorization`: Role assignment API (US-005) and route-level role protection (US-006) covering all business rules RN-RB01 through RN-RB10
- `rate-limiting`: Expanded rate limiting on register (3/IP/hour) and order creation (10/user/hour) with 429 responses and Retry-After header (US-073)

### Modified Capabilities
- `user-auth`: Add rate limiting scenarios for the register endpoint (3/IP/hour) to the existing auth spec

## Impact

- **Backend**: New routes in `backend/app/routes/roles.py`; modify `backend/app/core/dependencies.py` to wire role checks into existing route modules; update `backend/app/main.py` for new rate limits; no new models needed (RolModel and UsuarioRolModel already exist)
- **API**: `GET /api/v1/roles` (list roles), `GET /api/v1/usuarios/{id}/roles` (list user roles), `PUT /api/v1/usuarios/{id}/roles` (assign roles), `DELETE /api/v1/usuarios/{id}/roles/{rol_id}` (remove role)
- **Dependencies**: slowapi already present; no new packages required
- **Seeds**: No changes needed (4 roles already seeded); seeds will be updated for test environment only
- **Tests**: New test module `backend/app/tests/test_rbac.py` covering role assignment, enforcement, rate limiting, and edge cases (last-admin protection)
