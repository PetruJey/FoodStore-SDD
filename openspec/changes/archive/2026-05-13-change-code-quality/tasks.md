## 1. Base de Datos: Migración y Modelos

- [x] 1.1 Agregar migración Alembic para `estados_pedido` y `formas_pago`
- [x] 1.2 Corregir `EstadoPedidoModel` y `FormaPagoModel`: reemplazar `default_factory=datetime.utcnow` por `sa_column_kwargs={"server_default": func.now()}`

## 2. Backend: Manejo de Errores Unificado

- [x] 2.1 Reemplazar `HTTPException` por `AppError`/`BadRequestError`/`NotFoundError` en `auth/service.py` (register, login)
- [x] 2.2 Reemplazar `HTTPException` por `AppError`/`UnauthorizedError`/`ForbiddenError` en `auth/dependencies.py` (get_current_user, require_role)
- [x] 2.3 Documentar con comentario inline por qué `refresh_token()` mantiene `HTTPException` (commit antes de raise por replay attack detection)

## 3. Backend: Configuración y Seed

- [x] 3.1 Agregar `MP_NOTIFICATION_URL: str = ""` a `Settings` en `config.py`
- [x] 3.2 Agregar `ALGORITHM` y `MP_NOTIFICATION_URL` a `.env.example`
- [x] 3.3 Corregir seed: `"PREPARANDO"` → `"EN_PREPARACION"`, `"ENVIADO"` → `"EN_CAMINO"`

## 4. Frontend: Seguridad — Tokens fuera de localStorage

- [x] 4.1 Modificar `authStore.ts`: remover `persist` middleware, almacenar tokens solo en memoria
- [x] 4.2 Actualizar `partialize` para que no persista tokens (solo datos de usuario no sensibles si se requiere persistencia)
- [x] 4.3 Verificar que el interceptor de Axios en `client.ts` funciona correctamente sin persistencia (refresh automático)

## 5. Frontend: Arquitectura FSD

- [x] 5.1 Crear `features/auth/components/` con `LoginForm.tsx` y `RegisterForm.tsx`
- [x] 5.2 Mover lógica de login/register desde `pages/Login.tsx` y `pages/Register.tsx` a los componentes en `features/auth/`
- [x] 5.3 Refactorizar `pages/Login.tsx` y `pages/Register.tsx` para que importen desde `features/auth/` en vez de directo de `stores/`

## 6. Frontend: Convenciones de Código

- [x] 6.1 Renombrar archivos de pages a kebab-case: `Login.tsx` → `login.tsx`, `Register.tsx` → `register.tsx`, `AdminDashboard.tsx` → `admin-dashboard.tsx`, `Carrito.tsx` → `carrito.tsx`, `Checkout.tsx` → `checkout.tsx`, `Home.tsx` → `home.tsx`, `Productos.tsx` → `productos.tsx`, `Profile.tsx` → `profile.tsx`
- [x] 6.2 Renombrar stores: `authStore.ts` → `auth-store.ts`, `cartStore.ts` → `cart-store.ts`
- [x] 6.3 Actualizar todos los imports que referencien los archivos renombrados
- [x] 6.4 Crear directorio `frontend/src/types/` con un `index.ts` de placeholder
