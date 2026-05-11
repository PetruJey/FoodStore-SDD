## ADDED Requirements

### Requirement: FastAPI project scaffold
The backend SHALL be a FastAPI application with modular feature-first directory structure.

#### Scenario: Application starts without errors
- **WHEN** the application is started with `uvicorn app.main:app --reload`
- **THEN** it SHALL serve the API at `http://localhost:8000`
- **AND** the OpenAPI docs SHALL be available at `http://localhost:8000/docs`

#### Scenario: Directory structure follows feature-first layout
- **WHEN** inspecting the `backend/app/` directory
- **THEN** it SHALL contain `main.py`, `core/`, `modules/`, and `db/` subdirectories

### Requirement: Database connection with SQLModel
The backend SHALL connect to PostgreSQL using SQLModel as the ORM.

#### Scenario: Connection string from environment
- **WHEN** the application starts
- **THEN** it SHALL read `DATABASE_URL` from environment variables
- **AND** create the SQLModel engine with that connection string

#### Scenario: Session management
- **WHEN** a request requires database access
- **THEN** the system SHALL use a session dependency that provides transaction-scoped sessions

### Requirement: Project-level dependencies
The backend SHALL declare all Python dependencies in `requirements.txt`.

#### Scenario: Core dependencies exist
- **WHEN** inspecting `requirements.txt`
- **THEN** it SHALL include: `fastapi`, `sqlmodel`, `alembic`, `passlib[bcrypt]`, `python-jose`, `python-multipart`, `slowapi`, `pydantic-settings`, `psycopg2-binary`, `uvicorn`, `mercadopago`

### Requirement: Alembic migrations configured
The backend SHALL use Alembic for database schema migrations.

#### Scenario: Initial migration exists
- **WHEN** running `alembic upgrade head`
- **THEN** the migration SHALL execute without errors
- **AND** the database SHALL contain the initial schema

#### Scenario: Migration directory structure
- **WHEN** inspecting the `backend/alembic/` directory
- **THEN** it SHALL contain `env.py`, `script.py.mako`, and `versions/`
- **AND** `alembic.ini` SHALL exist at `backend/alembic.ini`

### Requirement: Initial data models
The backend SHALL include initial SQLModel models for identity and access.

#### Scenario: User model exists
- **WHEN** inspecting the data models
- **THEN** there SHALL be a `Usuario` model with fields for id, email, nombre, password_hash
- **AND** it SHALL support soft-delete via a `deleted_at` field

#### Scenario: Role model exists
- **WHEN** inspecting the data models
- **THEN** there SHALL be a `Rol` model with name (ADMIN, STOCK, PEDIDOS, CLIENT)
- **AND** a `UsuarioRol` many-to-many relationship model

### Requirement: Repository pattern
The backend SHALL implement a generic `BaseRepository[T]` for database operations.

#### Scenario: Base repository CRUD
- **WHEN** using the BaseRepository
- **THEN** it SHALL provide get_by_id, list, create, update, and delete methods
- **AND** soft-delete SHALL set `deleted_at` instead of hard-deleting

### Requirement: Unit of Work pattern
The backend SHALL implement a generic Unit of Work for atomic transactions.

#### Scenario: UoW provides repositories
- **WHEN** entering a Unit of Work context
- **THEN** it SHALL provide access to registered repositories
- **AND** wrap all operations in a single database transaction

#### Scenario: Commit and rollback
- **WHEN** all operations succeed
- **THEN** the UoW SHALL commit the transaction
- **WHEN** any operation fails
- **THEN** the UoW SHALL rollback the transaction

### Requirement: JWT security utilities
The backend SHALL provide JWT token creation and verification utilities.

#### Scenario: Access token creation
- **WHEN** generating an access token
- **THEN** it SHALL encode user ID and expiration in the JWT
- **AND** sign with `SECRET_KEY` from environment using `HS256` algorithm

#### Scenario: Password hashing
- **WHEN** storing a user password
- **THEN** the system SHALL hash it with bcrypt (cost >= 10)

### Requirement: Docker Compose for development
The project SHALL include Docker Compose for local PostgreSQL.

#### Scenario: PostgreSQL service defined
- **WHEN** inspecting `docker-compose.yml`
- **THEN** it SHALL define a `postgres` service with PostgreSQL 15
- **AND** expose port 5432
- **AND** use environment variables for database name, user, and password

#### Scenario: Adminer service for DB inspection
- **WHEN** inspecting `docker-compose.yml`
- **THEN** it MAY include an `adminer` service for database inspection
- **AND** expose port 8080

### Requirement: Pydantic Settings configuration
The backend SHALL use Pydantic Settings for environment variable management.

#### Scenario: Settings class exists
- **WHEN** inspecting `app/core/config.py`
- **THEN** there SHALL be a `Settings` class inheriting from `BaseSettings`
- **AND** it SHALL read `DATABASE_URL`, `SECRET_KEY`, `ALGORITHM`, `ACCESS_TOKEN_EXPIRE_MINUTES`, `REFRESH_TOKEN_EXPIRE_DAYS`, `CORS_ORIGINS`, `MP_ACCESS_TOKEN` from environment

### Requirement: Seed data for development
The backend SHALL include seed data for initial development.

#### Scenario: Seed script exists
- **WHEN** running the seed script
- **THEN** it SHALL create default roles (ADMIN, STOCK, PEDIDOS, CLIENT)
- **AND** create an admin user with predefined credentials
