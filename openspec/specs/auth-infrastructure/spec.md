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

### Requirement: Rate limiting on login
The system SHALL limit login attempts to 5 per IP per 15-minute sliding window.

#### Scenario: Login within rate limit
- **WHEN** fewer than 5 login attempts have been made from the same IP in 15 minutes
- **THEN** the login request SHALL be processed normally

#### Scenario: Login rate limit exceeded
- **WHEN** 5 or more login attempts have been made from the same IP in 15 minutes
- **THEN** the system SHALL return HTTP 429 Too Many Requests
- **AND** the response SHALL include a Retry-After header indicating seconds until the window resets

### Requirement: Rate limiting on registration
The system SHALL limit registration attempts to 3 per IP per 1-hour sliding window.

#### Scenario: Registration within rate limit
- **WHEN** fewer than 3 registration attempts have been made from the same IP in 1 hour
- **THEN** the registration request SHALL be processed normally

#### Scenario: Registration rate limit exceeded
- **WHEN** 3 or more registration attempts have been made from the same IP in 1 hour
- **THEN** the system SHALL return HTTP 429 Too Many Requests

### Requirement: Refresh token with familyId
The system SHALL use a familyId (UUID v4) to group refresh token generations for rotation tracking.

#### Scenario: Refresh token creation
- **WHEN** a refresh token is created during login or registration
- **THEN** it SHALL contain a unique `family_id` (UUID v4) in its JWT payload
- **AND** a RefreshToken record SHALL be stored in the database with the token's `jti`, `family_id`, `user_id`, `expires_at`, and `used` flag

#### Scenario: Token rotation marks old as used
- **WHEN** a refresh token is successfully rotated
- **THEN** the old token's `used` flag SHALL be set to true in the database
- **AND** a new RefreshToken record SHALL be created with the same `family_id`

### Requirement: Replay attack detection
The system SHALL detect and block replay attacks on used refresh tokens.

#### Scenario: Reuse of revoked token
- **WHEN** a refresh token with `used=true` is presented to the refresh endpoint
- **THEN** the system SHALL mark ALL tokens in the same `family_id` as compromised
- **AND** the system SHALL return HTTP 401
- **AND** the user SHALL be forced to re-authenticate
