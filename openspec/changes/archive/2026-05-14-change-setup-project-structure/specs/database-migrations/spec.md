## ADDED Requirements

### Requirement: All 16 SQLModel models
The system SHALL have ALL 16 tables defined as SQLModel models: Usuario, Rol, UsuarioRol, RefreshToken, DireccionEntrega, Categoria, Producto, Ingrediente, ProductoCategoria, ProductoIngrediente, FormaPago, EstadoPedido, Pedido, DetallePedido, HistorialEstadoPedido, Pago

#### Scenario: All models defined
- **WHEN** importing the models module
- **THEN** all 16 model classes SHALL be importable and SHALL map to the correct table names

### Requirement: Auditoria fields
The system SHALL have all main tables with auditoria fields: creado_en (timestamp default NOW), actualizado_en (timestamp auto-update)

#### Scenario: Main tables have timestamps
- **WHEN** inspecting main table models
- **THEN** each model SHALL have `creado_en` with default `NOW()` and `actualizado_en` with auto-update behavior

### Requirement: Soft delete fields
The system SHALL have tables supporting soft delete with eliminado_en (timestamp nullable)

#### Scenario: Soft delete columns exist
- **WHEN** inspecting models that support soft delete
- **THEN** they SHALL have an `eliminado_en` column of type nullable timestamp

### Requirement: Self-referencing categoria
The system SHALL have Categoria with padre_id as nullable self-referencing FK

#### Scenario: Categoria self-reference
- **WHEN** inspecting the Categoria model
- **THEN** `padre_id` SHALL be a nullable foreign key referencing `categorias.id`

### Requirement: Unique rol constraint
The system SHALL have UsuarioRol with UNIQUE(usuario_id, rol_id)

#### Scenario: Unique constraint on UsuarioRol
- **WHEN** inspecting the UsuarioRol table schema
- **THEN** there SHALL be a UNIQUE constraint on the `(usuario_id, rol_id)` composite

### Requirement: Alembic with autogenerate
The system SHALL have Alembic configured with autogenerate from SQLModel models

#### Scenario: Alembic autogenerate
- **WHEN** running `alembic revision --autogenerate -m "test"`
- **THEN** Alembic SHALL detect changes from SQLModel models without errors

### Requirement: Idempotent seed script
The system SHALL have seed script inserting idempotently: 4 Roles, 6 EstadoPedido, 3 FormaPago, 1 admin user using INSERT ... ON CONFLICT DO NOTHING

#### Scenario: Seed runs idempotently
- **WHEN** running the seed script twice
- **THEN** the second run SHALL NOT create duplicate rows

#### Scenario: Seed inserts required data
- **WHEN** running the seed script
- **THEN** the database SHALL contain 4 roles, 6 estado de pedido values, 3 formas de pago, and 1 admin user

### Requirement: Alembic downgrade
The system SHALL have alembic downgrade -1 working without errors

#### Scenario: Alembic downgrade works
- **WHEN** running `alembic downgrade -1`
- **THEN** the command SHALL complete without errors
