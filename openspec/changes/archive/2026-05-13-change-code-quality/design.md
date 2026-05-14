## Context

El módulo de autenticación (change-auth-module, Sprint 1 v1.0) y la estructura base (change-setup-project-structure, Sprint 0) fueron implementados y verificados contra la documentación principal del proyecto. La auditoría detectó 18 incumplimientos; los 4 críticos y 7 correcciones previas ya fueron aplicados. Quedan 12 issues de calidad y consistencia que no dependen de features futuras.

Este cambio se enfoca exclusivamente en código existente que ya está implementado pero no cumple con los estándares documentados.

## Goals / Non-Goals

**Goals:**
- Eliminar exposición de tokens JWT en localStorage (seguridad)
- Agregar migración faltante para `estados_pedido` y `formas_pago`
- Unificar manejo de errores: reemplazar `HTTPException` por `AppError` en auth service y dependencies
- Corregir nombres de estados en seed para que coincidan con la FSM documentada
- Agregar variable `MP_NOTIFICATION_URL` a config
- Reorganizar frontend para cumplir con FSD (mover lógica de pages a features)
- Renombrar archivos frontend a kebab-case según convención
- Consistencia en modelos (server_default vs default_factory)
- Completar `.env.example` y estructura `types/`

**Non-Goals:**
- NO implementar features nuevas (RBAC, catálogo, etc.)
- NO cambiar comportamiento funcional del auth module
- NO modificar la API pública (endpoints, schemas de request/response)
- NO tocar migraciones existentes (solo agregar nueva)

## Decisions

### 1. Tokens en localStorage → Sesión en memoria + cookie httpOnly simulada

**Decisión**: Reemplazar `zustand/persist` por almacenamiento en memoria en `authStore`, combinado con el interceptor de Axios que ya maneja refresh automático.

**Alternativa considerada**: Cookies httpOnly con backend set-cookie. Descartado porque requeriría cambios en el backend y rompe la arquitectura SPA actual (el frontend es standalone con API REST).

**Razón**: El riesgo de XSS es real y localStorage no ofrece protección. La sesión en memoria significa que al recargar la página se pierde la sesión, pero el interceptor de Axios ya implementa refresh automático. En un change futuro se puede implementar cookie httpOnly con backend changes.

### 2. AppError en vez de HTTPException

**Decisión**: Reemplazar todos los `HTTPException` en `auth/service.py` y `auth/dependencies.py` por `AppError` y sus subtipos (`NotFoundError`, `BadRequestError`, `UnauthorizedError`, `ForbiddenError`).

**Razón**: El `app_error_handler` en `errors.py` ya maneja `AppError` con formato RFC 7807. El uso de `HTTPException` directo bypasea este handler y produce respuestas inconsistentes.

**Excepción**: La función `refresh_token()` hace commits manuales antes de los raises (por detección de replay attacks). Estos casos mantienen `HTTPException` porque la transacción ya fue commiteada y el error es genuinamente HTTP. Se documenta con comentario inline.

### 3. Renombre de archivos frontend a kebab-case

**Decisión**: Renombrar archivos de `PascalCase.tsx` a `kebab-case.tsx` y actualizar imports en todos los archivos que los referencien.

**Razón**: AGENTS.md establece kebab-case como convención para archivos frontend. Mantener consistencia evita confusiones.

**Riesgo**: Los archivos renombrados perderán su historial de git. Para mitigar, se hace un rename por archivo (no delete+create) para que git trackee el movimiento.

### 4. Migración para estados_pedido y formas_pago

**Decisión**: Crear nueva migración Alembic que agregue las tablas `estados_pedido` y `formas_pago`.

**Razón**: Actualmente los modelos existen en Python pero no en BD. Sin migración, el seed falla al intentar insertar en tablas que no existen.

## Risks / Trade-offs

- **[Seguridad]** Sesión en memoria pierde autenticación al recargar → Mitigación: el interceptor de Axios ya tiene refresh automático. Si el refresh token expiró, redirige a login.
- **[Renombres]** Git pierde historial de archivos renombrados si no se hace con `git mv` → Mitigación: se usará rename de archivos (no delete+create) para que git pueda rastrear el movimiento.
- **[HTTPException en refresh_token]** No reemplazamos HTTPException en refresh_token porque necesita commit antes de raise → Mitigación: se documenta con comentario inline explicando por qué.
