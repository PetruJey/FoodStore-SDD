## ADDED Requirements

### Requirement: Password hashing
The system SHALL have password hashing using passlib with bcrypt (cost >= 10)

#### Scenario: Hash password
- **WHEN** hashing a password
- **THEN** the result SHALL be a bcrypt hash string with cost factor >= 10

#### Scenario: Verify password
- **WHEN** verifying a password against its hash
- **THEN** the verification SHALL return True for the correct password and False otherwise

### Requirement: JWT tokens
The system SHALL have JWT tokens using python-jose with HS256 algorithm

#### Scenario: Create access token
- **WHEN** creating an access token with a subject and expiration
- **THEN** a valid JWT string SHALL be returned encoded with HS256

#### Scenario: Decode valid token
- **WHEN** decoding a valid JWT
- **THEN** the payload SHALL contain the original subject and expiration claim

### Requirement: get_current_user dependency
The system SHALL have get_current_user dependency extracting Bearer token, decoding JWT, validating signature and expiration, returning Usuario or raising 401

#### Scenario: Valid token returns user
- **WHEN** a valid Bearer token is provided
- **THEN** `get_current_user` SHALL return the corresponding Usuario

#### Scenario: Expired token raises 401
- **WHEN** an expired Bearer token is provided
- **THEN** `get_current_user` SHALL raise HTTPException with status code 401

#### Scenario: Missing token raises 401
- **WHEN** no Authorization header is provided
- **THEN** `get_current_user` SHALL raise HTTPException with status code 401

### Requirement: require_role factory
The system SHALL have require_role(roles: list[str]) factory verifying authenticated user has at least one required role, raising 403 otherwise

#### Scenario: User has required role
- **WHEN** the authenticated user has one of the required roles
- **THEN** `require_role` SHALL allow access

#### Scenario: User lacks required role
- **WHEN** the authenticated user does not have any of the required roles
- **THEN** `require_role` SHALL raise HTTPException with status code 403

### Requirement: Depends compatibility
The system SHALL have both dependencies usable with FastAPI Depends()

#### Scenario: Depends injection
- **WHEN** used as `Depends(get_current_user)` or `Depends(require_role(["admin"]))`
- **THEN** FastAPI SHALL resolve the dependency correctly
