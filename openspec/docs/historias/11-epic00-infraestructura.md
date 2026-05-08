# EPIC 00 — Infraestructura y Setup (Sprint 0)

> **Sprint 0** — Sin esta epica no existe NADA. Es la fundacion sobre la que se construye todo lo demas. Cada historia posterior depende directa o indirectamente de estas.

## US-000: Inicializacion del repositorio y estructura del proyecto

- **Titulo**: Scaffolding del monorepo y estructura base
- **Historia**: Como **Lider Tecnico**, quiero tener el repositorio Git inicializado con la estructura de carpetas del backend (feature-first) y del frontend (Feature-Sliced Design), para que el equipo pueda comenzar a desarrollar sobre una base organizada y consistente.
- **Prioridad**: Alta
- **Dependencias**: Ninguna

**Criterios de Aceptacion**:
- [ ] GIVEN un repositorio vacio, WHEN se ejecuta el setup inicial, THEN existe un monorepo con carpetas `/backend` y `/frontend` claramente separadas.
- [ ] El backend tiene la estructura feature-first: carpetas por modulo (`auth/`, `usuarios/`, `productos/`, `categorias/`, `ingredientes/`, `pedidos/`, `pagos/`, `direcciones/`, `admin/`, `refreshtokens/`), cada una con sus archivos `model.py`, `schemas.py`, `repository.py`, `service.py`, `router.py`.
- [ ] El frontend tiene la estructura FSD: `app/`, `pages/`, `widgets/`, `features/`, `entities/`, `shared/`.
- [ ] Existe un `.gitignore` que excluye: `.env`, `__pycache__/`, `node_modules/`, `.venv/`, `*.pyc`, `dist/`, `.DS_Store`.
- [ ] Existe un `README.md` raiz con instrucciones basicas de setup (clonar, instalar, ejecutar).
- [ ] Existe un `.env.example` en backend y frontend con todas las variables documentadas y valores de ejemplo.
- [ ] El historial de Git muestra commits progresivos (no un solo commit masivo).

**Notas Tecnicas**:
- Backend: Python con FastAPI, estructura modular vertical
- Frontend: React + TypeScript + Vite
- Convencion de commits: conventional commits

## US-000a: Configuracion del entorno backend (FastAPI + dependencias)

- **Titulo**: Setup del backend con FastAPI y dependencias core
- **Historia**: Como **Desarrollador**, quiero tener el proyecto backend configurado con FastAPI, SQLModel, Alembic y todas las dependencias necesarias, para poder comenzar a implementar los modulos funcionales.
- **Prioridad**: Alta
- **Dependencias**: US-000

**Criterios de Aceptacion**:
- [ ] GIVEN el proyecto backend, WHEN se ejecuta `pip install -r requirements.txt` (o `poetry install`), THEN se instalan todas las dependencias: FastAPI, SQLModel, Alembic, Passlib[bcrypt], python-jose, slowapi, mercadopago, uvicorn, httpx, pydantic[email-validator].
- [ ] GIVEN el proyecto backend, WHEN se ejecuta `uvicorn main:app --reload`, THEN el servidor arranca sin errores en el puerto 8000.
- [ ] La documentacion Swagger es accesible en `/docs` y ReDoc en `/redoc`.
- [ ] Existe un archivo `main.py` que configura la app FastAPI con: CORS middleware (origenes desde variable de entorno), rate limiting middleware, y registro de routers con prefijo `/api/v1`.
- [ ] Existe un modulo `core/` o `config/` con: `config.py` (lectura de variables de entorno con valores por defecto), `database.py` (engine y session factory de SQLAlchemy), `security.py` (funciones de hashing y JWT).
- [ ] El CORS permite el origen `http://localhost:5173` en desarrollo.

