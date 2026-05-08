# 5. Especificación de API REST

Todos los endpoints usan el prefijo /api/v1. Los errores siguen RFC 7807 (Problem Details). La documentación interactiva se genera automáticamente en /docs (Swagger UI) y /redoc.

**Convenciones globales:**

```
Error estándar RFC 7807: { "detail": "mensaje", "code": "ERROR_CODE", "field": "campo_opcional" }
Paginación: GET /recursos?page=1&size=20 → { "items": [...], "total": N, "page": 1, "size": 20, "pages": P }
Soft delete: todos los GET filtran WHERE deleted_at IS NULL. Los registros eliminados no son visibles.
```

## 5.1 Módulo Auth

| Método | Endpoint | Body / Params | Response | Auth requerida |
|--------|----------|---------------|----------|---------------|
| POST | /api/v1/auth/register | { nombre, apellido, email, password } | 201 UserResponse | No |
| POST | /api/v1/auth/login | { email, password } | 200 TokenResponse | No — rate limited 5/15min |
| POST | /api/v1/auth/refresh | { refresh_token } | 200 TokenResponse | No |
| POST | /api/v1/auth/logout | { refresh_token } | 204 No Content | Bearer token |
| GET | /api/v1/auth/me | — | 200 UserResponse | Bearer token |

## 5.2 Módulo Productos

| Método | Endpoint | Descripción | Rol requerido | Response |
|--------|----------|-------------|---------------|----------|
| GET | /api/v1/productos | Listar (filtro: categoria, disponible, search, page, size) | Público | 200 PaginatedProductos |
| GET | /api/v1/productos/{id} | Detalle con ingredientes, categorías y stock | Público | 200 ProductoDetail |
| POST | /api/v1/productos | Crear producto con ingredientes y categorías | ADMIN | 201 ProductoRead |
| PUT | /api/v1/productos/{id} | Actualizar producto | ADMIN | 200 ProductoRead |
| PATCH | /api/v1/productos/{id}/disponibilidad | Cambiar disponible (true/false) | ADMIN, STOCK | 200 ProductoRead |
| DELETE | /api/v1/productos/{id} | Soft delete producto | ADMIN | 204 No Content |
| GET | /api/v1/productos/{id}/ingredientes | Listar ingredientes del producto | Público | 200 List[IngredienteRead] |
| POST | /api/v1/productos/{id}/ingredientes | Asociar ingrediente a producto | ADMIN | 201 ProductoIngredienteRead |
| DELETE | /api/v1/productos/{id}/ingredientes/{ing_id} | Quitar ingrediente de producto | ADMIN | 204 No Content |

## 5.3 Módulo Pedidos

| Método | Endpoint | Descripción | Rol requerido | Response |
|--------|----------|-------------|---------------|----------|
| GET | /api/v1/pedidos | Listar propios (CLIENT) o todos (ADMIN/PEDIDOS) | CLIENT/ADMIN/PEDIDOS | 200 PaginatedPedidos |
| GET | /api/v1/pedidos/{id} | Detalle completo con líneas, trazabilidad y estado de pago | Propietario/ADMIN | 200 PedidoDetail |
| POST | /api/v1/pedidos | Crear pedido desde carrito. Todo en una transacción (UoW). | CLIENT | 201 PedidoRead |
| PATCH | /api/v1/pedidos/{id}/estado | Avanzar estado. Valida FSM. UoW atómico. | ADMIN/PEDIDOS | 200 PedidoRead |
| GET | /api/v1/pedidos/{id}/historial | Historial completo. ORDER BY created_at ASC. | Propietario/ADMIN | 200 List[HistorialRead] |
| DELETE | /api/v1/pedidos/{id} | Cancelar propio (solo PENDIENTE o CONFIRMADO). | CLIENT propietario | 200 PedidoRead |

## 5.4 Módulo Pagos (MercadoPago) ★

| Método | Endpoint | Descripción | Rol requerido | Response |
|--------|----------|-------------|---------------|----------|
| POST | /api/v1/pagos/crear | Crea pago con token de tarjeta. Registra en tabla Pago. | CLIENT | 201 PagoResponse |
| POST | /api/v1/pagos/webhook | Endpoint IPN de MercadoPago. Actualiza estado del pago y del pedido. | Público (validar firma) | 200 { status: ok } |
| GET | /api/v1/pagos/{pedido_id} | Consulta el pago asociado a un pedido. | Propietario/ADMIN | 200 PagoResponse |
