# 6. Schemas de Request / Response (Pydantic v2)

Todos los schemas usan Pydantic v2. Se definen schemas separados para Create, Update y Read. Nunca se expone el model de SQLModel directamente como response.

## 6.1 Auth

| Schema | Campos requeridos | Validaciones |
|--------|-------------------|-------------|
| LoginRequest | email: EmailStr, password: str | password mínimo 8 caracteres |
| RegisterRequest | nombre, apellido, email: EmailStr, password: str | nombre/apellido min 2 max 80. password min 8. Unicidad de email en servicio. |
| TokenResponse | access_token, refresh_token, token_type, expires_in: int | token_type = 'bearer'. expires_in en segundos. |
| UserResponse | id, nombre, apellido, email, roles: list[str], created_at | Nunca incluye password_hash. |

## 6.2 Pedidos

| Schema | Campos | Validaciones / Notas |
|--------|--------|---------------------|
| CrearPedidoRequest | items: list[ItemPedidoRequest], forma_pago_codigo: str, direccion_id: int\|None, notas: str\|None | Mínimo 1 item. forma_pago_codigo debe existir en catálogo. |
| ItemPedidoRequest | producto_id: int, cantidad: int, personalizacion: list[int]\|None | cantidad ≥ 1. personalizacion = IDs de ingredientes removidos (INTEGER[]). |
| AvanzarEstadoRequest | nuevo_estado: str, motivo: str\|None | motivo obligatorio si nuevo_estado = CANCELADO (RN-05). |
| PedidoRead | id, estado_codigo, total, created_at | Versión compacta para listados. |
| PedidoDetail | id, estado_codigo, subtotal, descuento, costo_envio, total, items, historial, pago | Versión completa para vista de detalle. |
| DetallePedidoRead | producto_id, nombre_snapshot, precio_snapshot, cantidad, personalizacion | Snapshot: precio y nombre no reflejan cambios posteriores. |
