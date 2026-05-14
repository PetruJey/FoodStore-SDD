## ADDED Requirements

### Requirement: Generic BaseRepository
The system SHALL have BaseRepository[T] as a generic class parameterized with TypeVar

#### Scenario: Generic parameterization
- **WHEN** instantiating `BaseRepository[ProductoModel]`
- **THEN** it SHALL accept only ProductoModel as the type parameter

### Requirement: CRUD operations
The system SHALL have BaseRepository implementing: get_by_id(id), list_all(skip, limit, filters), count(filters), create(obj), update(id, data), soft_delete(id), hard_delete(id)

#### Scenario: get_by_id returns entity
- **WHEN** calling `get_by_id(1)`
- **THEN** the repository SHALL return the entity with id=1, or None if not found

#### Scenario: list_all returns paginated results
- **WHEN** calling `list_all(skip=0, limit=10)`
- **THEN** the repository SHALL return a list of up to 10 entities

#### Scenario: count returns total
- **WHEN** calling `count(filters={...})`
- **THEN** the repository SHALL return the total count of entities matching the filters

#### Scenario: create persists entity
- **WHEN** calling `create(producto)`
- **THEN** the entity SHALL be added to the session and SHALL have an id assigned

#### Scenario: update modifies entity
- **WHEN** calling `update(1, {"nombre": "Nuevo"})`
- **THEN** the entity with id=1 SHALL have its nombre updated

#### Scenario: soft_delete sets timestamp
- **WHEN** calling `soft_delete(1)`
- **THEN** the entity SHALL have `eliminado_en` set to current timestamp

#### Scenario: hard_delete removes entity
- **WHEN** calling `hard_delete(1)`
- **THEN** the entity SHALL be removed from the session

### Requirement: Soft-delete exclusion
The system SHALL have get_by_id and list_all excluding soft-deleted records (eliminado_en IS NOT NULL) by default

#### Scenario: Soft-deleted excluded from list
- **WHEN** calling `list_all()`
- **THEN** entities with `eliminado_en IS NOT NULL` SHALL NOT be included in results

#### Scenario: Soft-deleted excluded from get_by_id
- **WHEN** calling `get_by_id(1)` on a soft-deleted entity
- **THEN** it SHALL return None

### Requirement: Session injection
The system SHALL have BaseRepository receiving SQLAlchemy session via constructor injection

#### Scenario: Session injected
- **WHEN** instantiating `BaseRepository(session)`
- **THEN** the session SHALL be stored as an instance attribute
