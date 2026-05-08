# 3. Modelo de Datos — ERD v5

El esquema aplica Tercera Forma Normal (3FN), Soft Delete (deleted_at TIMESTAMPTZ), Snapshot Pattern en pedidos y Audit Trail append-only en HistorialEstadoPedido. La versión 5 incorpora todas las correcciones de auditoría: RefreshToken, Ingrediente, ProductoIngrediente, Pago completo y correcciones de tipos.

## 3.1 Dominio 1 — Identidad y Acceso

| Entidad | Campo clave | Tipo | Restricción | Notas |
|---------|------------|------|-------------|-------|
| Usuario | id | BIGSERIAL | PK | Soft-delete vía deleted_at |
| Usuario | email | VARCHAR(254) | UQ, NN | Validar con EmailStr (Pydantic v2) |
| Usuario | password_hash | CHAR(60) | NN | bcrypt cost≥12. NUNCA almacenar plaintext |
| Rol | codigo | VARCHAR(20) | PK (semántica) | ADMIN \| STOCK \| PEDIDOS \| CLIENT |
| UsuarioRol | (usuario_id, rol_codigo) | BIGINT + VARCHAR | PK compuesta | Pivot N:M. Incluye asignado_por_id |
| RefreshToken ★ | token_hash | CHAR(64) | UQ, NN | SHA-256 del token. revoked_at NULL = activo |
| RefreshToken ★ | expires_at | TIMESTAMPTZ | NN | 7 días desde emisión |
| RefreshToken ★ | revoked_at | TIMESTAMPTZ | NULL | Se completa en POST /auth/logout |
| DireccionEntrega ★ | alias | VARCHAR(50) | NULL | Ej: 'Casa', 'Trabajo' |
| DireccionEntrega ★ | linea1 | TEXT | NN |  |
| DireccionEntrega ★ | es_principal | BOOLEAN | NN, default false | Solo una por usuario |