**Notas Tecnicas**:
- Variables de entorno: DATABASE_URL, SECRET_KEY, JWT_ACCESS_TOKEN_EXPIRE_MINUTES (30), JWT_REFRESH_TOKEN_EXPIRE_DAYS (7), CORS_ORIGINS, MERCADOPAGO_ACCESS_TOKEN, MERCADOPAGO_PUBLIC_KEY
- Base de datos: PostgreSQL, connection string en DATABASE_URL
- Middleware de errores: RFC 7807 (Problem Details for HTTP APIs)

## US-000b: Configuracion de PostgreSQL, migraciones y seed data

- **Titulo**: Base de datos, migraciones Alembic y datos semilla
- **Historia**: Como **Desarrollador**, quiero tener PostgreSQL configurado con Alembic para migraciones y un script de seed que cargue los datos iniciales, para que el sistema tenga las tablas y datos catalogo necesarios para funcionar.
- **Prioridad**: Alta
- **Dependencias**: US-000a

**Criterios de Aceptacion**:
- [ ] GIVEN una base de datos PostgreSQL vacia, WHEN se ejecuta `alembic upgrade head`, THEN se crean TODAS las tablas del ERD v5 sin errores: Usuario, Rol, UsuarioRol, RefreshToken, DireccionEntrega, Categoria, Producto, Ingrediente, ProductoCategoria, ProductoIngrediente, FormaPago, EstadoPedido, Pedido, DetallePedido, HistorialEstadoPedido, Pago.
- [ ] Todas las tablas principales tienen campos de auditoria: `creado_en` (timestamp, default NOW), `actualizado_en` (timestamp, auto-update).
- [ ] Las tablas que soportan soft delete tienen el campo `eliminado_en` (timestamp nullable).
- [ ] Los tipos de datos son correctos: precios como NUMERIC de precision fija, personalizacion como INTEGER[], email con constraint UNIQUE, etc.
- [ ] Las claves foraneas y restricciones de integridad referencial estan definidas.
- [ ] Categoria tiene `padre_id` como FK autoreferencial nullable.
- [ ] UsuarioRol tiene restriccion UNIQUE compuesta (usuario_id, rol_id).
- [ ] GIVEN las tablas creadas, WHEN se ejecuta el script de seed, THEN se cargan:
  - 4 Roles: ADMIN (1), STOCK (2), PEDIDOS (3), CLIENT (4)
  - 6 EstadoPedido: PENDIENTE (1), CONFIRMADO (2), EN_PREPARACION (3), EN_CAMINO (4), ENTREGADO (5), CANCELADO (6)
  - Formas de pago: Tarjeta de credito, Tarjeta de debito (activas)
  - 1 Usuario administrador con rol ADMIN y credenciales configurables por variables de entorno
- [ ] Las migraciones son reversibles: `alembic downgrade -1` no genera errores.
- [ ] El script de seed es idempotente: ejecutarlo multiples veces no duplica datos.

**Reglas de Negocio**: Los IDs de Roles y EstadoPedido son estables y se referencian en el codigo.

**Notas Tecnicas**:
- Alembic con autogenerate desde modelos SQLModel
- Seed como script Python invocable: `python -m scripts.seed` o similar
- Usar `INSERT ... ON CONFLICT DO NOTHING` para idempotencia
- Los IDs de seed deben ser explicitos (no autogenerados) para consistencia

## US-000c: Configuracion del entorno frontend (React + Vite + dependencias)

- **Titulo**: Setup del frontend con React, TypeScript, Vite y dependencias core
- **Historia**: Como **Desarrollador**, quiero tener el proyecto frontend configurado con React, TypeScript, Vite y todas las librerias necesarias, para poder comenzar a construir la interfaz de usuario.
- **Prioridad**: Alta
- **Dependencias**: US-000

