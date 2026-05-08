# 10. Configuración y Setup

## 10.1 Variables de Entorno

| Variable | Descripción | Valor ejemplo |
|----------|-------------|---------------|
| DATABASE_URL | Conexión a PostgreSQL | postgresql://user:pass@localhost:5432/foodstore_db |
| SECRET_KEY | Clave secreta para firmar JWT (mín. 32 chars) | your-super-secret-key-min-32-chars |
| ALGORITHM | Algoritmo JWT | HS256 |
| ACCESS_TOKEN_EXPIRE_MINUTES | Expiración del access token en minutos | 30 |
| REFRESH_TOKEN_EXPIRE_DAYS | Expiración del refresh token en días | 7 |
| CORS_ORIGINS | Orígenes permitidos (JSON array) | ["http://localhost:5173"] |
| MP_ACCESS_TOKEN | Access Token de MercadoPago (backend) | TEST-xxxx |
| MP_PUBLIC_KEY | Public Key de MercadoPago (para el frontend) | TEST-xxxx |
| MP_NOTIFICATION_URL | URL del webhook IPN de MercadoPago | https://dominio.com/api/v1/pagos/webhook |
| VITE_API_URL | URL base del backend (Vite — frontend) | http://localhost:8000 |
| VITE_MP_PUBLIC_KEY | Public Key MP expuesta al frontend vía Vite | TEST-xxxx |

## 10.2 Seed Data Obligatorio — app/db/seed.py

El script seed.py debe ejecutarse una vez después de alembic upgrade head. Sin este paso, la aplicación no funciona: no existen roles, estados de pedido ni formas de pago.

| Entidad | Registros a insertar |
|---------|---------------------|
| Rol | ADMIN, STOCK, PEDIDOS, CLIENT — los cuatro roles del sistema RBAC |
| EstadoPedido | PENDIENTE, CONFIRMADO, EN_PREP, EN_CAMINO, ENTREGADO, CANCELADO — con es_terminal correspondiente |
| FormaPago | MERCADOPAGO (habilitado), EFECTIVO (habilitado), TRANSFERENCIA (habilitado) |
| Usuario admin | admin@foodstore.com / Admin1234! — con rol ADMIN asignado. Contraseña debe cambiarse en producción. |
