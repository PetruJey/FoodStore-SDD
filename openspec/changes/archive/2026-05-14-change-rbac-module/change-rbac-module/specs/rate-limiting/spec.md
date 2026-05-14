## ADDED Requirements

### Requirement: Rate limiting on registration
The system SHALL limit registration attempts to 3 per IP per 1-hour sliding window.

#### Scenario: Registration within rate limit
- **WHEN** fewer than 3 registration attempts have been made from the same IP in a 1-hour window
- **THEN** the registration request SHALL be processed normally

#### Scenario: Registration rate limit exceeded
- **WHEN** 3 or more registration attempts have been made from the same IP in a 1-hour window
- **THEN** the system SHALL return HTTP 429 Too Many Requests
- **AND** the response SHALL include a Retry-After header indicating seconds until the window resets
- **AND** the response SHALL include X-RateLimit-Limit, X-RateLimit-Remaining, and X-RateLimit-Reset headers

### Requirement: Rate limiting on order creation
The system SHALL limit order creation to 10 per authenticated user per 1-hour sliding window.

#### Scenario: Order creation within rate limit
- **WHEN** an authenticated user has created fewer than 10 orders in a 1-hour window
- **THEN** the order creation request SHALL be processed normally

#### Scenario: Order creation rate limit exceeded
- **WHEN** an authenticated user has created 10 or more orders in a 1-hour window
- **THEN** the system SHALL return HTTP 429 Too Many Requests
- **AND** the response SHALL include a Retry-After header indicating seconds until the window resets
- **AND** the response SHALL include X-RateLimit-Limit, X-RateLimit-Remaining, and X-RateLimit-Reset headers

### Requirement: Standard rate limit response format
The system SHALL return a consistent response format for all rate-limited endpoints.

#### Scenario: Rate limit response structure
- **WHEN** a request is rate-limited
- **THEN** the system SHALL return HTTP 429 with body `{"detail": "Demasiadas solicitudes. Intente de nuevo más tarde."}`
- **AND** the response SHALL include a Retry-After header with the number of seconds until the rate limit resets
- **AND** the response SHALL include X-RateLimit-Limit (max requests allowed), X-RateLimit-Remaining (requests remaining in window), and X-RateLimit-Reset (Unix timestamp when the window resets) headers
