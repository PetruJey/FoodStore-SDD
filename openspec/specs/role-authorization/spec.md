## ADDED Requirements

### Requirement: List all roles
The system SHALL expose a `GET /api/v1/roles` endpoint that returns all available roles.

#### Scenario: Admin lists roles
- **WHEN** an authenticated ADMIN sends `GET /api/v1/roles`
- **THEN** the system SHALL return HTTP 200 with the list of all 4 roles (ADMIN, CLIENT, STOCK, PEDIDOS) and their stable IDs

#### Scenario: Non-admin requests role list
- **WHEN** an authenticated user without ADMIN role sends `GET /api/v1/roles`
- **THEN** the system SHALL return HTTP 403

#### Scenario: Unauthenticated request
- **WHEN** a request without a valid token is sent to `GET /api/v1/roles`
- **THEN** the system SHALL return HTTP 401

### Requirement: Get user roles
The system SHALL expose a `GET /api/v1/usuarios/{id}/roles` endpoint that returns the roles assigned to a specific user.

#### Scenario: Admin gets user roles
- **WHEN** an authenticated ADMIN sends `GET /api/v1/usuarios/{id}/roles`
- **THEN** the system SHALL return HTTP 200 with the list of roles assigned to that user

#### Scenario: Non-admin requests user roles
- **WHEN** an authenticated user without ADMIN role sends `GET /api/v1/usuarios/{id}/roles`
- **THEN** the system SHALL return HTTP 403

#### Scenario: Non-existent user
- **WHEN** an ADMIN sends `GET /api/v1/usuarios/{id}/roles` with a non-existent user ID
- **THEN** the system SHALL return HTTP 404

### Requirement: Assign roles to user
The system SHALL expose a `PUT /api/v1/usuarios/{id}/roles` endpoint that allows an ADMIN to assign one or more roles to a user.

#### Scenario: Admin assigns roles
- **WHEN** an authenticated ADMIN sends `PUT /api/v1/usuarios/{id}/roles` with a valid list of role IDs
- **THEN** the system SHALL replace all existing role assignments for the user with the new set
- **AND** the system SHALL return HTTP 200 with the updated list of roles
- **AND** the system SHALL enforce the UNIQUE composite constraint on (usuario_id, rol_id)

#### Scenario: Non-admin tries to assign roles
- **WHEN** an authenticated user without ADMIN role sends `PUT /api/v1/usuarios/{id}/roles`
- **THEN** the system SHALL return HTTP 403

#### Scenario: Assign non-existent role
- **WHEN** an ADMIN sends `PUT /api/v1/usuarios/{id}/roles` with a role ID that does not exist
- **THEN** the system SHALL return HTTP 422

#### Scenario: Assign to non-existent user
- **WHEN** an ADMIN sends `PUT /api/v1/usuarios/{id}/roles` with a non-existent user ID
- **THEN** the system SHALL return HTTP 404

### Requirement: Remove role from user
The system SHALL expose a `DELETE /api/v1/usuarios/{id}/roles/{rol_id}` endpoint that allows an ADMIN to remove a single role from a user.

#### Scenario: Admin removes role
- **WHEN** an authenticated ADMIN sends `DELETE /api/v1/usuarios/{id}/roles/{rol_id}`
- **THEN** the system SHALL remove the role assignment
- **AND** the system SHALL return HTTP 204 No Content

#### Scenario: Last ADMIN cannot self-remove
- **WHEN** an ADMIN sends `DELETE /api/v1/usuarios/{id}/roles/{rol_id}` targeting their own ADMIN role and they are the last remaining ADMIN
- **THEN** the system SHALL NOT remove the role
- **AND** the system SHALL return HTTP 409 with error code "LAST_ADMIN"

#### Scenario: Non-admin tries to remove role
- **WHEN** an authenticated user without ADMIN role sends `DELETE /api/v1/usuarios/{id}/roles/{rol_id}`
- **THEN** the system SHALL return HTTP 403

#### Scenario: Remove non-existent assignment
- **WHEN** an ADMIN sends `DELETE /api/v1/usuarios/{id}/roles/{rol_id}` for a role that is not assigned to the user
- **THEN** the system SHALL return HTTP 404

