# Reglas de Negocio — Datos e Integridad

| ID | Regla | Historias Asociadas |
| --- | --- | --- |
| RN-DA01 | Todas las tablas principales tienen campos de auditoría: creado_en (default NOW) y actualizado_en (auto-update) | US-000b |
| RN-DA02 | Los IDs de seed (Roles, EstadoPedido) son ESTABLES y explícitos; se referencian en el código | US-000b |
| RN-DA03 | El script de seed es idempotente: ejecutarlo múltiples veces no duplica datos | US-000b |
| RN-DA04 | El email del usuario tiene restricción UNIQUE e índice para optimizar búsquedas en login | US-001, US-002 |
| RN-DA05 | El HistorialEstadoPedido es append-only: NUNCA se actualiza ni se elimina un registro | US-044 |
| RN-DA06 | Los snapshots garantizan inmutabilidad: cambios futuros en productos/direcciones NO afectan pedidos existentes | US-037, US-038 |
| RN-DA07 | La paginación usa skip/limit con total de registros para que el frontend construya controles | US-018, US-049, US-051 |
| RN-DA08 | Los errores de API siguen el estándar RFC 7807 (Problem Details for HTTP APIs) | US-068 |
