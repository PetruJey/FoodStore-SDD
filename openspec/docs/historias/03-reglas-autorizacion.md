# Reglas de Negocio — Autorizacion y Roles (RBAC)

| ID | Regla | Historias Asociadas |
| --- | --- | --- |
| RN-RB01 | Existen 4 roles fijos con IDs estables: ADMIN (1), STOCK (2), PEDIDOS (3), CLIENT (4) | US-000b, US-005 |
| RN-RB02 | Un usuario puede tener múltiples roles simultáneamente (M2M con restricción UNIQUE compuesta) | US-005 |
| RN-RB03 | Solo ADMIN puede asignar/modificar roles de otros usuarios | US-005, US-054 |
| RN-RB04 | Un ADMIN no puede quitarse el rol ADMIN a sí mismo si es el último administrador del sistema | US-005, US-054 |
| RN-RB05 | Un CLIENT solo puede ver y operar sobre sus propios datos, nunca los de otros usuarios | US-049, US-050, US-025, US-061 |
| RN-RB06 | Gestor de Stock NO tiene acceso a pedidos, usuarios ni métricas | US-006, US-075 |
| RN-RB07 | Gestor de Pedidos NO tiene acceso a catálogo ni gestión de usuarios | US-006, US-075 |
| RN-RB08 | Solo ADMIN puede cancelar pedidos en estado EN_PREPARACIÓN | US-043 |
| RN-RB09 | Si el usuario no posee el rol requerido, el sistema retorna HTTP 403 Forbidden | US-006, US-076 |
| RN-RB10 | Endpoint sin token válido retorna HTTP 401; rutas públicas (catálogo, login, registro) no requieren auth | US-006, US-076 |