**Criterios de Aceptacion**:
- [ ] GIVEN el proyecto frontend, WHEN se ejecuta `npm install`, THEN se instalan todas las dependencias: react, react-dom, react-router-dom, @tanstack/react-query, @tanstack/react-form, zustand, axios, recharts, tailwindcss, @mercadopago/sdk-js.
- [ ] GIVEN el proyecto frontend, WHEN se ejecuta `npm run dev`, THEN el servidor de desarrollo arranca sin errores en el puerto 5173.
- [ ] TypeScript esta configurado en modo estricto (`strict: true` en `tsconfig.json`).
- [ ] Tailwind CSS esta configurado con PostCSS y purging de clases en produccion.
- [ ] Existe la configuracion de Axios con:
  - Base URL desde variable de entorno `VITE_API_BASE_URL`
  - Interceptor de request que adjunta el access token del authStore al header `Authorization: Bearer <token>`
  - Interceptor de response que, ante un 401, intenta refresh automatico con el refresh token, actualiza el authStore, y reintenta la peticion original
- [ ] Existe el archivo `.env.example` con: `VITE_API_BASE_URL=http://localhost:8000/api/v1`, `VITE_MERCADOPAGO_PUBLIC_KEY=TEST-xxx`.
- [ ] El routing base esta configurado con react-router-dom (rutas publicas y privadas).
- [ ] TanStack Query esta configurado con un `QueryClientProvider` en el App root.

**Notas Tecnicas**:
- Vite con plugin React + SWC para fast refresh
- Tailwind v3+ con PostCSS
- Axios instance centralizada en `shared/api/axios.ts`
- QueryClient con defaults razonables: staleTime, retry, refetchOnWindowFocus

## US-000d: Implementacion de patrones base (BaseRepository, Unit of Work, dependencias FastAPI)

- **Titulo**: Patrones de infraestructura del backend
- **Historia**: Como **Desarrollador**, quiero tener implementados el BaseRepository generico, el Unit of Work y las dependencias de FastAPI (get_current_user, require_role), para que los modulos funcionales puedan construirse sobre una base solida y consistente.
- **Prioridad**: Alta
- **Dependencias**: US-000b

**Criterios de Aceptacion**:
- [ ] Existe un `BaseRepository[T]` generico con los metodos: `get_by_id(id)`, `list_all(skip, limit, filters)`, `count(filters)`, `create(obj)`, `update(id, data)`, `soft_delete(id)`, `hard_delete(id)`.
- [ ] `get_by_id` y `list_all` excluyen registros con `eliminado_en IS NOT NULL` por defecto.
- [ ] Existe un `UnitOfWork` implementado como context manager (`async with`) que:
  - Crea una sesion de SQLAlchemy al entrar
  - Expone los repositorios como atributos (`uow.productos`, `uow.pedidos`, etc.)
  - Ejecuta `commit()` al salir exitosamente
  - Ejecuta `rollback()` automaticamente si se lanza una excepcion
- [ ] Existe la dependencia `get_current_user` que:
  - Extrae el token del header `Authorization: Bearer <token>`
  - Decodifica y valida el JWT (firma, expiracion)
  - Retorna el objeto Usuario o lanza HTTP 401
- [ ] Existe la dependencia factory `require_role(roles: list[str])` que:
  - Recibe una lista de roles permitidos
  - Verifica que el usuario autenticado tenga al menos uno de esos roles
  - Lanza HTTP 403 si no tiene permiso
- [ ] Existe un middleware o handler de excepciones que formatea errores segun RFC 7807 con campos: `type`, `title`, `status`, `detail`, `instance`.

**Notas Tecnicas**:
- BaseRepository parametrizado con TypeVar para tipado generico
- UoW inicializa repos en `__aenter__`, commit/rollback en `__aexit__`
- get_current_user usa `Depends(oauth2_scheme)` de FastAPI
- require_role retorna un `Callable` que FastAPI puede usar como dependencia

## US-000e: Configuracion de los stores de Zustand (authStore, cartStore, paymentStore, uiStore)

- **Titulo**: Stores de estado del cliente con Zustand
- **Historia**: Como **Desarrollador**, quiero tener los cuatro stores de Zustand configurados con sus acciones base y persistencia, para que el frontend tenga una gestion de estado consistente desde el inicio.
- **Prioridad**: Alta
- **Dependencias**: US-000c

