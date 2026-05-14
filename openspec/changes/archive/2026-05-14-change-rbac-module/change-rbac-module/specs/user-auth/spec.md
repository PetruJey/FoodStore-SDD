## MODIFIED Requirements

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
