## ADDED Requirements

### Requirement: RFC 7807 error format
The system SHALL have all errors following format: { type, title, status, detail, instance }

#### Scenario: Error response format
- **WHEN** any error occurs
- **THEN** the response body SHALL contain `type`, `title`, `status`, `detail`, and `instance` fields

### Requirement: Custom exception classes
The system SHALL have custom exception classes: ValidationError (400), UnauthorizedError (401), ForbiddenError (403), NotFoundError (404)

#### Scenario: ValidationError raised
- **WHEN** raising `ValidationError(detail="mensaje")`
- **THEN** the response SHALL have status code 400

#### Scenario: UnauthorizedError raised
- **WHEN** raising `UnauthorizedError(detail="mensaje")`
- **THEN** the response SHALL have status code 401

#### Scenario: ForbiddenError raised
- **WHEN** raising `ForbiddenError(detail="mensaje")`
- **THEN** the response SHALL have status code 403

#### Scenario: NotFoundError raised
- **WHEN** raising `NotFoundError(detail="mensaje")`
- **THEN** the response SHALL have status code 404

### Requirement: Global exception handler
The system SHALL have global exception handler catching all HTTPException subclasses and formatting as RFC 7807

#### Scenario: Handler catches HTTPException
- **WHEN** any HTTPException subclass is raised
- **THEN** the global exception handler SHALL format it as RFC 7807 and return the appropriate status code

### Requirement: 500 error safety
The system SHALL have 500 errors logged with stack trace on server but NOT expose details in response

#### Scenario: 500 error hides details
- **WHEN** a 500 error occurs
- **THEN** the server SHALL log the full stack trace, but the response SHALL contain a generic message without internal details

### Requirement: Per-field validation
The system SHALL have validation errors including per-field details: [{ field, message }]

#### Scenario: Validation error details
- **WHEN** a ValidationError with multiple fields is raised
- **THEN** the response SHALL include an array of per-field errors, each with `field` and `message`
