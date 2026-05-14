## ADDED Requirements

### Requirement: FastAPI main configuration
The system SHALL have FastAPI app configured in main.py with CORS middleware (origins from env var), rate limiting middleware, and router registration with /api/v1 prefix

#### Scenario: App starts with middleware and routers
- **WHEN** the FastAPI application starts
- **THEN** CORS middleware SHALL be configured with origins from `CORS_ORIGINS` env var, rate limiting middleware SHALL be active, and all routers SHALL be registered under `/api/v1` prefix

### Requirement: Docs endpoints
The system SHALL have Swagger docs at /docs and ReDoc at /redoc

#### Scenario: Swagger UI accessible
- **WHEN** sending GET request to `/docs`
- **THEN** the response SHALL return Swagger UI HTML page

#### Scenario: ReDoc accessible
- **WHEN** sending GET request to `/redoc`
- **THEN** the response SHALL return ReDoc HTML page

### Requirement: Config module
The system SHALL have a config.py module reading env vars: DATABASE_URL, SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES (30), REFRESH_TOKEN_EXPIRE_DAYS (7), CORS_ORIGINS, MP_ACCESS_TOKEN, MP_PUBLIC_KEY

#### Scenario: Config reads environment variables
- **WHEN** `config.py` is imported
- **THEN** it SHALL expose all required attributes with correct defaults for `ACCESS_TOKEN_EXPIRE_MINUTES` (30) and `REFRESH_TOKEN_EXPIRE_DAYS` (7)

### Requirement: Database module
The system SHALL have database.py with SQLAlchemy engine and async session factory

#### Scenario: Database engine and session factory
- **WHEN** `database.py` is imported
- **THEN** it SHALL provide a SQLAlchemy async engine and an async session factory

### Requirement: CORS dev origins
The system SHALL allow http://localhost:5173 in development

#### Scenario: CORS allows Vite dev server
- **WHEN** a request originates from `http://localhost:5173`
- **THEN** the server SHALL respond with appropriate CORS headers allowing the origin

### Requirement: Server port
The system SHALL run on port 8000 with uvicorn

#### Scenario: Server listens on port 8000
- **WHEN** starting the server with uvicorn
- **THEN** it SHALL bind to port 8000

### Requirement: Requirements.txt
The system SHALL have requirements.txt with: fastapi, sqlmodel, alembic, passlib[bcrypt], python-jose, slowapi, mercadopago, uvicorn, httpx, pydantic[email-validator]

#### Scenario: All dependencies listed
- **WHEN** inspecting `requirements.txt`
- **THEN** it SHALL contain all specified packages
