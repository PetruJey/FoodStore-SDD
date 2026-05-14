## ADDED Requirements

### Requirement: Async context manager
The system SHALL have UnitOfWork implemented as async context manager (async with)

#### Scenario: Async with syntax
- **WHEN** using `async with UnitOfWork() as uow`
- **THEN** the UnitOfWork SHALL enter and exit without errors

### Requirement: Session creation
The system SHALL have UnitOfWork creating a SQLAlchemy session on enter

#### Scenario: Session created on enter
- **WHEN** entering the `async with UnitOfWork()` block
- **THEN** a new SQLAlchemy session SHALL be created internally

### Requirement: Repository accessors
The system SHALL have UnitOfWork exposing repositories as attributes (uow.productos, uow.pedidos, etc.)

#### Scenario: Repository attributes accessible
- **WHEN** inside `async with UnitOfWork() as uow`
- **THEN** `uow.productos`, `uow.usuarios`, `uow.pedidos`, and other repository attributes SHALL be accessible and operational

### Requirement: Auto-commit
The system SHALL have UnitOfWork executing commit() on successful exit

#### Scenario: Commit on success
- **WHEN** the `async with` block exits without exceptions
- **THEN** `session.commit()` SHALL be called

### Requirement: Auto-rollback
The system SHALL have UnitOfWork executing rollback() automatically on exception

#### Scenario: Rollback on exception
- **WHEN** an exception is raised inside the `async with` block
- **THEN** `session.rollback()` SHALL be called before the exception propagates