**Criterios de Aceptacion**:
- [ ] Existe `authStore` con:
  - Estado: `accessToken`, `refreshToken`, `user` (id, nombre, email, roles), `isAuthenticated`
  - Acciones: `login(tokens, user)`, `logout()`, `updateTokens(tokens)`
  - Selectores: `isAuthenticated()`, `hasRole(role)`
  - Persistencia en localStorage con clave `food-store-auth`
  - `partialize` que excluye estados transitorios (isLoading)
- [ ] Existe `cartStore` con:
  - Estado: `items` (array de {productoId, producto, cantidad, personalizacion})
  - Acciones: `addItem(producto, cantidad, personalizacion)`, `removeItem(productoId)`, `updateQuantity(productoId, cantidad)`, `clearCart()`
  - Selectores: `totalItems()`, `totalPrice()`, `getItem(productoId)`
  - Persistencia en localStorage con clave `food-store-cart`
  - El carrito sobrevive al cierre del navegador, refresh de pagina, y logout/login
- [ ] Existe `paymentStore` con:
  - Estado: `checkoutStep`, `preferenceId`, `paymentStatus`, `error`
  - Acciones: `startCheckout(pedidoId)`, `setPreference(preferenceId)`, `updatePaymentStatus(status)`, `resetPayment()`
  - SIN persistencia en localStorage (estado transitorio)
- [ ] Existe `uiStore` con:
  - Estado: `theme` (light/dark), `sidebarOpen`, `toasts`
  - Persistencia selectiva: solo `theme` se persiste
- [ ] Todos los stores usan suscripcion por slice (no `useStore()` completo).

**Notas Tecnicas**:
- Cada store en su propio archivo dentro de `shared/stores/` o `entities/`
- Usar `useStore.getState()` en el interceptor de Axios (fuera de React)
- Middleware persist con `partialize` para filtrar que se guarda

## US-068: Manejo de errores estandarizado en backend

- **Titulo**: Formato de error consistente en API
- **Historia**: Como **Sistema**, quiero que todos los errores de la API sigan un formato consistente, para facilitar el manejo en el frontend y debugging.
- **Prioridad**: Alta
- **Dependencias**: Ninguna

**Criterios de Aceptacion**:
- [ ] Todos los errores siguen el formato: `{ statusCode, message, errors?, timestamp }`.
- [ ] Los errores de validacion incluyen detalle por campo: `{ field, message }[]`.
- [ ] Los errores no exponen stack traces ni detalles de implementacion en produccion.
- [ ] Se loguean errores 500 con stack trace en el servidor.

**Notas Tecnicas**:
- Exception filter/middleware global
- Clases de error custom: `ValidationError`, `UnauthorizedError`, `ForbiddenError`, `NotFoundError`
- Patron: mapear excepciones a HTTP status codes en un solo lugar

## US-074: Validacion y sanitizacion de inputs

- **Titulo**: Proteccion contra inyeccion y datos malformados
- **Historia**: Como **Sistema**, quiero validar y sanitizar todos los inputs del usuario, para prevenir inyecciones SQL/XSS y datos corruptos.
- **Prioridad**: Alta
- **Dependencias**: Ninguna

**Criterios de Aceptacion**:
- [ ] Todos los inputs se validan en backend con esquemas (Zod, class-validator o similar).
- [ ] Los strings se sanitizan contra XSS (escape de HTML entities).
- [ ] Los queries parametrizados previenen SQL injection (ORM con bindings).
- [ ] Los campos numericos rechazan valores no numericos con error 400.

**Notas Tecnicas**:
- Validation pipe global (NestJS) o middleware equivalente
- ORM con queries parametrizados (nunca concatenar SQL)
- Library de sanitizacion: DOMPurify para frontend, helmet para headers
