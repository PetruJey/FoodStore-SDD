## 1. Project Scaffold — Monorepo Structure

- [x] 1.1 Create /backend directory with feature-first module folders: auth/, usuarios/, productos/, categorias/, ingredientes/, pedidos/, pagos/, direcciones/, admin/, refreshtokens/
- [x] 1.2 Create /frontend directory with FSD layers: app/, pages/, widgets/, features/, entities/, shared/
- [x] 1.3 Add __init__.py to each backend module folder
- [x] 1.4 Create .gitkeep placeholder files in each module for git tracking
- [x] 1.5 Create .gitignore with exclusions: .env, __pycache__/, node_modules/, .venv/, *.pyc, dist/, .DS_Store
- [x] 1.6 Create docker-compose.yml with PostgreSQL service (port 5432, env vars for DB name/user/pass)
- [x] 1.7 Create README.md with setup instructions (clone, backend setup, frontend setup, docker)

## 2. Backend Core — FastAPI Configuration

- [x] 2.1 Create requirements.txt with: fastapi, sqlmodel, alembic, passlib[bcrypt], python-jose, slowapi, mercadopago, uvicorn, httpx, pydantic[email-validator]
- [x] 2.2 Create backend/.env.example with ALL env vars: DATABASE_URL, SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES, REFRESH_TOKEN_EXPIRE_DAYS, CORS_ORIGINS, MP_ACCESS_TOKEN, MP_PUBLIC_KEY
- [x] 2.3 Create core/__init__.py and core/config.py with Settings class reading env vars via pydantic-settings
- [x] 2.4 Create core/database.py with SQLAlchemy async engine, session factory, and get_session dependency
- [x] 2.5 Create core/security.py with hash_password(), verify_password() (passlib+bcrypt), create_access_token(), create_refresh_token(), decode_token() (python-jose)
- [x] 2.6 Create main.py with FastAPI app, CORS middleware (origins from settings), rate limiting middleware, and /api/v1 router registration
- [x] 2.7 Verify server starts with `uvicorn main:app --reload` and /docs is accessible

## 3. Database — SQLModel Models, Migrations, and Seed

- [x] 3.1 Create app/__init__.py and app/db/__init__.py
- [x] 3.2 Create all SQLModel models (16 tables) in app/models/: Usuario, Rol, UsuarioRol, RefreshToken, DireccionEntrega, Categoria, Producto, Ingrediente, ProductoCategoria, ProductoIngrediente, FormaPago, EstadoPedido, Pedido, DetallePedido, HistorialEstadoPedido, Pago
- [x] 3.3 Add auditoria fields (creado_en, actualizado_en) to all main tables
- [x] 3.4 Add eliminado_en (nullable timestamp) to tables requiring soft delete
- [x] 3.5 Configure Alembic with SQLModel metadata and autogenerate support
- [x] 3.6 Generate initial migration with `alembic revision --autogenerate` and verify DDL
- [x] 3.7 Test `alembic upgrade head` creates all tables and `alembic downgrade -1` reverses
- [x] 3.8 Create app/db/seed.py with idempotent inserts (INSERT ... ON CONFLICT DO NOTHING) for: 4 Roles (ADMIN, STOCK, PEDIDOS, CLIENT), 6 EstadoPedido (PENDIENTE, CONFIRMADO, EN_PREPARACION, EN_CAMINO, ENTREGADO, CANCELADO), 3 FormaPago (MERCADOPAGO, EFECTIVO, TRANSFERENCIA), 1 admin user with ADMIN role
- [x] 3.9 Make seed script executable via `python -m app.db.seed`

## 4. Frontend Core — Vite, React, Tailwind, Routing

- [x] 4.1 Initialize frontend with Vite + React + TypeScript template
- [x] 4.2 Configure tsconfig.json with strict: true
- [x] 4.3 Install dependencies: react-router-dom, @tanstack/react-query, @tanstack/react-form, zustand, axios, recharts, tailwindcss, @mercadopago/sdk-js
- [x] 4.4 Configure Tailwind CSS with PostCSS and production purging
- [x] 4.5 Create frontend/.env.example with VITE_API_BASE_URL and VITE_MERCADOPAGO_PUBLIC_KEY
- [x] 4.6 Set up App.tsx with QueryClientProvider and RouterProvider
- [x] 4.7 Configure react-router-dom with public routes and private route wrapper (placeholder)
- [x] 4.8 Verify `npm run dev` starts without errors on port 5173

## 5. Base Repository — Generic CRUD Pattern

- [x] 5.1 Create core/repository.py with BaseRepository[T] generic class
- [x] 5.2 Implement methods: get_by_id(id), list_all(skip, limit, filters), count(filters), create(obj), update(id, data), soft_delete(id), hard_delete(id)
- [x] 5.3 Ensure get_by_id and list_all exclude soft-deleted records by default (eliminado_en IS NOT NULL)
- [x] 5.4 Add typing with TypeVar for generic type parameter

## 6. Unit of Work — Transaction Management

- [x] 6.1 Create core/uow.py with UnitOfWork async context manager
- [x] 6.2 Implement __aenter__: create SQLAlchemy session, initialize repository instances
- [x] 6.3 Implement __aexit__: commit on success, rollback on exception
- [x] 6.4 Add module-based repository properties (uow.productos, uow.pedidos, etc.)

## 7. Auth Infrastructure — JWT Dependencies

- [x] 7.1 Create core/dependencies.py with get_current_user (extract Bearer token, decode, validate, return Usuario or 401)
- [x] 7.2 Create require_role(roles: list[str]) factory that returns a dependency checking user roles (403 if unauthorized)
- [x] 7.3 Ensure both dependencies use FastAPI's Depends() for integration

## 8. Error Handling — RFC 7807

- [x] 8.1 Create core/exceptions.py with custom exception classes: ValidationError(400), UnauthorizedError(401), ForbiddenError(403), NotFoundError(404)
- [x] 8.2 Create core/error_handler.py with global exception handler for RFC 7807 format
- [x] 8.3 Add per-field validation error details in error response
- [x] 8.4 Ensure 500 errors log stack trace server-side but return generic message to client

## 9. HTTP Client — Axios with JWT Interceptors

- [x] 9.1 Create shared/api/axios.ts with centralized Axios instance (base URL from VITE_API_BASE_URL)
- [x] 9.2 Add request interceptor to attach Authorization: Bearer <token> from authStore
- [x] 9.3 Add response interceptor to catch 401, attempt token refresh, update authStore, and retry original request
- [x] 9.4 Ensure interceptors work outside React context (use store.getState())

## 10. Zustand Stores — Client State Management

- [x] 10.1 Create stores/ or entities/ directory for Zustand stores
- [x] 10.2 Create authStore with: accessToken, refreshToken, user, isAuthenticated; actions: login, logout, updateTokens; selectors: isAuthenticated, hasRole; persist in localStorage key "food-store-auth"
- [x] 10.3 Create cartStore with: items array; actions: addItem, removeItem, updateQuantity, clearCart; selectors: totalItems, totalPrice, getItem; persist in localStorage key "food-store-cart"
- [x] 10.4 Create paymentStore with: checkoutStep, preferenceId, paymentStatus, error; actions: startCheckout, setPreference, updatePaymentStatus, resetPayment; NO persistence
- [x] 10.5 Create uiStore with: theme, sidebarOpen, toasts; persist only theme in localStorage
- [x] 10.6 Ensure all stores use slice subscriptions (not full useStore())
