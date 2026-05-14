## ADDED Requirements

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