### Requirement: Route protection by role — missing token
The system SHALL reject requests to protected routes when no valid authentication token is provided.

#### Scenario: No token on protected route
- **WHEN** a request without a Bearer token is sent to any protected route
- **THEN** the system SHALL return HTTP 401 Unauthorized

#### Scenario: Expired token on protected route
- **WHEN** a request with an expired Bearer token is sent to any protected route
- **THEN** the system SHALL return HTTP 401 Unauthorized

### Requirement: Route protection by role — insufficient role
The system SHALL reject requests to protected routes when the authenticated user lacks the required role, returning HTTP 403.

#### Scenario: Insufficient role
- **WHEN** an authenticated user without the required role accesses a protected route
- **THEN** the system SHALL return HTTP 403 Forbidden

#### Scenario: Missing role at all
- **WHEN** an authenticated user with no roles assigned accesses a route requiring any role
- **THEN** the system SHALL return HTTP 403 Forbidden

### Requirement: Public routes require no auth
The system SHALL allow access to public routes without any authentication token.

#### Scenario: Public route without token
- **WHEN** a request without a Bearer token is sent to a public route (e.g., `POST /api/v1/auth/login`, `POST /api/v1/auth/register`, `GET /api/v1/productos`)
- **THEN** the system SHALL process the request normally without authentication

### Requirement: Role-based access per module
The system SHALL enforce role-based access to API modules according to business rules: STOCK only accesses catalog, PEDIDOS only accesses orders, CLIENT only accesses own data, ADMIN accesses everything.

#### Scenario: STOCK accesses catalog
- **WHEN** a user with STOCK role sends a request to catalog endpoints (`/api/v1/productos`, `/api/v1/categorias`)
- **THEN** the system SHALL allow access

#### Scenario: STOCK cannot access orders
- **WHEN** a user with STOCK role sends a request to order endpoints (`/api/v1/pedidos`)
- **THEN** the system SHALL return HTTP 403

#### Scenario: STOCK cannot access user management
- **WHEN** a user with STOCK role sends a request to user management endpoints (`/api/v1/usuarios`)
- **THEN** the system SHALL return HTTP 403

#### Scenario: STOCK cannot access metrics
- **WHEN** a user with STOCK role sends a request to metrics endpoints
- **THEN** the system SHALL return HTTP 403

#### Scenario: PEDIDOS accesses orders
- **WHEN** a user with PEDIDOS role sends a request to order endpoints (`/api/v1/pedidos`)
- **THEN** the system SHALL allow access

#### Scenario: PEDIDOS cannot access catalog
- **WHEN** a user with PEDIDOS role sends a request to catalog endpoints (`/api/v1/productos`, `/api/v1/categorias`)
- **THEN** the system SHALL return HTTP 403

#### Scenario: PEDIDOS cannot access user management
- **WHEN** a user with PEDIDOS role sends a request to user management endpoints (`/api/v1/usuarios`)
- **THEN** the system SHALL return HTTP 403

#### Scenario: CLIENT accesses own data
- **WHEN** a user with CLIENT role sends a request to their own user data
- **THEN** the system SHALL allow access

#### Scenario: CLIENT cannot access other users' data
- **WHEN** a user with CLIENT role sends a request to another user's data
- **THEN** the system SHALL return HTTP 403

#### Scenario: ADMIN accesses all modules
- **WHEN** a user with ADMIN role sends a request to any endpoint
- **THEN** the system SHALL allow access

### Requirement: Only ADMIN can cancel EN_PREPARACION orders
The system SHALL restrict order cancellation for orders in EN_PREPARACION status to ADMIN users only.

#### Scenario: ADMIN cancels EN_PREPARACION order
- **WHEN** an authenticated ADMIN sends a cancel request for an order in EN_PREPARACION status
- **THEN** the system SHALL cancel the order and return HTTP 200

#### Scenario: Non-ADMIN cancels EN_PREPARACION order
- **WHEN** an authenticated user without ADMIN role sends a cancel request for an order in EN_PREPARACION status
- **THEN** the system SHALL return HTTP 403 Forbidden
