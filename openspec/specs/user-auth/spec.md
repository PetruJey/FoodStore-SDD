## ADDED Requirements

### Requirement: User registration
The system SHALL allow new users to register with name, email and password, automatically assigning the CLIENT role. The system SHALL rate-limit registration to 3 attempts per IP per 1-hour sliding window.

#### Scenario: Successful registration
- **WHEN** a user submits valid name, email and password to `POST /api/v1/auth/register`
- **THEN** the system SHALL create the user with hashed password (bcrypt cost >= 10)
- **AND** the system SHALL assign the CLIENT role automatically
- **AND** the system SHALL return HTTP 201 with access token (30min), refresh token (7d), and user data

#### Scenario: Duplicate email
- **WHEN** a user submits registration with an email that already exists
- **THEN** the system SHALL return HTTP 409 with error code "EMAIL_ALREADY_REGISTERED"

#### Scenario: Weak password
- **WHEN** a user submits a password with fewer than 8 characters
- **THEN** the system SHALL return HTTP 422 with validation error indicating minimum length

#### Scenario: Invalid email format
- **WHEN** a user submits an email that doesn't match RFC 5322 simplified format
- **THEN** the system SHALL return HTTP 422 with validation error

#### Scenario: Role not from request
- **WHEN** a registration request includes a role field
- **THEN** the system SHALL ignore the role field and always assign CLIENT

#### Scenario: Rate limit exceeded on registration
- **WHEN** a client exceeds 3 registration attempts per IP in a 1-hour window
- **THEN** the system SHALL return HTTP 429 with Retry-After header

### Requirement: User login
The system SHALL authenticate users by email and password, returning JWT tokens.

#### Scenario: Successful login
- **WHEN** a user submits valid email and password to `POST /api/v1/auth/login`
- **THEN** the system SHALL return HTTP 200 with access token (30min), refresh token (7d), and user data

#### Scenario: Invalid credentials
- **WHEN** a user submits an incorrect password or non-existent email to login
- **THEN** the system SHALL return HTTP 401 with generic message "Credenciales inválidas"
- **AND** the system SHALL NOT reveal whether the email exists or the password is wrong

#### Scenario: Rate limit exceeded on login
- **WHEN** a client exceeds 5 login attempts per IP in a 15-minute window
- **THEN** the system SHALL return HTTP 429 with Retry-After header

### Requirement: Token refresh with rotation
The system SHALL rotate refresh tokens, issuing a new pair and revoking the old one, with replay attack detection.

#### Scenario: Successful refresh
- **WHEN** a valid, non-expired refresh token is sent to `POST /api/v1/auth/refresh`
- **THEN** the system SHALL revoke the current refresh token
- **AND** the system SHALL issue a new access token (30min) and a new refresh token (7d) with the same familyId
- **AND** the system SHALL return HTTP 200 with the new token pair

#### Scenario: Expired refresh token
- **WHEN** an expired refresh token is sent to the refresh endpoint
- **THEN** the system SHALL return HTTP 401 indicating the session has expired

#### Scenario: Replay attack detection
- **WHEN** a previously revoked refresh token is sent to the refresh endpoint
- **THEN** the system SHALL revoke ALL refresh tokens in the same family
- **AND** the system SHALL return HTTP 401 indicating the session has been compromised

#### Scenario: Invalid refresh token
- **WHEN** a malformed or tampered refresh token is sent
- **THEN** the system SHALL return HTTP 401

### Requirement: User logout
The system SHALL allow authenticated users to invalidate their current refresh token.

#### Scenario: Successful logout
- **WHEN** an authenticated user sends a valid refresh token to `POST /api/v1/auth/logout`
- **THEN** the system SHALL revoke the refresh token in the database
- **AND** the system SHALL return HTTP 204 No Content
