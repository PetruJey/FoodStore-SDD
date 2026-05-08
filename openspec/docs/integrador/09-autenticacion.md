# 4. Autenticación y Autorización

## 4.1 Flujo de Autenticación

| Paso | Actor | Acción | Resultado esperado |
|------|-------|--------|-------------------|
| 1 | Cliente | POST /api/v1/auth/login con email + password | HTTP 200 + access token (30 min) + refresh token (7 días) |
| 2 | Frontend | Almacena access token en authStore (Zustand). NO en localStorage directamente. | Token disponible para interceptor Axios |
| 3 | Frontend | Interceptor Axios agrega Authorization: Bearer \<token\> a cada request | Request autenticado hacia el backend |
| 4 | Backend | Dependency get_current_user() valida JWT y carga el usuario | Objeto usuario inyectado en el handler |
| 5 | Backend | require_role([Rol.ADMIN]) verifica roles del token | HTTP 403 si rol insuficiente |
| 6 | Cliente | POST /api/v1/auth/refresh con refresh token | Nuevo access token sin requerir re-login |
| 7 | Cliente | POST /api/v1/auth/logout | Refresh token marcado como revoked_at en tabla RefreshToken |

## 4.2 Roles y Permisos (RBAC)

| Rol | Código | Permisos principales | Restricciones |
|-----|--------|---------------------|---------------|
| Administrador | ADMIN | CRUD completo: usuarios, categorías, productos, pedidos, stock. Asigna roles. | Sin restricciones. |
| Gestor de Stock | STOCK | Leer productos, actualizar stock_cantidad y disponible, ver ingredientes. | Sin acceso a usuarios ni datos financieros. |
| Gestor de Pedidos | PEDIDOS | Ver todos los pedidos, avanzar estados CONFIRMADO → ENTREGADO, ver historial. | Sin acceso a productos ni finanzas. |
| Cliente | CLIENT | Ver catálogo, gestionar carrito, crear pedidos, ver sus propios pedidos. | Solo accede a sus propios datos. |

## 4.3 Rate Limiting en Autenticación

| Configuración | Valor |
|---------------|-------|
| Librería | slowapi — integración nativa con FastAPI |
| Límite | 5 intentos fallidos por dirección IP en 15 minutos |
| Endpoint protegido | POST /api/v1/auth/login |
| Respuesta al superar | HTTP 429 Too Many Requests con header Retry-After |
| Configuración | Middleware global en app/main.py + decorador @limiter.limit() en el router de auth |
