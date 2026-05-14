# user-auth Specification

## Purpose
TBD - created by archiving change change-auth-module. Update Purpose after archive.
## Requirements
### Requirement: User registration
The system SHALL allow new users to register with name, email, and password, automatically assigning the CLIENT role.

#### Scenario: Successful registration
- **WHEN** a new user submits a valid name, email, and password (8+ characters)
- **THEN** the system SHALL create the user account with hashed password (bcrypt, cost >= 10)
- **AND** assign the CLIENT role automatically
- **AND** return an access token (30 min) and refresh token (7 days)

#### Scenario: Duplicate email registration
- **WHEN** a user attempts to register with an email that already exists
- **THEN** the system SHALL return an error "El email ya está registrado"

#### Scenario: Weak password rejected
- **WHEN** a user attempts to register with a password shorter than 8 characters
- **THEN** the system SHALL reject the registration with a validation error

### Requirement: User login with JWT
The system SHALL authenticate users via email and password, returning a JWT access token and refresh token.

#### Scenario: Successful login
- **WHEN** a user submits valid email and password
- **THEN** the system SHALL return HTTP 200
- **AND** return an access token with 30-minute expiration containing userId, email, and rol
- **AND** return a refresh token with 7-day expiration

#### Scenario: Invalid credentials
- **WHEN** a user submits invalid email or password
- **THEN** the system SHALL return HTTP 401
- **AND** SHALL NOT reveal whether the email exists or the password is wrong

#### Scenario: Rate limiting on login
- **WHEN** 5 failed login attempts occur from the same IP within 15 minutes
- **THEN** the system SHALL return HTTP 429 with Retry-After header

### Requirement: Token refresh with rotation
The system SHALL rotate access tokens using refresh tokens, implementing family-based replay detection.

#### Scenario: Successful token refresh
- **WHEN** a valid, non-expired refresh token is submitted
- **THEN** the system SHALL return a new access token (30 min) and a new refresh token (7 days)
- **AND** mark the previous refresh token as revoked

#### Scenario: Expired refresh token
- **WHEN** an expired refresh token is submitted
- **THEN** the system SHALL return HTTP 401
- **AND** require the user to re-authenticate

#### Scenario: Replay attack detection
- **WHEN** an already-used refresh token is submitted (reuse detected)
- **THEN** the system SHALL revoke ALL refresh tokens in the same family
- **AND** return HTTP 401

### Requirement: Logout
The system SHALL allow authenticated users to terminate their session by revoking the current refresh token.

#### Scenario: Successful logout
- **WHEN** an authenticated user requests logout with a valid refresh token
- **THEN** the system SHALL mark the refresh token as revoked
- **AND** return HTTP 200

#### Scenario: Post-logout access token
- **WHEN** an access token issued before logout is used
- **THEN** it SHALL remain valid until its natural expiration (stateless JWT)

### Requirement: Auth store in frontend
The frontend SHALL provide a Zustand store for authentication state with localStorage persistence and automatic token refresh.

#### Scenario: Login persists across page reloads
- **WHEN** a user logs in and reloads the page
- **THEN** the auth state SHALL be restored from localStorage
- **AND** the user SHALL remain authenticated

#### Scenario: Auto-refresh on 401
- **WHEN** the API returns 401 due to expired access token
- **THEN** the Axios interceptor SHALL automatically attempt to refresh the token
- **AND** retry the original request
- **AND** if refresh fails, clear auth state and redirect to login

### Requirement: Login and registration pages
The frontend SHALL provide dedicated pages for login and registration with form validation.

#### Scenario: Login form validation
- **WHEN** a user submits an empty email or password
- **THEN** the form SHALL display inline validation errors
- **AND** NOT submit the request

#### Scenario: Registration form validation
- **WHEN** a user submits registration with password < 8 characters
- **THEN** the form SHALL display inline validation errors
- **AND** NOT submit the request

#### Scenario: Successful login redirect
- **WHEN** login is successful
- **THEN** the user SHALL be redirected to the catalog or home page

