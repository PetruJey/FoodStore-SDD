## Why

La auditoría de coherencia contra la documentación principal (AGENTS.md, AGENTS-REFERENCIA.md, CHANGES.md, README.md) detectó 18 incumplimientos en el código existente. Se corrigieron 4 críticos + 7 correcciones previas en la sesión anterior. Quedan 12 issues (2 críticos, 6 importantes, 4 menores) que afectan la seguridad, consistencia y calidad del código ya implementado del módulo de autenticación y estructura base.

## What Changes

### CRÍTICOS

1. **Tokens JWT en localStorage** — `frontend/src/shared/stores/authStore.ts` usa `zustand/middleware/persist` que guarda access_token y refresh_token en localStorage, exponiéndolos a ataques XSS. Se reemplazará por almacenamiento en memoria con interceptor que maneje sesión.
2. **EstadoPedidoModel y FormaPagoModel sin migración** — Las tablas `estados_pedido` y `formas_pago` existen en `models.py` y se seedean en `seed.py` pero nunca se crean en BD. Falta migración de Alembic.

### IMPORTANTES

3. **`auth/service.py` usa `HTTPException` de FastAPI** en vez de `AppError`/`NotFoundError`/`BadRequestError`/`UnauthorizedError` de `core/errors.py` — rompe el manejo unificado de errores RFC 7807.
4. **`auth/dependencies.py` usa `HTTPException`** igual que service — misma inconsistencia.
5. **Seed: nombres de estados incorrectos** — `"PREPARANDO"` debe ser `"EN_PREPARACION"`, `"ENVIADO"` debe ser `"EN_CAMINO"` para coincidir con la FSM documentada en AGENTS-REFERENCIA.md.
6. **`config.py` no tiene `MP_NOTIFICATION_URL`** — variable necesaria para el webhook de MercadoPago, documentada en AGENTS-REFERENCIA.md.
7. **`features/auth/` vacío** — solo tiene `types.ts`. Los componentes de login/register están directamente en `pages/` violando la arquitectura FSD.
8. **`pages/Login.tsx` y `Register.tsx` importan `authStore` directo** — según FSD, `pages` debe importar desde `features/`, no saltarse capas.

### MENORES

9. **`EstadoPedidoModel` y `FormaPagoModel`** usan `default_factory=datetime.utcnow` en vez de `sa_column_kwargs={"server_default": func.now()}` — inconsistencia de estilo con el resto de los modelos.
10. **Archivos frontend no siguen kebab-case** — `Login.tsx`, `Register.tsx`, `AdminDashboard.tsx`, `Carrito.tsx`, `Checkout.tsx`, `Home.tsx`, `Productos.tsx`, `Profile.tsx`, `authStore.ts`, `cartStore.ts`.
11. **`.env.example` no incluye `ALGORITHM`** — está documentado en AGENTS-REFERENCIA.md como variable de entorno requerida.
12. **`frontend/src/types/` no existe** — documentado en la estructura FSD de AGENTS-REFERENCIA.md pero el directorio nunca se creó.

## Capabilities

### New Capabilities

<!-- No se introducen nuevas capacidades. Este cambio es de calidad de código sobre el módulo de autenticación existente. -->

### Modified Capabilities

<!-- No hay cambios a nivel de requerimientos de specs. Todas las correcciones son de implementación y consistencia interna. -->

## Impact

- **Backend**: `auth/service.py`, `auth/dependencies.py`, `db/seed.py`, `db/models.py`, `core/config.py`, `core/errors.py`, migración Alembic.
- **Frontend**: `stores/authStore.ts`, renombrar 8 archivos en `pages/`, crear estructura en `features/auth/`, crear `types/`.
- **Config**: `.env.example` y `config.py` con nuevas variables.
- **BD**: Nueva migración para `estados_pedido` y `formas_pago`.
